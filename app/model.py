"""
Model inference logic for Dog Breed Classification
Based on ResNet-34 ONNX model (96 dog breeds)
"""
import os
import numpy as np
from PIL import Image
import io
import time
from typing import Dict, Tuple
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DogsClassifier:
    """Dogs breed classification model wrapper"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the classifier
        
        Args:
            model_path: Path to ONNX model file
        """
        self.model_path = model_path or "models/resnet34_int8.onnx"
        self.image_size = (224, 224)
        self.session = None
        
        # Load dog breed labels from ResNet-34
        labels_path = "models/resnet34_dog_breeds.json"
        with open(labels_path, 'r') as f:
            raw_labels = json.load(f)
        
        # Filter out non-dog classes
        NON_DOG_IDS = ["29", "48", "275", "388", "537", "865", "934"]
        self.id2label = {int(k): v for k, v in raw_labels.items() if k not in NON_DOG_IDS}
        
        # Create categories list (sorted by ID)
        sorted_ids = sorted(self.id2label.keys())
        self.categories = [self.id2label[i] for i in sorted_ids]
        self.id_mapping = {i: idx for idx, i in enumerate(sorted_ids)}
        
        self._load_model()
    
    def _load_model(self):
        """Load ONNX model"""
        try:
            import onnxruntime as ort
            
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model not found: {self.model_path}")
            
            # Configure ONNX Runtime for MAXIMUM CPU optimization
            sess_options = ort.SessionOptions()
            
            # Enable all graph optimizations
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            
            # Optimize thread count (4 threads for better parallelism)
            sess_options.intra_op_num_threads = 4
            sess_options.inter_op_num_threads = 1
            
            # Use sequential execution for better latency
            sess_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            
            # Enable memory pattern optimization
            sess_options.enable_mem_pattern = True
            sess_options.enable_cpu_mem_arena = True
            
            # Disable profiling for production
            sess_options.enable_profiling = False
            
            self.session = ort.InferenceSession(
                self.model_path,
                sess_options=sess_options,
                providers=['CPUExecutionProvider']
            )
            
            logger.info(f"✅ Dog model loaded successfully from {self.model_path}")
            logger.info(f"   Architecture: ResNet-34")
            logger.info(f"   Classes: {len(self.categories)} dog breeds")
            logger.info(f"   Optimizations: threads=4, sequential mode, all graph opts enabled")
            logger.info(f"   Input name: {self.session.get_inputs()[0].name}")
            logger.info(f"   Input shape: {self.session.get_inputs()[0].shape}")
            
        except Exception as e:
            logger.error(f"Error loading ONNX model: {e}")
            raise
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess image for ONNX model inference (highly optimized)
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Preprocessed image as numpy array
        """
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize with BILINEAR (faster than LANCZOS, good enough quality)
        image = image.resize(self.image_size, Image.BILINEAR)
        
        # Convert to numpy array and normalize in one go
        img_array = np.asarray(image, dtype=np.float32)
        
        # Vectorized operations (fastest approach)
        # Normalize to [0, 1]
        img_array = img_array * 0.00392156862745098  # 1/255
        
        # ImageNet normalization (vectorized)
        img_array[:, :, 0] = (img_array[:, :, 0] - 0.485) / 0.229
        img_array[:, :, 1] = (img_array[:, :, 1] - 0.456) / 0.224
        img_array[:, :, 2] = (img_array[:, :, 2] - 0.406) / 0.225
        
        # Transpose to CHW format (contiguous)
        img_array = np.ascontiguousarray(np.transpose(img_array, (2, 0, 1)))
        
        # Add batch dimension
        img_array = img_array[np.newaxis, :, :, :]
        
        return img_array
    
    def predict(self, image_bytes: bytes) -> Tuple[str, float, Dict[str, float], float]:
        """
        Run inference on image
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Tuple of (predicted_class, confidence, all_predictions, inference_time_ms)
        """
        start_time = time.time()
        
        # Preprocess image
        input_data = self.preprocess_image(image_bytes)
        
        # Run inference
        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: input_data})
        logits = outputs[0][0]  # Shape: (1000,) for ImageNet
        
        # Apply softmax (optimized with in-place operations)
        logits_max = np.max(logits)
        exp_logits = np.exp(logits - logits_max)
        probabilities = exp_logits / np.sum(exp_logits)
        
        # Filter to only dog breed classes
        dog_probs = {}
        for class_id, breed_name in self.id2label.items():
            dog_probs[breed_name] = float(probabilities[class_id])
        
        # Get top prediction from dog breeds only
        sorted_dogs = sorted(dog_probs.items(), key=lambda x: x[1], reverse=True)
        predicted_class = sorted_dogs[0][0]
        confidence = sorted_dogs[0][1]
        
        # Get top 5 dog breed predictions
        all_predictions = dict(sorted_dogs[:5])
        
        # Calculate inference time
        inference_time_ms = (time.time() - start_time) * 1000
        
        return predicted_class, confidence, all_predictions, inference_time_ms
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.session is not None
    
    def get_model_version(self) -> str:
        """Get current model version"""
        return "resnet34-int8"


# Global model instance (loaded once at startup)
_model_instance = None


def get_model() -> DogsClassifier:
    """Get or create model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = DogsClassifier()
    return _model_instance


def predict_sync(image_bytes: bytes) -> Tuple[str, float, Dict[str, float], float]:
    """
    Synchronous prediction function for ProcessPoolExecutor
    This function will be called in a separate process
    """
    model = get_model()
    return model.predict(image_bytes)
