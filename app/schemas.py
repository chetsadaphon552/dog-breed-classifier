"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Dict, Optional
from datetime import datetime


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint"""
    
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "prediction": "plastic",
                "confidence": 0.9523,
                "description": "พลาสติก - ขวดน้ำ, ถุงพลาสติก, ภาชนะพลาสติก",
                "recyclable": True,
                "all_predictions": {
                    "plastic": 0.9523,
                    "paper": 0.0234,
                    "metal": 0.0123,
                    "glass": 0.0089,
                    "cardboard": 0.0021,
                    "trash": 0.0010
                },
                "inference_time_ms": 45.23,
                "model_version": "onnx-quantized",
                "timestamp": "2026-05-01T10:30:00"
            }
        }
    )
    
    prediction: str = Field(..., description="Predicted waste category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    description: Optional[str] = Field(None, description="Category description in Thai")
    recyclable: Optional[bool] = Field(None, description="Whether the waste is recyclable")
    all_predictions: Dict[str, float] = Field(..., description="All category probabilities")
    inference_time_ms: float = Field(..., description="Inference time in milliseconds")
    model_version: str = Field(..., description="Model version used")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0 and 1')
        return round(v, 4)


class ErrorResponse(BaseModel):
    """Error response model"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "ValidationError",
                "message": "Invalid file format",
                "details": "Only JPG, JPEG, PNG, and BMP files are allowed",
                "timestamp": "2026-05-01T10:30:00"
            }
        }
    )
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response"""
    
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_version": "onnx-quantized",
                "timestamp": "2026-05-01T10:30:00"
            }
        }
    )
    
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_version: str = Field(..., description="Model version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
