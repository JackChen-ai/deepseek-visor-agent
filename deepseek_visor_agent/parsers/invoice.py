"""
Invoice Parser - Extract structured data from invoice documents
"""

import re
from typing import Dict, Any
from .base import BaseParser


class InvoiceParser(BaseParser):
    """Parser for extracting invoice fields from markdown"""

    def parse(self, markdown: str) -> Dict[str, Any]:
        """
        Extract invoice fields from markdown.

        Args:
            markdown: OCR output in markdown format

        Returns:
            dict: Extracted fields including total, date, vendor, items
        """
        fields = {
            "total": self._extract_total(markdown),
            "date": self._extract_date(markdown),
            "vendor": self._extract_vendor(markdown),
            "items": self._extract_items(markdown)
        }

        return fields

    def _extract_total(self, text: str) -> str:
        """Extract total amount from text"""
        # Pattern: $XXX.XX or Total: $XXX.XX
        patterns = [
            r"Total[:\s]+\$?([\d,]+\.?\d*)",
            r"Amount[:\s]+\$?([\d,]+\.?\d*)",
            r"\$\s*([\d,]+\.\d{2})"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"${match.group(1)}"

        return ""

    def _extract_date(self, text: str) -> str:
        """Extract date from text"""
        # Pattern: YYYY-MM-DD, MM/DD/YYYY, etc.
        patterns = [
            r"Date[:\s]+(\d{4}-\d{2}-\d{2})",
            r"Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
            r"(\d{4}-\d{2}-\d{2})",
            r"(\d{1,2}/\d{1,2}/\d{4})"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return ""

    def _extract_vendor(self, text: str) -> str:
        """Extract vendor name from text"""
        # Usually the first line or after "From:"
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and not any(kw in line.lower() for kw in ['invoice', 'receipt', 'date', 'total']):
                return line

        return ""

    def _extract_items(self, text: str) -> list:
        """Extract line items from text (placeholder implementation)"""
        # TODO: Implement line item extraction
        return []

    def get_fields_schema(self) -> Dict[str, Any]:
        """Get JSON schema for invoice fields"""
        return {
            "type": "object",
            "properties": {
                "total": {"type": "string", "description": "Total amount"},
                "date": {"type": "string", "description": "Invoice date"},
                "vendor": {"type": "string", "description": "Vendor name"},
                "items": {"type": "array", "description": "Line items"}
            }
        }
