def get_confidence(evidence_type: str) -> str:
    if evidence_type == "direct":
        return "HIGH"
    if evidence_type == "ambiguous":
        return "MEDIUM"
    if evidence_type == "inferred":
        return "LOW"
    return "UNKNOWN"