"""
Streamlit Web App for Dog Breed Classification
อัปโหลดรูปหมา → ระบุสายพันธุ์ → แสดงข้อมูลการดูแล

Combined Space: FastAPI + Streamlit in same container
API calls via localhost for lowest latency
"""
import streamlit as st
import requests
from PIL import Image
import io
import time

# Configuration - localhost for same container
API_URL = "http://localhost:8000/predict"
HEALTH_URL = "http://localhost:8000/health"

# Helper function to call API with retry
def call_api_with_retry(url, files=None, max_retries=3, timeout=60):
    """Call API with retry logic for cold start"""
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
                    raise Exception(f"API ปฏิเสธการเชื่อมต่อ (403)")
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

# File uploader
uploaded_file = st.file_uploader(
    "อัปโหลดรูปหมา",
    type=['jpg', 'jpeg', 'png', 'webp']
)

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    # Predict button
    if st.button("🔍 ระบุสายพันธุ์", type="primary", use_container_width=True):
        with st.spinner("กำลังวิเคราะห์..."):
            try:
                # Prepare file for API
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Call API with retry
                response = call_api_with_retry(API_URL, files=files, max_retries=3, timeout=60)
                
                result = response.json()
                
                # Display result
                st.success("✅ วิเคราะห์เสร็จสิ้น")
                
                # Breed name and confidence
                st.subheader(f"🐕 {result['breed_name'].title()}")
                st.metric("ความมั่นใจ", f"{result['confidence']*100:.1f}%")
                st.caption(f"เวลาประมวลผล: {result['inference_time_ms']:.1f} ms")
                
                # Care information
                if result.get("care_info"):
                    st.divider()
                    st.subheader("💚 ข้อมูลการดูแล")
                    
                    care = result["care_info"]
                    
                    with st.expander("🎭 นิสัย", expanded=True):
                        st.write(care["personality"])
                    
                    with st.expander("🏃 การออกกำลังกาย"):
                        st.write(care["exercise"])
                    
                    with st.expander("🍖 โภชนาการ"):
                        st.write(care["nutrition"])
                    
                    with st.expander("🏥 การดูแลสุขภาพ"):
                        st.write(care["health_care"])
                    
                    with st.expander("✂️ การดูแลขน"):
                        st.write(care["grooming"])
                
                # Top 5 predictions
                if result.get("top_5_predictions"):
                    st.divider()
                    st.subheader("🏆 Top 5 สายพันธุ์")
                    
                    for i, pred in enumerate(result["top_5_predictions"], 1):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"{i}. {pred['breed_name'].title()}")
                        with col2:
                            st.write(f"{pred['confidence']*100:.1f}%")
                    
            except Exception as e:
                st.error(f"❌ {str(e)}")

# Footer
st.divider()
st.caption("MLOps Project 2026 | ResNet-34 (ONNX INT8)")
