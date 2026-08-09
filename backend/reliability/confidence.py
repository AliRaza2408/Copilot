def calculate_confidence(evaluations: list[dict], missing_info: list[dict], conflicts: list[dict]) -> str:
    """Calculates overall system confidence based on data quality."""
    if not evaluations:
        return "LOW"
    
    has_failures = any(e["eligibility"] == "INELIGIBLE" for e in evaluations)
    has_unknowns = any(e["eligibility"] == "REQUIRES_REVIEW" for e in evaluations)
    
    if conflicts or has_failures:
        return "LOW"
    elif missing_info or has_unknowns:
        return "MEDIUM"
    else:
        return "HIGH"