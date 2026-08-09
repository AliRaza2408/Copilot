import re

REQ_KEYWORDS = [
    "product requirement", "mandatory requirement", "technical specification",
    "product specification", "must have", "must not exceed", "maximum acceptable",
    "minimum quality", "shall be", "must be"
]

SUPPLIER_HEADER_PATTERNS = [
    r"supplier\s*name\s*[:=]",
    r"company\s*name\s*[:=]",
    r"supplier\s*profile\s*[:=]",
    r"^supplier\s+[a-z0-9]",
    r"^company\s*[:=]",
]

COMMERCIAL_FIELDS = [
    "moq", "minimum order quantity", "lead time", "unit price",
    "incoterm", "payment terms", "quality score"
]

POLICY_KEYWORDS = [
    "manual", "policy", "procedure", "appendix", "definition",
    "revision", "controlled", "confidential and proprietary",
    "document number", "release date", "standards", "supplier quality",
    "quality system", "this document", "purpose", "scope", "table of contents"
]


def _looks_like_supplier_profile(text_lower: str) -> bool:
    has_name = any(re.search(p, text_lower) for p in SUPPLIER_HEADER_PATTERNS)
    if not has_name:
        # Tabular (CSV/XLSX) layout: "Field: Supplier Name" / "Value: X"
        has_name = bool(re.search(r"supplier\s*name", text_lower)) and bool(re.search(r"\bvalue\b", text_lower))
    if not has_name:
        return False
    numeric_fields = sum(1 for k in COMMERCIAL_FIELDS if k in text_lower)
    return numeric_fields >= 1


def _looks_like_requirements(text_lower: str) -> bool:
    return any(k in text_lower for k in REQ_KEYWORDS)


def _looks_like_quotation(text_lower: str) -> bool:
    hits = sum(1 for k in ["quotation", "unit price", "incoterm", "payment terms", "valid until", "quote"] if k in text_lower)
    return hits >= 2


def _looks_like_quality_report(text_lower: str) -> bool:
    hits = sum(1 for k in ["quality report", "defect rate", "quality score", "inspection report", "ppm"] if k in text_lower)
    return hits >= 2


def classify_document(text: str) -> str:
    """Classify a document into a processing bucket.

    Returns one of:
      "product_requirements" - a requirements/specification document
      "supplier_profile"    - a supplier profile / quotation with commercial fields
      "quotation"           - a quotation / pricing document
      "quality_report"      - a quality / inspection report
      "policy_document"     - a standards/policy/manual (no concrete supplier data)
      "unknown"             - could not be confidently classified
    """
    text_lower = text.lower()
    word_count = len(text.split())

    # Long, structured documents (manuals, policy, standards) are not supplier
    # profiles even if they mention "supplier" / "quality" / "PPAP" keywords.
    policy_hits = sum(1 for k in POLICY_KEYWORDS if k in text_lower)
    if word_count > 1500 or policy_hits >= 3:
        # A very long strongly-typed supplier quote is vanishingly rare; still
        # allow it if it has an explicit supplier header + commercial fields.
        if _looks_like_supplier_profile(text_lower):
            return "supplier_profile"
        return "policy_document"

    if _looks_like_supplier_profile(text_lower):
        return "supplier_profile"

    if _looks_like_requirements(text_lower):
        return "product_requirements"

    if _looks_like_quotation(text_lower):
        return "quotation"

    if _looks_like_quality_report(text_lower):
        return "quality_report"

    return "unknown"
