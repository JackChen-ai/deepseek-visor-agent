"""
Device Manager - Automatic device detection and model selection

Detects optimal configuration based on available hardware:
- CUDA GPUs with memory estimation
- Apple Silicon MPS
- CPU fallback
- FlashAttention availability
"""

import torch
import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DeviceManager:
    """Automatic device detection and optimal configuration selection"""

    @staticmethod
    def detect_optimal_config() -> Dict[str, Any]:
        """
        Detect the optimal configuration based on available hardware.

        Returns:
            dict: Configuration with keys:
                - device: "cuda" | "mps" | "cpu"
                - model_variant: "gundam" | "base" | "tiny"
                - use_flash_attn: bool
                - max_memory_gb: float
        """
        config = {
            "device": "cpu",
            "model_variant": "tiny",
            "use_flash_attn": False,
            "max_memory_gb": 0
        }

        # 1. Check for CUDA
        if torch.cuda.is_available():
            config["device"] = "cuda"
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            config["max_memory_gb"] = gpu_memory

            # Select model variant based on GPU memory
            if gpu_memory >= 48:
                config["model_variant"] = "gundam"
                logger.info(f"Selected Gundam model (GPU memory: {gpu_memory:.1f}GB)")
            elif gpu_memory >= 24:
                config["model_variant"] = "base"
                logger.info(f"Selected Base model (GPU memory: {gpu_memory:.1f}GB)")
            else:
                config["model_variant"] = "tiny"
                logger.info(f"Selected Tiny model (GPU memory: {gpu_memory:.1f}GB)")

            # Check for FlashAttention
            try:
                import flash_attn
                config["use_flash_attn"] = True
                logger.info("FlashAttention detected and enabled")
            except ImportError:
                logger.warning("FlashAttention not available, using standard attention")

        # 2. Check for Apple Silicon MPS
        elif torch.backends.mps.is_available():
            config["device"] = "mps"
            config["model_variant"] = "tiny"  # MPS recommended to use Tiny
            config["max_memory_gb"] = psutil.virtual_memory().available / 1e9
            logger.info(f"Apple MPS detected, using Tiny model (Available memory: {config['max_memory_gb']:.1f}GB)")

        # 3. CPU fallback
        else:
            config["max_memory_gb"] = psutil.virtual_memory().available / 1e9
            logger.info(f"No GPU detected, using CPU with Tiny model (Available memory: {config['max_memory_gb']:.1f}GB)")

        return config

    @staticmethod
    def get_device_info() -> str:
        """Get human-readable device information"""
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            return f"CUDA: {gpu_name} ({gpu_memory:.1f}GB)"
        elif torch.backends.mps.is_available():
            return "Apple Silicon MPS"
        else:
            return "CPU"
