---
title: Dog Breed Classifier
emoji: 🐕
colorFrom: red
colorTo: pink
sdk: docker
app_port: 7860
tags:
- streamlit
- fastapi
- computer-vision
- image-classification
- dog-breeds
pinned: false
short_description: Dog breed classification with care info (API + UI)
license: apache-2.0
---

# 🐕 Dog Breed Classifier (Combined API + UI)

ระบบจำแนกสายพันธุ์สุนัขแบบครบวงจร - FastAPI Backend + Streamlit UI ใน Space เดียว

## ✨ ฟีเจอร์

### 🎨 Streamlit UI (Port 7860)
- 📤 อัปโหลดรูปหมา
- 🔍 ระบุสายพันธุ์ (103 สายพันธุ์)
- 💚 ข้อมูลการดูแล 5 ด้าน
- 🏆 Top 5 predictions

### 🚀 FastAPI Backend (Port 8000)
- `GET /health` - Health check
- `POST /predict` - Dog breed prediction
- `GET /docs` - Swagger UI

## 🔧 เทคโนโลยี

- **Model**: ResNet-34 (ONNX INT8)
- **Backend**: FastAPI + ProcessPoolExecutor
- **Frontend**: Streamlit
- **Deployment**: Docker (combined container)

## 📊 Performance

- **Inference Time**: ~28 ms (localhost, no network overhead)
- **Accuracy**: 87.0% on Stanford Dogs
- **Model Size**: 20.92 MB (74.8% reduction)
- **Latency**: ต่ำสุด (API + UI อยู่ใน container เดียว)

## 🚀 วิธีใช้

### Web UI (แนะนำ)
เปิดหน้า Space นี้แล้วอัปโหลดรูปหมาได้เลย!

### API Endpoint
```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST "http://localhost:8000/predict" \
  -F "file=@dog.jpg"
```

### Swagger UI
เปิด: `/docs` (เมื่อรันบน localhost)

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Docker Container (HF Space)       │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │  FastAPI     │  │  Streamlit  │ │
│  │  (Port 8000) │←─│  (Port 7860)│ │
│  │              │  │             │ │
│  │  - /health   │  │  - Upload   │ │
│  │  - /predict  │  │  - Display  │ │
│  │  - /docs     │  │  - Results  │ │
│  └──────────────┘  └─────────────┘ │
│         ↓                           │
│  ┌──────────────┐                  │
│  │  ONNX Model  │                  │
│  │  (ResNet-34) │                  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

## 🔗 Links

- **GitHub Repository**: https://github.com/chetsadaphon552/dog-breed-classifier
- **CI/CD**: Auto-deploy from GitHub Actions

---

**Made with ❤️ for MLOps Course 2026**
