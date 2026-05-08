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

## ⚡ Quick Start

### Try the API Now (No Installation Required)

```bash
# 1. Check API health
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health

# 2. Predict dog breed (replace with your image path)
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@your_dog_image.jpg" | jq .

# 3. View API documentation
# Open in browser: https://chetsadaphon66-dog-breed-classifier.hf.space/docs
```

### Test with Sample Image

```bash
# Download sample image
curl -o pug.jpg https://images.dog.ceo/breeds/pug/n02110958_1008.jpg

# Predict breed
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@pug.jpg" | jq .
```

**Expected Response:**
```json
{
  "success": true,
  "breed_name": "pug",
  "confidence": 0.92,
  "inference_time_ms": 28.5
}
```

## 📊 Model Optimization Results

| Model | Size (MB) | Latency (ms) | Speedup | Size Reduction |
|-------|-----------|--------------|---------|----------------|
| PyTorch FP32 | 83.00 | 43.00 | 1.00x | - |
| ONNX FP32 | 83.14 | 17.73 | 2.42x | 0% |
| **ONNX INT8** | **20.92** | **27.92** | **1.54x** | **74.8%** |

**Accuracy**: 74.6% on Stanford Dogs Dataset (96 breeds)

### Performance Metrics
- **Throughput (Local)**: 10-12 TPS (Transactions Per Second)
- **Throughput (Cloud)**: 8-9 TPS on Hugging Face Spaces
- **Inference Time**: 28ms (ONNX INT8)
- **Total Response Time**: 35-45ms (including preprocessing)
- **Error Rate**: 0% (tested with 500-2,000 requests)

## 🚀 Live Demo

**🌐 Web UI (Streamlit)**: https://chetsadaphon66-dog-breed-classifier.hf.space

**📖 API Documentation (Swagger UI)**: https://chetsadaphon66-dog-breed-classifier.hf.space/docs

**🔗 API Endpoint**: https://chetsadaphon66-dog-breed-classifier.hf.space

> **Note**: Currently deployed in **API-only mode** on Hugging Face Spaces (Port 7860). See [SWITCH_MODE.md](SWITCH_MODE.md) for switching between API-only and Combined (API + UI) modes.

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
  "service": "Dog Breed Classification API",
  "model": "ResNet-34 (ONNX INT8)",
  "version": "1.0.0"
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
  "breed_name": "pug",
  "confidence": 0.9234,
  "top_5_predictions": [
    {
      "breed_name": "pug",
      "confidence": 0.9234
    },
    {
      "breed_name": "boston_bull",
      "confidence": 0.0456
    },
    {
      "breed_name": "french_bulldog",
      "confidence": 0.0189
    },
    {
      "breed_name": "chihuahua",
      "confidence": 0.0089
    },
    {
      "breed_name": "english_bulldog",
      "confidence": 0.0032
    }
  ],
  "inference_time_ms": 27.92,
  "total_time_ms": 35.45
}
```

### 6. View API Metrics

```bash
# Get real-time API statistics
curl https://chetsadaphon66-dog-breed-classifier.hf.space/metrics | jq .
```

**Response:**
```json
{
  "uptime_seconds": 3600.45,
  "total_requests": 1250,
  "successful_requests": 1200,
  "failed_requests": 50,
  "success_rate": 96.0,
  "average_inference_time_ms": 28.5,
  "requests_per_second": 0.35,
  "top_5_breeds": {
    "pug": 150,
    "golden_retriever": 120,
    "german_shepherd": 100,
    "chihuahua": 80,
    "beagle": 75
  }
}
```

### 7. Test with Sample Images

```bash
# Download sample dog image
curl -o test_dog.jpg https://images.dog.ceo/breeds/pug/n02110958_1008.jpg

# Predict breed
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@test_dog.jpg" | jq .
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

| Environment | Requests | Throughput | Avg Latency | Error Rate |
|-------------|----------|------------|-------------|------------|
| **Local** | 500 | 12.19 TPS | 2,831 ms | 0% |
| **Local (Stress)** | 2,000 | 10.09 TPS | 15,674 ms | 0% |
| **Cloud (HF Spaces)** | 500 | 8.69 TPS | 4,570 ms | 0% |

**Key Findings:**
- ✅ System is stable (0% error rate) even under 200 concurrent users
- ✅ Cloud throughput is ~71% of local (due to network latency)
- ✅ Bottleneck: ProcessPoolExecutor (2 workers)

## 🔄 CI/CD Pipeline

### Workflow

1. **Push to GitHub** → Triggers CI/CD
2. **Run Tests** → pytest validates all endpoints (10 tests, 85% coverage)
3. **Deploy** → Auto-deploy to HF Spaces if tests pass (2-3 minutes)

### Deployment Modes

The project supports two deployment modes:

#### 1. API-only Mode (Current) ✅
- **Port**: 7860
- **Services**: FastAPI + Swagger UI
- **Use Case**: High-throughput API, load testing, production
- **Access**: 
  - API: https://chetsadaphon66-dog-breed-classifier.hf.space
  - Docs: https://chetsadaphon66-dog-breed-classifier.hf.space/docs

#### 2. Combined Mode (API + Streamlit UI)
- **Port**: 7860 (Streamlit), 8000 (API)
- **Services**: FastAPI + Streamlit Web UI
- **Use Case**: Demo, user-friendly interface
- **Switch**: See [SWITCH_MODE.md](SWITCH_MODE.md) for instructions

### Setup GitHub Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add secret:
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face token (from https://huggingface.co/settings/tokens)

## 📈 Performance Optimization

### Techniques Applied

1. **Model Quantization**: INT8 dynamic quantization (74.8% size reduction)
2. **ONNX Conversion**: 2.42x faster inference vs PyTorch
3. **ProcessPoolExecutor**: Non-blocking CPU-bound operations (2 workers)
4. **Multi-stage Docker**: Minimal production image (~500MB)
5. **Async FastAPI**: High concurrency support

### Benchmarking

```bash
cd models
python step2_benchmark.py
```

## 📊 Monitoring & Logging

### Real-time Metrics

The API provides a `/metrics` endpoint for monitoring:

```bash
curl https://chetsadaphon66-dog-breed-classifier.hf.space/metrics | jq .
```

**Metrics include:**
- Uptime
- Total requests (successful/failed)
- Success rate
- Average inference time
- Requests per second
- Top 5 predicted breeds

### Structured Logging

All requests are logged with:
- 📥 Request received
- 📄 File processing
- 🖼️ Image preprocessing
- 🤖 Model inference
- 🎯 Prediction result
- ❌ Errors (if any)

**Example log:**
```
2026-05-09 14:30:45 - api - INFO - 📥 Received prediction request: filename=dog.jpg
2026-05-09 14:30:45 - api - INFO - 🖼️  Image preprocessed: time=5.23ms
2026-05-09 14:30:45 - api - INFO - 🤖 Starting model inference...
2026-05-09 14:30:45 - api - INFO - ✅ Inference completed: time=27.92ms
2026-05-09 14:30:45 - api - INFO - 🎯 Prediction: pug (92.34%)
```

## 💰 Cost Analysis

### Deployment Options

| Platform | Monthly Cost | Predictions/Month | Cost/Prediction |
|----------|--------------|-------------------|-----------------|
| **HF Spaces (Free)** | $0 | 21M | $0.00 |
| **Google Cloud Run** | ~$3-10 | 1M | $0.000003 |
| **AWS t3.medium** | ~$30 | 38M | $0.00000078 |
| **AWS c6i.xlarge** | ~$123 | 77M | $0.00000158 |

### ROI Example (Pet Clinic Use Case)

```
Usage: 3,000 predictions/month
Revenue: $50/prediction
Cost (AWS t3.medium): $30/month

Monthly Revenue: 3,000 × $50 = $150,000
Monthly Cost: $30
Profit: $149,970
ROI: 499,900%
```

**Conclusion**: Highly cost-effective for production deployment ✅

For detailed cost analysis, see [COST_ANALYSIS.md](COST_ANALYSIS.md)

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root health check |
| `/health` | GET | Detailed health status |
| `/predict` | POST | Dog breed prediction (multipart/form-data) |
| `/metrics` | GET | Real-time API statistics |
| `/docs` | GET | Swagger UI (Interactive API documentation) |
| `/redoc` | GET | ReDoc (Alternative API documentation) |

### Interactive API Documentation

Visit **https://chetsadaphon66-dog-breed-classifier.hf.space/docs** to:
- 📖 View all available endpoints
- 🧪 Test API directly in browser
- 📝 See request/response schemas
- 💡 Get code examples in multiple languages

## 📝 Error Handling

The API implements production-ready error handling:

- **400 Bad Request**: Invalid file type, corrupted image, file too large (>10MB)
- **422 Unprocessable Entity**: Missing required fields
- **500 Internal Server Error**: Model inference failure
- **Pydantic Validation**: Automatic request/response validation

### Common Issues

#### Issue 1: "Connection refused" or "Connection timeout"
**Solution**: Check if API is running and accessible
```bash
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health
```

#### Issue 2: "Invalid file type"
**Solution**: Only JPG, JPEG, PNG formats are supported
```bash
# Check file type
file your_image.jpg

# Convert if needed (using ImageMagick)
convert your_image.webp your_image.jpg
```

#### Issue 3: "File too large"
**Solution**: Maximum file size is 10MB
```bash
# Check file size
ls -lh your_image.jpg

# Resize if needed (using ImageMagick)
convert your_image.jpg -resize 800x800 your_image_resized.jpg
```

#### Issue 4: Slow response time
**Possible causes**:
- Network latency (Cloud deployment)
- High concurrent load
- Large image file

**Solution**: 
- Use smaller images (< 1MB recommended)
- Test locally for faster response
- Check `/metrics` endpoint for system load

## 🙏 Acknowledgments

- **Model**: microsoft/resnet-34 from Hugging Face
- **Dataset**: Stanford Dogs Dataset (120 breeds, 20,580 images)
- **Frameworks**: FastAPI, ONNX Runtime, PyTorch
- **Deployment**: Hugging Face Spaces
- **Testing**: pytest, JMeter
- **CI/CD**: GitHub Actions

## 📚 Documentation

- [COST_ANALYSIS.md](COST_ANALYSIS.md) - Detailed cost analysis and ROI
- [MONITORING_AND_LOGGING.md](MONITORING_AND_LOGGING.md) - Monitoring features
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [SWITCH_MODE.md](SWITCH_MODE.md) - Switch between API-only and Combined modes
- [DOCKER_AND_CICD.md](DOCKER_AND_CICD.md) - Docker and CI/CD documentation

## 📄 License

This project is for educational purposes (MLOps Course).

## 👥 Author

**Chetsadaphon Kanthiya**
- GitHub: [@chetsadaphon552](https://github.com/chetsadaphon552)
- Hugging Face: [@chetsadaphon66](https://huggingface.co/chetsadaphon66)

## 🌟 Project Stats

![GitHub stars](https://img.shields.io/github/stars/chetsadaphon552/dog-breed-classifier?style=social)
![GitHub forks](https://img.shields.io/github/forks/chetsadaphon552/dog-breed-classifier?style=social)
![GitHub issues](https://img.shields.io/github/issues/chetsadaphon552/dog-breed-classifier)
![GitHub last commit](https://img.shields.io/github/last-commit/chetsadaphon552/dog-breed-classifier)

---

**Made with ❤️ for MLOps Course - May 2026**

**🚀 Live Demo**: https://chetsadaphon66-dog-breed-classifier.hf.space  
**📖 API Docs**: https://chetsadaphon66-dog-breed-classifier.hf.space/docs

