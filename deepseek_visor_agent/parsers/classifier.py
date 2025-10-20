"""
Document Classifier - Identify document type from markdown content
"""

import re
from typing import Literal

DocumentType = Literal["invoice", "contract", "resume", "general"]


def classify_document(markdown: str) -> DocumentType:
    """
    Classify document type based on content analysis.

    Args:
        markdown: OCR output in markdown format

    Returns:
        str: Document type ("invoice" | "contract" | "resume" | "general")
    """
    text_lower = markdown.lower()

    # Invoice indicators
    invoice_keywords = ["invoice", "receipt", "total", "amount", "payment", "bill", "due"]
    invoice_score = sum(1 for kw in invoice_keywords if kw in text_lower)

    # Contract indicators
    contract_keywords = ["agreement", "contract", "party", "parties", "terms", "conditions", "effective date"]
    contract_score = sum(1 for kw in contract_keywords if kw in text_lower)

    # Resume indicators
    resume_keywords = ["experience", "education", "skills", "resume", "cv", "curriculum vitae"]
    resume_score = sum(1 for kw in resume_keywords if kw in text_lower)

    # Check for currency symbols (strong invoice indicator)
    if re.search(r'\$\s*\d+|\d+\.\d{2}', markdown):
        invoice_score += 2

    # Determine document type based on scores
    scores = {
        "invoice": invoice_score,
        "contract": contract_score,
        "resume": resume_score
    }

    max_score = max(scores.values())
    if max_score >= 2:  # Minimum confidence threshold
        return max(scores, key=scores.get)

    return "general"
