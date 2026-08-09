from models.conflict import Conflict

def detect_conflicts(facts: list[dict]) -> list[Conflict]:
    grouped = {}
    
    for fact in facts:
        field = fact.get("field")
        if not field:
            continue
        grouped.setdefault(field, []).append(fact)

    conflicts = []

    for field, field_facts in grouped.items():
        values = {str(fact.get("value")) for fact in field_facts}
        
        if len(values) > 1:
            conflicts.append(
                Conflict(
                    field=field,
                    values=list(values),
                    sources=[fact.get("source") for fact in field_facts],
                    severity="HIGH",
                    explanation=f"Conflicting values found for {field}."
                )
            )

    return conflicts