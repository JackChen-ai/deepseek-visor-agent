"""
Inference Engine - Wrapper for DeepSeek-OCR model inference

Handles model loading, device management, and inference execution.
"""

from typing import Dict, Union, Any
from pathlib import Path
import time
import logging
import torch

from .device_manager import DeviceManager
from .utils.error_handler import auto_fallback_decorator, ModelLoadError

logger = logging.getLogger(__name__)


class DeepSeekOCRInference:
    """DeepSeek-OCR inference engine with automatic device and model management"""

    def __init__(self, model_variant: str = "auto", device: str = "auto"):
        """
        Initialize the inference engine.

        Args:
            model_variant: "auto" | "gundam" | "base" | "tiny"
            device: "auto" | "cuda" | "mps" | "cpu"
        """
        self.config = DeviceManager.detect_optimal_config()

        # Override auto-detected settings if specified
        if model_variant != "auto":
            self.config["model_variant"] = model_variant
        if device != "auto":
            self.config["device"] = device

        logger.info(f"Initializing with config: {self.config}")

        self.model = None
        self.tokenizer = None

        # Lazy loading - models will be loaded on first inference call
        self._initialized = False

    def _load_model(self):
        """Load the DeepSeek-OCR model"""
        try:
            from transformers import AutoModelForCausalLM

            model_id = f"deepseek-ai/deepseek-ocr-{self.config['model_variant']}"
            logger.info(f"Loading model: {model_id}")

            load_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.bfloat16 if self.config["device"] != "cpu" else torch.float32,
            }

            if self.config["use_flash_attn"]:
                load_kwargs["attn_implementation"] = "flash_attention_2"

            model = AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
            return model.to(self.config["device"])

        except Exception as e:
            raise ModelLoadError(f"Failed to load model: {e}")

    def _load_tokenizer(self):
        """Load the tokenizer"""
        try:
            from transformers import AutoTokenizer

            model_id = f"deepseek-ai/deepseek-ocr-{self.config['model_variant']}"
            logger.info(f"Loading tokenizer: {model_id}")

            return AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

        except Exception as e:
            raise ModelLoadError(f"Failed to load tokenizer: {e}")

    def _ensure_initialized(self):
        """Ensure model and tokenizer are loaded"""
        if not self._initialized:
            self.model = self._load_model()
            self.tokenizer = self._load_tokenizer()
            self._initialized = True

    @auto_fallback_decorator
    def infer(
        self,
        image_path: Union[str, Path],
        prompt: str = "<image>\n<|grounding|>Convert the document to markdown.",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run OCR inference on an image.

        Args:
            image_path: Path to the image file
            prompt: Prompt template for the model
            **kwargs: Additional arguments passed to model.infer()

        Returns:
            dict: {
                "markdown": str,
                "raw_output": str,
                "metadata": {
                    "model": str,
                    "device": str,
                    "inference_time_ms": int
                }
            }
        """
        self._ensure_initialized()

        start_time = time.time()

        # Load and preprocess image
        from PIL import Image
        image = Image.open(image_path).convert("RGB")

        # Run inference
        logger.info(f"Running inference on {image_path}")
        output = self.model.infer(
            self.tokenizer,
            image,
            prompt,
            **kwargs
        )

        inference_time = int((time.time() - start_time) * 1000)

        logger.info(f"Inference completed in {inference_time}ms")

        return {
            "markdown": output,
            "raw_output": output,
            "metadata": {
                "model": self.config["model_variant"],
                "device": self.config["device"],
                "inference_time_ms": inference_time
            }
        }
