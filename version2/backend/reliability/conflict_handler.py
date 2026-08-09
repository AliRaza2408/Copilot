from models.system_issue import SystemIssue
from models.supplier import Supplier

def detect_supplier_conflicts(suppliers: list[Supplier]) -> list[SystemIssue]:
    """
    Scans extracted suppliers to see if the same supplier has 
    conflicting values across multiple documents.
    """
    issues = []
    grouped_suppliers = {}

    # Group all extracted supplier data by their name
    for sup in suppliers:
        name = sup.name.lower()
        if name not in grouped_suppliers:
            grouped_suppliers[name] = []
        grouped_suppliers[name].append(sup)

    # Check for conflicts within the same supplier
    for name, sup_list in grouped_suppliers.items():
        if len(sup_list) < 2:
            continue # Only 1 document for this supplier, no conflict possible

        # Compare fields across the documents
        fields_to_check = [
            "minimum_order_quantity", 
            "lead_time_days", 
            "quality_score", 
            "manufacturing_capability"
        ]
        
        original_name = sup_list[0].name

        for field in fields_to_check:
            values = set()
            for sup in sup_list:
                val = getattr(sup, field)
                if val is not None:
                    values.add(str(val))
            
            # If we found more than 1 unique value for this field, it's a conflict!
            if len(values) > 1:
                issues.append(SystemIssue(
                    type="CONFLICT",
                    severity="HIGH",
                    message=f"Conflicting {field.replace('_', ' ')} found for {original_name}: {', '.join(values)}",
                    requires_review=True
                ))

    return issues

def detect_unknown_constraints(evaluations: list[dict]) -> list[SystemIssue]:
    """Flags any constraint that couldn't be verified."""
    issues = []
    for eval_result in evaluations:
        for constraint in eval_result.get("constraints", []):
            if constraint["status"] == "UNKNOWN":
                issues.append(SystemIssue(
                    type="CONFLICT",
                    severity="MEDIUM",
                    message=f"Could not verify {constraint['requirement_name']} for {eval_result['supplier']}.",
                    requires_review=True
                ))
    return issues