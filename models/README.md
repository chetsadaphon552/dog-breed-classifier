# 🤖 Models Directory

## 📦 โมเดลที่ใช้ในโปรเจค

โปรเจคนี้ใช้โมเดล **Vision Transformer (ViT)** จาก Hugging Face สำหรับจำแนกขยะ 6 ประเภท

### Model Information

| Property | Value |
|----------|-------|
| **Model Name** | yangy50/garbage-classification |
| **Architecture** | Vision Transformer (ViT) |
| **Base Model** | google/vit-base-patch16-224-in21k |
| **Input Size** | 224×224 pixels |
| **Categories** | cardboard, glass, metal, paper, plastic, trash |
| **Hugging Face** | [Link](https://huggingface.co/yangy50/garbage-classification) |

---

## 🚀 วิธีใช้งาน (3 ขั้นตอน)

### Step 1: ดาวน์โหลดและแปลงโมเดล

```bash
python models/step1_download_and_convert.py
```

**หน้าที่:**
- ✅ ดาวน์โหลดโมเดลจาก Hugging Face
- ✅ แปลงเป็น ONNX FP32
- ✅ ทำ INT8 Quantization
- ✅ Benchmark เบื้องต้น

**ผลลัพธ์:**
- `model_original.pth` (327 MB) - PyTorch
- `model.onnx` (328 MB) - ONNX FP32
- `model_quantized.onnx` (83 MB) - ONNX INT8 ⭐

**เวลา:** ~5-10 นาที

---

### Step 2: Benchmark โมเดล

```bash
python models/step2_benchmark.py
```

**หน้าที่:**
- ✅ เปรียบเทียบ performance ทั้ง 3 เวอร์ชัน
- ✅ วัด latency, throughput
- ✅ สร้างกราฟเปรียบเทียบ

**ผลลัพธ์:**
- `benchmark_results.json` - ผลลัพธ์แบบ JSON
- `benchmark_results.png` - กราฟเปรียบเทียบ

**เวลา:** ~2-3 นาที

---

### Step 3: ประเมินความแม่นยำ

```bash
python models/step3_evaluate_accuracy.py
```

**หน้าที่:**
- ✅ ดาวน์โหลด Kaggle dataset
- ✅ ทดสอบความแม่นยำ (300 images)
- ✅ สร้าง confusion matrix
- ✅ คำนวณ precision, recall, f1-score

**ผลลัพธ์:**
- `model_evaluation_results.json` - ผลลัพธ์แบบละเอียด
- `confusion_matrix.png` - Confusion matrix
- `classification_metrics.png` - กราฟ metrics

**เวลา:** ~5-10 นาที

---

## 📁 ไฟล์โมเดล

หลังจากรัน Step 1 จะได้โมเดล 3 เวอร์ชัน:

| ไฟล์ | ขนาด | ประเภท | ใช้งาน |
|------|------|--------|--------|
| **model_quantized.onnx** ⭐ | **83 MB** | **ONNX INT8** | **✅ ใช้ใน API** |
| model.onnx | 328 MB | ONNX FP32 | สำหรับเปรียบเทียบ |
| model_original.pth | 327 MB | PyTorch | สำหรับเปรียบเทียบ |

---

## 📊 Performance Metrics

### Model Optimization Results (จาก Step 1 & 2)

| Model Type | Size (MB) | Latency (ms) | Speedup |
|------------|-----------|--------------|---------|
| PyTorch FP32 | 327.39 | 124.51 | 1.00× |
| ONNX FP32 | 327.57 | 92.61 | 1.34× |
| **ONNX INT8** ⭐ | **83.06** | **37.74** | **3.30×** |

**Optimization Summary:**
- 🚀 **3.30× faster** than PyTorch baseline
- 📦 **74.6% smaller** (327 MB → 83 MB)
- ⚡ **27 images/second** throughput

### Model Accuracy (จาก Step 3)

| Metric | Value |
|--------|-------|
| **Accuracy** | **97.33%** |
| **Avg Confidence** | **93.53%** |
| **Precision** | **97.48%** |
| **Recall** | **97.33%** |
| **F1-Score** | **97.33%** |

### Performance by Category

| Category | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Cardboard | 92.59% | 100% | 96.15% |
| Glass | 96.15% | 100% | 98.04% |
| Metal | 96.15% | 100% | 98.04% |
| Paper | 100% | 92% | 95.83% |
| Plastic | 100% | 98% | 98.99% |
| Trash | 100% | 94% | 96.91% |

---

## 🔧 Scripts ในโฟลเดอร์นี้

### ✅ ไฟล์ที่ใช้งาน (เรียงตามลำดับ)

1. **`step1_download_and_convert.py`** - ดาวน์โหลดและแปลงโมเดล
2. **`step2_benchmark.py`** - Benchmark performance
3. **`step3_evaluate_accuracy.py`** - ประเมินความแม่นยำ

### 📝 ไฟล์อื่นๆ

- `__init__.py` - Package initialization
- `README.md` - ไฟล์นี้

---

## 🎯 Quick Start

### สำหรับผู้ใช้งานครั้งแรก:

```bash
# 1. ดาวน์โหลดและสร้างโมเดล
python models/step1_download_and_convert.py

# 2. Benchmark (optional)
python models/step2_benchmark.py

# 3. ประเมินความแม่นยำ (optional)
python models/step3_evaluate_accuracy.py

# 4. รัน API
uvicorn app.main:app --reload

# 5. ทดสอบ
curl http://localhost:8000/health
```

---

## 🔍 Troubleshooting

### ปัญหา: "Model not found"

**วิธีแก้:**
```bash
# รัน Step 1 ใหม่
python models/step1_download_and_convert.py
```

### ปัญหา: "Out of memory"

**วิธีแก้:**
- ใช้โมเดล quantized (83 MB) แทน FP32 (327 MB)
- ปิดโปรแกรมอื่นๆ
- เพิ่ม RAM

### ปัญหา: "Download failed"

**วิธีแก้:**
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ลองดาวน์โหลดใหม่
- ใช้ VPN ถ้า Hugging Face ถูกบล็อก

### ปัญหา: "kagglehub not found" (Step 3)

**วิธีแก้:**
```bash
pip install kagglehub
```

---

## 📚 Additional Resources

### Model Documentation
- **Hugging Face**: https://huggingface.co/yangy50/garbage-classification
- **Base Model**: google/vit-base-patch16-224-in21k
- **Paper**: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"

### ONNX Resources
- **ONNX**: https://onnx.ai/
- **ONNX Runtime**: https://onnxruntime.ai/
- **Quantization Guide**: https://onnxruntime.ai/docs/performance/quantization.html

---

## ✅ Checklist

- [ ] รัน Step 1: ดาวน์โหลดโมเดล
- [ ] ตรวจสอบว่ามีไฟล์ `model_quantized.onnx`
- [ ] รัน Step 2: Benchmark (optional)
- [ ] รัน Step 3: ประเมินความแม่นยำ (optional)
- [ ] รัน API: `uvicorn app.main:app --reload`
- [ ] ทดสอบ prediction

---

## 📝 Notes

- โมเดลไม่ถูกเก็บใน Git repository (ขนาดใหญ่)
- ต้องรัน Step 1 ก่อนใช้งาน API
- Step 2 และ 3 เป็น optional (สำหรับดูผลลัพธ์)
- โมเดลที่ใช้จริงใน API คือ `model_quantized.onnx`

---

**Model Status**: ✅ Production Ready

**Last Updated**: May 1, 2026

**Model Version**: yangy50/garbage-classification (Vision Transformer)
