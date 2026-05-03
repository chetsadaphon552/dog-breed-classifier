#!/bin/bash
set -e

echo "🚀 Starting Dog Breed Classifier..."

# Start FastAPI in background
echo "📡 Starting FastAPI backend on port 8000..."
uvicorn api:app --host 0.0.0.0 --port 8000 --log-level info &
FASTAPI_PID=$!

# Wait for API to be ready
echo "⏳ Waiting for API to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ FastAPI is ready!"
        break
    fi
    echo "   Attempt $i/30..."
    sleep 2
done

# Check if FastAPI is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ FastAPI failed to start!"
    exit 1
fi

# Start Streamlit
echo "🎨 Starting Streamlit UI on port 7860..."
streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false

# If Streamlit exits, kill FastAPI
kill $FASTAPI_PID 2>/dev/null || true
