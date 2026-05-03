# 🐕 Dog Breed Classification - Complete Workflow

## 📋 Overview

This project implements a **Dog Breed Classification API** using **ResNet-34** from Microsoft.

- **Model**: microsoft/resnet-34 (Hugging Face)
- **Architecture**: ResNet-34 (CNN)
- **Dog Breeds**: 96 breeds (filtered from ImageNet 1000 classes)
- **Dataset**: Stanford Dogs (Kaggle)
- **Formats**: PyTorch FP32 → ONNX FP32 → ONNX INT8

---

## 🚀 Complete Pipeline

### Step 1: Download & Convert Model
```bash
python models/step1_download_and_convert.py
```

**What it does:**
1. Downloads `microsoft/resnet-34` from Hugging Face
2. Exports to ONNX FP32 (83 MB)
3. Quantizes to ONNX INT8 (21 MB)
4. Saves dog breed labels (96 breeds)

**Output:**
- `models/resnet34_fp32.onnx` (83 MB)
- `models/resnet34_int8.onnx` (21 MB)
- `models/resnet34_dog_breeds.json` (96 breeds)

---

### Step 2: Benchmark Performance
```bash
python models/step2_benchmark.py
```

**What it does:**
1. Benchmarks all 3 models (PyTorch FP32, ONNX FP32, ONNX INT8)
2. Measures inference time (100 iterations)
3. Compares speed and size
4. Generates comparison charts

**Output:**
- `benchmark_dogs_results.json` (detailed metrics)
- `benchmark_dogs_results.png` (comparison charts)

**Results:**
| Model | Size | Latency | Speedup |
|-------|------|---------|---------|
| PyTorch FP32 | 83 MB | 96 ms | 1.0× |
| ONNX FP32 | 83 MB | 18 ms | 5.2× |
| ONNX INT8 | 21 MB | 30 ms | 3.2× |

---

### Step 3: Evaluate Accuracy
```bash
python models/step3_evaluate_accuracy.py
```

**What it does:**
1. Downloads Stanford Dogs dataset from Kaggle
2. Tests all 3 models on 30 breeds (750 images)
3. Calculates accuracy, precision, recall, F1
4. Generates confusion matrix
5. Creates comparison charts

**Output:**
- `evaluation_results/resnet34_pytorch_fp32/` (PyTorch results)
- `evaluation_results/resnet34_onnx_fp32/` (ONNX FP32 results)
- `evaluation_results/resnet34_onnx_int8/` (ONNX INT8 results)
- `evaluation_results/resnet34_dogs_comparison.json` (comparison)
- `evaluation_results/resnet34_dogs_comparison.png` (charts)

**Results:**
- **Accuracy**: 86.80% (breed-specific)
- **Dog Detection**: 96.93% (any dog breed)
- **Tested**: 30 breeds, 750 images

---

## 🎯 Run API

### Option 1: Python (Development)
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Docker (Production)
```bash
# Build image
docker build -f Dockerfile.onnx -t dog-classification-api:latest .

# Run container
docker run -d --name dog-api -p 8000:8000 dog-classification-api:latest

# Check logs
docker logs dog-api

# Test API
curl http://localhost:8000/
```

### Test API
```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# List breeds
curl http://localhost:8000/breeds

# Predict
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@pug.jpg;type=image/jpeg'
```

### Swagger UI
http://localhost:8000/docs

---

## 📊 Model Comparison

### Size
- **PyTorch FP32**: 83 MB
- **ONNX FP32**: 83 MB (same size, faster inference)
- **ONNX INT8**: 21 MB (74.8% smaller)

### Speed (Local)
- **PyTorch FP32**: 96 ms
- **ONNX FP32**: 18 ms (5.2× faster)
- **ONNX INT8**: 30 ms (3.2× faster)

### Speed (Cloud - estimated 2.4× slower)
- **PyTorch FP32**: ~230 ms ⚠️ (exceeds 100ms target)
- **ONNX FP32**: ~44 ms ✅
- **ONNX INT8**: ~73 ms ✅

### Accuracy
- **All models**: 86.80% (same accuracy)
- **Dog Detection**: 96.93%

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application (Dog API)
│   ├── model.py             # ResNet-34 inference logic
│   ├── config.py            # Configuration (96 dog breeds)
│   └── schemas.py           # Pydantic models
│
├── models/
│   ├── step1_download_and_convert.py  # Download & convert ResNet-34
│   ├── step2_benchmark.py             # Benchmark all models
│   ├── step3_evaluate_accuracy.py     # Evaluate on Stanford Dogs
│   │
│   ├── resnet34_fp32.onnx             # ONNX FP32 model (83 MB)
│   ├── resnet34_int8.onnx             # ONNX INT8 model (21 MB)
│   └── resnet34_dog_breeds.json       # 96 dog breed labels
│
├── evaluation_results/
│   ├── resnet34_pytorch_fp32/         # PyTorch evaluation
│   ├── resnet34_onnx_fp32/            # ONNX FP32 evaluation
│   ├── resnet34_onnx_int8/            # ONNX INT8 evaluation
│   ├── resnet34_dogs_comparison.json  # Comparison data
│   └── resnet34_dogs_comparison.png   # Comparison charts
│
├── Dockerfile.onnx          # Docker image for production
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🔄 Complete Workflow Summary

1. **Step 1**: Download ResNet-34 → Convert to ONNX FP32 → Quantize to INT8
2. **Step 2**: Benchmark all 3 models → Compare speed & size
3. **Step 3**: Evaluate on Stanford Dogs → Calculate accuracy & metrics
4. **Deploy**: Run API with Docker or Python

---

## 🎯 Key Findings

### ✅ Meets Requirements
- **Size**: 21 MB (INT8) - much smaller than 300 MB target
- **Speed**: 73 ms (cloud) - meets <100ms target
- **Accuracy**: 86.80% - good performance

### 🏆 Best Model
- **ONNX INT8** (resnet34_int8.onnx)
  - Smallest: 21 MB
  - Fast: 30 ms (local), 73 ms (cloud)
  - Accurate: 86.80%
  - Production-ready ✅

### 📈 Optimization Results
- **Size Reduction**: 74.8% (83 MB → 21 MB)
- **Speed Improvement**: 3.2× faster than PyTorch
- **Accuracy**: No loss (86.80% maintained)

---

## 🛠️ Quick Commands

```bash
# Complete pipeline (run all steps)
python models/step1_download_and_convert.py
python models/step2_benchmark.py
python models/step3_evaluate_accuracy.py

# Run API (Python)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run API (Docker)
docker build -f Dockerfile.onnx -t dog-classification-api:latest .
docker run -d --name dog-api -p 8000:8000 dog-classification-api:latest

# Test API
curl http://localhost:8000/
curl http://localhost:8000/docs
```

---

## 📝 Notes

- **Dataset**: Stanford Dogs (120 breeds), but only 96 match ResNet-34
- **Evaluation**: Tested on 30 breeds (750 images) for faster testing
- **Non-dog classes**: Filtered out 7 non-dog classes (axolotl, Komodo dragon, etc.)
- **Cloud performance**: Estimated 2.4× slower than local (based on HF Spaces)

---

## 🎉 Success Criteria

✅ **Model Size**: 21 MB < 300 MB target
✅ **Inference Speed**: 73 ms < 100 ms target (cloud)
✅ **Accuracy**: 86.80% (good performance)
✅ **Production Ready**: Docker image available
✅ **API**: FastAPI with Swagger UI
✅ **Documentation**: Complete workflow documented

---

## 🚀 Next Steps

1. **Deploy to Cloud** (AWS, GCP, Azure, HF Spaces)
2. **Add more features**:
   - Batch prediction
   - Confidence threshold
   - Multi-language support
3. **Optimize further**:
   - Try ONNX Runtime optimizations
   - Test on GPU
   - Explore other quantization methods
