# GitHub Repository Setup Guide

## ✅ Repository Successfully Deployed!

Your repository is now live at: https://github.com/chetsadaphon552/dog-breed-classifier

## 🔐 Setup GitHub Secret for CI/CD

To enable automatic deployment to Hugging Face Spaces, you need to add your HF token as a GitHub secret:

### Step 1: Get Your Hugging Face Token

You need a Hugging Face token with **write** access.

Get your token from: https://huggingface.co/settings/tokens

(Create a new token if you don't have one)

### Step 2: Add Secret to GitHub

1. Go to your repository: https://github.com/chetsadaphon552/dog-breed-classifier
2. Click **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Fill in:
   - **Name**: `HF_TOKEN`
   - **Secret**: (paste your Hugging Face token here)
6. Click **Add secret**

### Step 3: Verify CI/CD Pipeline

1. Go to **Actions** tab in your repository
2. You should see the workflow running (or completed)
3. If tests pass, the app will auto-deploy to HF Spaces

## 🧪 Testing the Deployment

### Test Local API (if running locally)

```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST "http://localhost:8000/predict" -F "file=@pug.jpg"
```

### Test Cloud API (Hugging Face Spaces)

```bash
# Health check
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health

# Predict
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" -F "file=@pug.jpg"
```

## 📊 Next Steps

1. ✅ **Repository pushed to GitHub** - DONE
2. ⏳ **Add HF_TOKEN secret** - DO THIS NOW
3. ⏳ **Verify CI/CD pipeline** - Check Actions tab
4. ⏳ **Run JMeter load tests** - See `jmeter/README.md`
5. ⏳ **Complete project report** - See `docs/PROJECT_REPORT_TEMPLATE.md`

## 🎯 Dataset Files (Not in GitHub)

The following files are **NOT** pushed to GitHub (too large):
- `stanford-dogs-dataset.zip` (750MB)
- `annotations/` folder
- `images/` folder
- `models/cache_resnet34/` folder

These files are only needed for:
- Model training/evaluation (already completed)
- Local testing with the dataset

**For production deployment**, only these files are needed:
- ✅ `models/resnet34_int8.onnx` (21MB) - Included in repo
- ✅ `models/resnet34_dog_breeds.json` - Included in repo
- ✅ `api.py` and other code files - Included in repo

## ❓ Can We Test Without Dataset?

**YES!** You can test the API without the dataset:

1. **Use any dog image** from the internet
2. **Download sample images** from:
   - Google Images
   - Unsplash
   - Your own photos

The API only needs:
- The trained model (`resnet34_int8.onnx`)
- The breed mapping (`resnet34_dog_breeds.json`)
- An input image to classify

**Example:**
```bash
# Download a pug image
curl -o test_pug.jpg "https://images.unsplash.com/photo-1517849845537-4d257902454a"

# Test the API
curl -X POST "https://chetsadaphon66-dog-breed-classifier.hf.space/predict" \
  -F "file=@test_pug.jpg"
```

## 🔍 Verify Everything Works

### 1. Check GitHub Repository
- Visit: https://github.com/chetsadaphon552/dog-breed-classifier
- Verify files are there (no large dataset files)

### 2. Check GitHub Actions
- Go to **Actions** tab
- Verify workflow runs successfully

### 3. Check Hugging Face Space
- Visit: https://huggingface.co/spaces/chetsadaphon66/dog-breed-classifier
- Verify app is running

### 4. Test API
```bash
curl https://chetsadaphon66-dog-breed-classifier.hf.space/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Dog Breed Classification API",
  "model": "ResNet-34 (ONNX INT8)",
  "version": "1.0.0"
}
```

## 🎉 Success!

Your project is now fully deployed with:
- ✅ GitHub repository with clean history
- ✅ CI/CD pipeline configured
- ✅ Hugging Face Spaces deployment
- ✅ Production-ready API

**Just add the HF_TOKEN secret and you're done!**

