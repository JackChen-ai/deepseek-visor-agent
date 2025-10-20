"""
Simple test script to verify DeepSeek-OCR integration
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_device_detection():
    """Test device detection"""
    logger.info("=" * 60)
    logger.info("Testing Device Detection")
    logger.info("=" * 60)

    from deepseek_visor_agent import DeviceManager

    config = DeviceManager.detect_optimal_config()
    logger.info(f"Detected config: {config}")

    device_info = DeviceManager.get_device_info()
    logger.info(f"Device info:\n{device_info}")

    return config

def test_model_loading():
    """Test model loading"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Model Loading")
    logger.info("=" * 60)

    from deepseek_visor_agent.infer import DeepSeekOCRInference

    # Use CPU and tiny mode for initial testing
    logger.info("Initializing inference engine with CPU + tiny mode...")
    engine = DeepSeekOCRInference(inference_mode="tiny", device="cpu")

    logger.info("Loading model (this may take several minutes on first run)...")
    engine._ensure_initialized()

    logger.info("✅ Model loaded successfully!")
    return engine

def test_inference_with_dummy_image():
    """Test inference with a dummy image"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Inference (Dummy Image)")
    logger.info("=" * 60)

    from PIL import Image
    import tempfile
    from deepseek_visor_agent.infer import DeepSeekOCRInference

    # Create a simple test image
    logger.info("Creating dummy test image...")
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img = Image.new('RGB', (640, 480), color='white')
        # Add some text (simplified)
        img.save(tmp.name)
        test_image_path = tmp.name

    logger.info(f"Test image created at: {test_image_path}")

    # Initialize engine
    engine = DeepSeekOCRInference(inference_mode="tiny", device="cpu")

    try:
        logger.info("Running inference...")
        result = engine.infer(test_image_path)

        logger.info("✅ Inference completed successfully!")
        logger.info(f"Output preview: {result['markdown'][:200]}...")
        logger.info(f"Metadata: {result['metadata']}")

        return result
    finally:
        # Clean up
        Path(test_image_path).unlink(missing_ok=True)

def main():
    """Run all tests"""
    try:
        # Test 1: Device detection
        config = test_device_detection()

        # Test 2: Model loading
        engine = test_model_loading()

        # Test 3: Inference
        result = test_inference_with_dummy_image()

        logger.info("\n" + "=" * 60)
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("=" * 60)
        logger.info(f"\nYour system is configured to use:")
        logger.info(f"  - Device: {config['device']}")
        logger.info(f"  - Inference Mode: {config['inference_mode']}")
        logger.info(f"  - FlashAttention: {config['use_flash_attn']}")
        logger.info(f"  - Available Memory: {config['max_memory_gb']:.1f}GB")

    except Exception as e:
        logger.error(f"\n❌ Test failed with error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
