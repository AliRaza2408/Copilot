from models.system_issue import SystemIssue

def flag_unverified_extractions(suppliers) -> list[SystemIssue]:
    """
    Surfaces extracted supplier fields that could not be grounded in the source
    text. Distinct from "missing" (field absent) and "conflict" (field present
    but contradictory): this means the AI *claimed* a value that does not
    actually appear in any evidence.
    """
    issues = []
    for sup in suppliers:
        status = getattr(sup, "verification_status", None) or {}
        for field, state in status.items():
            if state == "UNVERIFIED":
                issues.append(SystemIssue(
                    type="UNVERIFIED_EXTRACTION",
                    severity="HIGH",
                    message=(
                        f"'{field}' for {sup.name} could not be verified against "
                        "the source document — the value does not appear in any "
                        "extracted evidence."
                    ),
                    source=None,
                    page=None,
                    requires_review=True
                ))
    return issues


def validate_claims(ai_answer: str, evidence: list[dict]) -> list[SystemIssue]:
    """
    Checks if the AI's answer contains numbers/facts not present in the evidence.
    """
    issues = []
    
    if not evidence:
        issues.append(SystemIssue(
            type="UNSUPPORTED_CLAIM",
            severity="HIGH",
            message="AI provided an answer but no evidence was retrieved to support it.",
            requires_review=True
        ))
        return issues

    # Combine all evidence text into one string for easy searching
    all_evidence_text = " ".join([e.get("text", "") for e in evidence]).lower()

    # Simple claim check: Look for numbers in the AI answer and ensure they exist in the evidence
    import re
    # Find all numbers (e.g., 1500, 95.5, 20) in the AI's response
    claims = re.findall(r'\b\d[\d,\.]*\b', ai_answer.lower())
    
    for claim in claims:
        # Remove commas for checking (e.g., 1,500 -> 1500)
        clean_claim = claim.replace(",", "")
        if clean_claim not in all_evidence_text:
            issues.append(SystemIssue(
                type="UNSUPPORTED_CLAIM",
                severity="HIGH",
                message=f"AI claimed '{claim}', but this value could not be verified in the retrieved evidence.",
                requires_review=True
            ))
            
    return issues