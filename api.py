"""
FastAPI Image Classification Service
High-throughput dog breed classification using optimized ONNX model
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from contextlib import asynccontextmanager
import onnxruntime as ort
import numpy as np
from PIL import Image
import io
import logging
from concurrent.futures import ProcessPoolExecutor
import asyncio
from functools import lru_cache, partial
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MODEL_PATH = "models/resnet34_int8.onnx"  # Use quantized model for production
DOG_BREEDS_PATH = "models/resnet34_dog_breeds.json"
BREED_CARE_INFO_PATH = "models/breed_care_info.json"

# Global variables
onnx_session = None
dog_breeds = None
breed_care_info = None
executor = None


@lru_cache(maxsize=1)
def load_dog_breeds():
    """Load dog breeds mapping (cached)"""
    with open(DOG_BREEDS_PATH, 'r') as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_breed_care_info():
    """Load breed care information (cached)"""
    with open(BREED_CARE_INFO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_onnx_model():
    """Load ONNX model with optimizations"""
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess_options.intra_op_num_threads = 2  # Limit threads per inference
    
    session = ort.InferenceSession(
        MODEL_PATH,
        sess_options=sess_options,
        providers=['CPUExecutionProvider']
    )
    
    logger.info(f"ONNX model loaded: {MODEL_PATH}")
    return session


def run_inference_in_process(image_array_bytes: bytes, model_path: str, breeds_path: str) -> tuple:
    """
    Run inference in separate process (CPU-bound operation)
    This function will be executed in ProcessPoolExecutor
    
    Args:
        image_array_bytes: Serialized image array
        model_path: Path to ONNX model
        breeds_path: Path to breeds JSON
        
    Returns:
        Tuple of (predicted_class, confidence, top_5_predictions, inference_time_ms)
    """
    import time
    import onnxruntime as ort
    import numpy as np
    import json
    
    # Deserialize image array
    image_array = np.frombuffer(image_array_bytes, dtype=np.float32).reshape(1, 3, 224, 224)
    
    # Load model in this process
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess_options.intra_op_num_threads = 2
    
    session = ort.InferenceSession(
        model_path,
        sess_options=sess_options,
        providers=['CPUExecutionProvider']
    )
    
    # Load breeds
    with open(breeds_path, 'r') as f:
        dog_breeds = json.load(f)
    
    input_name = session.get_inputs()[0].name
    
    # Run inference
    start = time.perf_counter()
    outputs = session.run(None, {input_name: image_array})
    inference_time = (time.perf_counter() - start) * 1000
    
    logits = outputs[0][0]
    
    # Softmax
    exp_logits = np.exp(logits - np.max(logits))
    probabilities = exp_logits / exp_logits.sum()
    
    # Filter to only dog classes
    dog_class_ids = [int(c) for c in dog_breeds.keys()]
    dog_probs = probabilities[dog_class_ids]
    
    # Get top prediction
    max_dog_idx = int(np.argmax(dog_probs))
    predicted_class = dog_class_ids[max_dog_idx]
    confidence = float(dog_probs[max_dog_idx])
    
    # Get top 5 predictions
    top_5_indices = np.argsort(dog_probs)[-5:][::-1]
    top_5_predictions = [
        {
            "class_id": int(dog_class_ids[idx]),
            "breed_name": dog_breeds[str(dog_class_ids[idx])].split(',')[0],
            "confidence": float(dog_probs[idx])
        }
        for idx in top_5_indices
    ]
    
    return predicted_class, confidence, top_5_predictions, inference_time


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    global onnx_session, dog_breeds, breed_care_info, executor
    
    # Startup
    logger.info("Starting up application...")
    
    # Load model and breeds
    onnx_session = load_onnx_model()
    dog_breeds = load_dog_breeds()
    breed_care_info = load_breed_care_info()
    
    # Initialize ProcessPoolExecutor for CPU-bound inference
    # Using max_workers=2 to handle concurrent requests
    executor = ProcessPoolExecutor(max_workers=2)
    
    logger.info(f"Loaded {len(dog_breeds)} dog breed classes")
    logger.info("ProcessPoolExecutor initialized with 2 workers")
    logger.info("Application ready!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    
    if executor:
        executor.shutdown(wait=True)
        logger.info("ProcessPoolExecutor shut down")
    
    logger.info("Application stopped")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Dog Breed Classification API",
    description="High-throughput image classification service using optimized ONNX model",
    version="1.0.0",
    lifespan=lifespan
)

# Response models
class BreedCareInfo(BaseModel):
    """Breed care information"""
    personality: str
    exercise: str
    nutrition: str
    health_care: str
    grooming: str

class PredictionResponse(BaseModel):
    """Response model for prediction endpoint"""
    success: bool
    predicted_class: int
    breed_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    top_5_predictions: Optional[List[dict]] = None
    care_info: Optional[BreedCareInfo] = None
    inference_time_ms: float

class ErrorResponse(BaseModel):
    """Response model for errors"""
    success: bool = False
    error: str
    detail: Optional[str] = None


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess image for model inference
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        Preprocessed image array
        
    Raises:
        ValueError: If image is corrupted or invalid
    """
    try:
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB (handle RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to 224x224
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        img_array = np.array(image).astype(np.float32) / 255.0
        
        # ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img_array = (img_array - mean) / std
        
        # Transpose to CHW format and add batch dimension
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
        
        return img_array
        
    except Exception as e:
        raise ValueError(f"Failed to preprocess image: {str(e)}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Dog Breed Classification API",
        "model": "ResNet-34 (ONNX INT8)",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": onnx_session is not None,
        "breeds_loaded": dog_breeds is not None,
        "care_info_loaded": breed_care_info is not None,
        "num_breeds": len(dog_breeds) if dog_breeds else 0
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Predict dog breed from uploaded image
    
    Args:
        file: Uploaded image file
        
    Returns:
        Prediction results with breed name and confidence
        
    Raises:
        HTTPException: For various error conditions
    """
    # Validate file extension
    file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if f".{file_ext}" not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file
    try:
        image_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Check file size
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f} MB"
        )
    
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty file"
        )
    
    # Preprocess image
    try:
        image_array = preprocess_image(image_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image preprocessing failed: {str(e)}"
        )
    
    # Run inference using ProcessPoolExecutor (CPU-bound operation)
    # This prevents blocking the async event loop
    try:
        # Serialize image array for process communication
        image_array_bytes = image_array.tobytes()
        
        # Run inference in separate process
        loop = asyncio.get_event_loop()
        predicted_class, confidence, top_5, inference_time = await loop.run_in_executor(
            executor,
            partial(run_inference_in_process, image_array_bytes, MODEL_PATH, DOG_BREEDS_PATH)
        )
        
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}"
        )
    
    # Get breed name
    breed_name = dog_breeds[str(predicted_class)].split(',')[0]
    
    # Get care information
    care_data = None
    if str(predicted_class) in breed_care_info:
        care_info_dict = breed_care_info[str(predicted_class)]["care_info"]
        care_data = BreedCareInfo(**care_info_dict)
    
    return PredictionResponse(
        success=True,
        predicted_class=predicted_class,
        breed_name=breed_name,
        confidence=confidence,
        top_5_predictions=top_5,
        care_info=care_data,
        inference_time_ms=inference_time
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc.detail)
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).model_dump()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
