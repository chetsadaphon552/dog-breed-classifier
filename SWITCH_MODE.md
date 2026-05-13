# 🔄 วิธีสลับโหมด API-only และ Streamlit UI

## ตอนนี้มี 3 branches:

1. **main** - Branch หลักที่ HF Spaces deploy (ปัจจุบัน: API-only)
2. **api-only** - โหมด API-only สำหรับ Load Testing
3. **streamlit-ui** - โหมด Streamlit UI สำหรับใช้งานปกติ

---

##  คำสั่งสลับโหมด (Copy & Paste):
.\venv\Scripts\Activate.ps1

###  สลับเป็น API-only (สำหรับ Load Test):

git reset --hard api-only
git push --force

git add .
git commit -m "Update files"
git checkout main
git merge api-only
git push

```powershell
git checkout main
git merge api-only
git push
```

รอ 1-2 นาที แล้วทดสอบ:
```powershell
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health
```

ผลลัพธ์:
```json
{
  "status": "healthy",
  "service": "Dog Breed Classification API",
  "model": "ResNet-34 (ONNX INT8)",
  "version": "1.0.0"
}
```

---

### สลับเป็น Streamlit UI (ใช้งานปกติ):

git reset --hard streamlit-ui
git push --force


git add .
git commit -m "Update switch mode instructions"
git checkout main
git merge streamlit-ui
git push


```powershell
git checkout main
git merge streamlit-ui
git push
```

รอ 1-2 นาที แล้วเปิด browser:
```
https://chetsadaphon66-dog-breed-classifier.hf.space
```

จะได้ Streamlit UI พร้อม upload รูป

---

##  สรุปคำสั่งแบบย่อ:

| โหมด | คำสั่ง |
|------|--------|
| **API-only** | `git checkout main && git merge api-only && git push` |
| **Streamlit UI** | `git checkout main && git merge streamlit-ui && git push` |
| **ดู branch ปัจจุบัน** | `git branch` |
| **ดูสถานะไฟล์** | `git status` |
| **เข้า venv** | `.\venv\Scripts\Activate.ps1` |

---

## เช็คว่าอยู่โหมดไหน:

### วิธีที่ 1: เช็คจาก Git
```powershell
git log --oneline -1
```

- ถ้าเห็น `"Streamlit UI mode"` = โหมด UI
- ถ้าเห็น `"API-only"` = โหมด API-only

### วิธีที่ 2: เช็คจาก API
```powershell
curl https://chetsadaphon66-dog-breed-classifier.hf.space/
```

- ถ้าได้ JSON response = API-only
- ถ้าได้ HTML (Streamlit) = UI mode

---

##  สำหรับ HF Spaces:

- HF Spaces deploy จาก **main branch** เท่านั้น
- การ merge จะทำให้ main เปลี่ยนโหมด
- GitHub Actions จะ auto-deploy ภายใน 1-2 นาที

---

##  หมายเหตุ:

### ถ้ามีไฟล์ที่ยังไม่ได้ commit:
```powershell
git add .
git commit -m "Update files"
git push
```

### ถ้าต้องการยกเลิกการเปลี่ยนแปลง:
```powershell
git checkout .
```

### ถ้าต้องการดู commit history:
```powershell
git log --oneline --graph --all -10
```

---

##  Quick Start:

### ตอนนี้อยู่โหมด: **API-only**

**ถ้าต้องการสลับเป็น UI:**
```powershell
git checkout main && git merge streamlit-ui && git push
```

**ถ้าต้องการรัน Load Test:**
```powershell
cd jmeter
.\run_loadtest.ps1
```

---

## รัน Load Test (JMeter):

### วิธีที่ 1: ใช้ PowerShell Script
```powershell
cd jmeter
.\run_loadtest.ps1
```

### วิธีที่ 2: เปิด JMeter GUI
```powershell
cd jmeter
jmeter -t dog_classifier_loadtest.jmx
```

### วิธีที่ 3: รัน CLI Mode
```powershell
cd jmeter
jmeter -n -t dog_classifier_loadtest.jmx -l results.jtl -e -o report/
```

---

##  ดูผลลัพธ์ Load Test:

หลังรัน Load Test เสร็จ:
```powershell
cd jmeter/report
start index.html
```

จะเปิด HTML report ใน browser
