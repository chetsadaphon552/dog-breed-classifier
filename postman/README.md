# 📮 Postman Collection

## Import Collection

1. Open Postman
2. Click **Import** button
3. Select `Dog_Breed_Classifier_API.postman_collection.json`
4. Collection will be imported with all endpoints

## Environment Variables

The collection uses the following variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `https://chetsadaphon66-dog-breed-classifier.hf.space` | Production API URL |
| `local_url` | `http://localhost:8000` | Local development URL (disabled by default) |

### Switch to Local Testing

1. In Postman, go to **Variables** tab
2. Enable `local_url` variable
3. Disable `base_url` variable
4. Update `base_url` value to `{{local_url}}`

## Available Endpoints

### 1. Health Checks

#### Root Health Check
- **Method**: GET
- **URL**: `{{base_url}}/`
- **Description**: Basic health check

#### Detailed Health Status
- **Method**: GET
- **URL**: `{{base_url}}/health`
- **Description**: Get model and breeds loading status

### 2. Predictions

#### Predict Dog Breed
- **Method**: POST
- **URL**: `{{base_url}}/predict`
- **Body**: Form-data with `file` key (image file)
- **Supported formats**: JPG, JPEG, PNG, WEBP
- **Max file size**: 10 MB

**Response Example:**
```json
{
  "success": true,
  "predicted_class": 254,
  "breed_name": "pug",
  "confidence": 0.9234,
  "top_5_predictions": [...],
  "care_info": {...},
  "inference_time_ms": 27.92
}
```

#### Error Testing
- **Invalid File Type**: Test with PDF or TXT file
- **Corrupted Image**: Test with corrupted image file

### 3. Documentation

#### Swagger UI
- **Method**: GET
- **URL**: `{{base_url}}/docs`
- **Description**: Interactive API documentation

#### ReDoc
- **Method**: GET
- **URL**: `{{base_url}}/redoc`
- **Description**: Alternative API documentation

## Testing Workflow

1. **Health Check**: Verify API is running
2. **Predict**: Upload dog image and get prediction
3. **Error Handling**: Test with invalid inputs
4. **Documentation**: View API specs

## Sample Test Images

You can use these public dog images for testing:

```bash
# Pug
https://images.dog.ceo/breeds/pug/n02110958_1008.jpg

# Golden Retriever
https://images.dog.ceo/breeds/retriever-golden/n02099601_100.jpg

# German Shepherd
https://images.dog.ceo/breeds/germanshepherd/n02106662_10083.jpg

# Chihuahua
https://images.dog.ceo/breeds/chihuahua/n02085620_10131.jpg
```

## Load Testing

For load testing, use JMeter instead of Postman:
- See `jmeter/` folder for load test configuration
- Postman is better for functional testing
- JMeter is better for performance testing

## Tips

1. **Save Responses**: Click "Save Response" to keep example responses
2. **Tests Tab**: Add assertions to validate responses
3. **Pre-request Scripts**: Add scripts to generate test data
4. **Collection Runner**: Run all requests sequentially

## Troubleshooting

### Connection Error
- Check if API is running
- Verify `base_url` variable is correct
- Check internet connection for cloud API

### 400 Bad Request
- Verify file format (JPG, PNG, WEBP only)
- Check file size (max 10 MB)
- Ensure file is not corrupted

### 500 Internal Server Error
- Check API logs
- Verify model is loaded correctly
- Report issue on GitHub

## Export Results

1. Run collection with **Collection Runner**
2. Click **Export Results**
3. Save as JSON or CSV
4. Include in project report

---

**Need help?** Check the [main README](../README.md) or open an issue on GitHub.
