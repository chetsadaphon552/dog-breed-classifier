# 🚀 Deployment Guide - API-only with Switch Mode

## 📋 Overview

โปรเจคนี้ใช้ **API-only mode** เป็นหลัก และสามารถ **switch mode** ได้เมื่อต้องการ:

- **API-only** (default) - สำหรับ production, load testing, API integration
- **Streamlit UI** (optional) - สำหรับ demo, user interface
- **Combined** (optional) - รัน API + UI พร้อมกัน

---

## 🔄 CI/CD Pipeline (API-only)

### Automatic Deployment

เมื่อ push code ไป `main` branch:

```bash
git add .
git commit -m "Update API"
git push origin main
```

**GitHub Actions จะ:**
1. ✅ รัน tests (10 tests, 85% coverage)
2. ✅ Deploy API-only ไป HF Spaces (ถ้า tests ผ่าน)
3. ✅ Service พร้อมใช้งานภายใน 2-3 นาที

**URL หลัง deploy:**
```
API: https://chetsadaphon66-dog-breed-classifier.hf.space
Docs: https://chetsadaphon66-dog-breed-classifier.hf.space/docs
```

---

## 🔀 Switch Mode (Manual)

### 1. Switch to Streamlit UI

```bash
# Switch to streamlit-ui branch
git reset --hard streamlit-ui
git push --force

# หรือใช้ script
./switch_to_ui.sh
```

**ผลลัพธ์:**
- ✅ Streamlit UI: `https://chetsadaphon66-dog-breed-classifier.hf.space`
- ❌ API endpoints ไม่สามารถเข้าถึงได้

**ใช้สำหรับ:**
- Demo กับผู้ใช้ทั่วไป
- Presentation
- User testing

---

### 2. Switch to API-only

```bash
# Switch to api-only branch
git reset --hard api-only
git push --force

# หรือใช้ script
./switch_to_api.sh
```

**ผลลัพธ์:**
- ✅ FastAPI: `https://chetsadaphon66-dog-breed-classifier.hf.space`
- ✅ Swagger UI: `https://chetsadaphon66-dog-breed-classifier.hf.space/docs`
- ✅ เหมาะสำหรับ load testing, API integration

**ใช้สำหรับ:**
- Production API
- Load testing (JMeter)
- API integration
- Performance testing

---

### 3. Switch to Combined Mode

```bash
# Switch to main branch (combined)
git reset --hard origin/main
git push --force

# หรือใช้ script
./switch_to_combined.sh
```

**ผลลัพธ์:**
- ✅ API: port 8000 (ภายใน container)
- ✅ UI: port 7860 (เข้าถึงได้จากภายนอก)
- ⚠️ UI เรียก API ภายใน container

**ใช้สำหรับ:**
- Development
- Full-stack testing
- Demo ที่ต้องการทั้ง UI และ API

---

## 📊 Mode Comparison

| Mode | URL | Swagger UI | Streamlit UI | Use Case |
|------|-----|------------|--------------|----------|
| **API-only** | `/` | ✅ `/docs` | ❌ | Production, Load Testing |
| **Streamlit UI** | `/` | ❌ | ✅ | Demo, User Testing |
| **Combined** | `/` (UI) | ⚠️ `:8000/docs` | ✅ | Development, Full Demo |

---

## 🧪 Testing Each Mode

### API-only Mode

```bash
# Health check
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health

# Predict
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@dog.jpg"

# Swagger UI
open https://chetsadaphon66-dog-breed-classifier.hf.space/docs
```

### Streamlit UI Mode

```bash
# Open in browser
open https://chetsadaphon66-dog-breed-classifier.hf.space

# Upload image through UI
# See results visually
```

### Combined Mode

```bash
# UI (main)
open https://chetsadaphon66-dog-breed-classifier.hf.space

# API (internal - accessed by UI)
# Not directly accessible from outside
```

---

## 🎯 Recommended Workflow

### For Development:
```bash
# Work on main branch (combined mode)
git checkout main
# Make changes
git add .
git commit -m "Add feature"
git push origin main
# CI/CD will deploy API-only
```

### For Load Testing:
```bash
# Switch to API-only
git reset --hard api-only
git push --force

# Run JMeter tests
cd jmeter
./run_loadtest.sh
```

### For Presentation:
```bash
# Switch to Streamlit UI
git reset --hard streamlit-ui
git push --force

# Demo with UI
open https://chetsadaphon66-dog-breed-classifier.hf.space
```

### Back to Production:
```bash
# Switch back to API-only
git reset --hard api-only
git push --force
```

---

## 📝 Switch Scripts

### Create `switch_to_api.sh`:
```bash
#!/bin/bash
echo "🔄 Switching to API-only mode..."
git reset --hard api-only
git push --force
echo "✅ Switched to API-only"
echo "📖 Docs: https://chetsadaphon66-dog-breed-classifier.hf.space/docs"
```

### Create `switch_to_ui.sh`:
```bash
#!/bin/bash
echo "🔄 Switching to Streamlit UI mode..."
git reset --hard streamlit-ui
git push --force
echo "✅ Switched to Streamlit UI"
echo "🎨 UI: https://chetsadaphon66-dog-breed-classifier.hf.space"
```

### Create `switch_to_combined.sh`:
```bash
#!/bin/bash
echo "🔄 Switching to Combined mode..."
git reset --hard origin/main
git push --force
echo "✅ Switched to Combined mode"
echo "🎨 UI: https://chetsadaphon66-dog-breed-classifier.hf.space"
echo "🚀 API: Internal (port 8000)"
```

---

## ⚠️ Important Notes

1. **CI/CD always deploys API-only** - ไม่ว่าจะ push อะไรไป main
2. **Switch mode manually** - ใช้ `git reset --hard` เมื่อต้องการเปลี่ยน
3. **Force push required** - เพราะเป็นการเปลี่ยน branch ทั้งหมด
4. **HF Spaces rebuild** - รอ 1-2 นาทีหลัง force push

---

## 🎓 For Presentation

### Slide: CI/CD Pipeline

**อธิบาย:**
> "CI/CD ของเรา deploy **API-only mode** อัตโนมัติ เพราะเหมาะสำหรับ production และ load testing
> 
> เมื่อต้องการ demo UI เราสามารถ **switch mode** ได้ด้วยคำสั่งเดียว
> 
> นี่ทำให้เรามีความยืดหยุ่นในการใช้งาน โดยไม่ต้อง maintain หลาย deployments"

### Demo Flow:

1. **แสดง API-only (production)**
   ```
   https://chetsadaphon66-dog-breed-classifier.hf.space/docs
   ```

2. **อธิบาย switch mode**
   ```bash
   git reset --hard streamlit-ui
   git push --force
   ```

3. **แสดง Streamlit UI (demo)**
   ```
   https://chetsadaphon66-dog-breed-classifier.hf.space
   ```

4. **อธิบายว่าใช้ code base เดียวกัน**
   - ไม่ต้อง maintain 2 projects
   - Switch ได้ตามต้องการ
   - Flexible deployment

---

## 📊 Architecture

```
┌─────────────────────────────────────┐
│   GitHub Repository (main)          │
│   • api.py                          │
│   • app.py                          │
│   • Dockerfile (API-only)           │
│   • Dockerfile.combined             │
│   • Dockerfile.streamlit            │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│   GitHub Actions (CI/CD)            │
│   • Run tests                       │
│   • Deploy API-only (default)       │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│   HF Spaces (Production)            │
│   • API-only (default)              │
│   • Can switch to UI/Combined       │
└─────────────────────────────────────┘
```

---

## ✅ Summary

**Default (CI/CD):**
- ✅ API-only mode
- ✅ Automatic deployment
- ✅ Production-ready

**Manual Switch:**
- 🔄 Streamlit UI (for demo)
- 🔄 Combined mode (for development)
- 🔄 Back to API-only (for production)

**Benefits:**
- ✅ Single codebase
- ✅ Flexible deployment
- ✅ Easy to switch
- ✅ No duplicate maintenance

---

**Created:** May 2026  
**Project:** Dog Breed Classification MLOps  
**Author:** Chetsadaphon Kantawong
