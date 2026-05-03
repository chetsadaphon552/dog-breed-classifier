"""
FastAPI application for dog breed classification
ResNet-34 model with 96 dog breeds
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ProcessPoolExecutor
import asyncio
from functools import partial
import logging
from typing import Optional
from PIL import Image
import io

from app.config import (
    APP_NAME, APP_VERSION, DOG_BREEDS, NUM_CLASSES,
    IMAGE_SIZE, ALLOWED_EXTENSIONS, MAX_FILE_SIZE, MAX_WORKERS
)
from app.schemas import PredictionResponse, ErrorResponse, HealthResponse
from app.model import get_model, predict_sync

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Dog Breed Classification API",
    version="1.0.0",
    description="""
    🐕 **Dog Breed Classification API** using ResNet-34 ONNX INT8
    
    ## Features
    - **96 dog breeds** from ImageNet
    - **Fast inference**: ~30ms per image
    - **Small model**: 21 MB (INT8 quantized)
    - **High accuracy**: 86.80% on Stanford Dogs dataset
    
    ## Model Info
    - **Architecture**: ResNet-34 (CNN)
    - **Source**: microsoft/resnet-34 (Hugging Face)
    - **Format**: ONNX INT8
    - **Input**: 224×224 RGB images
    
    ## Usage
    Upload an image of a dog and get the predicted breed with confidence score.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Root", "description": "Root endpoints"},
        {"name": "Health", "description": "Health check endpoints"},
        {"name": "Prediction", "description": "Dog breed prediction endpoints"},
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Process pool for CPU-bound inference
executor = ProcessPoolExecutor(max_workers=MAX_WORKERS)


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    logger.info("🐕 Starting Dog Breed Classification API...")
    try:
        model = get_model()
        logger.info(f"✅ Model loaded: {model.is_loaded()}")
        logger.info(f"📊 Dog breeds: {NUM_CLASSES}")
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")
    executor.shutdown(wait=True)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🐕 Dog Breed Classification API",
        "version": APP_VERSION,
        "model": "ResNet-34 ONNX INT8",
        "breeds": NUM_CLASSES,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns the current status of the API and model.
    """
    model = get_model()
    return HealthResponse(
        status="healthy",
        model_loaded=model.is_loaded(),
        model_version=model.get_model_version()
    )


@app.get("/breeds", tags=["Prediction"])
async def list_breeds():
    """
    List all supported dog breeds
    
    Returns a list of all 96 dog breeds that the model can recognize.
    """
    return {
        "total_breeds": NUM_CLASSES,
        "breeds": DOG_BREEDS
    }


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If validation fails
    """
    # Check file extension
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
    
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type .{file_ext} not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Invalid content type: {file.content_type}. Must be an image."
        )


async def validate_image_content(image_bytes: bytes) -> None:
    """
    Validate image content
    
    Args:
        image_bytes: Image bytes
        
    Raises:
        HTTPException: If validation fails
    """
    # Check file size
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )
    
    # Check if file is empty
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file"
        )
    
    # Try to open image to verify it's valid
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()  # Verify it's a valid image
        
        # Re-open for format check (verify() closes the file)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Check image dimensions (reasonable limits)
        width, height = image.size
        if width < 10 or height < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too small: {width}x{height}. Minimum size: 10x10"
            )
        if width > 10000 or height > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too large: {width}x{height}. Maximum size: 10000x10000"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupted or invalid image file: {str(e)}"
        )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        413: {"model": ErrorResponse, "description": "File Too Large"},
        415: {"model": ErrorResponse, "description": "Unsupported Media Type"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    tags=["Prediction"],
    summary="Predict dog breed from image",
    description="""
    Upload an image of a dog to get the predicted breed.
    
    **Supported formats**: JPG, JPEG, PNG, BMP
    **Max file size**: 10MB
    **Response time**: ~30-50ms
    
    The API returns:
    - Predicted breed name
    - Confidence score (0-1)
    - Top 5 predictions with probabilities
    - Inference time in milliseconds
    """
)
async def predict(
    file: UploadFile = File(
        ...,
        description="Image file of a dog (JPG, PNG, BMP)",
        example="dog.jpg"
    )
):
    """
    Classify dog breed from image
    
    Upload an image and get the predicted dog breed with confidence score.
    """
    try:
        # Validate file metadata
        validate_image_file(file)
        
        # Read file content
        image_bytes = await file.read()
        
        # Validate image content
        await validate_image_content(image_bytes)
        
        # Run inference in process pool (CPU-bound operation)
        loop = asyncio.get_event_loop()
        predicted_class, confidence, all_predictions, inference_time_ms = await loop.run_in_executor(
            executor,
            predict_sync,
            image_bytes
        )
        
        # Return response
        model = get_model()
        return PredictionResponse(
            prediction=predicted_class,
            confidence=confidence,
            description=f"Dog breed: {predicted_class}",
            recyclable=None,  # Not applicable for dogs
            all_predictions=all_predictions,
            inference_time_ms=inference_time_ms,
            model_version=model.get_model_version()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error during prediction: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler"""
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=exc.detail,
        details=None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(mode='json')
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        details=str(exc)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(mode='json')
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
