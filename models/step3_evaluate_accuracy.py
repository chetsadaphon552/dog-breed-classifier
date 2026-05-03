"""
Step 27: Evaluate ResNet-34 Dogs - All Models (PyTorch FP32, ONNX FP32, ONNX INT8)
Similar to step3_evaluate_accuracy.py but for dog breed classification
Uses Stanford Dogs dataset from Kaggle
"""
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Tuple
import json
from PIL import Image
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_dataset():
    """Download or load Stanford Dogs dataset"""
    try:
        import zipfile
        from pathlib import Path
        
        logger.info("Loading Stanford Dogs dataset...")
        
        # Step 1: Check if dataset already extracted
        possible_paths = [
            Path("Images"),
            Path("images"),
            Path("stanford-dogs-dataset/Images"),
            Path("datasets/stanford-dogs/Images"),
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_dir():
                subdirs = [d for d in path.iterdir() if d.is_dir()]
                if len(subdirs) > 0:
                    logger.info(f" Dataset already extracted: {path}")
                    return str(path.parent if path.name in ["Images", "images"] else path)
        
        logger.info("Dataset not found locally. Attempting to download...")
        
        # Step 2: Check if zip file exists
        zip_path = Path("stanford-dogs-dataset.zip")
        
        if zip_path.exists():
            logger.info(f" Found existing zip file: {zip_path}")
        else:
            # Step 3: Try to download using Kaggle API
            logger.info("Downloading Stanford Dogs dataset from Kaggle...")
            logger.info("Dataset size: ~750MB")
            
            try:
                import subprocess
                
                # Check if kaggle is installed
                result = subprocess.run(
                    ["kaggle", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode != 0:
                    raise FileNotFoundError("Kaggle CLI not found")
                
                logger.info(" Kaggle CLI found")
                
                # Download dataset
                dataset_name = "jessicali9530/stanford-dogs-dataset"
                logger.info(f"Downloading: {dataset_name}")
                
                result = subprocess.run(
                    ["kaggle", "datasets", "download", "-d", dataset_name],
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minutes timeout
                )
                
                if result.returncode != 0:
                    logger.error(f"Download failed: {result.stderr}")
                    raise Exception(f"Kaggle download failed: {result.stderr}")
                
                logger.info("Download complete")
                
                # Kaggle downloads as dataset-name.zip, rename if needed
                downloaded_zip = Path("stanford-dogs-dataset.zip")
                if not downloaded_zip.exists():
                    # Try alternative names
                    alt_names = [
                        Path("jessicali9530-stanford-dogs-dataset.zip"),
                        Path("stanford-dogs-dataset.zip"),
                    ]
                    for alt in alt_names:
                        if alt.exists():
                            downloaded_zip = alt
                            break
                
                if not downloaded_zip.exists():
                    raise Exception("Downloaded zip file not found")
                
                zip_path = downloaded_zip
                
            except FileNotFoundError:
                logger.error(" Kaggle CLI not installed")
                logger.info("\nTo install Kaggle CLI:")
                logger.info("  pip install kaggle")
                logger.info("\nThen configure your API credentials:")
                logger.info("  1. Go to https://www.kaggle.com/account")
                logger.info("  2. Create API token (downloads kaggle.json)")
                logger.info("  3. Place kaggle.json in ~/.kaggle/")
                logger.info("\nAlternatively, download manually:")
                logger.info("  https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset")
                return None
                
            except subprocess.TimeoutExpired:
                logger.error(" Download timeout (>10 minutes)")
                logger.info("\nPlease download manually:")
                logger.info("  https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset")
                return None
                
            except Exception as e:
                logger.error(f"Download failed: {e}")
                logger.info("\nPlease download manually:")
                logger.info("  1. Go to: https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset")
                logger.info("  2. Download the dataset")
                logger.info("  3. Save as: stanford-dogs-dataset.zip")
                logger.info("  4. Run this script again")
                return None
        
        # Step 4: Extract zip file
        logger.info(f" Extracting dataset from: {zip_path}")
        logger.info("   This may take a few minutes...")
        
        extract_dir = Path(".")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files
            file_list = zip_ref.namelist()
            logger.info(f"   Found {len(file_list)} files in archive")
            
            # Extract all files
            zip_ref.extractall(extract_dir)
        
        logger.info(" Dataset extracted successfully")
        
        # Step 5: Find extracted Images folder
        for path in possible_paths:
            if path.exists() and path.is_dir():
                subdirs = [d for d in path.iterdir() if d.is_dir()]
                if len(subdirs) > 0:
                    logger.info(f" Dataset location: {path}")
                    return str(path.parent if path.name in ["Images", "images"] else path)
        
        logger.error(" Could not find Images folder after extraction")
        return None
        
    except Exception as e:
        logger.error(f" Error loading dataset: {e}")
        import traceback
        traceback.print_exc()
        
        logger.info("\nTroubleshooting:")
        logger.info("  1. Install Kaggle CLI: pip install kaggle")
        logger.info("  2. Configure API: https://www.kaggle.com/docs/api")
        logger.info("  3. Or download manually: https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset")
        return None


def load_dog_breeds_mapping():
    """Load ResNet-34 dog breeds mapping"""
    dog_breeds_file = "models/resnet34_dog_breeds.json"
    
    if not Path(dog_breeds_file).exists():
        logger.error(f"Dog breeds file not found: {dog_breeds_file}")
        return None
    
    with open(dog_breeds_file, 'r') as f:
        dog_breeds = json.load(f)
    
    logger.info(f"Loaded {len(dog_breeds)} dog breed classes")
    return dog_breeds


def load_pytorch_model():
    """Load PyTorch ResNet-34 model"""
    try:
        from transformers import AutoModelForImageClassification
        
        model_id = "microsoft/resnet-34"
        logger.info(f"Loading PyTorch model: {model_id}")
        
        model = AutoModelForImageClassification.from_pretrained(
            model_id,
            cache_dir="models/cache_resnet34"
        )
        model.eval()
        
        logger.info(" PyTorch model loaded successfully")
        return model
        
    except Exception as e:
        logger.error(f"Error loading PyTorch model: {e}")
        logger.warning("Skipping PyTorch model evaluation")
        return None


def load_onnx_model(model_path: str):
    """Load ONNX model"""
    import onnxruntime as ort
    
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess_options.intra_op_num_threads = 4
    
    session = ort.InferenceSession(
        model_path,
        sess_options=sess_options,
        providers=['CPUExecutionProvider']
    )
    
    logger.info(f" ONNX model loaded: {model_path}")
    return session


def preprocess_image_pytorch(image_path: str):
    """Preprocess image for PyTorch model"""
    from PIL import Image
    import torchvision.transforms as transforms
    
    img = Image.open(image_path).convert('RGB')
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    img_tensor = transform(img)
    img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
    
    return img_tensor


def preprocess_image_onnx(image_path: str) -> np.ndarray:
    """Preprocess image for ONNX model"""
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    
    img_array = np.array(img).astype(np.float32) / 255.0
    
    # Normalize
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img_array = (img_array - mean) / std
    
    # Transpose to CHW format
    img_array = np.transpose(img_array, (2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    
    return img_array


def predict_pytorch(model, image_path: str, dog_breeds: Dict) -> Tuple[int, float, bool, float]:
    """
    Run inference with PyTorch model (DOGS ONLY)
    
    Returns:
        predicted_class: int (always a dog breed)
        confidence: float
        is_dog: bool (always True - filtered to dogs only)
        inference_time_ms: float
    """
    import torch
    import torch.nn.functional as F
    
    img_tensor = preprocess_image_pytorch(image_path)
    
    start = time.perf_counter()
    with torch.no_grad():
        outputs = model(img_tensor)
        logits = outputs.logits if hasattr(outputs, 'logits') else outputs
        probabilities = F.softmax(logits, dim=1)[0]
    inference_time = (time.perf_counter() - start) * 1000
    
    # Filter to only dog classes
    dog_class_ids = [int(c) for c in dog_breeds.keys()]
    
    # Get probabilities for dog classes only
    dog_probs = probabilities[dog_class_ids]
    
    # Find the dog class with highest probability
    max_dog_idx = int(torch.argmax(dog_probs))
    predicted_class = dog_class_ids[max_dog_idx]
    confidence = float(dog_probs[max_dog_idx])
    
    # Always True since we filter to dogs only
    is_dog = True
    
    return predicted_class, confidence, is_dog, inference_time


def predict_onnx(session, image_path: str, dog_breeds: Dict) -> Tuple[int, float, bool, float]:
    """
    Run inference with ONNX model (DOGS ONLY)
    
    Returns:
        predicted_class: int (always a dog breed)
        confidence: float
        is_dog: bool (always True - filtered to dogs only)
        inference_time_ms: float
    """
    img_array = preprocess_image_onnx(image_path)
    
    input_name = session.get_inputs()[0].name
    
    start = time.perf_counter()
    outputs = session.run(None, {input_name: img_array})
    inference_time = (time.perf_counter() - start) * 1000
    
    logits = outputs[0][0]
    
    # Softmax
    exp_logits = np.exp(logits - np.max(logits))
    probabilities = exp_logits / exp_logits.sum()
    
    # Filter to only dog classes
    dog_class_ids = [int(c) for c in dog_breeds.keys()]
    
    # Get probabilities for dog classes only
    dog_probs = probabilities[dog_class_ids]
    
    # Find the dog class with highest probability
    max_dog_idx = int(np.argmax(dog_probs))
    predicted_class = dog_class_ids[max_dog_idx]
    confidence = float(dog_probs[max_dog_idx])
    
    # Always True since we filter to dogs only
    is_dog = True
    
    return predicted_class, confidence, is_dog, inference_time


def normalize_breed_name(breed_name: str) -> str:
    """Normalize breed name for comparison"""
    # Remove ImageNet ID prefix (e.g., n02106166-)
    if '-' in breed_name:
        breed_name = breed_name.split('-', 1)[1]
    
    # Convert to lowercase and replace underscores/hyphens with spaces
    breed_name = breed_name.lower().replace('_', ' ').replace('-', ' ')
    
    return breed_name


def load_stanford_dogs_dataset(dataset_path: str, dog_breeds: Dict, max_samples_per_breed: int = 25) -> Tuple[List[str], List[str], List[int]]:
    """
    Load images from Stanford Dogs dataset (only breeds in ResNet-34)
    
    Args:
        dataset_path: Path to dataset directory
        dog_breeds: ResNet-34 dog breeds mapping
        max_samples_per_breed: Maximum samples per breed
        
    Returns:
        image_paths: List of image paths
        breed_names: List of breed names (for reference)
        true_labels: List of true ImageNet class IDs
    """
    dataset_dir = Path(dataset_path)
    
    logger.info(f"Loading Stanford Dogs dataset from: {dataset_dir}")
    
    # Find Images folder
    possible_dirs = [
        dataset_dir / "Images" / "Images",  # Nested Images folder
        dataset_dir / "Images",
        dataset_dir / "images",
        dataset_dir / "stanford-dogs-dataset" / "Images",
        dataset_dir,
    ]
    
    images_dir = None
    for dir_path in possible_dirs:
        if dir_path.exists() and dir_path.is_dir():
            # Check if it has breed folders
            subdirs = [d for d in dir_path.iterdir() if d.is_dir()]
            if len(subdirs) > 0:
                images_dir = dir_path
                break
    
    if images_dir is None:
        logger.error(f"Could not find Images directory in {dataset_dir}")
        return [], [], []
    
    logger.info(f"Found images directory: {images_dir}")
    
    # Create reverse mapping: normalized breed name -> ImageNet class ID
    breed_name_to_id = {}
    for class_id, breed_label in dog_breeds.items():
        # Extract breed name from label (e.g., "Chihuahua" from "Chihuahua")
        normalized = normalize_breed_name(breed_label.split(',')[0])
        breed_name_to_id[normalized] = int(class_id)
    
    # Get all breed folders
    breed_folders = sorted([d for d in images_dir.iterdir() if d.is_dir()])
    
    logger.info(f"Found {len(breed_folders)} breed folders in dataset")
    
    # Filter to only breeds that are in ResNet-34
    matched_breeds = []
    for breed_folder in breed_folders:
        breed_name = breed_folder.name
        normalized_breed = normalize_breed_name(breed_name)
        
        # Find matching ImageNet class ID
        class_id = None
        for norm_name, cid in breed_name_to_id.items():
            if norm_name in normalized_breed or normalized_breed in norm_name:
                class_id = cid
                break
        
        if class_id is not None:
            matched_breeds.append((breed_folder, class_id))
    
    logger.info(f"Matched {len(matched_breeds)} breeds in ResNet-34")
    
    # Select subset of breeds for testing (use all matched breeds or sample)
    import random
    random.seed(42)
    
    if len(matched_breeds) > 30:
        # Sample 30 breeds for faster testing
        selected_breeds = random.sample(matched_breeds, 30)
        logger.info(f"Sampling 30 breeds for testing")
    else:
        selected_breeds = matched_breeds
        logger.info(f"Using all {len(matched_breeds)} matched breeds")
    
    image_paths = []
    breed_names = []
    true_labels = []
    
    for breed_folder, class_id in sorted(selected_breeds, key=lambda x: x[0].name):
        breed_name = breed_folder.name
        
        # Get all images in breed folder
        image_files = list(breed_folder.glob("*.jpg")) + list(breed_folder.glob("*.png"))
        
        # Limit samples per breed
        if len(image_files) > max_samples_per_breed:
            image_files = random.sample(image_files, max_samples_per_breed)
        
        for img_path in image_files:
            image_paths.append(str(img_path))
            breed_names.append(breed_name)
            true_labels.append(class_id)
        
        logger.info(f"  {breed_name}: {len(image_files)} images → Class {class_id}")
    
    logger.info(f"Total images loaded: {len(image_paths)}")
    logger.info(f"All breeds have matching classes in ResNet-34")
    
    return image_paths, breed_names, true_labels


def evaluate_model(model, dataset_path: str, dog_breeds: Dict, max_samples: int = 25, model_type: str = "onnx") -> Dict:
    """
    Evaluate model on Stanford Dogs dataset
    
    Args:
        model: Model (PyTorch or ONNX session)
        dataset_path: Path to dataset
        dog_breeds: Dog breeds mapping
        max_samples: Max samples per breed
        model_type: "pytorch" or "onnx"
        
    Returns:
        Evaluation results
    """
    logger.info(f"Evaluating model (type: {model_type})")
    
    # Load dataset
    image_paths, breed_names, true_labels = load_stanford_dogs_dataset(dataset_path, dog_breeds, max_samples)
    
    if len(image_paths) == 0:
        logger.error("No images loaded!")
        return None
    
    # Run predictions
    logger.info("Running predictions...")
    predicted_classes = []
    confidences = []
    inference_times = []
    failed_images = []
    
    for i, img_path in enumerate(image_paths):
        try:
            # Predict
            if model_type == "pytorch":
                pred_class, confidence, is_dog, inf_time = predict_pytorch(model, img_path, dog_breeds)
            else:
                pred_class, confidence, is_dog, inf_time = predict_onnx(model, img_path, dog_breeds)
            
            predicted_classes.append(pred_class)
            confidences.append(confidence)
            inference_times.append(inf_time)
            
        except Exception as e:
            logger.warning(f"Error processing {img_path}: {e}")
            failed_images.append(img_path)
            # Remove from lists
            breed_names.pop(i - len(failed_images))
            true_labels.pop(i - len(failed_images))
            continue
        
        if (i + 1) % 50 == 0:
            logger.info(f"  Progress: {i+1}/{len(image_paths)}")
    
    logger.info(f"Predictions complete. Failed: {len(failed_images)}")
    
    # Convert to numpy
    predicted_classes = np.array(predicted_classes)
    true_labels = np.array(true_labels)
    confidences = np.array(confidences)
    inference_times = np.array(inference_times)
    
    # Calculate accuracy (exact breed match)
    correct_predictions = np.sum(predicted_classes == true_labels)
    accuracy = correct_predictions / len(predicted_classes) if len(predicted_classes) > 0 else 0
    
    # Also calculate "is dog" accuracy (any dog breed)
    is_dog_predictions = np.array([str(pc) in dog_breeds for pc in predicted_classes])
    dog_accuracy = np.sum(is_dog_predictions) / len(is_dog_predictions)
    
    # Create confusion matrix for breeds
    try:
        from sklearn.metrics import confusion_matrix, classification_report
    except ImportError:
        logger.error("scikit-learn not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "scikit-learn==1.4.0"])
        from sklearn.metrics import confusion_matrix, classification_report
    
    # Get unique classes that actually appear in true labels (support > 0)
    unique_true_classes = sorted(set(true_labels.tolist()))
    all_unique_classes = sorted(set(true_labels.tolist() + predicted_classes.tolist()))
    
    # Filter to only classes with support > 0 (classes that appear in true_labels)
    labels_with_support = unique_true_classes
    names_with_support = [dog_breeds.get(str(c), f"Class {c}").split(',')[0] for c in labels_with_support]
    
    # All class names for confusion matrix (includes predictions)
    all_class_names = [dog_breeds.get(str(c), f"Class {c}").split(',')[0] for c in all_unique_classes]
    
    # Confusion matrix with all classes (for visualization)
    cm = confusion_matrix(true_labels, predicted_classes, labels=all_unique_classes)
    
    # Classification report - ONLY classes with support > 0
    report = classification_report(
        true_labels,
        predicted_classes,
        labels=labels_with_support,  # Only classes that appear in dataset
        target_names=names_with_support,  # Only their names
        zero_division=0
    )
    
    results = {
        "model_type": model_type,
        "num_samples": len(predicted_classes),
        "num_failed": len(failed_images),
        "accuracy": float(accuracy),
        "correct_predictions": int(correct_predictions),
        "dog_accuracy": float(dog_accuracy),
        "avg_confidence": float(np.mean(confidences)),
        "mean_inference_ms": float(np.mean(inference_times)),
        "median_inference_ms": float(np.median(inference_times)),
        "confusion_matrix": cm.tolist(),
        "class_names": all_class_names,  # All classes for confusion matrix
        "class_ids": all_unique_classes,  # All class IDs
        "classification_report": report,  # Only classes with support > 0
        "tested_breeds": len(labels_with_support),  # Number of breeds actually tested
        "dog_breeds_in_model": len(dog_breeds),
        "dataset": "Stanford Dogs (matched breeds only)"
    }
    
    return results


def plot_confusion_matrix(cm: np.ndarray, categories: List[str], output_path: str, model_name: str = ""):
    """Plot confusion matrix"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        logger.error(f"Visualization libraries not installed. Installing...")
        import subprocess
        if "matplotlib" in str(e):
            subprocess.check_call(["pip", "install", "matplotlib==3.8.2"])
        if "seaborn" in str(e):
            subprocess.check_call(["pip", "install", "seaborn==0.13.1"])
        import matplotlib.pyplot as plt
        import seaborn as sns
    
    # Limit display to reasonable size
    if len(categories) > 20:
        logger.warning(f"Too many categories ({len(categories)}), showing top 20 only")
        # Sum rows and columns to find most common classes
        row_sums = cm.sum(axis=1)
        top_indices = np.argsort(row_sums)[-20:]
        cm = cm[top_indices][:, top_indices]
        categories = [categories[i] for i in top_indices]
    
    fig_height = max(8, len(categories) * 0.4)
    fig_width = max(10, len(categories) * 0.5)
    plt.figure(figsize=(fig_width, fig_height))
    
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=categories,
        yticklabels=categories,
        cbar_kws={'label': 'Count'}
    )
    
    title = f'Confusion Matrix - {model_name}' if model_name else 'Confusion Matrix'
    plt.title(title, fontsize=16, pad=20)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Confusion matrix saved: {output_path}")
    plt.close()


def plot_comparison(all_results: List[Dict], output_path: str):
    """Plot comparison of all models"""
    import matplotlib.pyplot as plt
    
    model_names = [r['display_name'] for r in all_results]
    accuracies = [r['accuracy'] * 100 for r in all_results]
    confidences = [r['avg_confidence'] * 100 for r in all_results]
    inference_times = [r['mean_inference_ms'] for r in all_results]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: Accuracy
    ax1 = axes[0]
    bars1 = ax1.bar(model_names, accuracies, alpha=0.8, color='#3498db')
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_ylim([0, 105])
    ax1.grid(axis='y', alpha=0.3)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%', ha='center', va='bottom', fontsize=10)
    
    # Plot 2: Confidence
    ax2 = axes[1]
    bars2 = ax2.bar(model_names, confidences, alpha=0.8, color='#2ecc71')
    ax2.set_ylabel('Avg Confidence (%)', fontsize=12)
    ax2.set_title('Average Confidence', fontsize=14, fontweight='bold')
    ax2.set_ylim([0, 105])
    ax2.grid(axis='y', alpha=0.3)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%', ha='center', va='bottom', fontsize=10)
    
    # Plot 3: Inference Time
    ax3 = axes[2]
    bars3 = ax3.bar(model_names, inference_times, alpha=0.8, color='#e74c3c')
    ax3.set_ylabel('Inference Time (ms)', fontsize=12)
    ax3.set_title('Inference Speed', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}ms', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Comparison plot saved: {output_path}")
    plt.close()


def print_results(results: Dict, model_name: str):
    """Print formatted results"""
    
    print("\n" + "=" * 100)
    print(f"MODEL EVALUATION RESULTS - {model_name}")
    print("=" * 100)
    
    print(f"\nModel Type: {results['model_type']}")
    print(f"Dataset: {results['dataset']}")
    print(f"Total Samples: {results['num_samples']} (Failed: {results['num_failed']})")
    print(f"Breeds Tested: {results.get('tested_breeds', 'N/A')} (out of {results['dog_breeds_in_model']} in model)")
    
    print(f"\nPerformance Metrics:")
    print(f"  Breed Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    print(f"  Correct Breed: {results['correct_predictions']}/{results['num_samples']}")
    print(f"  Dog Detection: {results['dog_accuracy']:.4f} ({results['dog_accuracy']*100:.2f}%)")
    print(f"  Avg Confidence: {results['avg_confidence']:.4f} ({results['avg_confidence']*100:.2f}%)")
    print(f"  Mean Inference: {results['mean_inference_ms']:.2f} ms")
    print(f"  Median Inference: {results['median_inference_ms']:.2f} ms")
    
    print("\n" + "=" * 100)
    print(f"CLASSIFICATION REPORT (Only {results.get('tested_breeds', 'N/A')} Tested Breeds - Support > 0)")
    print("=" * 100)
    print("=" * 100)
    print(results['classification_report'])
    
    print("=" * 100)


def print_comparison(all_results: List[Dict]):
    """Print comparison of all models"""
    
    print("\n" + "=" * 100)
    print("MODEL COMPARISON SUMMARY - ResNet-34 Dogs")
    print("=" * 100)
    
    header = f"{'Model':<20} {'Accuracy':<12} {'Confidence':<12} {'Inference':<12} {'Samples':<10}"
    print(header)
    print("-" * 100)
    
    for results in all_results:
        model_name = results['display_name']
        accuracy = results['accuracy'] * 100
        confidence = results['avg_confidence'] * 100
        inference = results['mean_inference_ms']
        samples = results['num_samples']
        
        row = f"{model_name:<20} {accuracy:<12.2f}% {confidence:<12.2f}% {inference:<12.2f}ms {samples:<10}"
        print(row)
    
    print("=" * 100)
    
    # Find best model
    best_accuracy = max(all_results, key=lambda x: x['accuracy'])
    best_speed = min(all_results, key=lambda x: x['mean_inference_ms'])
    
    print(f"\nBest Accuracy: {best_accuracy['display_name']} ({best_accuracy['accuracy']*100:.2f}%)")
    print(f"Fastest: {best_speed['display_name']} ({best_speed['mean_inference_ms']:.2f}ms)")
    print("=" * 100)


def main():
    """Main function"""
    import time
    start_time = time.time()
    
    print("\n" + "=" * 100)
    print("ResNet-34 DOG BREED CLASSIFICATION - ALL MODELS EVALUATION")
    print("=" * 100)
    
    # Create results directory
    results_dir = Path("evaluation_results")
    results_dir.mkdir(exist_ok=True)
    logger.info(f"Results directory: {results_dir}")
    
    # Step 1: Load dataset
    print("\nStep 1: Loading Stanford Dogs dataset...")
    dataset_path = download_dataset()
    
    if dataset_path is None:
        logger.error("Failed to download dataset")
        return
    
    # Step 2: Load dog breeds mapping
    print("\nStep 2: Loading dog breeds mapping...")
    dog_breeds = load_dog_breeds_mapping()
    
    if dog_breeds is None:
        logger.error("Failed to load dog breeds mapping")
        return
    
    # Step 3: Define models to evaluate
    # Format: (model_loader, model_path, model_type, display_name, folder_name)
    models_to_evaluate = [
        ("pytorch", None, "pytorch", "PyTorch FP32", "resnet34_pytorch_fp32"),
        ("onnx", "models/resnet34_fp32.onnx", "onnx", "ONNX FP32", "resnet34_onnx_fp32"),
        ("onnx", "models/resnet34_int8.onnx", "onnx", "ONNX INT8", "resnet34_onnx_int8"),
    ]
    
    all_results = []
    
    # Step 4: Evaluate each model
    print("\nStep 3: Evaluating models...")
    for loader_type, model_path, model_type, model_name, folder_name in models_to_evaluate:
        print(f"\n{'='*100}")
        print(f"Evaluating: {model_name}")
        print(f"{'='*100}")
        
        # Load model
        if loader_type == "pytorch":
            model = load_pytorch_model()
            if model is None:
                logger.warning(f"Skipping {model_name}")
                continue
        else:
            if not Path(model_path).exists():
                logger.warning(f"Model not found: {model_path} - Skipping")
                continue
            model = load_onnx_model(model_path)
        
        # Evaluate
        results = evaluate_model(model, dataset_path, dog_breeds, max_samples=25, model_type=model_type)
        
        if results is None:
            logger.error(f"Evaluation failed for {model_name}")
            continue
        
        # Add metadata
        results['display_name'] = model_name
        results['folder_name'] = folder_name
        all_results.append(results)
        
        print_results(results, model_name)
    
    if len(all_results) == 0:
        logger.error("No models evaluated successfully")
        return
    
    # Step 5: Print comparison
    if len(all_results) > 1:
        print_comparison(all_results)
    
    # Step 6: Save results
    print("\nStep 4: Saving results...")
    
    # Save individual results in separate folders
    for results in all_results:
        folder_name = results['folder_name']
        
        # Create folder for each model
        model_dir = results_dir / folder_name
        model_dir.mkdir(exist_ok=True)
        
        # Save JSON
        output_json = model_dir / "evaluation_results.json"
        with open(output_json, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved: {output_json}")
        
        # Plot confusion matrix
        cm = np.array(results['confusion_matrix'])
        output_cm = model_dir / "confusion_matrix.png"
        plot_confusion_matrix(cm, results['class_names'], str(output_cm), results['display_name'])
    
    # Save comparison in main results folder
    if len(all_results) > 1:
        comparison_data = {
            "models": [r['display_name'] for r in all_results],
            "accuracies": [r['accuracy'] for r in all_results],
            "confidences": [r['avg_confidence'] for r in all_results],
            "inference_times": [r['mean_inference_ms'] for r in all_results],
            "detailed_results": all_results
        }
        
        comparison_json = results_dir / "resnet34_dogs_comparison.json"
        with open(comparison_json, 'w') as f:
            json.dump(comparison_data, f, indent=2)
        logger.info(f"Comparison saved: {comparison_json}")
        
        # Plot comparison
        comparison_plot = results_dir / "resnet34_dogs_comparison.png"
        plot_comparison(all_results, str(comparison_plot))
    
    print("\n" + "=" * 100)
    print("EVALUATION COMPLETE!")
    print("=" * 100)
    print(f"\nAll results saved in: {results_dir}/")
    print("\nFolder structure:")
    for results in all_results:
        folder_name = results['folder_name']
        print(f"\n  {folder_name}/")
        print(f"    - evaluation_results.json")
        print(f"    - confusion_matrix.png")
    
    if len(all_results) > 1:
        print(f"\n  Comparison (in {results_dir}/):")
        print(f"    - resnet34_dogs_comparison.json")
        print(f"    - resnet34_dogs_comparison.png")
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print("\n" + "=" * 100)
    print(f"Tip: Open {results_dir}/ folder to view all results")
    print(f"Time elapsed: {minutes}m {seconds}s")
    print("=" * 100)


if __name__ == "__main__":
    main()
