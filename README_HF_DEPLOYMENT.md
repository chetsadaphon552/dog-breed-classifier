# 🚀 Hugging Face Spaces Deployment Guide

## Prerequisites

1. **Hugging Face Account**: https://huggingface.co/join
2. **HF Token**: https://huggingface.co/settings/tokens (with write access)
3. **GitHub Repository**: Your project code

## Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Configure:
   - **Name**: `dog-breed-classifier` (or your choice)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU Basic (free tier)
4. Click "Create Space"

## Step 2: Prepare Files for HF Spaces

Required files in root directory:
- ✅ `Dockerfile` - Already created
- ✅ `api.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `models/resnet34_int8.onnx` - Model file
- ✅ `models/resnet34_dog_breeds.json` - Breed mapping

## Step 3: Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secrets:

### Required Secrets:

**HF_TOKEN**
```
Your Hugging Face token from https://huggingface.co/settings/tokens
```

**HF_SPACE_NAME**
```
your-username/dog-breed-classifier
```

Example: `john-doe/dog-breed-classifier`

## Step 4: Push to GitHub

```bash
git add .
git commit -m "Add API and deployment config"
git push origin main
```

GitHub Actions will automatically:
1. Run tests
2. Build Docker image
3. Deploy to Hugging Face Spaces

## Step 5: Verify Deployment

1. Go to your HF Space: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
2. Wait for build to complete (~5-10 minutes)
3. Test API:

```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
```

## Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Clone your HF Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy files
cp ../api.py .
cp ../Dockerfile .
cp ../requirements.txt .
cp -r ../models .

# Commit and push
git add .
git commit -m "Deploy API"
git push
```

## Troubleshooting

### Build Fails

- Check Dockerfile syntax
- Verify all files are present
- Check HF Space logs

### API Not Responding

- Check if container started successfully
- Verify port 7860 is exposed
- Check application logs in HF Space

### Model Not Loading

- Verify model files are in `models/` folder
- Check file sizes (HF has limits)
- Ensure paths are correct in code

## Testing Deployed API

### Health Check

```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
```

### Predict

```bash
curl -X POST "https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict" \
  -F "file=@dog_image.jpg"
```

### Python

```python
import requests

url = "https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict"
files = {"file": open("dog.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Performance Expectations

- **Cold Start**: 30-60 seconds (first request after idle)
- **Warm Latency**: 60-100 ms
- **Throughput**: 10-20 requests/second
- **Concurrent Users**: Up to 50 (free tier)

## Upgrading Hardware

For better performance:
1. Go to Space Settings
2. Change Hardware to:
   - **CPU Upgrade**: Faster inference
   - **GPU**: Much faster (if model supports)

## Monitoring

- **Logs**: Available in HF Space interface
- **Metrics**: Use JMeter for load testing
- **Uptime**: HF Spaces auto-sleep after 48h inactivity

## Cost

- **Free Tier**: CPU Basic (sufficient for demo)
- **Paid Tiers**: Starting at $0.60/hour for upgraded CPU
- **GPU**: Starting at $0.60/hour

## Next Steps

1. ✅ Create HF Space
2. ✅ Add GitHub secrets
3. ✅ Push code
4. ✅ Wait for deployment
5. ✅ Test API
6. ✅ Run JMeter load tests
7. ✅ Document results

