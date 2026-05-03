---
title: Dog Breed Classifier
emoji: 🐕
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🐕 Dog Breed Classification API

High-throughput image classification service using optimized ONNX ResNet-34 model.

## 🎯 Features

- **96 Dog Breeds** classification
- **ONNX INT8** quantized model (74.8% smaller, 1.54x faster)
- **FastAPI** with async support
- **ProcessPoolExecutor** for high concurrency
- **Production-ready** error handling

## 📊 Performance

| Metric | Value |
|--------|-------|
| Model Size | 20.92 MB (74.8% reduction) |
| Inference Time | ~28 ms (local) |
| Throughput | 15-20 TPS (cloud) |
| Accuracy | 87.0% on Stanford Dogs |

## 🚀 Usage

### Health Check

```bash
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "breeds_loaded": true,
  "num_breeds": 96
}
```

### Predict Dog Breed

```bash
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@dog_image.jpg"
```

**Response:**
```json
{
  "success": true,
  "predicted_class": 254,
  "breed_name": "pug",
  "confidence": 0.739,
  "top_5_predictions": [
    {
      "class_id": 254,
      "breed_name": "pug",
      "confidence": 0.739
    },
    {
      "class_id": 245,
      "breed_name": "French bulldog",
      "confidence": 0.036
    }
  ],
  "inference_time_ms": 28.5
}
```

### Python Example

```python
import requests

url = "https://chetsadaphon66-dog-breed-classifier.hf.space/predict"
files = {"file": open("dog.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## 🔧 API Endpoints

- `GET /` - Root health check
- `GET /health` - Detailed health status
- `POST /predict` - Dog breed prediction
- `GET /docs` - Swagger UI documentation

## 🏗️ Architecture

- **Model**: ResNet-34 (microsoft/resnet-34)
- **Optimization**: ONNX + INT8 quantization
- **Framework**: FastAPI + Uvicorn
- **Concurrency**: ProcessPoolExecutor (2 workers)
- **Container**: Docker (Python 3.11 slim)

## 📈 Optimization Results

| Model | Size (MB) | Latency (ms) | Speedup |
|-------|-----------|--------------|---------|
| PyTorch FP32 | 83.00 | 43.00 | 1.00x |
| ONNX FP32 | 83.14 | 17.73 | 2.42x |
| **ONNX INT8** | **20.92** | **27.92** | **1.54x** |

## 🧪 Testing

- **Unit Tests**: 10/10 passed (pytest)
- **Load Tests**: JMeter (35 TPS local, 15 TPS cloud)
- **CI/CD**: GitHub Actions

## 📝 Documentation

- **API Docs**: `/docs` (Swagger UI)
- **ReDoc**: `/redoc`

## 🙏 Acknowledgments

- Model: microsoft/resnet-34
- Dataset: Stanford Dogs Dataset
- Framework: FastAPI, ONNX Runtime

---

**Made with ❤️ for MLOps Course**

