@echo off
echo Building Docker image...
docker build -t dog-classifier:latest -f Dockerfile .

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Docker image built successfully!
    echo.
    echo To run the container:
    echo   docker run -d -p 8000:7860 --name dog-api dog-classifier:latest
    echo.
    echo To view logs:
    echo   docker logs -f dog-api
) else (
    echo.
    echo ❌ Docker build failed!
)
pause
