---
title: Dog Breed Classifier UI
emoji: 🐕
colorFrom: red
colorTo: pink
sdk: docker
app_port: 8501
tags:
- streamlit
- computer-vision
- image-classification
- dog-breeds
pinned: false
short_description: ระบุสายพันธุ์สุนัขจากรูปภาพ พร้อมข้อมูลการดูแล
license: apache-2.0
---

# 🐕 Dog Breed Classifier UI

หน้าเว็บสำหรับระบุสายพันธุ์สุนัขจากรูปภาพ พร้อมข้อมูลการดูแล

## ✨ ฟีเจอร์

- 📤 **อัปโหลดรูปหมา** - รองรับ JPG, PNG, WEBP
- 🔍 **ระบุสายพันธุ์** - รองรับ 103 สายพันธุ์
- 💚 **ข้อมูลการดูแล** - 5 ด้าน (นิสัย, ออกกำลังกาย, โภชนาการ, สุขภาพ, ดูแลขน)
- 🏆 **Top 5 Predictions** - แสดงสายพันธุ์ที่เป็นไปได้

## 🚀 วิธีใช้

1. อัปโหลดรูปหมา
2. คลิก "🔍 ระบุสายพันธุ์"
3. ดูผลลัพธ์และข้อมูลการดูแล

## 🔧 เทคโนโลยี

- **Model**: ResNet-34 (ONNX INT8)
- **Backend**: FastAPI + ProcessPoolExecutor
- **Frontend**: Streamlit
- **API**: https://chetsadaphon66-dog-breed-classifier.hf.space

## 📊 Performance

- **Inference Time**: ~28 ms
- **Accuracy**: 87.0% on Stanford Dogs
- **Model Size**: 20.92 MB (74.8% reduction)

## 🔗 Links

- **API Backend**: https://huggingface.co/spaces/chetsadaphon66/dog-breed-classifier
- **GitHub Repository**: https://github.com/chetsadaphon552/dog-breed-classifier

---

**Made with ❤️ for MLOps Course 2026**

