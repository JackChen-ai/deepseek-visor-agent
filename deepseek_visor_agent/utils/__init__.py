"""Utility modules for DeepSeek Visor Agent"""

from .error_handler import (
    OCRError,
    OOMError,
    ModelLoadError,
    ImageProcessingError,
    auto_fallback_decorator
)

__all__ = [
    "OCRError",
    "OOMError",
    "ModelLoadError",
    "ImageProcessingError",
    "auto_fallback_decorator"
]
