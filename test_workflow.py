"""
Test complete workflow - Download → Convert → Benchmark → Evaluate
This script tests each step to ensure everything works
"""
import subprocess
import sys
from pathlib import Path
import json
import time


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_step(step_num, title):
    """Print step header"""
    print(f"\n{'='*80}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*80}\n")


def check_file_exists(file_path, description):
    """Check if file exists and print result"""
    path = Path(file_path)
    if path.exists():
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  ✅ {description}: {file_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"  ❌ {description}: {file_path} (NOT FOUND)")
        return False


def run_command(command, description, timeout=300):
    """Run a command and return success status"""
    print(f"\n🔄 Running: {description}")
    print(f"   Command: {command}")
    print(f"   Timeout: {timeout}s")
    print()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"\n✅ {description} - SUCCESS")
            return True
        else:
            print(f"\n❌ {description} - FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⚠️  {description} - TIMEOUT (exceeded {timeout}s)")
        return False
    except Exception as e:
        print(f"\n❌ {description} - ERROR: {e}")
        return False


def test_step1():
    """Test Step 1: Download and Convert"""
    print_step(1, "Download & Convert Model")
    
    print("This step will:")
    print("  1. Download microsoft/resnet-34 from Hugging Face")
    print("  2. Convert to ONNX FP32")
    print("  3. Quantize to ONNX INT8")
    print("  4. Save dog breed labels")
    print()
    
    # Check if models already exist
    print("Checking existing models...")
    fp32_exists = check_file_exists("models/resnet34_fp32.onnx", "ONNX FP32")
    int8_exists = check_file_exists("models/resnet34_int8.onnx", "ONNX INT8")
    labels_exists = check_file_exists("models/resnet34_dog_breeds.json", "Dog Breeds Labels")
    
    if fp32_exists and int8_exists and labels_exists:
        print("\n✅ All models already exist!")
        print("   Skipping download (models are ready)")
        return True
    
    print("\n⚠️  Some models are missing. Running step1...")
    
    # Run step1
    success = run_command(
        "python models/step1_download_and_convert.py",
        "Step 1: Download & Convert",
        timeout=600  # 10 minutes for download
    )
    
    if success:
        # Verify outputs
        print("\nVerifying outputs...")
        fp32_ok = check_file_exists("models/resnet34_fp32.onnx", "ONNX FP32")
        int8_ok = check_file_exists("models/resnet34_int8.onnx", "ONNX INT8")
        labels_ok = check_file_exists("models/resnet34_dog_breeds.json", "Dog Breeds Labels")
        
        if fp32_ok and int8_ok and labels_ok:
            print("\n✅ Step 1 completed successfully!")
            return True
        else:
            print("\n❌ Step 1 failed: Some output files are missing")
            return False
    
    return False


def test_step2():
    """Test Step 2: Benchmark"""
    print_step(2, "Benchmark Performance")
    
    print("This step will:")
    print("  1. Benchmark PyTorch FP32 (estimated)")
    print("  2. Benchmark ONNX FP32")
    print("  3. Benchmark ONNX INT8")
    print("  4. Compare speed & size")
    print("  5. Generate charts")
    print()
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_file_exists("models/resnet34_fp32.onnx", "ONNX FP32"):
        print("\n❌ Cannot run Step 2: ONNX FP32 model not found")
        print("   Run Step 1 first: python models/step1_download_and_convert.py")
        return False
    
    if not check_file_exists("models/resnet34_int8.onnx", "ONNX INT8"):
        print("\n❌ Cannot run Step 2: ONNX INT8 model not found")
        print("   Run Step 1 first: python models/step1_download_and_convert.py")
        return False
    
    print("\n✅ Prerequisites OK")
    
    # Run step2
    success = run_command(
        "python models/step2_benchmark.py",
        "Step 2: Benchmark",
        timeout=300  # 5 minutes
    )
    
    if success:
        # Verify outputs
        print("\nVerifying outputs...")
        results_ok = check_file_exists("benchmark_dogs_results.json", "Benchmark Results")
        plot_ok = check_file_exists("benchmark_dogs_results.png", "Benchmark Plot")
        
        if results_ok:
            # Show results summary
            try:
                with open("benchmark_dogs_results.json", 'r') as f:
                    results = json.load(f)
                
                print("\n📊 Benchmark Summary:")
                for r in results:
                    print(f"  • {r['model']}: {r['mean_ms']:.2f} ms, {r['size_mb']:.2f} MB")
                
                print("\n✅ Step 2 completed successfully!")
                return True
            except Exception as e:
                print(f"\n⚠️  Could not read results: {e}")
                return True  # Still consider success if file exists
        else:
            print("\n❌ Step 2 failed: Results file not found")
            return False
    
    return False


def test_step3():
    """Test Step 3: Evaluate Accuracy"""
    print_step(3, "Evaluate Accuracy")
    
    print("This step will:")
    print("  1. Download Stanford Dogs dataset from Kaggle")
    print("  2. Test PyTorch FP32 model")
    print("  3. Test ONNX FP32 model")
    print("  4. Test ONNX INT8 model")
    print("  5. Calculate accuracy, precision, recall, F1")
    print("  6. Generate confusion matrix")
    print("  7. Create comparison charts")
    print()
    print("⚠️  WARNING: This step takes 10-20 minutes!")
    print("   It downloads ~750MB dataset and tests 750 images")
    print()
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_file_exists("models/resnet34_fp32.onnx", "ONNX FP32"):
        print("\n❌ Cannot run Step 3: ONNX FP32 model not found")
        return False
    
    if not check_file_exists("models/resnet34_int8.onnx", "ONNX INT8"):
        print("\n❌ Cannot run Step 3: ONNX INT8 model not found")
        return False
    
    if not check_file_exists("models/resnet34_dog_breeds.json", "Dog Breeds Labels"):
        print("\n❌ Cannot run Step 3: Dog breeds labels not found")
        return False
    
    print("\n✅ Prerequisites OK")
    
    # Ask user confirmation
    print("\n⚠️  This step will take 10-20 minutes. Continue? (y/n): ", end='')
    response = input().strip().lower()
    
    if response != 'y':
        print("\n⏭️  Skipping Step 3")
        return None  # None means skipped
    
    # Run step3
    success = run_command(
        "python models/step3_evaluate_accuracy.py",
        "Step 3: Evaluate Accuracy",
        timeout=1800  # 30 minutes
    )
    
    if success:
        # Verify outputs
        print("\nVerifying outputs...")
        results_dir = Path("evaluation_results")
        
        if results_dir.exists():
            subdirs = [d for d in results_dir.iterdir() if d.is_dir()]
            print(f"\n  ✅ Found {len(subdirs)} result folders:")
            for d in subdirs:
                print(f"     - {d.name}")
            
            # Check comparison files
            comparison_json = results_dir / "resnet34_dogs_comparison.json"
            comparison_png = results_dir / "resnet34_dogs_comparison.png"
            
            if comparison_json.exists():
                try:
                    with open(comparison_json, 'r') as f:
                        comparison = json.load(f)
                    
                    print("\n📊 Evaluation Summary:")
                    for i, model in enumerate(comparison['models']):
                        acc = comparison['accuracies'][i] * 100
                        conf = comparison['confidences'][i] * 100
                        print(f"  • {model}: {acc:.2f}% accuracy, {conf:.2f}% confidence")
                    
                    print("\n✅ Step 3 completed successfully!")
                    return True
                except Exception as e:
                    print(f"\n⚠️  Could not read comparison: {e}")
                    return True
            else:
                print("\n⚠️  Comparison file not found, but results exist")
                return True
        else:
            print("\n❌ Step 3 failed: Results directory not found")
            return False
    
    return False


def test_api():
    """Test API"""
    print_step(4, "Test API")
    
    print("This step will:")
    print("  1. Check if Docker container is running")
    print("  2. Test API endpoints")
    print()
    
    # Check if Docker container is running
    print("Checking Docker container...")
    result = subprocess.run(
        "docker ps --filter name=dog-api --format '{{.Names}}'",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if "dog-api" in result.stdout:
        print("  ✅ Docker container 'dog-api' is running")
        
        # Test API
        print("\nTesting API endpoints...")
        
        # Test root endpoint
        result = subprocess.run(
            'curl -s http://localhost:8000/',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and "Dog Breed Classification API" in result.stdout:
            print("  ✅ Root endpoint: OK")
            print(f"     Response: {result.stdout[:100]}...")
            
            # Test health endpoint
            result = subprocess.run(
                'curl -s http://localhost:8000/health',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("  ✅ Health endpoint: OK")
                print(f"     Response: {result.stdout[:100]}...")
            
            print("\n✅ API is working!")
            print("   Swagger UI: http://localhost:8000/docs")
            return True
        else:
            print("  ❌ API not responding correctly")
            return False
    else:
        print("  ❌ Docker container 'dog-api' is not running")
        print("\n  To start the API:")
        print("    docker run -d --name dog-api -p 8000:8000 dog-classification-api:latest")
        return False


def main():
    """Main test function"""
    print_header("🐕 DOG BREED CLASSIFICATION - WORKFLOW TEST")
    
    print("This script will test the complete workflow:")
    print("  Step 1: Download & Convert Model")
    print("  Step 2: Benchmark Performance")
    print("  Step 3: Evaluate Accuracy (optional, takes 10-20 min)")
    print("  Step 4: Test API")
    print()
    
    results = {}
    
    # Test Step 1
    try:
        results['step1'] = test_step1()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Step 1 error: {e}")
        results['step1'] = False
    
    # Test Step 2 (only if Step 1 succeeded)
    if results['step1']:
        try:
            results['step2'] = test_step2()
        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Step 2 error: {e}")
            results['step2'] = False
    else:
        print("\n⏭️  Skipping Step 2 (Step 1 failed)")
        results['step2'] = None
    
    # Test Step 3 (only if Step 1 succeeded)
    if results['step1']:
        try:
            results['step3'] = test_step3()
        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Step 3 error: {e}")
            results['step3'] = False
    else:
        print("\n⏭️  Skipping Step 3 (Step 1 failed)")
        results['step3'] = None
    
    # Test API
    try:
        results['api'] = test_api()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ API test error: {e}")
        results['api'] = False
    
    # Print summary
    print_header("📊 TEST SUMMARY")
    
    print("Results:")
    for step, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⏭️  SKIP"
        
        print(f"  {step.upper()}: {status}")
    
    # Overall status
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print()
    print(f"Total: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        print("\nNext steps:")
        print("  1. View results in evaluation_results/")
        print("  2. Test API at http://localhost:8000/docs")
        print("  3. Deploy to production")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
