"""
Streamlit Web App for Dog Breed Classification
Combined Space: FastAPI + Streamlit in same container
"""
import streamlit as st
import requests
from PIL import Image
import io
import time

# Configuration
API_URL = "http://localhost:8000/predict"
HEALTH_URL = "http://localhost:8000/health"

# Helper function to call API with retry
def call_api_with_retry(url, files=None, max_retries=3, timeout=60):
    """Call API with retry logic"""
    for attempt in range(max_retries):
        try:
            if files:
                response = requests.post(url, files=files, timeout=timeout)
            else:
                response = requests.get(url, timeout=timeout)
            
            if response.status_code == 200:
                return response
            elif response.status_code == 403:
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    raise Exception("API ปฏิเสธการเชื่อมต่อ")
            else:
                raise Exception(f"API error: {response.status_code}")
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            else:
                raise Exception("API timeout")
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            else:
                raise Exception("ไม่สามารถเชื่อมต่อ API")
    
    raise Exception("ไม่สามารถเรียก API ได้")

# Page config
st.set_page_config(
    page_title="Dog Breed Classifier",
    page_icon="🐕",
    layout="centered"
)

# Simple header
st.title("🐕 Dog Breed Classifier")
st.caption("ระบุสายพันธุ์สุนัขจากรูปภาพ")
st.divider()

# File uploader
uploaded_file = st.file_uploader(
    "เลือกรูปภาพ",
    type=['jpg', 'jpeg', 'png', 'webp']
)

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(image, use_column_width=True)
    
    st.markdown("")
    
    # Predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button(
            "วิเคราะห์สายพันธุ์", 
            type="primary", 
            use_container_width=True
        )
    
    if predict_button:
        with st.spinner("กำลังวิเคราะห์..."):
            try:
                # Prepare file for API
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Call API
                response = call_api_with_retry(API_URL, files=files, max_retries=3, timeout=60)
                result = response.json()
                
                # Success
                st.success("วิเคราะห์เสร็จสิ้น")
                st.divider()
                
                # Main result
                st.subheader(f"🐕 {result['breed_name'].title()}")
                
                # Metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ความมั่นใจ", f"{result['confidence']*100:.1f}%")
                with col2:
                    st.metric("เวลาประมวลผล", f"{result['inference_time_ms']:.0f} ms")
                
                st.markdown("")
                
                # Care information
                if result.get("care_info"):
                    st.subheader("ข้อมูลการดูแล")
                    
                    care = result["care_info"]
                    
                    with st.expander("นิสัยและบุคลิกภาพ", expanded=True):
                        st.write(care["personality"])
                    
                    with st.expander("การออกกำลังกาย"):
                        st.write(care["exercise"])
                    
                    with st.expander("โภชนาการ"):
                        st.write(care["nutrition"])
                    
                    with st.expander("การดูแลสุขภาพ"):
                        st.write(care["health_care"])
                    
                    with st.expander("การดูแลขน"):
                        st.write(care["grooming"])
                
                # Top 5 predictions
                if result.get("top_5_predictions"):
                    st.divider()
                    st.subheader("Top 5 สายพันธุ์ที่เป็นไปได้")
                    
                    for i, pred in enumerate(result["top_5_predictions"], 1):
                        confidence_pct = pred['confidence'] * 100
                        
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"**{i}.** {pred['breed_name'].title()}")
                            st.progress(pred['confidence'])
                        with col2:
                            st.write(f"**{confidence_pct:.1f}%**")
                        
                        if i < len(result["top_5_predictions"]):
                            st.markdown("")
                    
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")

else:
    st.info("กรุณาอัปโหลดรูปหมาเพื่อเริ่มต้น")

# Footer
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.caption("ResNet-34 (ONNX INT8)")
with col2:
    st.caption("96 Dog Breeds")
