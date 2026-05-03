---
title: Waste Classification API
emoji: ♻️
colorFrom: green
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
license: mit
---

# ♻️ Waste Classification API

High-throughput API for waste classification using ONNX INT8 quantized model.

## 🚀 Features

- **Fast Inference**: ~90-100ms on CPU (ONNX INT8 quantized)
- **High Throughput**: Handles concurrent requests efficiently
- **6 Waste Categories**: cardboard, glass, metal, paper, plastic, trash
- **Production Ready**: Comprehensive error handling and validation
- **RESTful API**: Easy to integrate

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Model Size | 85.47 MB (74% reduction) |
| Inference Time | ~90-100ms (CPU) |
| Accuracy | High (pre-trained on waste dataset) |
| Format | ONNX INT8 Quantized |

## 🔗 API Endpoints

### Health Check
```bash
GET /health
```

### Predict
```bash
POST /predict
Content-Type: multipart/form-data
Body: file (image/jpeg, image/png, image/bmp)
```

## 💻 Usage Examples

### cURL
```bash
# Health check
curl https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME/health

# Predict
curl -X POST https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME/predict \
  -F "file=@image.jpg"
```

### Python
```python
import requests

# Predict
url = "https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME/predict"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📝 Response Format

```json
{
  "prediction": "plastic",
  "confidence": 0.85,
  "description": "พลาสติก - ขวดน้ำ, ถุงพลาสติก, ภาชนะพลาสติก",
  "recyclable": true,
  "all_predictions": {
    "cardboard": 0.05,
    "glass": 0.03,
    "metal": 0.02,
    "paper": 0.03,
    "plastic": 0.85,
    "trash": 0.02
  },
  "inference_time_ms": 95.2,
  "model_version": "onnx-quantized",
  "timestamp": "2026-05-03T12:00:00.000000"
}
```

## 🎯 Waste Categories

| Category | Thai | Recyclable | Examples |
|----------|------|------------|----------|
| cardboard | กระดาษแข็ง | ✅ Yes | กล่องพัสดุ, กล่องซีเรียล |
| glass | แก้ว | ✅ Yes | ขวดแก้ว, โหลแก้ว |
| metal | โลหะ | ✅ Yes | กระป๋องเครื่องดื่ม, กระป๋องอาหาร |
| paper | กระดาษ | ✅ Yes | กระดาษ A4, หนังสือพิมพ์ |
| plastic | พลาสติก | ✅ Yes | ขวดน้ำ, ถุงพลาสติก |
| trash | ขยะทั่วไป | ❌ No | ถุงขนม, เศษอาหาร |

## 🛠️ Technical Stack

- **Framework**: FastAPI
- **Model**: ONNX INT8 Quantized
- **Inference**: ONNX Runtime
- **Concurrency**: ProcessPoolExecutor
- **Container**: Docker (multi-stage build)

## 📚 Documentation

- **Interactive API Docs**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **GitHub Repository**: [Link to your repo]

## 🔒 Error Handling

The API handles various error cases:
- **400**: Invalid image, corrupted file, empty file
- **413**: File too large (max 10MB)
- **415**: Unsupported file type
- **422**: Missing required fields
- **500**: Internal server error

## 🚀 Performance

- **Latency**: ~90-100ms (P95)
- **Throughput**: ~10 requests/second (single instance)
- **Concurrency**: Handles multiple concurrent requests
- **Resource**: CPU-optimized (no GPU required)

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

MLOps Project - High-Throughput Image Classification Service

## 🙏 Acknowledgments

- Base model: `yangy50/garbage-classification`
- Framework: FastAPI, ONNX Runtime
- Deployment: Hugging Face Spaces

