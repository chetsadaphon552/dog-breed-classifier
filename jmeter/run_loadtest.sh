#!/bin/bash
# JMeter Load Test Runner for Linux/macOS
# Run this script to execute load tests and generate HTML reports

set -e

TARGET="${1:-cloud}"  # cloud or local
IMAGE_PATH="${2:-test_images/pug.jpg}"

echo "🔥 JMeter Load Test Runner"
echo "================================"

# Check if JMeter is installed
if ! command -v jmeter &> /dev/null; then
    echo "❌ JMeter not found!"
    echo "Install JMeter:"
    echo "  macOS: brew install jmeter"
    echo "  Linux: sudo apt install jmeter"
    echo "  Or download from: https://jmeter.apache.org/download_jmeter.cgi"
    exit 1
fi

echo "✅ JMeter found: $(which jmeter)"

# Check if test image exists
if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ Test image not found: $IMAGE_PATH"
    echo "Creating test_images folder and downloading sample image..."
    
    mkdir -p test_images
    
    echo "Downloading pug.jpg..."
    curl -o test_images/pug.jpg https://images.dog.ceo/breeds/pug/n02110958_1008.jpg
    
    if [ -f "test_images/pug.jpg" ]; then
        echo "✅ Sample image downloaded"
        IMAGE_PATH="test_images/pug.jpg"
    else
        echo "❌ Failed to download sample image"
        exit 1
    fi
fi

echo "✅ Test image found: $IMAGE_PATH"

# Set API configuration based on target
if [ "$TARGET" = "local" ]; then
    API_HOST="localhost"
    API_PROTOCOL="http"
    REPORT_DIR="report_local"
    RESULTS_FILE="results_local.jtl"
    echo "🎯 Target: Local API (http://localhost:8000)"
else
    API_HOST="chetsadaphon66-dog-breed-classifier.hf.space"
    API_PROTOCOL="https"
    REPORT_DIR="report_cloud"
    RESULTS_FILE="results_cloud.jtl"
    echo "🎯 Target: Cloud API (https://$API_HOST)"
fi

# Clean up old results
if [ -d "$REPORT_DIR" ]; then
    echo "🧹 Cleaning up old report..."
    rm -rf "$REPORT_DIR"
fi

if [ -f "$RESULTS_FILE" ]; then
    rm -f "$RESULTS_FILE"
fi

# Run JMeter test
echo ""
echo "🚀 Running load test..."
echo "   - Users: 5 (warmup) + 10 (load) + 20 (stress)"
echo "   - Total requests: 325"
echo "   - Duration: ~60 seconds"
echo ""

START_TIME=$(date +%s)

jmeter -n \
  -t dog_classifier_loadtest.jmx \
  -JAPI_HOST="$API_HOST" \
  -JAPI_PROTOCOL="$API_PROTOCOL" \
  -JIMAGE_PATH="$IMAGE_PATH" \
  -l "$RESULTS_FILE" \
  -e \
  -o "$REPORT_DIR"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "✅ Load test completed in $DURATION seconds"

# Check if report was generated
if [ -f "$REPORT_DIR/index.html" ]; then
    echo ""
    echo "📊 HTML Report generated:"
    echo "   $REPORT_DIR/index.html"
    echo ""
    echo "Opening report in browser..."
    
    # Open browser based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$REPORT_DIR/index.html"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$REPORT_DIR/index.html" 2>/dev/null || echo "Please open $REPORT_DIR/index.html manually"
    fi
else
    echo "⚠️  HTML report not found"
fi

# Display quick summary
if [ -f "$RESULTS_FILE" ]; then
    echo ""
    echo "📈 Quick Summary:"
    
    TOTAL_COUNT=$(tail -n +2 "$RESULTS_FILE" | wc -l)
    SUCCESS_COUNT=$(tail -n +2 "$RESULTS_FILE" | awk -F',' '$8=="true"' | wc -l)
    AVG_LATENCY=$(tail -n +2 "$RESULTS_FILE" | awk -F',' '{sum+=$2; count++} END {print sum/count}')
    
    echo "   Total Requests: $TOTAL_COUNT"
    echo "   Successful: $SUCCESS_COUNT"
    echo "   Failed: $((TOTAL_COUNT - SUCCESS_COUNT))"
    echo "   Average Latency: $(printf "%.2f" $AVG_LATENCY) ms"
    echo "   Success Rate: $(awk "BEGIN {printf \"%.2f\", ($SUCCESS_COUNT / $TOTAL_COUNT) * 100}")%"
fi

echo ""
echo "================================"
echo "✅ Done!"
echo ""
echo "Next steps:"
echo "  1. Review HTML report: $REPORT_DIR/index.html"
echo "  2. Analyze key metrics (TPS, P95 latency)"
echo "  3. Include results in project report"
echo ""
