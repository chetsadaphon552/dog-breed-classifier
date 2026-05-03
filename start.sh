#!/bin/bash

# Start FastAPI in background
echo "🚀 Starting FastAPI backend..."
uvicorn api:app --host 0.0.0.0 --port 8000 &

# Wait for API to be ready
echo "⏳ Waiting for API to start..."
sleep 5

# Start Streamlit
echo "🎨 Starting Streamlit UI..."
streamlit run app.py --server.port 7860 --server.address 0.0.0.0
