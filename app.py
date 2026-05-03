"""
Streamlit Web App for Dog Breed Classification
อัปโหลดรูปหมา → ระบุสายพันธุ์ → แสดงข้อมูลการดูแล
"""
import streamlit as st
import requests
from PIL import Image
import io
import time

# Configuration
API_URL = "https://chetsadaphon66-dog-breed-classifier.hf.space/predict"
HEALTH_URL = "https://chetsadaphon66-dog-breed-classifier.hf.space/health"

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
                    st.warning(f"⏳ API กำลัง cold start... (ลองครั้งที่ {attempt + 1}/{max_retries})")
                    time.sleep(5)  # Wait 5 seconds before retry
                    continue
                else:
                    raise Exception(f"API ปฏิเสธการเชื่อมต่อ (403). กรุณาเปิด API Space ที่ {HEALTH_URL.replace('/health', '')} ก่อน")
            else:
                raise Exception(f"API error: {response.status_code}")
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                st.warning(f"⏳ API ตอบสนองช้า... (ลองครั้งที่ {attempt + 1}/{max_retries})")
                time.sleep(5)
                continue
            else:
                raise Exception("API timeout หลังจากลองหลายครั้ง")
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                st.warning(f"⏳ กำลังเชื่อมต่อ API... (ลองครั้งที่ {attempt + 1}/{max_retries})")
                time.sleep(5)
                continue
            else:
                raise Exception("ไม่สามารถเชื่อมต่อ API")
    
    raise Exception("ไม่สามารถเรียก API ได้")


# Page config
st.set_page_config(
    page_title="🐕 Dog Breed Classifier",
    page_icon="🐕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .breed-name {
        font-size: 2rem;
        font-weight: bold;
        color: #FF6B6B;
        margin-bottom: 0.5rem;
    }
    .confidence {
        font-size: 1.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .care-section {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .care-title {
        font-weight: bold;
        color: #FF6B6B;
        margin-bottom: 0.3rem;
    }
    .top-5-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🐕 Dog Breed Classifier</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">ระบุสายพันธุ์สุนัข พร้อมข้อมูลการดูแล</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 เกี่ยวกับระบบ")
    st.write("""
    **ระบบจำแนกสายพันธุ์สุนัข**
    
    ✨ **ฟีเจอร์:**
    - ระบุสายพันธุ์จากรูปภาพ
    - แสดงข้อมูลการดูแล 5 ด้าน
    - รองรับ 103 สายพันธุ์
    
    🎯 **วิธีใช้:**
    1. อัปโหลดรูปหมา
    2. รอระบบวิเคราะห์
    3. ดูผลลัพธ์และข้อมูลการดูแล
    
    🔧 **เทคโนโลยี:**
    - ResNet-34 (ONNX INT8)
    - FastAPI + ProcessPoolExecutor
    - Streamlit UI
    """)
    
    # Check API health
    st.divider()
    st.subheader("🏥 สถานะระบบ")
    try:
        health_response = call_api_with_retry(HEALTH_URL, max_retries=1, timeout=10)
        st.success("✅ API ทำงานปกติ")
        health_data = health_response.json()
        st.caption(f"Model: {health_data.get('model_loaded', False)}")
        st.caption(f"Breeds: {health_data.get('num_breeds', 0)} สายพันธุ์")
    except Exception as e:
        st.warning(f"⚠️ {str(e)}")
        st.caption("💡 เปิด API Space: https://huggingface.co/spaces/chetsadaphon66/dog-breed-classifier")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 อัปโหลดรูปหมา")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "เลือกรูปภาพ (JPG, PNG, WEBP)",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="อัปโหลดรูปหมาเพื่อระบุสายพันธุ์"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="รูปที่อัปโหลด", use_column_width=True)
        
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
                    st.session_state['result'] = result
                    st.success("✅ วิเคราะห์เสร็จสิ้น!")
                        
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    st.info("💡 ลองเปิด API Space ก่อน: https://huggingface.co/spaces/chetsadaphon66/dog-breed-classifier")
    else:
        st.info("👆 กรุณาอัปโหลดรูปหมาเพื่อเริ่มต้น")

with col2:
    st.subheader("📊 ผลลัพธ์")
    
    if 'result' in st.session_state:
        result = st.session_state['result']
        
        # Main result
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="breed-name">🐕 {result["breed_name"].title()}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="confidence">ความมั่นใจ: {result["confidence"]*100:.1f}%</div>', unsafe_allow_html=True)
        st.progress(result["confidence"])
        st.caption(f"⏱️ เวลาประมวลผล: {result['inference_time_ms']:.1f} ms")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Care information
        if result.get("care_info"):
            st.markdown("---")
            st.subheader("💚 ข้อมูลการดูแล")
            
            care = result["care_info"]
            
            # Personality
            st.markdown('<div class="care-section">', unsafe_allow_html=True)
            st.markdown('<div class="care-title">🎭 นิสัย</div>', unsafe_allow_html=True)
            st.write(care["personality"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Exercise
            st.markdown('<div class="care-section">', unsafe_allow_html=True)
            st.markdown('<div class="care-title">🏃 การออกกำลังกาย</div>', unsafe_allow_html=True)
            st.write(care["exercise"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Nutrition
            st.markdown('<div class="care-section">', unsafe_allow_html=True)
            st.markdown('<div class="care-title">🍖 โภชนาการ</div>', unsafe_allow_html=True)
            st.write(care["nutrition"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Health care
            st.markdown('<div class="care-section">', unsafe_allow_html=True)
            st.markdown('<div class="care-title">🏥 การดูแลสุขภาพ</div>', unsafe_allow_html=True)
            st.write(care["health_care"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Grooming
            st.markdown('<div class="care-section">', unsafe_allow_html=True)
            st.markdown('<div class="care-title">✂️ การดูแลขน</div>', unsafe_allow_html=True)
            st.write(care["grooming"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Top 5 predictions
        if result.get("top_5_predictions"):
            st.markdown("---")
            st.subheader("🏆 Top 5 สายพันธุ์ที่เป็นไปได้")
            
            st.markdown('<div class="top-5-box">', unsafe_allow_html=True)
            for i, pred in enumerate(result["top_5_predictions"], 1):
                col_rank, col_breed, col_conf = st.columns([0.5, 2, 1])
                with col_rank:
                    st.write(f"**{i}.**")
                with col_breed:
                    st.write(pred["breed_name"].title())
                with col_conf:
                    st.write(f"{pred['confidence']*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📊 ผลลัพธ์จะแสดงที่นี่หลังจากอัปโหลดรูป")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🐕 Dog Breed Classifier | MLOps Project 2026</p>
    <p>Powered by ResNet-34 (ONNX INT8) + FastAPI + Streamlit</p>
</div>
""", unsafe_allow_html=True)
