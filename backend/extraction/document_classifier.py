def classify_document(text: str) -> str:
    text_lower = text.lower()

    if any(keyword in text_lower for keyword in [
        "product requirement", "mandatory requirement", 
        "technical specification", "product specification"
    ]):
        return "product_requirements"

    if any(keyword in text_lower for keyword in [
        "supplier profile", "supplier name", 
        "manufacturing capability", "factory profile"
    ]):
        return "supplier_profile"

    if any(keyword in text_lower for keyword in [
        "quotation", "unit price", "incoterm", "payment terms"
    ]):
        return "quotation"

    if any(keyword in text_lower for keyword in [
        "quality report", "defect rate", 
        "quality score", "inspection"
    ]):
        return "quality_report"

    return "unknown"