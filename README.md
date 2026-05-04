# 🐕 Dog Breed Classification API

High-throughput image classification service using optimized ONNX ResNet-34 model for MLOps course project.

[![CI/CD](https://github.com/chetsadaphon552/dog-breed-classifier/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/chetsadaphon552/dog-breed-classifier/actions)
[![HF Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/chetsadaphon66/dog-breed-classifier)

## 🎯 Project Overview

This project implements a production-ready dog breed classification API with:
- **96 Dog Breeds** classification
- **ONNX INT8** quantized model (74.8% smaller, 1.54x faster)
- **FastAPI** with async/await and ProcessPoolExecutor
- **Docker** containerization
- **CI/CD** pipeline with GitHub Actions
- **Auto-deployment** to Hugging Face Spaces

## 📊 Model Optimization Results

| Model | Size (MB) | Latency (ms) | Speedup | Size Reduction |
|-------|-----------|--------------|---------|----------------|
| PyTorch FP32 | 83.00 | 43.00 | 1.00x | - |
| ONNX FP32 | 83.14 | 17.73 | 2.42x | 0% |
| **ONNX INT8** | **20.92** | **27.92** | **1.54x** | **74.8%** |

**Accuracy**: 87.0% on Stanford Dogs Dataset (30 breeds tested)

## 🚀 Live Demo

**API Endpoint**: https://chetsadaphon66-dog-breed-classifier.hf.space

**Streamlit UI**: https://chetsadaphon66-dog-breed-classifier.hf.space (Port 7860)

## 📡 API Usage Examples

### 1. Health Check

```bash
# Basic health check
curl https://chetsadaphon66-dog-breed-classifier.hf.space/

# Detailed health status
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "breeds_loaded": true,
  "care_info_loaded": true,
  "num_breeds": 96
}
```

### 2. Predict Dog Breed (cURL)

```bash
# Basic prediction
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@dog_image.jpg"

# Save response to file
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@dog_image.jpg" \
  -o response.json

# Pretty print JSON response
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@dog_image.jpg" | jq .
```

### 3. Python Example

```python
import requests

# Predict dog breed
url = "https://chetsadaphon66-dog-breed-classifier.hf.space/predict"
files = {"file": open("dog.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()

print(f"Breed: {result['breed_name']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Inference Time: {result['inference_time_ms']:.2f}ms")
```

### 4. JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('dog.jpg'));

axios.post('https://chetsadaphon66-dog-breed-classifier.hf.space/predict', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Breed:', response.data.breed_name);
  console.log('Confidence:', response.data.confidence);
})
.catch(error => console.error('Error:', error));
```

### 5. PowerShell Example (Windows)

```powershell
# Predict dog breed
$uri = "https://chetsadaphon66-dog-breed-classifier.hf.space/predict"
$filePath = "C:\path\to\dog.jpg"

$form = @{
    file = Get-Item -Path $filePath
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

**Response Example:**
```json
{
  "success": true,
  "predicted_class": 254,
  "breed_name": "pug",
  "confidence": 0.9234,
  "top_5_predictions": [
    {
      "class_id": 254,
      "breed_name": "pug",
      "confidence": 0.9234
    },
    {
      "class_id": 195,
      "breed_name": "Boston bull",
      "confidence": 0.0456
    },
    {
      "class_id": 245,
      "breed_name": "French bulldog",
      "confidence": 0.0189
    }
  ],
  "care_info": {
    "personality": "สายพันธุ์นี้มีนิสัยขี้เล่น รักเจ้าของ ตลก เหมาะกับครอบครัวที่มีเด็ก",
    "exercise": "ควรเดินเล่นเบาๆ 20-30 นาที/วัน ระวังออกกำลังกายหนักเพราะหายใจลำบาก",
    "nutrition": "ควบคุมปริมาณอาหาร 1-1.5 ถ้วย/วัน เพราะง่ายต่อการอ้วน",
    "health_care": "ควรระวังปัญหาทางเดินหายใจ โรคอ้วน และตา พบสัตวแพทย์ปีละ 2 ครั้ง",
    "grooming": "ควรแปรงขนสัปดาห์ละ 2-3 ครั้ง ทำความสะอาดรอยพับบนใบหน้า"
  },
  "inference_time_ms": 27.92
}
```

### 6. Test with Sample Images

```bash
# Download sample dog image
curl -o test_dog.jpg https://images.dog.ceo/breeds/pug/n02110958_1008.jpg

# Predict breed
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@test_dog.jpg"
```

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client    │────▶│   FastAPI    │────▶│ ProcessPool     │
│  (HTTP)     │     │  (Async)     │     │ Executor        │
└─────────────┘     └──────────────┘     └─────────────────┘
                            │                      │
                            │                      ▼
                            │             ┌─────────────────┐
                            │             │  ONNX Runtime   │
                            │             │  (INT8 Model)   │
                            │             └─────────────────┘
                            ▼
                    ┌──────────────┐
                    │   Response   │
                    │   (JSON)     │
                    └──────────────┘
```

### Key Components

- **FastAPI**: Async web framework with Pydantic validation
- **ProcessPoolExecutor**: Handles CPU-bound inference without blocking
- **ONNX Runtime**: Optimized inference engine
- **Docker**: Multi-stage build for minimal image size (~500MB)
- **GitHub Actions**: Automated testing and deployment

## 📁 Project Structure

```
dog-breed-classifier/
├── api.py                          # FastAPI application
├── Dockerfile                      # Production container
├── requirements.txt                # Python dependencies
├── test_api.py                     # Unit tests (10 tests)
├── models/
│   ├── step1_download_and_convert.py   # Model conversion
│   ├── step2_benchmark.py              # Performance testing
│   ├── step3_evaluate_accuracy.py      # Accuracy evaluation
│   ├── resnet34_int8.onnx              # Quantized model
│   └── resnet34_dog_breeds.json        # Breed mapping
├── jmeter/
│   ├── dog_classifier_loadtest.jmx     # Load test plan
│   └── README.md                       # JMeter guide
├── .github/
│   └── workflows/
│       └── ci-cd.yml                   # CI/CD pipeline
└── docs/
    ├── CURL_COMMANDS.md                # API usage examples
    ├── PROJECT_REPORT_TEMPLATE.md      # Report template
    └── GIT_SETUP.md                    # Deployment guide
```

## 🛠️ Local Development

### Prerequisites

- Python 3.11+
- Docker (optional)
- Git

### Setup

1. **Clone repository**
```bash
git clone https://github.com/chetsadaphon552/dog-breed-classifier.git
cd dog-breed-classifier
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run API locally**
```bash
python api.py
```

API will be available at: http://localhost:8000

### Run Tests

```bash
pytest test_api.py -v
```

**Expected output**: 10/10 tests passed ✅

## 🐳 Docker

### Build and Run

```bash
# Build image
docker build -t dog-classifier .

# Run container
docker run -p 7860:7860 dog-classifier
```

### Pre-built Image

```bash
docker pull chetsadaphon66/dog-classifier:latest
docker run -p 7860:7860 chetsadaphon66/dog-classifier:latest
```

## 🧪 Testing

### Unit Tests

```bash
pytest test_api.py -v --cov=api
```

### Load Testing (JMeter)

```bash
cd jmeter
jmeter -n -t dog_classifier_loadtest.jmx -l results.jtl -e -o report/
```

**Performance Results:**
- **Local**: 35 TPS, P95 latency: 45ms
- **Cloud (HF Spaces)**: 15-20 TPS, P95 latency: 120ms

## 🔄 CI/CD Pipeline

### Workflow

1. **Push to GitHub** → Triggers CI/CD
2. **Run Tests** → pytest validates all endpoints
3. **Deploy** → Auto-deploy to HF Spaces if tests pass

### Setup GitHub Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add secret:
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face token (from https://huggingface.co/settings/tokens)

## 📈 Performance Optimization

### Techniques Applied

1. **Model Quantization**: INT8 dynamic quantization (74.8% size reduction)
2. **ONNX Conversion**: 2.42x faster inference vs PyTorch
3. **ProcessPoolExecutor**: Non-blocking CPU-bound operations
4. **Multi-stage Docker**: Minimal production image
5. **Async FastAPI**: High concurrency support

### Benchmarking

```bash
cd models
python step2_benchmark.py
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root health check |
| `/health` | GET | Detailed health status |
| `/predict` | POST | Dog breed prediction |
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |

## 📝 Error Handling

The API implements production-ready error handling:

- **400 Bad Request**: Invalid file type, corrupted image, file too large
- **500 Internal Server Error**: Model inference failure
- **Pydantic Validation**: Automatic request/response validation

## 🙏 Acknowledgments

- **Model**: microsoft/resnet-34 from Hugging Face
- **Dataset**: Stanford Dogs Dataset
- **Frameworks**: FastAPI, ONNX Runtime, PyTorch
- **Deployment**: Hugging Face Spaces

## 📄 License

This project is for educational purposes (MLOps Course).

## 👥 Author

**Chetsadaphon Kantawong**
- GitHub: [@chetsadaphon552](https://github.com/chetsadaphon552)
- Hugging Face: [@chetsadaphon66](https://huggingface.co/chetsadaphon66)

---

**Made with ❤️ for MLOps Course - May 2026**

