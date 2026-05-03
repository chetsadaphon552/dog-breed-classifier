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
    page_icon="🐶",
    layout="centered"
)

# Header with better styling
st.markdown("# 🐶 Dog Breed Classifier")
st.markdown("### ระบุสายพันธุ์สุนัขด้วย AI")
st.markdown("---")

# Instructions
with st.expander("ℹ️ วิธีใช้งาน"):
    st.markdown("""
    1. **อัปโหลดรูปหมา** - รองรับ JPG, PNG, WEBP
    2. **คลิกปุ่มวิเคราะห์** - รอสักครู่
    3. **ดูผลลัพธ์** - สายพันธุ์และข้อมูลการดูแล
    
    **รองรับ 103 สายพันธุ์** | **ความแม่นยำ 87%**
    """)

st.markdown("")

# File uploader with better styling
uploaded_file = st.file_uploader(
    "📁 เลือกรูปภาพ",
    type=['jpg', 'jpeg', 'png', 'webp'],
    help="อัปโหลดรูปหมาเพื่อระบุสายพันธุ์"
)

if uploaded_file is not None:
    # Display image in a nice way
    image = Image.open(uploaded_file)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(image, use_column_width=True, caption="รูปที่อัปโหลด")
    
    st.markdown("")
    
    # Centered predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button(
            "🔍 วิเคราะห์สายพันธุ์", 
            type="primary", 
            use_container_width=True
        )
    
    if predict_button:
        with st.spinner("⏳ กำลังวิเคราะห์..."):
            try:
                # Prepare file for API
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Call API with retry
                response = call_api_with_retry(API_URL, files=files, max_retries=3, timeout=60)
                
                result = response.json()
                
                # Success message
                st.success("✅ วิเคราะห์เสร็จสิ้น!")
                st.markdown("---")
                
                # Main result - breed name
                st.markdown(f"## 🐕 {result['breed_name'].title()}")
                
                # Metrics in columns
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ความมั่นใจ", f"{result['confidence']*100:.1f}%")
                with col2:
                    st.metric("เวลาประมวลผล", f"{result['inference_time_ms']:.0f} ms")
                with col3:
                    st.metric("อันดับ", "#1")
                
                st.markdown("")
                
                # Care information with better icons
                if result.get("care_info"):
                    st.markdown("### 📋 ข้อมูลการดูแล")
                    
                    care = result["care_info"]
                    
                    with st.expander("🎯 นิสัยและบุคลิกภาพ", expanded=True):
                        st.write(care["personality"])
                    
                    with st.expander("🏃‍♂️ การออกกำลังกาย"):
                        st.write(care["exercise"])
                    
                    with st.expander("🥩 โภชนาการและอาหาร"):
                        st.write(care["nutrition"])
                    
                    with st.expander("💊 การดูแลสุขภาพ"):
                        st.write(care["health_care"])
                    
                    with st.expander("✨ การดูแลขนและความสะอาด"):
                        st.write(care["grooming"])
                
                # Top 5 predictions with better layout
                if result.get("top_5_predictions"):
                    st.markdown("---")
                    st.markdown("### 🏆 สายพันธุ์ที่เป็นไปได้ (Top 5)")
                    
                    for i, pred in enumerate(result["top_5_predictions"], 1):
                        # Progress bar for confidence
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
                st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")
                st.info("💡 ลองอัปโหลดรูปใหม่หรือรอสักครู่แล้วลองอีกครั้ง")

else:
    # Show placeholder when no image
    st.info("👆 กรุณาอัปโหลดรูปหมาเพื่อเริ่มต้น")

# Footer with better styling
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 ResNet-34")
with col2:
    st.caption("⚡ ONNX INT8")
with col3:
    st.caption("📊 87% Accuracy")

st.markdown("")
st.caption("MLOps Project 2026 | Made with ❤️")
