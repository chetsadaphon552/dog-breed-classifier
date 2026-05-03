# 🐕 Dog Breed Classification API

High-throughput image classification service using optimized ONNX ResNet-34 model for dog breed recognition.

## 📊 Model Performance

| Model | Size | Latency (Mean) | Speedup | Size Reduction |
|-------|------|----------------|---------|----------------|
| PyTorch FP32 | 83.00 MB | 43.00 ms | 1.00x (baseline) | 0.0% |
| ONNX FP32 | 83.14 MB | 17.73 ms | **2.42x faster** | -0.2% |
| **ONNX INT8** | **20.92 MB** | **27.92 ms** | **1.54x faster** | **74.8% smaller** |

✅ **Production Model**: ONNX INT8 (Best balance of speed and size)

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn app:app --reload --port 8000
```

### Docker

```bash
docker build -t dog-classifier .
docker run -p 8000:7860 dog-classifier
```

## 🔧 API Usage

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Predict dog breed
curl -X POST "http://localhost:8000/predict" \
  -F "file=@dog_image.jpg"
```

### Python Example

```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("dog.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## 🧪 Testing

```bash
# Run tests
pytest test_api.py -v

# With coverage
pytest test_api.py --cov=app
```

## 📈 Load Testing

Use JMeter to test API performance under load.

## 🌐 Cloud Deployment

Deployed on Hugging Face Spaces with automated CI/CD.
