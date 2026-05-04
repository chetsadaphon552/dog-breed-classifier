# 🔥 JMeter Load Testing

## Prerequisites

### Install JMeter

**Windows:**
```powershell
# Using Chocolatey
choco install jmeter

# Or download from: https://jmeter.apache.org/download_jmeter.cgi
```

**macOS:**
```bash
brew install jmeter
```

**Linux:**
```bash
# Download and extract
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
cd apache-jmeter-5.6.3/bin
```

### Verify Installation

```bash
jmeter -v
```

Expected output: `Apache JMeter 5.x`

## Test Image Setup

1. **Create test_images folder:**
```bash
mkdir test_images
cd test_images
```

2. **Download sample dog image:**
```bash
# Pug image
curl -o pug.jpg https://images.dog.ceo/breeds/pug/n02110958_1008.jpg
```

Or use your own dog image (JPG, PNG, WEBP).

## Test Plan Overview

The load test includes 3 thread groups:

| Thread Group | Users | Loops | Ramp-up | Total Requests | Duration |
|--------------|-------|-------|---------|----------------|----------|
| **Warmup** | 5 | 5 | 10s | 25 | ~10s |
| **Load Test** | 10 | 10 | 20s | 100 | ~20s |
| **Stress Test** | 20 | 10 | 30s | 200 | ~30s |

**Total Requests**: 325

## Running Tests

### 1. GUI Mode (Development)

```bash
# Open JMeter GUI
jmeter

# Then:
# 1. File → Open → dog_classifier_loadtest.jmx
# 2. Update IMAGE_PATH variable if needed
# 3. Click green "Start" button
# 4. View results in listeners
```

### 2. CLI Mode (Production)

#### Test Cloud API (Hugging Face)

```bash
# Run test and generate HTML report
jmeter -n -t dog_classifier_loadtest.jmx \
  -l results_cloud.jtl \
  -e -o report_cloud/

# View report
open report_cloud/index.html  # macOS
start report_cloud/index.html  # Windows
xdg-open report_cloud/index.html  # Linux
```

#### Test Local API (Docker)

```bash
# 1. Start local API first
docker run -p 8000:8000 dog-classifier

# 2. Run test with local settings
jmeter -n -t dog_classifier_loadtest.jmx \
  -JAPI_HOST=localhost \
  -JAPI_PROTOCOL=http \
  -l results_local.jtl \
  -e -o report_local/
```

### 3. Custom Configuration

```bash
# Custom number of users and loops
jmeter -n -t dog_classifier_loadtest.jmx \
  -Jusers=50 \
  -Jloops=20 \
  -l results_custom.jtl \
  -e -o report_custom/
```

## Understanding Results

### Key Metrics

| Metric | Description | Good Value |
|--------|-------------|------------|
| **Throughput (TPS)** | Transactions per second | > 10 TPS |
| **Average Latency** | Mean response time | < 500ms |
| **P95 Latency** | 95th percentile | < 1000ms |
| **P99 Latency** | 99th percentile | < 2000ms |
| **Error Rate** | Failed requests % | < 1% |

### HTML Dashboard

The generated HTML report includes:

1. **Dashboard**: Overview with key metrics
2. **Over Time**: Response time, throughput graphs
3. **Throughput**: Requests per second
4. **Response Times**: Percentiles (P50, P90, P95, P99)
5. **Errors**: Error rate and types

### Expected Performance

#### Cloud (Hugging Face Spaces)
- **Throughput**: 10-15 TPS
- **P95 Latency**: 800-1200ms
- **P99 Latency**: 1500-2500ms
- **Bottleneck**: Network + CPU (free tier)

#### Local (Docker)
- **Throughput**: 25-35 TPS
- **P95 Latency**: 40-60ms
- **P99 Latency**: 80-120ms
- **Bottleneck**: CPU (inference time)

## Analyzing Results

### 1. View Summary

```bash
# Generate summary from results file
jmeter -g results_cloud.jtl -o report_summary/
```

### 2. Compare Local vs Cloud

```bash
# Run both tests
jmeter -n -t dog_classifier_loadtest.jmx -l results_cloud.jtl -e -o report_cloud/
jmeter -n -t dog_classifier_loadtest.jmx -JAPI_HOST=localhost -JAPI_PROTOCOL=http -l results_local.jtl -e -o report_local/

# Compare reports
echo "Cloud Report: report_cloud/index.html"
echo "Local Report: report_local/index.html"
```

### 3. Extract Key Metrics

```bash
# Using awk to extract metrics from JTL file
awk -F',' 'NR>1 {sum+=$2; count++} END {print "Average Latency:", sum/count "ms"}' results_cloud.jtl
```

## Troubleshooting

### Connection Refused
```
Error: Connection refused
```
**Solution**: Ensure API is running and accessible

### File Not Found
```
Error: test_images/pug.jpg not found
```
**Solution**: 
```bash
mkdir test_images
cd test_images
curl -o pug.jpg https://images.dog.ceo/breeds/pug/n02110958_1008.jpg
```

### Out of Memory
```
Error: Java heap space
```
**Solution**: Increase JMeter memory
```bash
export JVM_ARGS="-Xms512m -Xmx2048m"
jmeter -n -t dog_classifier_loadtest.jmx ...
```

### SSL Certificate Error
```
Error: SSL handshake failed
```
**Solution**: Add to jmeter.properties:
```
server.rmi.ssl.disable=true
```

## Advanced Testing

### 1. Spike Test (Sudden Load)

```bash
# 100 users in 5 seconds
jmeter -n -t dog_classifier_loadtest.jmx \
  -Jusers=100 \
  -Jrampup=5 \
  -Jloops=5 \
  -l results_spike.jtl \
  -e -o report_spike/
```

### 2. Endurance Test (Long Duration)

```bash
# 10 users for 10 minutes
jmeter -n -t dog_classifier_loadtest.jmx \
  -Jusers=10 \
  -Jduration=600 \
  -l results_endurance.jtl \
  -e -o report_endurance/
```

### 3. Different Image Sizes

```bash
# Test with multiple images
# Edit test plan to use CSV Data Set Config
# Create images.csv with different image paths
```

## Performance Optimization Tips

Based on test results, consider:

1. **High Latency (> 2s)**
   - Increase ProcessPoolExecutor workers
   - Use smaller model (ONNX INT8)
   - Add caching layer

2. **Low Throughput (< 5 TPS)**
   - Scale horizontally (more instances)
   - Optimize image preprocessing
   - Use CDN for static assets

3. **High Error Rate (> 5%)**
   - Check API logs
   - Increase timeout values
   - Add retry logic

## Reporting

### For Project Report

Include these sections:

1. **Test Configuration**
   - Number of users
   - Ramp-up time
   - Total requests

2. **Results Summary**
   - Throughput (TPS)
   - Average latency
   - P95/P99 latency
   - Error rate

3. **Graphs**
   - Response time over time
   - Throughput over time
   - Response time percentiles

4. **Analysis**
   - Bottlenecks identified
   - Performance comparison (local vs cloud)
   - Recommendations

### Export Results

```bash
# Copy HTML report
cp -r report_cloud/ ../docs/jmeter_results/

# Take screenshots
# 1. Dashboard overview
# 2. Response time graph
# 3. Throughput graph
# 4. Statistics table
```

## CI/CD Integration

Add to `.github/workflows/performance-test.yml`:

```yaml
name: Performance Test

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  jmeter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install JMeter
        run: |
          wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar -xzf apache-jmeter-5.6.3.tgz
      - name: Run Load Test
        run: |
          apache-jmeter-5.6.3/bin/jmeter -n -t jmeter/dog_classifier_loadtest.jmx \
            -l results.jtl -e -o report/
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: jmeter-report
          path: report/
```

## Resources

- [JMeter Documentation](https://jmeter.apache.org/usermanual/index.html)
- [Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [Performance Testing Guide](https://www.blazemeter.com/blog/jmeter-tutorial)

---

**Need help?** Check the [main README](../README.md) or open an issue on GitHub.
