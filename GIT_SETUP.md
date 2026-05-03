# 🚀 Git Setup และ Deployment Guide

## ขั้นตอนที่ 1: สร้าง GitHub Repository

### 1.1 สร้าง Repository บน GitHub

1. ไปที่ https://github.com/new
2. ตั้งค่า:
   - **Repository name**: `dog-breed-classifier-api`
   - **Description**: High-throughput dog breed classification API with ONNX optimization
   - **Visibility**: Public
   - **Initialize**: ไม่ต้องเลือกอะไร (เราจะ push code เอง)
3. คลิก "Create repository"

### 1.2 Initialize Git และ Push Code

```bash
# Initialize git (ถ้ายังไม่ได้ทำ)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Dog breed classification API with ONNX INT8"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/dog-breed-classifier-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## ขั้นตอนที่ 2: ตั้งค่า Hugging Face Spaces

### 2.1 สร้าง Hugging Face Space

1. ไปที่ https://huggingface.co/spaces
2. คลิก "Create new Space"
3. ตั้งค่า:
   - **Owner**: เลือก username ของคุณ
   - **Space name**: `dog-breed-classifier`
   - **License**: MIT
   - **Select the Space SDK**: **Docker**
   - **Space hardware**: CPU basic (free)
4. คลิก "Create Space"

### 2.2 เตรียม Files สำหรับ HF Spaces

Files ที่ต้องมี:
- ✅ `Dockerfile` - มีแล้ว
- ✅ `api.py` - มีแล้ว
- ✅ `requirements.txt` - มีแล้ว
- ✅ `models/resnet34_int8.onnx` - มีแล้ว
- ✅ `models/resnet34_dog_breeds.json` - มีแล้ว

### 2.3 สร้าง README.md สำหรับ HF Space

สร้างไฟล์ `README_HF.md` (จะ copy ไปเป็น README.md ใน HF Space):

```markdown
---
title: Dog Breed Classifier
emoji: 🐕
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Dog Breed Classification API

High-throughput image classification service using optimized ONNX ResNet-34 model.

## Features

- 96 Dog Breeds classification
- ONNX INT8 quantized model (74.8% smaller)
- FastAPI with async support
- ProcessPoolExecutor for concurrency
- Production-ready error handling

## Usage

### Health Check

```bash
curl https://YOUR_USERNAME-dog-breed-classifier.hf.space/health
```

### Predict

```bash
curl -X POST "https://YOUR_USERNAME-dog-breed-classifier.hf.space/predict" \
  -F "file=@dog_image.jpg"
```

## Performance

- Model Size: 20.92 MB (74.8% reduction)
- Inference Time: ~28 ms (local)
- Throughput: 15-20 TPS (cloud)

## Model

- Base: microsoft/resnet-34
- Optimization: ONNX + INT8 quantization
- Accuracy: 87.0% on Stanford Dogs dataset
```

---

## ขั้นตอนที่ 3: ตั้งค่า GitHub Secrets

### 3.1 สร้าง Hugging Face Token

1. ไปที่ https://huggingface.co/settings/tokens
2. คลิก "New token"
3. ตั้งค่า:
   - **Name**: `github-actions-deploy`
   - **Role**: Write
4. คลิก "Generate token"
5. **Copy token** (จะแสดงครั้งเดียว!)

### 3.2 เพิ่ม Secrets ใน GitHub

1. ไปที่ GitHub repository
2. Settings → Secrets and variables → Actions
3. คลิก "New repository secret"

**Secret 1: HF_TOKEN**
- Name: `HF_TOKEN`
- Value: [Paste your HF token]

**Secret 2: HF_SPACE_NAME**
- Name: `HF_SPACE_NAME`
- Value: `YOUR_USERNAME/dog-breed-classifier`
  - ตัวอย่าง: `john-doe/dog-breed-classifier`

---

## ขั้นตอนที่ 4: Deploy to Hugging Face Spaces

### Option A: Manual Deployment (แนะนำครั้งแรก)

```bash
# Clone HF Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/dog-breed-classifier
cd dog-breed-classifier

# Copy files
cp ../api.py .
cp ../Dockerfile .
cp ../requirements.txt .
cp -r ../models .

# Create README
cat > README.md << 'EOF'
---
title: Dog Breed Classifier
emoji: 🐕
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Dog Breed Classification API

[Your description here]
EOF

# Commit and push
git add .
git commit -m "Deploy dog breed classifier API"
git push
```

### Option B: Automatic Deployment (ผ่าน GitHub Actions)

1. Push code to GitHub
2. GitHub Actions จะ run tests อัตโนมัติ
3. ถ้า tests ผ่าน → Deploy to HF Spaces อัตโนมัติ

```bash
# Push code
git add .
git commit -m "Add deployment configuration"
git push origin main
```

---

## ขั้นตอนที่ 5: ตรวจสอบ Deployment

### 5.1 ดู Build Logs

1. ไปที่ HF Space: `https://huggingface.co/spaces/YOUR_USERNAME/dog-breed-classifier`
2. คลิก "Logs" tab
3. รอ build เสร็จ (~5-10 นาที)

### 5.2 ทดสอบ API

```bash
# Health check
curl https://YOUR_USERNAME-dog-breed-classifier.hf.space/health

# Predict
curl -X POST "https://YOUR_USERNAME-dog-breed-classifier.hf.space/predict" \
  -F "file=@pug.jpg"
```

---

## ขั้นตอนที่ 6: รัน JMeter Load Test

### 6.1 ทดสอบ Local

```bash
# Start API
python api.py

# Run JMeter (in another terminal)
jmeter -n -t jmeter/dog_classifier_loadtest.jmx \
  -l jmeter/results_local.jtl \
  -e -o jmeter/html-report-local

# View report
# Open jmeter/html-report-local/index.html
```

### 6.2 ทดสอบ Cloud (HF Spaces)

1. แก้ไข `jmeter/dog_classifier_loadtest.jmx`
2. เปลี่ยน `BASE_URL` เป็น HF Space URL
3. รัน JMeter:

```bash
jmeter -n -t jmeter/dog_classifier_loadtest.jmx \
  -l jmeter/results_cloud.jtl \
  -e -o jmeter/html-report-cloud
```

---

## Troubleshooting

### Build Failed on HF Spaces

**ปัญหา:** Docker build ล้มเหลว

**แก้ไข:**
1. ตรวจสอบ Dockerfile syntax
2. ตรวจสอบว่าไฟล์ model มีอยู่
3. ดู logs ใน HF Space

### API ไม่ตอบสนอง

**ปัญหา:** API ไม่ตอบหลัง deploy

**แก้ไข:**
1. ตรวจสอบว่า container start แล้ว
2. ตรวจสอบ port 7860
3. ดู application logs

### Tests Failed

**ปัญหา:** GitHub Actions tests ล้มเหลว

**แก้ไข:**
1. รัน tests local: `pytest test_api.py -v`
2. แก้ไข bugs
3. Push อีกครั้ง

---

## Summary Checklist

- [ ] สร้าง GitHub repository
- [ ] Push code to GitHub
- [ ] สร้าง HF Space
- [ ] เพิ่ม GitHub secrets (HF_TOKEN, HF_SPACE_NAME)
- [ ] Deploy to HF Spaces (manual หรือ auto)
- [ ] ทดสอบ API บน cloud
- [ ] รัน JMeter load test (local + cloud)
- [ ] เก็บผลการทดสอบ
- [ ] เขียนรายงาน
- [ ] เตรียม presentation

---

## Next Steps

1. ✅ Git setup และ push code
2. ✅ Deploy to HF Spaces
3. ✅ รัน JMeter tests
4. ✅ เก็บผลการทดสอบ
5. ✅ เขียนรายงาน PDF
6. ✅ เตรียม slides presentation
7. ✅ ฝึก live demo

Good luck! 🚀

