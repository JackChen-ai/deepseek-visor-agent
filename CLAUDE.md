# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepSeek Visor Agent is a production-ready wrapper for DeepSeek-OCR that provides automatic device detection, inference mode selection, and structured output for AI agent frameworks (LangChain, LlamaIndex, Dify).

**Critical Architecture Concept**: DeepSeek-OCR is a SINGLE model (`deepseek-ai/DeepSeek-OCR`) with 5 inference modes, NOT multiple model files. The modes (tiny/small/base/large/gundam) control resolution parameters (`base_size`, `image_size`, `crop_mode`), not different model weights.

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

- `ERROR_ANALYSIS_AND_FIXES.md`: Root cause analysis of Day 1 architecture error
- `DAY1_COMPLETION_REPORT.md`: Project initialization summary
- `project_development_plan_v2.md`: 75-day development roadmap

## Naming Conventions

- **PyPI package**: `deepseek-visor-agent` (hyphen)
- **Python module**: `deepseek_visor_agent` (underscore)
- **Import**: `from deepseek_visor_agent import VisionDocumentTool`

## When Making Changes

1. **Verify against official docs**: https://huggingface.co/deepseek-ai/DeepSeek-OCR
2. **Remember**: 1 model + 5 modes, NOT 5 different models
3. **Test inference modes**: Ensure mode params are passed correctly to `model.infer()`
4. **Update tests**: When adding parsers or modes

## Common Pitfalls

- Assuming "Gundam" is a separate model file (it's a dynamic resolution mode)
- Reloading model during fallback (unnecessary and slow)
- Confusing `model_variant` terminology (should be `inference_mode`)
- Using incorrect HuggingFace model paths

See `ERROR_ANALYSIS_AND_FIXES.md` for detailed explanation of the architecture.
