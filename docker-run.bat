@echo off
echo Stopping existing container (if any)...
docker stop dog-api 2>nul
docker rm dog-api 2>nul

echo.
echo Starting Dog Breed Classification API...
docker run -d -p 8000:7860 --name dog-api dog-classifier:latest

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Container started successfully!
    echo.
    echo API is running at: http://localhost:8000
    echo Health check: http://localhost:8000/health
    echo.
    echo To view logs:
    echo   docker logs -f dog-api
    echo.
    echo To stop:
    echo   docker stop dog-api
) else (
    echo.
    echo ❌ Failed to start container!
)
pause
