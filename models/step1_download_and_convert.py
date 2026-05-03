"""
Step 22: Test microsoft/resnet-34
ResNet-34 - ควรเล็กกว่า ViT-base
Official Microsoft model
"""
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
from onnxruntime.quantization import quantize_dynamic, QuantType
from pathlib import Path
import time
import numpy as np
from PIL import Image
import json
import onnxruntime as ort


def download_and_convert():
    """Download PyTorch model and convert to ONNX INT8"""
    print("=" * 80)
    print("Step 22: ResNet-34 (Microsoft) → ONNX INT8")
    print("=" * 80)
    
    try:
        model_id = "microsoft/resnet-34"
        
        # 1. โหลดโมเดล PyTorch
        print(f"\n1. โหลดโมเดล PyTorch จาก {model_id}")
        print("   Architecture: ResNet-34 (CNN)")
        print("   Official Microsoft model")
        
        model = AutoModelForImageClassification.from_pretrained(
            model_id,
            cache_dir="models/cache_resnet34"
        )
        processor = AutoImageProcessor.from_pretrained(
            model_id,
            cache_dir="models/cache_resnet34"
        )
        model.eval()
        
        id2label = model.config.id2label
        print(f"[OK] โหลดสำเร็จ: {len(id2label)} classes")
        print(f"   Task: ImageNet classification")
        
        # Check model size
        param_count = sum(p.numel() for p in model.parameters())
        param_size_mb = param_count * 4 / (1024 * 1024)
        print(f"   Parameters: {param_count:,}")
        print(f"   Estimated FP32 size: {param_size_mb:.2f} MB")
        
        if param_size_mb < 300:
            print(f"   SMALLER THAN 300 MB! ({param_size_mb:.0f} MB)")
        if param_size_mb < 100:
            print(f"   MUCH SMALLER! ({param_size_mb:.0f} MB)")
        
        # 2. Export เป็น FP32 ONNX
        print("\n2. Export เป็น ONNX FP32...")
        fp32_path = "models/resnet34_fp32.onnx"
        dummy_input = torch.randn(1, 3, 224, 224)
        
        torch.onnx.export(
            model,
            dummy_input,
            fp32_path,
            opset_version=13,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
        )
        
        fp32_size = Path(fp32_path).stat().st_size / (1024 * 1024)
        print(f"[OK] ONNX FP32 สำเร็จ: {fp32_size:.2f} MB")
        
        if fp32_size < 300:
            savings = 328 - fp32_size
            print(f"   {savings:.0f}MB SMALLER THAN ViT-base!")
        
        # 3. แปลงเป็น INT8
        print("\n3. แปลงเป็น INT8...")
        int8_path = "models/resnet34_int8.onnx"
        
        quantize_dynamic(
            model_input=fp32_path,
            model_output=int8_path,
            weight_type=QuantType.QUInt8
        )
        
        int8_size = Path(int8_path).stat().st_size / (1024 * 1024)
        reduction = (1 - int8_size / fp32_size) * 100
        
        print(f"[OK] ONNX INT8 สำเร็จ: {int8_size:.2f} MB")
        print(f"   ลดขนาด: {reduction:.1f}%")
        
        if int8_size < 83:
            savings = 83 - int8_size
            print(f"   {savings:.0f}MB SMALLER THAN tribber93!")
        
        # Save labels (first 10 only for brevity)
        sample_labels = {k: v for k, v in list(id2label.items())[:10]}
        with open("models/resnet34_labels_sample.json", 'w') as f:
            json.dump(sample_labels, f, indent=2)
        
        return fp32_path, int8_path, id2label, fp32_size, int8_size
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None, None


def test_model(model_path, model_name):
    """Test ONNX model performance"""
    print(f"\n{'=' * 80}")
    print(f"Testing: {model_name}")
    print("=" * 80)
    
    try:
        test_image = Image.new('RGB', (224, 224), color=(73, 109, 137))
        img_array = np.array(test_image).astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_array = (img_array - mean) / std
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
        
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.intra_op_num_threads = 4
        
        session = ort.InferenceSession(
            model_path,
            sess_options=sess_options,
            providers=['CPUExecutionProvider']
        )
        
        input_name = session.get_inputs()[0].name
        
        print("   Warming up...")
        for _ in range(5):
            _ = session.run(None, {input_name: img_array})
        
        print("   Running benchmark (100 iterations)...")
        times = []
        for _ in range(100):
            start = time.perf_counter()
            outputs = session.run(None, {input_name: img_array})
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
        
        times = np.array(times)
        size_mb = Path(model_path).stat().st_size / (1024 * 1024)
        
        result = {
            "model_name": model_name,
            "size_mb": float(size_mb),
            "mean_ms": float(np.mean(times)),
            "median_ms": float(np.median(times)),
            "std_ms": float(np.std(times)),
            "works": True
        }
        
        print(f"[OK] ทำงานได้!")
        print(f"   Mean:   {result['mean_ms']:.2f} ms")
        print(f"   Median: {result['median_ms']:.2f} ms")
        print(f"   Size:   {result['size_mb']:.2f} MB")
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        print(f"[FAILED] ล้มเหลว: {error_msg[:200]}")
        if "ConvInteger" in error_msg:
            print("\n[WARNING] ConvInteger operator error - INT8 ไม่รองรับ")
        return {"model_name": model_name, "works": False, "error": error_msg}


def main():
    """Main execution"""
    import time
    start_time = time.time()
    
    print("\n" + "=" * 80)
    print("ResNet-34 (Microsoft Official)")
    print("=" * 80 + "\n")
    
    fp32_path, int8_path, id2label, fp32_size, int8_size = download_and_convert()
    
    if not fp32_path:
        return
    
    print("\n" + "=" * 80)
    print("TESTING MODELS")
    print("=" * 80)
    
    results = []
    
    print("\nTesting INT8...")
    if int8_path and Path(int8_path).exists():
        int8_result = test_model(int8_path, "resnet34_int8")
        results.append(int8_result)
    
    if results and results[0].get("works"):
        int8 = results[0]
        
        print(f"\n" + "=" * 80)
        print("COMPARISON")
        print("=" * 80)
        
        print(f"\nResNet-34 (NEW):")
        print(f"   FP32: {fp32_size:.0f} MB")
        print(f"   INT8: {int8['size_mb']:.0f} MB")
        print(f"   Latency: {int8['mean_ms']:.0f} ms")
        print(f"   Classes: {len(id2label)} (ImageNet)")
        print(f"   Cloud: ~{int8['mean_ms'] * 2.4:.0f} ms")
        
        print(f"\nPrevious Best:")
        print(f"   watersplash (ViT): 328 MB FP32, 83 MB INT8, 74 ms")
        print(f"   tribber93 (ViT):   328 MB FP32, 83 MB INT8, 77 ms")
        
        print(f"\nSIZE COMPARISON:")
        print(f"   ViT-base:  328 MB FP32, 83 MB INT8")
        print(f"   ResNet-34: {fp32_size:.0f} MB FP32, {int8['size_mb']:.0f} MB INT8")
        
        if fp32_size < 300:
            print(f"   FP32 SMALLER THAN 300 MB!")
        if int8['size_mb'] < 83:
            print(f"   INT8 SMALLER THAN 83 MB!")
        
        print(f"\nSPEED COMPARISON:")
        if int8['mean_ms'] < 74:
            speedup = 74 / int8['mean_ms']
            print(f"   FASTER! ({speedup:.2f}x faster than watersplash)")
        elif int8['mean_ms'] < 77:
            print(f"   Faster than tribber93")
        else:
            print(f"   Slower")
        
        print(f"\nSUMMARY:")
        print(f"   Architecture: ResNet-34 (CNN)")
        print(f"   Size: {int8['size_mb']:.0f} MB INT8")
        print(f"   Speed: {int8['mean_ms']:.0f} ms")
        print(f"   Cloud: ~{int8['mean_ms'] * 2.4:.0f} ms")
        
        if int8['mean_ms'] * 2.4 < 100:
            print(f"   MEETS <100ms TARGET!")
        
        if fp32_size < 300:
            print(f"\nSUCCESS: Found model with FP32 < 300 MB!")
        if int8['size_mb'] < 83 and int8['mean_ms'] < 74:
            print(f"NEW WINNER: ResNet-34 (smaller + faster)!")
        elif int8['size_mb'] < 83:
            print(f"NEW WINNER: ResNet-34 (smallest INT8)!")
        elif int8['mean_ms'] < 74:
            print(f"NEW WINNER: ResNet-34 (fastest)!")
    else:
        print(f"\n[FAILED] INT8 quantization failed")
        if results and results[0].get("error"):
            print(f"   Error: {results[0]['error'][:100]}")
    
    with open("benchmark_resnet34_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"\nResults saved!")
    print(f"Time elapsed: {minutes}m {seconds}s")


if __name__ == "__main__":
    main()
