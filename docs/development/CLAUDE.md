# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepSeek Visor Agent is a production-ready wrapper for DeepSeek-OCR that provides automatic device detection, inference mode selection, and structured output for AI agent frameworks (LangChain, LlamaIndex, Dify).

**Critical Architecture Concept**: DeepSeek-OCR is a SINGLE model (`deepseek-ai/DeepSeek-OCR`) with 5 inference modes, NOT multiple model files. The modes (tiny/small/base/large/gundam) control resolution parameters (`base_size`, `image_size`, `crop_mode`), not different model weights.

### ✅ Verified Architecture Facts (2025-10-21)

**Based on complete source code verification**:
- ✅ **All 5 modes are fully open-sourced** via `model.infer()` parameters
- ✅ **GitHub repo contains complete code**:
  - HuggingFace version: `DeepSeek-OCR-master/DeepSeek-OCR-hf/`
  - vLLM optimized version: `DeepSeek-OCR-master/DeepSeek-OCR-vllm/`
- ✅ **`crop_mode` parameter exists** in source code (Gundam mode is production-ready)
- ✅ **vLLM support is fully open-sourced** with 2500 tokens/s throughput capability

**Official References**:
- GitHub: `https://github.com/deepseek-ai/DeepSeek-OCR`
- Official Example: `DeepSeek-OCR-master/DeepSeek-OCR-hf/run_dpsk_ocr.py`
- Architecture Analysis: `/docs/architecture/DEEPSEEK_OCR_ADVANTAGES.md`

## Development Commands

### Installation
```bash
# Development installation
pip install -e .
pip install -r requirements-dev.txt

# IMPORTANT: transformers version must be 4.46.3 for compatibility
pip install 'transformers==4.46.3' 'tokenizers>=0.20.0,<0.21.0'

# With optional dependencies
pip install -e ".[flash-attn]"  # For FlashAttention support
pip install -e ".[all]"         # All optional dependencies
```

### Version Compatibility (CRITICAL)

**transformers 版本要求**：必须使用 `4.46.3`

- ✅ **4.46.3**：经过验证，模型加载正常
- ❌ **4.51.x**：LlamaFlashAttention2 导入错误
- ❌ **4.57.x**：LlamaFlashAttention2 导入错误

**模型下载**：
- 位置：`~/.cache/huggingface/hub/models--deepseek-ai--DeepSeek-OCR/`
- 大小：6.2 GB
- 首次加载约需 3-5 分钟（下载）+ 46 秒（加载）

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_device_manager.py -v

# Run with coverage
pytest tests/ -v --cov=deepseek_visor_agent --cov-report=xml

# Run single test
pytest tests/test_device_manager.py::test_device_detection -v
```

### Code Quality
```bash
# Format code
black deepseek_visor_agent/ tests/

# Lint
ruff check deepseek_visor_agent/ tests/

# Type checking
mypy deepseek_visor_agent/
```

### Building
```bash
# Build package
python -m build

# Install locally for testing
pip install -e .
```

## Architecture

### Core Inference Flow

1. **Device Detection** (`device_manager.py`):
   - Detects CUDA/MPS/CPU
   - Selects inference mode based on GPU VRAM
   - Returns config with `inference_mode` (NOT `model_variant`)

2. **Model Loading** (`infer.py`):
   - Loads model ONCE: `MODEL_ID = "deepseek-ai/DeepSeek-OCR"`
   - Model is cached, never reloaded
   - Inference parameters change per mode via `_get_mode_params()`

3. **Auto Fallback** (`utils/error_handler.py`):
   - On OOM: gundam → large → base → small → tiny
   - Only changes `config["inference_mode"]`
   - Does NOT reload model (critical fix from Day 1)

4. **Document Processing** (`tool.py`):
   - `VisionDocumentTool(inference_mode="auto")` is main API
   - Calls inference engine → classifier → parser
   - Returns structured dict with markdown + extracted fields

### Inference Modes (NOT Models)

```python
INFERENCE_MODES = {
    "tiny":   {"base_size": 512,  "image_size": 512,  "crop_mode": False, "min_vram_gb": 4},
    "small":  {"base_size": 640,  "image_size": 640,  "crop_mode": False, "min_vram_gb": 8},
    "base":   {"base_size": 1024, "image_size": 1024, "crop_mode": False, "min_vram_gb": 16},
    "large":  {"base_size": 1280, "image_size": 1280, "crop_mode": False, "min_vram_gb": 24},
    "gundam": {"base_size": 1024, "image_size": 640,  "crop_mode": True,  "min_vram_gb": 48}
}
```

These are passed to `model.infer()` as parameters, NOT used to select different model files.

### Parser System

- `BaseParser` (abstract): Defines interface for document parsers
- `InvoiceParser`: Extracts total/date/vendor from invoices (regex-based)
- `ContractParser`: Placeholder for contract extraction
- `classify_document()`: Auto-detects document type from markdown

## Critical Fixes from Day 1

**DO NOT**:
- Use `f"deepseek-ai/deepseek-ocr-{mode}"` - this model path doesn't exist
- Call `self._load_model()` in fallback - model is already loaded
- Use `model_variant` anywhere - correct term is `inference_mode`

**Correct Pattern**:
```python
# ✅ Correct: Single model, parameterized inference
MODEL_ID = "deepseek-ai/DeepSeek-OCR"
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

mode_params = INFERENCE_MODES[config["inference_mode"]]
output = model.infer(
    tokenizer, image, prompt,
    base_size=mode_params["base_size"],
    image_size=mode_params["image_size"],
    crop_mode=mode_params["crop_mode"]
)
```

## Key Files

- `device_manager.py`: Hardware detection + mode selection (INFERENCE_MODES dict)
- `infer.py`: Single model loading + parameterized inference
- `tool.py`: Main API (`VisionDocumentTool`)
- `utils/error_handler.py`: Auto-fallback decorator (mode switching only)
- `parsers/`: Document-specific field extraction

## Integration Examples

Located in `examples/`:
- `langchain_example.py`: LangChain `@tool` integration
- `llamaindex_example.py`: LlamaIndex `FunctionTool` integration
- `dify_integration.md`: REST API setup for Dify/Flowise

## Documentation Files

**Architecture & Business**:
- `/docs/architecture/DEEPSEEK_OCR_ADVANTAGES.md`: **✅ Complete architecture analysis with source code verification**
  - All 5 modes verified as open-sourced
  - Official code examples and usage patterns
  - Performance benchmarks from paper (Fox Benchmark, OmniDocBench)
- `/docs/business/PRD.md`: **Product Requirements Document (verified feasible)**
  - All features can be implemented with open-source code
  - Commercial strategy: Open SDK + Hosted API + Data generation service
  - Target: AI Agent developers, Low-code platforms, AI companies

**Development**:
- `DAY1_REPORT.md`: Day 1 progress - device detection, basic inference
- `DAY2_REPORT.md`: Day 2 progress - parser system, error handling
- `CLAUDE.md` (this file): Development guide for Claude Code

## Naming Conventions

- **PyPI package**: `deepseek-visor-agent` (hyphen)
- **Python module**: `deepseek_visor_agent` (underscore)
- **Import**: `from deepseek_visor_agent import VisionDocumentTool`

## When Making Changes

1. **Verify against official code**:
   - GitHub: `https://github.com/deepseek-ai/DeepSeek-OCR`
   - Official example: `run_dpsk_ocr.py` shows all 5 modes usage
2. **Remember**: 1 model + 5 modes, NOT 5 different models
3. **Test inference modes**: Ensure mode params are passed correctly to `model.infer()`
4. **Update tests**: When adding parsers or modes
5. **Reference architecture docs**: `/docs/architecture/DEEPSEEK_OCR_ADVANTAGES.md` contains verified technical details

## Common Pitfalls

❌ **WRONG**: Assuming "Gundam" is a separate model file
✅ **CORRECT**: Gundam is a dynamic resolution mode (`crop_mode=True`)

❌ **WRONG**: Reloading model during fallback
✅ **CORRECT**: Only change `config["inference_mode"]`, model stays loaded

❌ **WRONG**: Using `model_variant` terminology
✅ **CORRECT**: Use `inference_mode` consistently

❌ **WRONG**: Assuming modes are "experimental" or "not open-sourced"
✅ **CORRECT**: All 5 modes are production-ready and fully open-sourced (verified 2025-10-21)

❌ **WRONG**: Using incorrect HuggingFace paths like `deepseek-ai/deepseek-ocr-{mode}`
✅ **CORRECT**: Single model path `deepseek-ai/DeepSeek-OCR` with mode parameters
