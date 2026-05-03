"""
Clean up project - Keep only Dog Breed Classification files
Remove all garbage/waste classification files and old experiments
"""
import os
import shutil
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 80)
    print(f"{text}")
    print("=" * 80 + "\n")


def remove_file(file_path, description=""):
    """Remove a file"""
    try:
        if Path(file_path).exists():
            os.remove(file_path)
            print(f"  [DELETED] {file_path} {description}")
            return True
        return False
    except Exception as e:
        print(f"  [ERROR] deleting {file_path}: {e}")
        return False


def remove_directory(dir_path, description=""):
    """Remove a directory"""
    try:
        if Path(dir_path).exists():
            shutil.rmtree(dir_path)
            print(f"  [DELETED] {dir_path}/ {description}")
            return True
        return False
    except Exception as e:
        print(f"  [ERROR] deleting {dir_path}: {e}")
        return False


def main():
    print_header("PROJECT CLEANUP - Dog Breed Classification")
    
    print("This script will remove:")
    print("  - Old garbage/waste classification files")
    print("  - Experimental model files (aalaa, facial, trash_vit, etc.)")
    print("  - Old step files (step4-26)")
    print("  - Duplicate documentation files")
    print("  - Test/benchmark files for old models")
    print()
    print("This script will KEEP:")
    print("  - Dog breed classification (ResNet-34)")
    print("  - Step 1, 2, 3 (download, benchmark, evaluate)")
    print("  - FastAPI application (app/)")
    print("  - Docker files (Dockerfile.onnx)")
    print("  - Main documentation (README.md, WORKFLOW.md)")
    print()
    
    # Run automatically without asking
    deleted_count = 0
    
    # ========================================
    # 1. Remove old model files (non-dog)
    # ========================================
    print_header("1. Removing Old Model Files")
    
    old_models = [
        # Garbage/waste models
        "models/model.onnx",
        "models/model_quantized.onnx",
        "models/model_dogs.onnx",
        "models/model_dogs_quantized.onnx",
        "models/model_dogs_optimized.onnx",
        
        # Experimental models
        "models/aalaa_fp32.onnx",
        "models/aalaa_int8.onnx",
        "models/aalaa_labels.json",
        "models/facial_fp32.onnx",
        "models/facial_int8.onnx",
        "models/facial_labels.json",
        "models/trash_vit_labels.json",
        "models/model_trash_vit.onnx",
        "models/model_trash_vit_int8.onnx",
        "models/model_trash_vit_int8_v2.onnx",
        "models/model_trash_vit_opset13.onnx",
        "models/tribber93_fp32.onnx",
        "models/tribber93_int8.onnx",
        "models/tribber93_labels.json",
        "models/watersplash_fp32.onnx",
        "models/watersplash_int8.onnx",
        "models/watersplash_labels.json",
        "models/dogs_labels.json",  # Old format
    ]
    
    for model in old_models:
        if remove_file(model, "(old model)"):
            deleted_count += 1
    
    # ========================================
    # 2. Remove cache directories
    # ========================================
    print_header("2. Removing Cache Directories")
    
    cache_dirs = [
        "models/cache",
        "models/cache_aalaa_vit",
        "models/cache_efficientnet",
        "models/cache_facial",
        "models/cache_mobilenet_trash",
        "models/cache_mobilenetv3",
        "models/cache_resnet50_garbage",
        "models/cache_resnet50_raw",
        "models/cache_trash_vit",
        "models/cache_vit_tiny_food",
        "models/cache_watersplash",
        "models/backup_waste",
        # Keep: models/cache_dogs (might be needed)
        # Keep: models/cache_resnet34 (might be needed)
    ]
    
    for cache_dir in cache_dirs:
        if remove_directory(cache_dir, "(cache)"):
            deleted_count += 1
    
    # ========================================
    # 3. Remove old step files
    # ========================================
    print_header("3. Removing Old Step Files")
    
    old_steps = [
        "models/step3_test_new_cnn_model.py",
        "models/step4_test_dogs_model.py",
        "models/step5_quantize_dogs_static.py",
        "models/step6_optimize_dogs_for_production.py",
        "models/step7_test_mobilenet_food.py",
        "models/step8_test_trash_vit.py",
        "models/step9_test_resnet50_garbage.py",
        "models/step10_resnet50_raw_pytorch.py",
        "models/step11_force_int8_quantization.py",
        "models/step12_final_int8_attempt.py",
        "models/step13_efficientnet_garbage.py",
        "models/step14_optimum_export.py",
        "models/step15_tribber93_pytorch_to_int8.py",
        "models/step16_test_aalaa_vit.py",
        "models/step17_test_facial_expression.py",
        "models/step18_test_mobilenet_trash.py",
        "models/step19_test_mobilenetv3_ecovision.py",
        "models/step20_test_watersplash.py",
        "models/step21_test_vit_tiny_food.py",
        "models/step23_resnet34_dogs_only.py",
        "models/step24_test_accuracy_stanford_dogs.py",
        "models/step25_evaluate_resnet34_dogs.py",
        "models/step26_visualize_resnet34_results.py",
        "models/check_breed_coverage.py",
        "models/check_test_breeds.py",
        "models/count_actual_breeds.py",
    ]
    
    for step in old_steps:
        if remove_file(step, "(old experiment)"):
            deleted_count += 1
    
    # ========================================
    # 4. Remove old benchmark files
    # ========================================
    print_header("4. Removing Old Benchmark Files")
    
    old_benchmarks = [
        "benchmark_aalaa_results.json",
        "benchmark_facial_results.json",
        "benchmark_resnet34_results.json",
        "benchmark_results.json",
        "benchmark_results.png",
        "benchmark_trash_vit_results.json",
        "benchmark_tribber93_final.json",
        "benchmark_watersplash_results.json",
        "benchmark_docker_results.json",
        "benchmark_comparison.png",
        "benchmark_complete_comparison.png",
        "benchmark_docker_api.py",
        "compare_local_vs_docker.py",
        "test_mobilenet_speed.py",
        "test_model_comparison.py",
        "visualize_benchmark.py",
        # Keep: benchmark_dogs_results.json
        # Keep: benchmark_dogs_results.png
        # Keep: benchmark_dogs_final.json
    ]
    
    for benchmark in old_benchmarks:
        if remove_file(benchmark, "(old benchmark)"):
            deleted_count += 1
    
    # ========================================
    # 5. Remove duplicate documentation
    # ========================================
    print_header("5. Removing Duplicate Documentation")
    
    old_docs = [
        "ALL_MODELS_FINAL_COMPARISON.md",
        "API_USAGE_GUIDE.md",
        "BENCHMARK_COMPARISON.md",
        "CURL_EXAMPLES.md",
        "DEPENDENCIES.md",
        "DEPLOYMENT_GUIDE.md",
        "DEPLOYMENT_SUCCESS.md",
        "DEPLOY_NOW.md",
        "DOCKER_LINUX_PERFORMANCE_ESTIMATE.md",
        "DOCKER_ONNX_INT8_SUCCESS.md",
        "DOCKER_SUCCESS.md",
        "DOCKER_TROUBLESHOOTING.md",
        "EVALUATION_FOLDER_STRUCTURE.md",
        "FILE_CLEANUP_SUMMARY.md",
        "FINAL_MODEL_COMPARISON.md",
        "FINAL_PROJECT_STRUCTURE.md",
        "GETTING_STARTED.md",
        "LATENCY_TEST_RESULTS.md",
        "MODEL_COMPARISON_REPORT.md",
        "MODELS_TESTED_SUMMARY.md",
        "NEXT_STEPS.md",
        "PROJECT_CHECKLIST.md",
        "PROJECT_PROGRESS_UPDATE.md",
        "PROJECT_STATUS_CHECKLIST.md",
        "PROJECT_STRUCTURE.md",
        "QUICK_REFERENCE.md",
        "QUICK_START.md",
        "READY_TO_DEPLOY.md",
        "SETUP_WSL2_DOCKER.md",
        "SETUP_WSL2_STEP_BY_STEP.md",
        "SOLUTION_FOR_100MS.md",
        "START_API.md",
        "START_DOG_API.md",
        "STEP3_USAGE.md",
        "SUCCESS_TRIBBER93_INT8.md",
        "DOCKER_GUIDE.md",
        # Keep: README.md
        # Keep: README_HF.md
        # Keep: WORKFLOW.md
    ]
    
    for doc in old_docs:
        if remove_file(doc, "(duplicate doc)"):
            deleted_count += 1
    
    # ========================================
    # 6. Remove deployment scripts
    # ========================================
    print_header("6. Removing Old Deployment Scripts")
    
    old_scripts = [
        "deploy_final.sh",
        "deploy_simple.ps1",
        "deploy_to_hf.ps1",
        "deploy_wsl.sh",
        "rebuild_docker_wsl2.sh",
        "run_docker_wsl2.sh",
        "setup_wsl2.ps1",
        "test_api_local.ps1",
        "test_docker_api.ps1",
        "test_docker_prediction.sh",
        "test_docker_wsl2.ps1",
        "build_and_run_docker.bat",
        "start_server.ps1",
        "docker-entrypoint.sh",
        "docker-compose.yml",
        "Dockerfile.complete",
        # Keep: Dockerfile.onnx (for API deployment)
    ]
    
    for script in old_scripts:
        if remove_file(script, "(old script)"):
            deleted_count += 1
    
    # ========================================
    # 7. Remove test/coverage files
    # ========================================
    print_header("7. Removing Test/Coverage Files")
    
    test_files = [
        ".coverage",
        ".coverage.film.pid22988.XNQKuL7x.HncM6AGlhtqh",
        ".coverage.film.pid2416.XCznu8qx.HncM6AGlhtqh",
        ".coverage.film.pid26392.XVIG33wx.HncM6AGlhtqh",
        ".coverage.film.pid492.Xl6KlLVx.HncM6AGlhtqh",
        "coverage.xml",
        "pytest.ini",
        ".dockerignore.onnx",
    ]
    
    for test_file in test_files:
        if remove_file(test_file, "(test/coverage)"):
            deleted_count += 1
    
    # Remove test directories
    test_dirs = [
        "tests",
        ".pytest_cache",
        "htmlcov",
        "jmeter",
        "postman",
        "scripts",
        "hf_deployment",
        "docs",
        "evaluation_results",  # Will be regenerated by step3
    ]
    
    for test_dir in test_dirs:
        if remove_directory(test_dir, "(test/docs)"):
            deleted_count += 1
    
    # ========================================
    # Summary
    # ========================================
    print_header("CLEANUP COMPLETE")
    
    print(f"Total items deleted: {deleted_count}")
    print()
    print("Files KEPT:")
    print("  - models/step1_download_and_convert.py")
    print("  - models/step2_benchmark.py")
    print("  - models/step3_evaluate_accuracy.py")
    print("  - models/resnet34_fp32.onnx")
    print("  - models/resnet34_int8.onnx")
    print("  - models/resnet34_dog_breeds.json")
    print("  - app/ (FastAPI application)")
    print("  - Dockerfile.onnx (for deployment)")
    print("  - README.md, WORKFLOW.md")
    print("  - test_workflow.py")
    print("  - benchmark_dogs_results.json/png")
    print("  - evaluation_results/ (if exists)")
    print()
    print("Project is now clean and focused on Dog Breed Classification!")
    print()
    print("Next steps:")
    print("  1. Run: python test_workflow.py")
    print("  2. Deploy: docker build -f Dockerfile.onnx -t dog-api .")


if __name__ == "__main__":
    main()
