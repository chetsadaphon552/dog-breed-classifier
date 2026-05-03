"""
Complete Pipeline - Dog Breed Classification
1. Download & Convert model (Step 1)
2. Benchmark performance (Step 2)
3. Evaluate accuracy (Step 3)
"""
import subprocess
import sys
import time
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"{text}")
    print("=" * 80 + "\n")


def print_step(step_num, title):
    """Print step header"""
    print(f"\n{'='*80}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*80}\n")


def run_command(command, description, timeout=None):
    """Run a command and return success status"""
    print(f"Running: {description}")
    print(f"   Command: {command}")
    if timeout:
        print(f"   Timeout: {timeout}s")
    print()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            timeout=timeout,
            check=True
        )
        
        print(f"\n[SUCCESS] {description}")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"\n[TIMEOUT] {description} - exceeded {timeout}s")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n[FAILED] {description} - exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n[ERROR] {description} - {e}")
        return False


def check_file_exists(file_path, description):
    """Check if file exists and print result"""
    path = Path(file_path)
    if path.exists():
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  [OK] {description}: {file_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"  [NOT FOUND] {description}: {file_path}")
        return False


def main():
    """Main pipeline function"""
    print_header("DOG BREED CLASSIFICATION - COMPLETE PIPELINE")
    
    print("This pipeline will:")
    print("  1. Download & Convert model (Step 1)")
    print("  2. Benchmark performance (Step 2)")
    print("  3. Evaluate accuracy (Step 3)")
    print()
    print("Note: Make sure you have installed requirements:")
    print("  pip install -r requirements.txt")
    print()
    
    # Run automatically without asking
    start_time = time.time()
    results = {}
    
    # ========================================
    # STEP 1: Download & Convert Model
    # ========================================
    print_step(1, "Download & Convert Model")
    
    # Check if models already exist
    print("Checking existing models...")
    fp32_exists = check_file_exists("models/resnet34_fp32.onnx", "ONNX FP32")
    int8_exists = check_file_exists("models/resnet34_int8.onnx", "ONNX INT8")
    labels_exists = check_file_exists("models/resnet34_dog_breeds.json", "Dog Breeds")
    
    if fp32_exists and int8_exists and labels_exists:
        print("\n[OK] All models already exist! Skipping download...")
        results['step1'] = True
    else:
        print("\n[INFO] Some models missing. Running Step 1...")
        results['step1'] = run_command(
            "python models/step1_download_and_convert.py",
            "Step 1: Download & Convert",
            timeout=600  # 10 minutes
        )
        
        if not results['step1']:
            print("\n[FAILED] Step 1 failed")
            return
        
        # Verify outputs
        print("\nVerifying outputs...")
        fp32_ok = check_file_exists("models/resnet34_fp32.onnx", "ONNX FP32")
        int8_ok = check_file_exists("models/resnet34_int8.onnx", "ONNX INT8")
        labels_ok = check_file_exists("models/resnet34_dog_breeds.json", "Dog Breeds")
        
        if not (fp32_ok and int8_ok and labels_ok):
            print("\n[FAILED] Step 1 failed: Some output files missing")
            return
    
    # ========================================
    # STEP 2: Benchmark Performance
    # ========================================
    print_step(2, "Benchmark Performance")
    
    results['step2'] = run_command(
        "python models/step2_benchmark.py",
        "Step 2: Benchmark",
        timeout=300  # 5 minutes
    )
    
    if not results['step2']:
        print("\n[FAILED] Step 2 failed")
        return
    
    # Verify outputs
    print("\nVerifying outputs...")
    check_file_exists("benchmark_dogs_results.json", "Benchmark Results")
    check_file_exists("benchmark_dogs_results.png", "Benchmark Plot")
    
    # ========================================
    # STEP 3: Evaluate Accuracy
    # ========================================
    print_step(3, "Evaluate Accuracy")
    
    print("This step will:")
    print("  1. Download Stanford Dogs dataset from Kaggle (~750MB)")
    print("  2. Or use existing dataset if already downloaded")
    print("  3. Evaluate 750 images across 30 dog breeds")
    print("  4. Generate accuracy reports and confusion matrices")
    print()
    print("Estimated time: 10-20 minutes")
    print()
    
    # Run step 3 automatically
    results['step3'] = run_command(
        "python models/step3_evaluate_accuracy.py",
        "Step 3: Evaluate",
        timeout=1800  # 30 minutes
    )
    
    if not results['step3']:
        print("\n[FAILED] Step 3 failed")
        print("   Check if Kaggle CLI is installed and configured")
        print("   Or download dataset manually from:")
        print("   https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset")
        return
    
    # Verify outputs
    print("\nVerifying outputs...")
    results_dir = Path("evaluation_results")
    if results_dir.exists():
        subdirs = [d for d in results_dir.iterdir() if d.is_dir()]
        print(f"\n  [OK] Found {len(subdirs)} result folders")
        for d in subdirs:
            print(f"     - {d.name}")
    
    check_file_exists("evaluation_results/resnet34_dogs_comparison.json", "Comparison")
    check_file_exists("evaluation_results/resnet34_dogs_comparison.png", "Comparison Plot")
    
    # ========================================
    # Summary
    # ========================================
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print_header("PIPELINE SUMMARY")
    
    print("Results:")
    for step, result in results.items():
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        
        print(f"  {step.upper()}: {status}")
    
    print()
    print(f"Total time: {minutes}m {seconds}s")
    
    # Check success
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    
    if failed == 0:
        print("\nPipeline completed successfully!")
        print("\nGenerated files:")
        print("  - models/resnet34_fp32.onnx (83 MB)")
        print("  - models/resnet34_int8.onnx (21 MB)")
        print("  - models/resnet34_dog_breeds.json")
        print("  - benchmark_dogs_results.json")
        print("  - benchmark_dogs_results.png")
        
        # Only show evaluation results if they actually exist
        if results.get('step3') is True and Path("evaluation_results/resnet34_dogs_comparison.json").exists():
            print("  - evaluation_results/ (3 folders)")
            print("  - evaluation_results/resnet34_dogs_comparison.json")
            print("  - evaluation_results/resnet34_dogs_comparison.png")
    else:
        print("\nPipeline completed with errors")
        print("   Check the output above for details")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
