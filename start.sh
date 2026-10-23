#!/bin/bash
set -e

echo "===== Application Startup at $(date) ====="

echo "Starting Dog Breed Classifier..."

# Start FastAPI on port 7860 (main HF Spaces port - accessible from outside)
echo "Starting FastAPI backend on port 7860..."
uvicorn api:app --host 0.0.0.0 --port 7860 --workers 2 --log-level info &
FASTAPI_PID=$!

# Wait for API to be ready
echo "Waiting for API to start..."
for i in {1..30}; do
    if curl -s http://localhost:7860/health > /dev/null 2>&1; then
        echo "FastAPI is ready!"
        break
    fi
    echo "   Attempt $i/30..."
    sleep 2
done

# Check if FastAPI is running
if ! curl -s http://localhost:7860/health > /dev/null 2>&1; then
    echo "FastAPI failed to start!"
    exit 1
fi

# Start Streamlit on port 8501 (internal - calls FastAPI via HF Space URL)
echo "Starting Streamlit UI on port 8501..."
streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false

kill $FASTAPI_PID 2>/dev/null || true
