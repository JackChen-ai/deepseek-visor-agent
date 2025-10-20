"""
LangChain Integration Example

Shows how to use DeepSeek Visor Agent as a LangChain tool.
"""

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from deepseek_visor_agent import VisionDocumentTool

# Initialize the OCR tool
ocr_tool = VisionDocumentTool()


@tool
def extract_invoice_data(image_path: str) -> dict:
    """
    Extract structured data from invoice images.

    Args:
        image_path: Path to the invoice image file

    Returns:
        dict: Extracted invoice fields including total, date, vendor
    """
    return ocr_tool.run(image_path, document_type="invoice")


@tool
def extract_contract_data(image_path: str) -> dict:
    """
    Extract structured data from contract documents.

    Args:
        image_path: Path to the contract image file

    Returns:
        dict: Extracted contract fields including parties, effective date
    """
    return ocr_tool.run(image_path, document_type="contract")


@tool
def analyze_document(image_path: str) -> dict:
    """
    Auto-detect document type and extract relevant data.

    Args:
        image_path: Path to the document image file

    Returns:
        dict: Document type and extracted fields
    """
    return ocr_tool.run(image_path, document_type="auto")


def main():
    """Example usage with LangChain agent"""

    # Create agent with OCR tools
    tools = [extract_invoice_data, extract_contract_data, analyze_document]

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Example 1: Extract invoice data
    print("\n=== Example 1: Invoice Extraction ===")
    response = agent.run(
        "Extract the total amount and date from the invoice at invoice_sample.jpg"
    )
    print(response)

    # Example 2: Auto-detect document type
    print("\n=== Example 2: Auto-detect Document ===")
    response = agent.run(
        "What type of document is document.jpg and what information can you extract?"
    )
    print(response)

    # Example 3: Process multiple documents
    print("\n=== Example 3: Batch Processing ===")
    response = agent.run(
        "Process all invoices in the invoices/ folder and calculate the total amount"
    )
    print(response)


if __name__ == "__main__":
    main()
