"""
Configuration for Dogs Breed Classification API
"""
import os
from pathlib import Path

# Application settings
APP_NAME = "Dogs Breed Classification API"
APP_VERSION = "1.0.0"

# Model settings
MODEL_PATH = os.getenv("MODEL_PATH", "models/resnet34_int8.onnx")
MODEL_TYPE = "dogs-breed"

# Load dog breed labels from ResNet-34
import json
LABELS_PATH = "models/resnet34_dog_breeds.json"
with open(LABELS_PATH, 'r') as f:
    raw_labels = json.load(f)

# Filter out non-dog classes and create clean breed list
NON_DOG_IDS = ["29", "48", "275", "388", "537", "865", "934"]
DOG_BREEDS = {int(k): v for k, v in raw_labels.items() if k not in NON_DOG_IDS}
NUM_CLASSES = len(DOG_BREEDS)

# Image settings
IMAGE_SIZE = (224, 224)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Server settings
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

# For backward compatibility
WASTE_CATEGORIES = list(DOG_BREEDS.values())  # Use dog breeds as categories
CATEGORY_DESCRIPTIONS = {breed: f"Dog breed: {breed}" for breed in DOG_BREEDS.values()}
RECYCLABLE = {breed: None for breed in DOG_BREEDS.values()}  # Not applicable for dogs
