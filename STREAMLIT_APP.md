# 🐕 Streamlit Web App - Dog Breed Classifier

หน้าเว็บสำหรับทดสอบระบบจำแนกสายพันธุ์สุนัข

## 🚀 วิธีรัน

### 1. ติดตั้ง Dependencies

```bash
pip install streamlit==1.31.0
```

### 2. รัน Streamlit App

```bash
streamlit run app.py
```

เว็บจะเปิดที่: http://localhost:8501

## ✨ ฟีเจอร์

### 📤 อัปโหลดรูป
- รองรับ JPG, PNG, WEBP
- แสดงตัวอย่างรูปที่อัปโหลด
- ปุ่มระบุสายพันธุ์

### 📊 แสดงผลลัพธ์
- **ชื่อสายพันธุ์** - ขนาดใหญ่ชัดเจน
- **ความมั่นใจ** - แสดงเป็น % พร้อม progress bar
- **เวลาประมวลผล** - milliseconds

### 💚 ข้อมูลการดูแล (5 ด้าน)
1. 🎭 **นิสัย** - ลักษณะนิสัยสุนัข
2. 🏃 **การออกกำลังกาย** - ระดับและเวลาที่แนะนำ
3. 🍖 **โภชนาการ** - ปริมาณและประเภทอาหาร
4. 🏥 **การดูแลสุขภาพ** - โรคประจำสายพันธุ์
5. ✂️ **การดูแลขน** - ความถี่และวิธีการ

### 🏆 Top 5 Predictions
- แสดง 5 สายพันธุ์ที่เป็นไปได้สูงสุด
- พร้อมความมั่นใจแต่ละสายพันธุ์

### 🏥 สถานะระบบ (Sidebar)
- เช็คสถานะ API
- แสดงจำนวนสายพันธุ์
- ข้อมูลเกี่ยวกับระบบ

## 🎨 UI/UX

### สี
- **หลัก**: #FF6B6B (แดงอมส้ม)
- **สำเร็จ**: #4CAF50 (เขียว)
- **พื้นหลัง**: #f0f2f6 (เทาอ่อน)

### Layout
- **2 คอลัมน์**: อัปโหลด (ซ้าย) | ผลลัพธ์ (ขวา)
- **Sidebar**: ข้อมูลและสถานะระบบ
- **Responsive**: ปรับขนาดตามหน้าจอ

## 📸 ตัวอย่างการใช้งาน

### 1. เปิดเว็บ
```bash
streamlit run app.py
```

### 2. อัปโหลดรูปหมา
- คลิก "Browse files"
- เลือกรูปหมา (JPG, PNG, WEBP)

### 3. คลิก "🔍 ระบุสายพันธุ์"
- รอระบบวิเคราะห์ (2-3 วินาที)
- ดูผลลัพธ์ทางขวา

### 4. อ่านข้อมูลการดูแล
- นิสัยสุนัข
- วิธีการดูแล
- ข้อควรระวัง

## 🔧 Configuration

### API Endpoint
```python
API_URL = "https://chetsadaphon66-dog-breed-classifier.hf.space/predict"
HEALTH_URL = "https://chetsadaphon66-dog-breed-classifier.hf.space/health"
```

### Page Config
```python
st.set_page_config(
    page_title="🐕 Dog Breed Classifier",
    page_icon="🐕",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 🐛 Troubleshooting

### ปัญหา: ไม่สามารถเชื่อมต่อ API
**แก้ไข**: ตรวจสอบว่า API ทำงานปกติ
```bash
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health
```

### ปัญหา: Streamlit ไม่เปิด
**แก้ไข**: ติดตั้ง streamlit ใหม่
```bash
pip install --upgrade streamlit
```

### ปัญหา: รูปอัปโหลดไม่ได้
**แก้ไข**: ตรวจสอบ file type (JPG, PNG, WEBP เท่านั้น)

## 📊 Performance

- **เวลาโหลดหน้า**: < 1 วินาที
- **เวลาอัปโหลด**: ขึ้นกับขนาดไฟล์
- **เวลาวิเคราะห์**: 2-3 วินาที (รวม API call)

## 🎯 Use Cases

### 1. Demo โปรเจค
- แสดงให้อาจารย์/เพื่อนดู
- ทดสอบ real-time

### 2. ทดสอบ Model
- ลองรูปหมาหลายๆ สายพันธุ์
- เช็คความแม่นยำ

### 3. เรียนรู้ข้อมูลสุนัข
- อ่านข้อมูลการดูแล
- เปรียบเทียบสายพันธุ์

## 📝 Code Structure

```python
app.py
├── Configuration (API URLs)
├── Page Config (title, icon, layout)
├── Custom CSS (styling)
├── Header (title, subtitle)
├── Sidebar (info, health check)
├── Main Content
│   ├── Column 1: Upload
│   │   ├── File uploader
│   │   ├── Image display
│   │   └── Predict button
│   └── Column 2: Results
│       ├── Breed name & confidence
│       ├── Care information (5 sections)
│       └── Top 5 predictions
└── Footer
```

## 🚀 Next Steps

### เพิ่มฟีเจอร์
- [ ] บันทึกประวัติการค้นหา
- [ ] เปรียบเทียบหลายรูป
- [ ] Export ผลลัพธ์เป็น PDF
- [ ] แชร์ผลลัพธ์ผ่าน social media

### ปรับปรุง UI
- [ ] เพิ่ม animation
- [ ] Dark mode
- [ ] Mobile responsive ดีขึ้น

---

**สร้างโดย**: Chetsadaphon Kantawong  
**วันที่**: 4 พฤษภาคม 2026  
**โปรเจค**: MLOps Final Project
