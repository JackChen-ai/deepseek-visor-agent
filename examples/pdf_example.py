"""
Example: Processing PDF documents with DeepSeek Visor Agent

This example demonstrates how to process multi-page PDF documents,
extracting structured data and markdown from each page.

Based on DeepSeek-OCR official PDF processing:
https://github.com/deepseek-ai/DeepSeek-OCR/blob/master/DeepSeek-OCR-vllm/run_dpsk_ocr_pdf.py
"""

from deepseek_visor_agent import VisionDocumentTool
from pathlib import Path


def example_basic_pdf_processing():
    """Process a PDF document and extract markdown"""
    print("=" * 80)
    print("Example 1: Basic PDF Processing")
    print("=" * 80)

    tool = VisionDocumentTool()

    # Process a PDF file (same API as image files)
    result = tool.run("contract.pdf")

    print(f"Document Type: {result['document_type']}")
    print(f"Pages Processed: {result['pages']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"\nMarkdown Output:\n{result['markdown'][:500]}...")

    # Pages are separated by <--- Page Split --->
    print(f"\nNote: Multi-page PDFs have page separators")


def example_pdf_with_page_range():
    """Process only specific pages from a PDF"""
    print("\n" + "=" * 80)
    print("Example 2: Process Specific Pages")
    print("=" * 80)

    tool = VisionDocumentTool()

    # Process only pages 0-2 (first 3 pages)
    result = tool.run(
        "long_contract.pdf",
        pdf_start_page=0,
        pdf_end_page=2
    )

    print(f"Pages Processed: {result['pages']}")
    print(f"Total Inference Time: {result['metadata']['total_inference_time_ms']}ms")
    print(f"Average Time per Page: {result['metadata']['inference_time_ms']}ms")


def example_pdf_invoice_extraction():
    """Extract structured data from a PDF invoice"""
    print("\n" + "=" * 80)
    print("Example 3: Invoice Data Extraction from PDF")
    print("=" * 80)

    tool = VisionDocumentTool()

    # PDF invoices work the same as image invoices
    result = tool.run(
        "invoice_multi_page.pdf",
        document_type="invoice"
    )

    print(f"Pages: {result['pages']}")
    print("\nExtracted Fields:")
    for key, value in result['fields'].items():
        print(f"  {key}: {value}")


def example_pdf_with_custom_dpi():
    """Process PDF with custom DPI for better quality"""
    print("\n" + "=" * 80)
    print("Example 4: Custom DPI for High-Quality Scans")
    print("=" * 80)

    tool = VisionDocumentTool()

    # Higher DPI = better quality but slower processing
    # Default is 144 DPI (same as DeepSeek-OCR official)
    result = tool.run(
        "high_res_document.pdf",
        pdf_dpi=200  # Increase for better quality
    )

    print(f"Processed at {200} DPI")
    print(f"Pages: {result['pages']}")
    print(f"Total Time: {result['metadata']['total_inference_time_ms']}ms")


def example_batch_pdf_processing():
    """Process multiple PDFs in a batch"""
    print("\n" + "=" * 80)
    print("Example 5: Batch PDF Processing")
    print("=" * 80)

    tool = VisionDocumentTool()

    pdf_files = [
        "invoice_001.pdf",
        "invoice_002.pdf",
        "invoice_003.pdf"
    ]

    results = []

    for pdf_file in pdf_files:
        print(f"\nProcessing {pdf_file}...")
        try:
            result = tool.run(pdf_file, document_type="invoice")
            results.append({
                "file": pdf_file,
                "total": result['fields'].get('total', 'N/A'),
                "date": result['fields'].get('date', 'N/A'),
                "pages": result['pages']
            })
        except Exception as e:
            print(f"  Error: {e}")
            continue

    # Print summary
    print("\n" + "-" * 80)
    print("Summary:")
    print("-" * 80)
    for r in results:
        print(f"{r['file']:<20} | Total: {r['total']:<12} | Date: {r['date']:<12} | Pages: {r['pages']}")


def example_save_pdf_pages_as_markdown():
    """Process PDF and save each page as separate markdown files"""
    print("\n" + "=" * 80)
    print("Example 6: Save Each Page as Markdown")
    print("=" * 80)

    from deepseek_visor_agent.utils.pdf_processor import pdf_to_images

    tool = VisionDocumentTool()
    pdf_path = "documentation.pdf"

    # Convert PDF to images first
    images = pdf_to_images(pdf_path)
    print(f"Converted {len(images)} pages")

    # Process each page separately
    output_dir = Path("output_markdown")
    output_dir.mkdir(exist_ok=True)

    for i, image in enumerate(images):
        print(f"Processing page {i + 1}/{len(images)}...")

        # Process the image directly (no file path needed)
        result = tool.run(image, document_type="general", extract_fields=False)

        # Save to markdown file
        md_file = output_dir / f"page_{i + 1:03d}.md"
        md_file.write_text(result['markdown'], encoding='utf-8')
        print(f"  Saved to {md_file}")

    print(f"\nAll pages saved to {output_dir}/")


def example_error_handling():
    """Demonstrate error handling for PDF processing"""
    print("\n" + "=" * 80)
    print("Example 7: Error Handling")
    print("=" * 80)

    from deepseek_visor_agent.utils.pdf_processor import PDFProcessingError

    tool = VisionDocumentTool()

    # Handle file not found
    try:
        result = tool.run("nonexistent.pdf")
    except PDFProcessingError as e:
        print(f"PDF Error: {e}")

    # Handle corrupted PDF
    try:
        result = tool.run("corrupted.pdf")
    except PDFProcessingError as e:
        print(f"PDF Error: {e}")

    # Handle invalid page range
    try:
        result = tool.run("doc.pdf", pdf_start_page=100)
    except PDFProcessingError as e:
        print(f"Page Range Error: {e}")


if __name__ == "__main__":
    print("\nDeepSeek Visor Agent - PDF Processing Examples")
    print("=" * 80)
    print("\nNOTE: These examples require actual PDF files to run.")
    print("Replace the file paths with your own PDFs.\n")

    # Uncomment the examples you want to run:

    # example_basic_pdf_processing()
    # example_pdf_with_page_range()
    # example_pdf_invoice_extraction()
    # example_pdf_with_custom_dpi()
    # example_batch_pdf_processing()
    # example_save_pdf_pages_as_markdown()
    # example_error_handling()

    print("\nTo run an example, uncomment it in the __main__ section.")
