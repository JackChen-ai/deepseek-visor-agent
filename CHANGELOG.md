# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-10-21

### Added
- **PDF file support**: Automatically convert PDF pages to images using PyMuPDF
  - Support for multi-page PDFs with automatic page splitting
  - Configurable DPI (default: 144)
  - Page range selection (`pdf_start_page`, `pdf_end_page`)
  - Automatic RGBA to RGB conversion
  - Example code in `examples/pdf_example.py`
- **Complete user journey documentation**: 4 real-world scenarios with code examples
  - Standalone Python scripts (invoice batch processing)
  - LangChain AI agents (document Q&A chatbot)
  - Batch PDF processing (contract analysis)
  - REST API integration (Dify/Flowise)
- **Comprehensive unit tests**: 26/26 tests passing (100%)
  - InvoiceParser: 10 test methods
  - ContractParser: 9 test methods
  - DocumentClassifier: 6 test methods
  - PDF processor tests with PyMuPDF availability detection

### Fixed
- **Parser accuracy improvements**:
  - Grand Total vs Subtotal: Fixed regex to prioritize "Grand Total" over "Subtotal"
  - Vendor extraction: Only remove "Corp." (with period), keep "Corp" intact
  - Vendor fallback: Added invoice context check to prevent false extractions
  - Contract parties: More flexible regex patterns with MULTILINE support
  - Effective date: Support "shall commence on [date]" format
  - Governing law: Handle complex legal phrasing
- **CI/CD compatibility**:
  - Added `_pymupdf_available()` helper to skip PDF tests when PyMuPDF not installed
  - Lowered matplotlib requirement to >=3.5.0 for Python 3.9 compatibility
  - All tests pass on GitHub Actions (Python 3.9, 3.10, 3.11)

### Changed
- **Dependencies**: Added PyMuPDF>=1.23.0 and matplotlib>=3.5.0 to core dependencies
- **Documentation**: Restructured README.md with detailed installation steps and prerequisites

## [0.1.0] - 2025-10-20

### Added
- Initial release of DeepSeek Visor Agent
- Core OCR functionality with DeepSeek-OCR model
- Automatic device detection (CUDA, MPS, CPU)
- Automatic fallback mechanism (Gundam → Base → Tiny modes)
- Document type classification (invoice, contract, resume)
- Structured field extraction:
  - InvoiceParser: total, date, vendor, invoice_number
  - ContractParser: parties, effective_date, contract_type, term, governing_law
- LangChain integration example
- LlamaIndex integration example
- Dify integration guide
- Apache 2.0 License
- PyPI package publication

[0.2.0]: https://github.com/JackChen-ai/deepseek-visor-agent/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/JackChen-ai/deepseek-visor-agent/releases/tag/v0.1.0
