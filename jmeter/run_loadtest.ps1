# JMeter Load Test Runner for Windows
# Run this script to execute load tests and generate HTML reports

param(
    [string]$Target = "cloud",  # cloud or local
    [string]$ImagePath = "test_images/pug.jpg"
)

Write-Host "🔥 JMeter Load Test Runner" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if JMeter is installed
$jmeterCmd = Get-Command jmeter -ErrorAction SilentlyContinue
if (-not $jmeterCmd) {
    Write-Host "❌ JMeter not found!" -ForegroundColor Red
    Write-Host "Install JMeter:" -ForegroundColor Yellow
    Write-Host "  choco install jmeter" -ForegroundColor Yellow
    Write-Host "  Or download from: https://jmeter.apache.org/download_jmeter.cgi" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ JMeter found: $($jmeterCmd.Source)" -ForegroundColor Green

# Check if test image exists
if (-not (Test-Path $ImagePath)) {
    Write-Host "❌ Test image not found: $ImagePath" -ForegroundColor Red
    Write-Host "Creating test_images folder and downloading sample image..." -ForegroundColor Yellow
    
    New-Item -ItemType Directory -Force -Path "test_images" | Out-Null
    
    Write-Host "Downloading pug.jpg..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://images.dog.ceo/breeds/pug/n02110958_1008.jpg" -OutFile "test_images/pug.jpg"
    
    if (Test-Path "test_images/pug.jpg") {
        Write-Host "✅ Sample image downloaded" -ForegroundColor Green
        $ImagePath = "test_images/pug.jpg"
    } else {
        Write-Host "❌ Failed to download sample image" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Test image found: $ImagePath" -ForegroundColor Green

# Set API configuration based on target
if ($Target -eq "local") {
    $apiHost = "localhost"
    $apiProtocol = "http"
    $reportDir = "report_local"
    $resultsFile = "results_local.jtl"
    Write-Host "🎯 Target: Local API (http://localhost:8000)" -ForegroundColor Cyan
} else {
    $apiHost = "chetsadaphon66-dog-breed-classifier.hf.space"
    $apiProtocol = "https"
    $reportDir = "report_cloud"
    $resultsFile = "results_cloud.jtl"
    Write-Host "🎯 Target: Cloud API (https://$apiHost)" -ForegroundColor Cyan
}

# Clean up old results
if (Test-Path $reportDir) {
    Write-Host "🧹 Cleaning up old report..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $reportDir
}

if (Test-Path $resultsFile) {
    Remove-Item -Force $resultsFile
}

# Run JMeter test
Write-Host ""
Write-Host "🚀 Running load test..." -ForegroundColor Cyan
Write-Host "   - Users: 5 (warmup) + 10 (load) + 20 (stress)" -ForegroundColor Gray
Write-Host "   - Total requests: 325" -ForegroundColor Gray
Write-Host "   - Duration: ~60 seconds" -ForegroundColor Gray
Write-Host ""

$jmeterArgs = @(
    "-n",
    "-t", "dog_classifier_loadtest.jmx",
    "-JAPI_HOST=$apiHost",
    "-JAPI_PROTOCOL=$apiProtocol",
    "-JIMAGE_PATH=$ImagePath",
    "-l", $resultsFile,
    "-e",
    "-o", $reportDir
)

$startTime = Get-Date

try {
    & jmeter $jmeterArgs
    
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    Write-Host ""
    Write-Host "✅ Load test completed in $([math]::Round($duration, 2)) seconds" -ForegroundColor Green
    
    # Check if report was generated
    if (Test-Path "$reportDir/index.html") {
        Write-Host ""
        Write-Host "📊 HTML Report generated:" -ForegroundColor Cyan
        Write-Host "   $reportDir/index.html" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Opening report in browser..." -ForegroundColor Cyan
        Start-Process "$reportDir/index.html"
    } else {
        Write-Host "⚠️  HTML report not found" -ForegroundColor Yellow
    }
    
    # Display quick summary
    if (Test-Path $resultsFile) {
        Write-Host ""
        Write-Host "📈 Quick Summary:" -ForegroundColor Cyan
        
        $results = Import-Csv $resultsFile
        $successCount = ($results | Where-Object { $_.success -eq "true" }).Count
        $totalCount = $results.Count
        $avgLatency = ($results | Measure-Object -Property elapsed -Average).Average
        
        Write-Host "   Total Requests: $totalCount" -ForegroundColor Gray
        Write-Host "   Successful: $successCount" -ForegroundColor Green
        Write-Host "   Failed: $($totalCount - $successCount)" -ForegroundColor $(if ($totalCount -eq $successCount) { "Green" } else { "Red" })
        Write-Host "   Average Latency: $([math]::Round($avgLatency, 2)) ms" -ForegroundColor Gray
        Write-Host "   Success Rate: $([math]::Round(($successCount / $totalCount) * 100, 2))%" -ForegroundColor Green
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Load test failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Done!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review HTML report: $reportDir/index.html" -ForegroundColor Yellow
Write-Host "  2. Analyze key metrics (TPS, P95 latency)" -ForegroundColor Yellow
Write-Host "  3. Include results in project report" -ForegroundColor Yellow
Write-Host ""
