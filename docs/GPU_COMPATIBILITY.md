# GPU Compatibility Guide

**Critical Reference for DeepSeek-OCR Hardware Requirements**

---

## ⚠️ FlashAttention 2.x Compute Capability Requirements

DeepSeek-OCR requires [FlashAttention 2.x](https://github.com/Dao-AILab/flash-attention), which **only supports NVIDIA GPUs with compute capability 7.5 or higher** (Turing architecture and newer).

### Compute Capability Table

| GPU Architecture | Compute Capability | FlashAttention 2.x | Examples |
|------------------|-------------------|-------------------|----------|
| **Ada Lovelace** | sm_89 | ✅ **Supported** | RTX 4090, RTX 4080, RTX 4070 Ti |
| **Ampere** | sm_80, sm_86 | ✅ **Supported** | RTX 3090, RTX 3080, RTX 3070, A100, A10 |
| **Turing** | sm_75 | ✅ **Supported** | RTX 2080 Ti, RTX 2070, RTX 2060, Tesla T4 |
| **Volta** | sm_70, sm_72 | ❌ **Not Supported** | Tesla V100, Titan V |
| **Pascal** | sm_60, sm_61 | ❌ **Not Supported** | GTX 1080 Ti, GTX 1070, GTX 1660, Titan Xp |
| **Maxwell** | sm_50, sm_52 | ❌ **Not Supported** | GTX 980, GTX 970 |

**Reference**: [NVIDIA CUDA GPU Compute Capabilities](https://developer.nvidia.com/cuda-gpus)

---

## Supported GPU Configurations

### Consumer GPUs (Desktop)

| GPU Model | VRAM | Recommended Mode | Price (USD, approx) | Notes |
|-----------|------|------------------|---------------------|-------|
| **RTX 4090** | 24GB | Gundam | $1,599 | Best for production workloads |
| **RTX 4080** | 16GB | Large | $1,199 | High-end consumer option |
| **RTX 3090** | 24GB | Large | $1,499 (used ~$800) | Best value for 24GB VRAM |
| **RTX 3080** | 10GB | Base | $699 (used ~$500) | Good for standard documents |
| **RTX 3070** | 8GB | Small | $499 (used ~$350) | Entry-level production |
| **RTX 2060** | 6GB | Tiny/Small | $329 (used ~$150) | **Minimum requirement** |

### Enterprise/Data Center GPUs

| GPU Model | VRAM | Recommended Mode | Cloud Cost (/hr) | Notes |
|-----------|------|------------------|------------------|-------|
| **A100-80GB** | 80GB | Gundam | ~$3.00 | Best for large-scale processing |
| **A100-40GB** | 40GB | Gundam | ~$1.50 | Production-ready |
| **A10** | 24GB | Large | ~$0.80 | Cost-effective cloud option |
| **Tesla T4** | 16GB | Base | ~$0.40 | Budget cloud GPU |

---

## Cloud GPU Rental Services

### Recommended Platforms

#### 1. **RunPod** (Recommended for Development)
- **Pricing**: RTX 3090 @ $0.20/hr, RTX 4090 @ $0.40/hr
- **Pros**: Simple setup, Jupyter notebook support, Docker templates
- **Cons**: Popular GPUs often out of stock
- **Best For**: Development, testing, short-term rentals
- **Sign Up**: [runpod.io](https://runpod.io)

#### 2. **Vast.ai** (Best Value)
- **Pricing**: RTX 3090 @ $0.15-0.30/hr (varies by availability)
- **Pros**: Competitive marketplace pricing, many GPU options
- **Cons**: Quality varies by host, setup more complex
- **Best For**: Cost-conscious production workloads
- **Sign Up**: [vast.ai](https://vast.ai)

#### 3. **Lambda Labs** (Best for Stability)
- **Pricing**: A100-40GB @ $1.10/hr, A10 @ $0.60/hr
- **Pros**: Reliable infrastructure, enterprise-grade support
- **Cons**: Higher pricing, requires minimum commitment
- **Best For**: Production deployments, enterprise use
- **Sign Up**: [lambdalabs.com/service/gpu-cloud](https://lambdalabs.com/service/gpu-cloud)

#### 4. **Google Colab Pro** (Quick Testing)
- **Pricing**: $9.99/month (limited GPU hours)
- **Pros**: No setup required, Jupyter notebook ready
- **Cons**: Session limits, GPU type not guaranteed
- **Best For**: Quick experiments, learning
- **Sign Up**: [colab.research.google.com](https://colab.research.google.com)

---

## Unsupported Hardware

### ❌ Pascal Architecture GPUs (GTX 10 Series)

**Why Not Supported**: FlashAttention 2.x requires `sm_75` (Turing), Pascal is `sm_60/61`.

**Common Models**:
- GTX 1080 Ti (11GB VRAM) - ❌ **Will NOT work**
- GTX 1080 (8GB VRAM) - ❌ **Will NOT work**
- GTX 1070 (8GB VRAM) - ❌ **Will NOT work**
- GTX 1660 Ti (6GB VRAM) - ❌ **Will NOT work**
- GTX 1060 (6GB VRAM) - ❌ **Will NOT work**

**Error You'll See**:
```
RuntimeError: FlashAttention only supports Turing, Ampere, Ada, or Hopper GPUs
```

### ❌ CPU-Only Mode

**Why Not Supported**: DeepSeek-OCR model code contains hardcoded CUDA operations.

**Workaround**: Hosted API planned for future release (no GPU required).

### ❌ AMD GPUs (ROCm)

**Status**: Untested. FlashAttention has experimental ROCm support, but compatibility not verified.

**Recommendation**: Use NVIDIA GPUs or wait for official ROCm support.

### ❌ Apple Silicon (M1/M2/M3)

**Status**: MPS backend may work for tiny models, but:
- FlashAttention not available on MPS
- Performance significantly slower than CUDA
- Large documents likely to fail

**Recommendation**: Use cloud GPU rental for production workloads.

---

## Installation Requirements

### CUDA Toolkit Version

```bash
# Check your CUDA version
nvidia-smi

# Required: CUDA 11.8 or 12.1+
# Recommended: CUDA 12.1
```

### FlashAttention 2.x Installation

```bash
# Install FlashAttention (requires compatible GPU)
pip install flash-attn==2.7.3 --no-build-isolation

# If installation fails, check:
# 1. CUDA version (11.8+ required)
# 2. GPU compute capability (sm_75+ required)
# 3. GCC version (7.5+ required)
```

**Common Installation Errors**:

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `CUDA_HOME environment variable is not set` | CUDA not installed/detected | Install CUDA Toolkit, set `CUDA_HOME=/usr/local/cuda` |
| `unsupported GNU version` | GCC version too old | Update GCC to 7.5+ |
| `architecture 'compute_60' not supported` | Pascal GPU detected | Upgrade to Turing+ GPU (RTX 2060+) |

---

## Performance Benchmarks by GPU

### Tesla T4 (16GB) - Verified Results ✅

**Test Environment**: Aliyun Cloud (ecs.gn6i-c16g1.4xlarge)
**Test Date**: 2025-10-21

| Inference Mode | Processing Time (per page) | VRAM Usage | Status |
|----------------|---------------------------|------------|--------|
| Tiny | 5.35s | ~3GB | ✅ Tested |
| Small | 6.53s | ~4GB | ✅ Tested |
| Base | 6.77s | ~6GB | ✅ Tested |
| Large | 6.35s | ~8GB | ✅ Tested |
| Gundam | 6.67s | ~10GB | ✅ Tested |

**Note**: Other GPU models have not been tested yet. Performance will vary based on architecture and VRAM. See [README.md](../README.md#-performance) for full test results.

---

## Troubleshooting

### Error: "FlashAttention only supports Turing, Ampere, Ada, or Hopper GPUs"

**Cause**: Your GPU architecture is Pascal (GTX 10 series) or older.

**Solution**:
1. Check GPU compute capability: `nvidia-smi --query-gpu=compute_cap --format=csv`
2. If output is `6.0` or `6.1` (Pascal), upgrade to RTX 2060+ or use cloud GPU
3. Alternatively, wait for our hosted API (no GPU required)

### Error: "CUDA out of memory"

**Cause**: Selected inference mode requires more VRAM than available.

**Solution**:
1. The tool will automatically fallback to lower modes (Gundam → Large → Base → Small → Tiny)
2. Manually specify a lower mode: `tool.run(image_path, inference_mode="small")`
3. Reduce batch size if processing multiple documents
4. Close other GPU-intensive applications

### Error: "RuntimeError: Expected all tensors to be on the same device"

**Cause**: Mixed CPU/GPU tensor placement.

**Solution**:
```python
# Ensure device is properly set
import torch
print(torch.cuda.is_available())  # Should be True
print(torch.cuda.get_device_name(0))  # Should show your GPU

# Reinstall with CUDA support
pip uninstall torch transformers
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install transformers==4.46.3
```

---

## Migration Guide for GTX 1080 Ti Users

If you previously planned to use GTX 1080 Ti based on outdated documentation:

### Option 1: Cloud GPU Rental (Recommended)
- **Cost**: ~$5/month for development (RunPod, 25 hours @ $0.20/hr)
- **Setup Time**: 15 minutes
- **Best For**: Occasional use, prototyping

### Option 2: GPU Upgrade
- **RTX 3070 (8GB)**: $350 used, good for Base mode
- **RTX 3090 (24GB)**: $800 used, best value for Gundam mode
- **Best For**: Frequent use, local development

### Option 3: Hosted API (Coming Soon)
- **Cost**: $0.01/page or $29/month unlimited
- **Setup Time**: Instant (API key)
- **Best For**: Production applications, no hardware management

---

## Verification Checklist

Before starting development, verify your hardware compatibility:

- [ ] GPU is NVIDIA (not AMD/Intel/Apple)
- [ ] GPU architecture is Turing, Ampere, or Ada (check [nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus))
- [ ] GPU has minimum 6GB VRAM (8GB+ recommended)
- [ ] CUDA Toolkit 11.8+ installed
- [ ] `nvidia-smi` command works
- [ ] FlashAttention 2.x installed successfully (`pip list | grep flash`)

**Quick Test**:
```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}'); print(f'Compute: {torch.cuda.get_device_capability(0) if torch.cuda.is_available() else \"N/A\"}')"
```

**Expected Output** (example with RTX 3090):
```
CUDA: True
GPU: NVIDIA GeForce RTX 3090
Compute: (8, 6)
```

If compute capability is `(7, 5)` or higher, you're ready to go!

---

## Getting Help

- **GPU Compatibility Questions**: [GitHub Issues](https://github.com/JackChen-ai/deepseek-visor-agent/issues)
- **Performance Benchmarks**: See [README.md](../README.md#-performance) for verified test results
- **FlashAttention Installation**: [Official Docs](https://github.com/Dao-AILab/flash-attention)
- **No Compatible GPU?**: Hosted API planned for future release

---

**Last Updated**: 2025-10-21
**Verification Status**: ✅ Compute capability requirements verified via [FlashAttention GitHub](https://github.com/Dao-AILab/flash-attention/blob/main/setup.py#L238)
