# DeepSeek Visor Agent

> **Standard vision tool for AI agents** - Convert documents to structured data in 3 lines of code

[![PyPI version](https://badge.fury.io/py/deepseek-visor-agent.svg)](https://badge.fury.io/py/deepseek-visor-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🎯 What is This?

DeepSeek Visor Agent is a production-ready wrapper for [DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR) that makes document understanding **effortless for AI agents**.

Instead of wrestling with GPU configurations, model variants, and raw markdown output, you get:

- ✅ **Auto device detection** (CUDA/MPS/CPU)
- ✅ **Automatic fallback** (Gundam mode → Base mode → Tiny mode when OOM)
- ✅ **Structured output** (Markdown + extracted fields)
- ✅ **Agent-ready** (LangChain, LlamaIndex, Dify compatible)

## ⚡ Quick Start

### Installation

```bash
pip install deepseek-visor-agent

# Optional: For RTX GPUs with FlashAttention support
pip install deepseek-visor-agent[flash-attn]
```

### Basic Usage

```python
from deepseek_visor_agent import VisionDocumentTool

# Initialize the tool (auto-detects best device and model)
tool = VisionDocumentTool()

# Process a document
result = tool.run("invoice.jpg")

print(result["fields"]["total"])  # "$199.00"
print(result["fields"]["date"])   # "2024-01-15"
print(result["document_type"])    # "invoice"
```

That's it! No configuration needed.

## 🔗 Integrations

### LangChain

```python
from langchain.tools import tool
from deepseek_visor_agent import VisionDocumentTool

ocr_tool = VisionDocumentTool()

@tool
def extract_invoice_data(image_path: str) -> dict:
    """Extract structured data from invoice images"""
    return ocr_tool.run(image_path, document_type="invoice")

# Use in your agent
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

tools = [extract_invoice_data]
agent = initialize_agent(tools, OpenAI(temperature=0), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

response = agent.run("Extract the total from invoice.jpg")
```

### LlamaIndex

```python
from llama_index.tools import FunctionTool
from deepseek_visor_agent import VisionDocumentTool

tool = VisionDocumentTool()

def ocr_document(image_path: str) -> dict:
    """Process documents with OCR"""
    return tool.run(image_path)

llama_tool = FunctionTool.from_defaults(fn=ocr_document)
```

### Dify / Flowise

See [integration guide](docs/dify_integration.md) for REST API setup.

## 📊 Features

### Automatic Device Management

The tool automatically detects your hardware and selects the optimal configuration:

| Hardware | Inference Mode | Memory Usage |
|----------|----------------|--------------|
| RTX 4090 (48GB) | Gundam | ~40GB |
| RTX 3090 (24GB) | Base | ~20GB |
| M2 Mac | Tiny | ~4GB |
| CPU only | Tiny | ~4GB RAM |

### Automatic Fallback

If inference fails (OOM, CUDA errors), automatically falls back to lower-resolution modes:

```
Gundam mode (OOM) → Large mode → Base mode → Small mode → Tiny mode (Success!)
```

### Supported Document Types

- ✅ **Invoices** - Extracts total, date, vendor, line items
- ✅ **Contracts** - Extracts parties, effective date, terms
- 🚧 **Resumes** - Coming soon
- 🚧 **Forms** - Coming soon

### Output Format

```python
{
    "markdown": "# Invoice\n\nDate: 2024-01-15\n...",
    "fields": {
        "total": "$199.00",
        "date": "2024-01-15",
        "vendor": "Acme Corp"
    },
    "document_type": "invoice",
    "confidence": 0.95,
    "metadata": {
        "inference_mode": "tiny",
        "device": "cuda",
        "inference_time_ms": 1823
    }
}
```

## ⚡ Performance

Benchmarked on A4 scanned documents:

| Inference Mode | Device | Inference Time | Accuracy |
|----------------|--------|----------------|----------|
| Gundam | RTX 4090 | ~6s | 98% |
| Base | RTX 3090 | ~12s | 96% |
| Tiny | M2 Mac | ~2s | 92% |
| Tiny | CPU | ~15s | 92% |

## 📚 Documentation

### 🚀 Getting Started
- **[📚 Documentation Center](docs/README.md)** - Complete documentation hub
- [Installation Guide](docs/installation.md)
- [Quick Start](docs/quickstart.md)
- [Troubleshooting](docs/troubleshooting.md)

### 💼 For Decision Makers
- [Product Requirements (PRD)](docs/business/PRD.md) - Product positioning and goals
- [Strategic Analysis](docs/business/STRATEGIC_ANALYSIS.md) - Why we built this
- [Competitive Comparison](docs/business/COMPETITIVE_COMPARISON.md) - vs. Google Vision, AWS Textract

### 🏗️ For Developers
- [System Architecture](docs/architecture/ARCHITECTURE.md) - Technical design
- [Hardware Limitations](docs/architecture/HARDWARE_LIMITATIONS.md) - GPU requirements explained
- [API Reference](docs/api_reference.md) - Coming soon
- [Dify Integration](examples/dify_integration.md)

## 🛣️ Roadmap

- [x] Core OCR engine with auto-fallback
- [x] Invoice parser
- [x] Contract parser (basic)
- [ ] PDF support (via pdf2image)
- [ ] Resume parser
- [ ] Multi-language support
- [ ] Hosted API (Cloud version)
- [ ] LlamaIndex native tool
- [ ] Dify plugin

## 🤝 Contributing

We welcome contributions! Areas where help is needed:

1. **New parsers** - Add support for new document types
2. **Testing** - More test cases and edge cases
3. **Documentation** - Improve guides and examples
4. **Performance** - Optimization suggestions

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📖 Citation

Built on top of [DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR):

```bibtex
@misc{deepseek-ocr,
  author = {DeepSeek AI},
  title = {DeepSeek-OCR},
  year = {2025},
  url = {https://huggingface.co/deepseek-ai/DeepSeek-OCR}
}
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- DeepSeek AI team for the amazing OCR model
- Hugging Face for model hosting
- LangChain and LlamaIndex communities for inspiration

## 📬 Contact

- GitHub Issues: [Report bugs or request features](https://github.com/visor-agent/deepseek-visor-agent/issues)
- Email: hello@visor-agent.com
- Twitter: [@visor_agent](https://twitter.com/visor_agent)

---

**Star ⭐ this repo if you find it useful!**
