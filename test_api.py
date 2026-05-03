"""
Unit tests for Dog Breed Classification API
"""
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io
import json

# Import app
from api import app, load_onnx_model, load_dog_breeds

# Initialize model before tests
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Setup module - load model once for all tests"""
    import api as api_module
    api_module.onnx_session = load_onnx_model()
    api_module.dog_breeds = load_dog_breeds()
    yield
    # Cleanup if needed

client = TestClient(app)


def create_test_image(size=(224, 224), color=(255, 0, 0)):
    """Create a test image in memory"""
    img = Image.new('RGB', size, color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_root_endpoint():
    """Test root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "model" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["breeds_loaded"] is True
    assert data["num_breeds"] > 0


def test_predict_endpoint_success():
    """Test prediction endpoint with valid image"""
    # Create test image
    img_bytes = create_test_image()
    
    # Send request
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Validate response structure
    assert data["success"] is True
    assert "predicted_class" in data
    assert "breed_name" in data
    assert "confidence" in data
    assert "top_5_predictions" in data
    assert "inference_time_ms" in data
    
    # Validate data types
    assert isinstance(data["predicted_class"], int)
    assert isinstance(data["breed_name"], str)
    assert isinstance(data["confidence"], float)
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["top_5_predictions"], list)
    assert len(data["top_5_predictions"]) == 5


def test_predict_endpoint_invalid_file_type():
    """Test prediction endpoint with invalid file type"""
    # Create text file
    text_file = io.BytesIO(b"This is not an image")
    
    response = client.post(
        "/predict",
        files={"file": ("test.txt", text_file, "text/plain")}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_predict_endpoint_corrupted_image():
    """Test prediction endpoint with corrupted image"""
    # Create corrupted image data
    corrupted_data = io.BytesIO(b"CORRUPTED_IMAGE_DATA")
    
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", corrupted_data, "image/jpeg")}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False


def test_predict_endpoint_empty_file():
    """Test prediction endpoint with empty file"""
    empty_file = io.BytesIO(b"")
    
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", empty_file, "image/jpeg")}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False


def test_predict_endpoint_large_file():
    """Test prediction endpoint with oversized file"""
    # Create large image (>10MB)
    large_img = Image.new('RGB', (5000, 5000), color=(255, 0, 0))
    img_bytes = io.BytesIO()
    large_img.save(img_bytes, format='JPEG', quality=100)
    img_bytes.seek(0)
    
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    # Should either succeed or return 400 (depending on actual size)
    assert response.status_code in [200, 400]


def test_predict_endpoint_different_formats():
    """Test prediction endpoint with different image formats"""
    formats = [
        ("test.jpg", "JPEG", "image/jpeg"),
        ("test.png", "PNG", "image/png"),
    ]
    
    for filename, img_format, mime_type in formats:
        img = Image.new('RGB', (224, 224), color=(0, 255, 0))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=img_format)
        img_bytes.seek(0)
        
        response = client.post(
            "/predict",
            files={"file": (filename, img_bytes, mime_type)}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


def test_model_prediction_consistency():
    """Test that model produces consistent predictions for same image"""
    img_bytes = create_test_image()
    
    # Make multiple requests with same image
    predictions = []
    for _ in range(3):
        img_bytes.seek(0)
        response = client.post(
            "/predict",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        predictions.append(data["predicted_class"])
    
    # All predictions should be the same
    assert len(set(predictions)) == 1


def test_top_5_predictions_format():
    """Test that top 5 predictions are properly formatted"""
    img_bytes = create_test_image()
    
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    top_5 = data["top_5_predictions"]
    assert len(top_5) == 5
    
    # Check each prediction has required fields
    for pred in top_5:
        assert "class_id" in pred
        assert "breed_name" in pred
        assert "confidence" in pred
        assert isinstance(pred["class_id"], int)
        assert isinstance(pred["breed_name"], str)
        assert isinstance(pred["confidence"], float)
        assert 0.0 <= pred["confidence"] <= 1.0
    
    # Check that confidences are in descending order
    confidences = [p["confidence"] for p in top_5]
    assert confidences == sorted(confidences, reverse=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
