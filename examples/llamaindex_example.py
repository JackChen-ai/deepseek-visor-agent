"""
LlamaIndex Integration Example

Shows how to use DeepSeek Visor Agent with LlamaIndex.
"""

from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from deepseek_visor_agent import VisionDocumentTool

# Initialize the OCR tool
ocr_tool = VisionDocumentTool()


def process_document(image_path: str) -> str:
    """
    Process a document with OCR and return structured data.

    Args:
        image_path: Path to the document image

    Returns:
        str: JSON string with extracted data
    """
    import json
    result = ocr_tool.run(image_path)
    return json.dumps(result, indent=2)


def extract_invoice_fields(image_path: str) -> str:
    """
    Extract specific fields from an invoice.

    Args:
        image_path: Path to the invoice image

    Returns:
        str: Formatted string with invoice fields
    """
    result = ocr_tool.run(image_path, document_type="invoice")
    fields = result.get("fields", {})

    return f"""
Invoice Details:
- Total: {fields.get('total', 'N/A')}
- Date: {fields.get('date', 'N/A')}
- Vendor: {fields.get('vendor', 'N/A')}
    """.strip()


def main():
    """Example usage with LlamaIndex agent"""

    # Create LlamaIndex tools
    document_tool = FunctionTool.from_defaults(
        fn=process_document,
        name="process_document",
        description="Process any document with OCR to extract structured data"
    )

    invoice_tool = FunctionTool.from_defaults(
        fn=extract_invoice_fields,
        name="extract_invoice",
        description="Extract specific fields from invoices (total, date, vendor)"
    )

    # Create ReAct agent
    llm = OpenAI(model="gpt-4", temperature=0)

    agent = ReActAgent.from_tools(
        [document_tool, invoice_tool],
        llm=llm,
        verbose=True
    )

    # Example 1: Process document
    print("\n=== Example 1: General Document Processing ===")
    response = agent.chat("Process the document at sample_invoice.jpg and tell me what you find")
    print(response)

    # Example 2: Specific invoice extraction
    print("\n=== Example 2: Invoice Field Extraction ===")
    response = agent.chat("Extract the invoice details from invoice_001.jpg")
    print(response)

    # Example 3: Comparison
    print("\n=== Example 3: Document Comparison ===")
    response = agent.chat(
        "Compare the totals from invoice_001.jpg and invoice_002.jpg. Which one is higher?"
    )
    print(response)


if __name__ == "__main__":
    main()
