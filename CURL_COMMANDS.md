# 🔧 cURL Commands Reference

## Local API (http://localhost:8000)

### Health Check

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Dog Breed Classification API",
  "model": "ResNet-34 (ONNX INT8)",
  "version": "1.0.0"
}
```

### Detailed Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
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
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@pug.jpg"
```

**Expected Response:**
```json
{
  "success": true,
  "predicted_class": 254,
  "breed_name": "pug",
  "confidence": 0.7389782667160034,
  "top_5_predictions": [
    {
      "class_id": 254,
      "breed_name": "pug",
      "confidence": 0.7389782667160034
    },
    {
      "class_id": 245,
      "breed_name": "French bulldog",
      "confidence": 0.035944633185863495
    },
    ...
  ],
  "inference_time_ms": 28.5
}
```

---

## Cloud API (Hugging Face Spaces)

Replace `YOUR_USERNAME` and `YOUR_SPACE_NAME` with your actual values.

### Health Check

```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
```

### Predict Dog Breed

```bash
curl -X POST "https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict" \
  -F "file=@dog_image.jpg"
```

---

## Windows PowerShell

### Health Check

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

### Predict

```powershell
$form = @{
    file = Get-Item -Path "pug.jpg"
}
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Form $form
```

---

## Python Requests

### Health Check

```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

### Predict

```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("pug.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## JavaScript (Node.js)

### Health Check

```javascript
const fetch = require('node-fetch');

fetch('http://localhost:8000/health')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Predict

```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

const form = new FormData();
form.append('file', fs.createReadStream('pug.jpg'));

fetch('http://localhost:8000/predict', {
  method: 'POST',
  body: form
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Error Responses

### Invalid File Type (400)

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@document.txt"
```

**Response:**
```json
{
  "success": false,
  "error": "Invalid file type. Allowed: .jpg, .jpeg, .png, .webp",
  "detail": "Invalid file type. Allowed: .jpg, .jpeg, .png, .webp"
}
```

### Empty File (400)

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@empty.jpg"
```

**Response:**
```json
{
  "success": false,
  "error": "Empty file",
  "detail": "Empty file"
}
```

### File Too Large (400)

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@huge_image.jpg"
```

**Response:**
```json
{
  "success": false,
  "error": "File too large. Maximum size: 10.0 MB",
  "detail": "File too large. Maximum size: 10.0 MB"
}
```

---

## Testing Multiple Images

### Bash Script

```bash
#!/bin/bash

for image in *.jpg; do
  echo "Testing: $image"
  curl -X POST "http://localhost:8000/predict" \
    -F "file=@$image" \
    -s | jq '.breed_name, .confidence'
  echo "---"
done
```

### PowerShell Script

```powershell
Get-ChildItem *.jpg | ForEach-Object {
    Write-Host "Testing: $($_.Name)"
    $form = @{ file = $_ }
    $result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Form $form
    Write-Host "Breed: $($result.breed_name)"
    Write-Host "Confidence: $($result.confidence)"
    Write-Host "---"
}
```

---

## Performance Testing

### Measure Response Time

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@pug.jpg" \
  -w "\nTime: %{time_total}s\n" \
  -o /dev/null -s
```

### Concurrent Requests (using GNU Parallel)

```bash
seq 10 | parallel -j 10 \
  'curl -X POST "http://localhost:8000/predict" -F "file=@pug.jpg" -s -o /dev/null -w "Time: %{time_total}s\n"'
```

