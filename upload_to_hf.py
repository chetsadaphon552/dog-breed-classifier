"""
Upload Streamlit app to Hugging Face Space
"""
from huggingface_hub import HfApi, login
import os

# Login with token from environment variable
token = os.getenv("HF_TOKEN")
if not token:
    raise ValueError("HF_TOKEN environment variable not set")
login(token=token)

# Initialize API
api = HfApi()

# Space details
repo_id = "chetsadaphon66/dog-breed-classifier-ui"
repo_type = "space"

print("📤 Uploading files to Hugging Face Space...")

# Upload files
try:
    # Upload streamlit app
    api.upload_file(
        path_or_fileobj="hf-streamlit-space/src/streamlit_app.py",
        path_in_repo="src/streamlit_app.py",
        repo_id=repo_id,
        repo_type=repo_type,
        commit_message="Deploy Dog Breed Classifier Streamlit UI"
    )
    print("✅ Uploaded src/streamlit_app.py")
    
    # Upload requirements.txt
    api.upload_file(
        path_or_fileobj="hf-streamlit-space/requirements.txt",
        path_in_repo="requirements.txt",
        repo_id=repo_id,
        repo_type=repo_type,
        commit_message="Update requirements.txt"
    )
    print("✅ Uploaded requirements.txt")
    
    # Upload README.md
    api.upload_file(
        path_or_fileobj="hf-streamlit-space/README.md",
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type=repo_type,
        commit_message="Update README.md"
    )
    print("✅ Uploaded README.md")
    
    print("\n🎉 Successfully deployed to Hugging Face Space!")
    print(f"🌐 URL: https://huggingface.co/spaces/{repo_id}")
    
except Exception as e:
    print(f"❌ Error: {e}")
