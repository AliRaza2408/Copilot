import re
from difflib import SequenceMatcher

# Fields we try to ground against the source text, with the keywords that give
# numeric fields their context (so "25" alone doesn't count — it must sit near
# a "lead time"/"days" style keyword).
NUMERIC_CONTEXT = {
    "moq": ["moq", "minimum order", "min order", "order quantity"],
    "lead_time_days": ["lead time", "delivery", "days", "lead-time"],
    "quality_score": ["quality", "score", "%", "rating"],
}

_NAME_PREFIXES = [
    "company name:", "supplier name:", "supplier:", "company:", "name:",
]


def _normalize(value) -> str:
    """Lowercase, strip punctuation/extra whitespace for substring matching."""
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def _strip_name_prefix(raw: str) -> str:
    name = str(raw).strip()
    for prefix in _NAME_PREFIXES:
        if name.lower().startswith(prefix):
            name = name[len(prefix):].strip()
    return name


def string_grounded(value, source_text: str, threshold: float = 0.8) -> bool:
    """Check a string/keyword value appears in the source text (fuzzy).

    Tolerates minor formatting/case differences via normalization and a token
    overlap fallback (e.g. "ISO9001" vs "ISO 9001").
    """
    if value is None:
        return True
    target = _normalize(value)
    if not target:
        return True
    source = _normalize(source_text)

    if target in source:
        return True

    # Token overlap fallback for minor variations
    target_tokens = target.split()
    if not target_tokens:
        return True
    matched = sum(1 for t in target_tokens if t in source)
    return (matched / len(target_tokens)) >= threshold


def number_in_context(value, source_text: str, context_keywords: list[str]) -> bool:
    """Check a numeric value appears in the source text near a context keyword."""
    if value is None:
        return True
    # Extract the leading number from the extracted value ("500 units" -> 500)
    num_match = re.search(r"[-+]?\d[\d,.]*", str(value))
    if not num_match:
        return False
    num = num_match.group(0).replace(",", "")
    source_lower = source_text.lower()

    for kw in context_keywords:
        for m in re.finditer(re.escape(kw), source_lower):
            window = source_lower[max(0, m.start() - 120): m.end() + 120]
            if num in re.sub(r"[^0-9]", "", window) or num in window:
                return True
            # Number may have commas/dots in source
            if any(n in window for n in re.findall(rf"{re.escape(num)}[.,]?\d*", window)):
                return True
    return False


def validate_supplier_extraction(supplier, evidence_text: str) -> dict:
    """Ground every extracted supplier field against the actual source text.

    Returns a per-field verification map:
        {"name": "VERIFIED", "moq": "UNVERIFIED", ...}
    Values are one of VERIFIED / UNVERIFIED. Fields that were not extracted
    (None/empty) are omitted so downstream only reports real claims.
    """
    result = {}

    name = _strip_name_prefix(getattr(supplier, "name", None) or "")
    if name:
        result["name"] = "VERIFIED" if string_grounded(name, evidence_text) else "UNVERIFIED"

    moq = getattr(supplier, "moq", None)
    if moq is not None:
        result["moq"] = "VERIFIED" if number_in_context(moq, evidence_text, NUMERIC_CONTEXT["moq"]) else "UNVERIFIED"

    lead = getattr(supplier, "lead_time_days", None)
    if lead is not None:
        result["lead_time_days"] = "VERIFIED" if number_in_context(lead, evidence_text, NUMERIC_CONTEXT["lead_time_days"]) else "UNVERIFIED"

    quality = getattr(supplier, "quality_score", None)
    if quality is not None:
        result["quality_score"] = "VERIFIED" if number_in_context(quality, evidence_text, NUMERIC_CONTEXT["quality_score"]) else "UNVERIFIED"

    certs = getattr(supplier, "certifications", None) or []
    if certs:
        all_verified = all(string_grounded(c, evidence_text) for c in certs)
        result["certifications"] = "VERIFIED" if all_verified else "UNVERIFIED"

    capability = getattr(supplier, "capability", None)
    if capability is not None:
        result["capability"] = "VERIFIED" if string_grounded(capability, evidence_text) else "UNVERIFIED"

    return result
