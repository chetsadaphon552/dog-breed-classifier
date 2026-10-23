# Combined FastAPI + Streamlit
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# numpy>=2.0 required by pyarrow (streamlit dependency)
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    python-multipart==0.0.6 \
    pydantic==2.5.3 \
    pillow==10.2.0 \
    "numpy>=2.0.0,<3.0.0" \
    onnxruntime==1.25.1 \
    streamlit==1.31.0 \
    requests==2.31.0

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy application code
COPY api.py .
COPY app.py .
COPY start.sh .
COPY models/resnet34_int8.onnx models/
COPY models/resnet34_dog_breeds.json models/
COPY models/breed_care_info.json models/

RUN chmod +x start.sh && chown -R appuser:appuser /app

USER appuser

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:7860/_stcore/health || exit 1

CMD ["./start.sh"]
