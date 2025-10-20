"""
Error handling utilities with automatic fallback support
"""

from functools import wraps
import logging
import torch

logger = logging.getLogger(__name__)


class OCRError(Exception):
    """Base exception for OCR-related errors"""
    pass


class OOMError(OCRError):
    """Out of memory error"""
    pass


class ModelLoadError(OCRError):
    """Model loading error"""
    pass


class ImageProcessingError(OCRError):
    """Image processing error"""
    pass


def auto_fallback_decorator(func):
    """
    Automatic fallback decorator: Gundam → Base → Tiny → Error

    If a model fails due to OOM or other errors, automatically
    falls back to a smaller model variant.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        variants = ["gundam", "base", "tiny"]
        current_variant = self.config["model_variant"]

        # Start from current model variant
        start_idx = variants.index(current_variant) if current_variant in variants else 0

        for variant in variants[start_idx:]:
            try:
                if variant != current_variant:
                    logger.warning(f"Falling back to {variant} model...")
                    self.config["model_variant"] = variant
                    self.model = self._load_model()

                return func(self, *args, **kwargs)

            except (RuntimeError, torch.cuda.OutOfMemoryError) as e:
                logger.error(f"{variant} model failed: {e}")
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()  # Clear GPU memory
                continue

        raise OCRError("All models failed. Try using CPU mode or reducing image size.")

    return wrapper
