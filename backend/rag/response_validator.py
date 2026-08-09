def validate_response(answer, evidence):
    warnings = []
    if not evidence:
        warnings.append("No supporting evidence found in the database.")
    
    # Basic check to see if LLM mentioned a source not in evidence
    # (Simplified for prototype)
    return {
        "valid": len(warnings) == 0,
        "warnings": warnings
    }