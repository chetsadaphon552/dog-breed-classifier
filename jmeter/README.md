# JMeter Load Testing

## Prerequisites

1. Download Apache JMeter: https://jmeter.apache.org/download_jmeter.cgi
2. Extract to a folder
3. Add JMeter `bin` folder to PATH

## Running Load Tests

### GUI Mode (for test development)

```bash
jmeter -t jmeter/dog_classifier_loadtest.jmx
```

### CLI Mode (for actual testing)

```bash
# Run test and generate HTML report
jmeter -n -t jmeter/dog_classifier_loadtest.jmx \
  -l jmeter/results.jtl \
  -e -o jmeter/html-report

# View report
# Open jmeter/html-report/index.html in browser
```

### Windows

```cmd
jmeter.bat -n -t jmeter\dog_classifier_loadtest.jmx -l jmeter\results.jtl -e -o jmeter\html-report
```

## Test Configuration

- **Users**: 10 concurrent users
- **Ramp-up**: 5 seconds
- **Loops**: 10 iterations per user
- **Total Requests**: 100

## Modifying Test Parameters

Edit `dog_classifier_loadtest.jmx` and change:

1. **Number of Users**: `ThreadGroup.num_threads`
2. **Ramp-up Time**: `ThreadGroup.ramp_time`
3. **Loop Count**: `LoopController.loops`
4. **Base URL**: `BASE_URL` variable
5. **Image Path**: `IMAGE_PATH` variable

## Metrics to Analyze

- **Throughput**: Requests per second (TPS)
- **Latency**: Response time (ms)
  - Average
  - Median (P50)
  - P95
  - P99
- **Error Rate**: % of failed requests
- **Response Codes**: Distribution of HTTP status codes

## Expected Results (Local)

- **Throughput**: ~30-40 TPS
- **Average Latency**: ~30-40 ms
- **P95 Latency**: ~50-60 ms
- **Error Rate**: 0%

## Expected Results (Cloud - Hugging Face Spaces)

- **Throughput**: ~10-20 TPS
- **Average Latency**: ~60-80 ms
- **P95 Latency**: ~100-120 ms
- **Error Rate**: 0%
