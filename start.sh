#!/bin/bash

# Start FastAPI only on port 7860 for load testing
echo "🚀 Starting FastAPI for load testing on port 7860..."
uvicorn api:app --host 0.0.0.0 --port 7860 --log-level info
