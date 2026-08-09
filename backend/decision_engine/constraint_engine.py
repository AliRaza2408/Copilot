from models.constraint import ConstraintResult
from models.requirements import Requirement
from models.supplier import Supplier

def safe_float(val):
    """Safely convert LLM outputs to floats for comparison."""
    if val is None:
        return None
    try:
        cleaned = str(val).replace('%', '').replace('days', '').replace('units', '').replace(',', '').strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return None

def normalize_operator(op: str) -> str:
    if not op:
        return "=="
    op = op.lower().strip()
    
    if "<=" in op or "less than or equal" in op or "must not exceed" in op or "maximum" in op:
        return "<="
    if ">=" in op or "greater than or equal" in op or "must be at least" in op or "minimum" in op:
        return ">="
    if "contains" in op or "must have" in op or "requires" in op or "required" in op or "has" in op:
        return "contains"
    if "==" in op or "is" in op or "must be" in op or "equals" in op:
        return "=="
    
    return op

def normalize_name(name: str) -> str:
    name = name.lower()
    if "moq" in name or "minimum order" in name or "order quantity" in name:
        return "moq"
    if "lead time" in name or "delivery time" in name:
        return "lead time"
    if "quality" in name:
        return "quality"
    if "capab" in name:
        return "capability"
    if "cert" in name or "iso" in name:
        return "certification"
    return name

def check_requirement(requirement: Requirement, supplier: Supplier) -> ConstraintResult:
    name = normalize_name(requirement.name)
    operator = normalize_operator(requirement.operator)
    
    actual_value = None
    status = "UNKNOWN"
    explanation = ""

    # MOQ Logic
    if name == "moq":
        actual_value = supplier.minimum_order_quantity
        req_val = safe_float(requirement.required_value)
        sup_val = safe_float(actual_value)  # <--- FIXED: Apply safe_float to supplier value
        
        if sup_val is None:
            status = "UNKNOWN"
            explanation = "Supplier MOQ information was not found or is not a number."
        elif req_val is not None and operator in ["<=", "=="]:
            if sup_val <= req_val:
                status = "PASS"
                explanation = f"Supplier MOQ of {sup_val} is within the maximum allowed value of {req_val}."
            else:
                status = "FAIL"
                explanation = f"Supplier MOQ of {sup_val} exceeds the maximum allowed value of {req_val}."

    # Lead Time Logic
    elif name == "lead time":
        actual_value = supplier.lead_time_days
        req_val = safe_float(requirement.required_value)
        sup_val = safe_float(actual_value)  # <--- FIXED: Apply safe_float to supplier value
        
        if sup_val is None:
            status = "UNKNOWN"
            explanation = "Supplier lead time information was not found or is not a number."
        elif req_val is not None and operator in ["<=", "=="]:
            if sup_val <= req_val:
                status = "PASS"
                explanation = f"Lead time of {sup_val} days is within the maximum allowed value of {req_val} days."
            else:
                status = "FAIL"
                explanation = f"Lead time of {sup_val} days exceeds the maximum allowed value of {req_val} days."

    # Capability Logic
    elif name == "capability":
        actual_value = supplier.manufacturing_capability
        if actual_value is None:
            status = "UNKNOWN"
            explanation = "Supplier manufacturing capability was not found."
        elif operator in ["==", "contains"]:
            if str(actual_value).lower() == str(requirement.required_value).lower():
                status = "PASS"
                explanation = f"Supplier capability '{actual_value}' matches the required capability."
            else:
                status = "FAIL"
                explanation = f"Supplier capability '{actual_value}' does not match the required capability '{requirement.required_value}'."

    # Certification Logic
    elif name == "certification":
        req_val = requirement.required_value if requirement.required_value else requirement.name
        required_cert = str(req_val).lower().replace("certification", "").replace("required", "").strip()
        supplier_certs = [str(c).lower() for c in supplier.certifications]
        actual_value = supplier.certifications
        
        if not supplier_certs:
            status = "UNKNOWN"
            explanation = "No supplier certification information was found."
        elif operator in ["contains", "=="]:
            if any(required_cert in cert for cert in supplier_certs):
                status = "PASS"
                explanation = f"Supplier has the required {req_val} certification."
            else:
                status = "FAIL"
                explanation = f"Required certification {req_val} was not found."

    # Quality Logic
    elif name == "quality":
        actual_value = supplier.quality_score
        req_val = safe_float(requirement.required_value)
        sup_val = safe_float(actual_value)  # <--- FIXED: Apply safe_float to supplier value
        
        if sup_val is None:
            status = "UNKNOWN"
            explanation = "Supplier quality score was not found or is not a number."
        elif req_val is not None and operator in [">=", "=="]:
            if sup_val >= req_val:
                status = "PASS"
                explanation = f"Quality score of {sup_val} meets the minimum required score of {req_val}."
            else:
                status = "FAIL"
                explanation = f"Quality score of {sup_val} is below the minimum required score of {req_val}."

    return ConstraintResult(
        requirement_name=requirement.name,
        supplier_name=supplier.name,
        status=status,
        required_value=requirement.required_value,
        actual_value=actual_value,
        source=requirement.source,
        location=requirement.location,
        explanation=explanation
    )

def evaluate_supplier(supplier: Supplier, requirements: list[Requirement]) -> dict:
    results = []
    
    for requirement in requirements:
        result = check_requirement(requirement, supplier)
        results.append(result)

    mandatory_results = [
        result for result, req in zip(results, requirements) if req.mandatory
    ]

    has_failure = any(result.status == "FAIL" for result in mandatory_results)
    has_unknown = any(result.status == "UNKNOWN" for result in mandatory_results)

    if has_failure:
        eligibility = "INELIGIBLE"
        risk_level = "HIGH"
    elif has_unknown:
        eligibility = "REQUIRES_REVIEW"
        risk_level = "MEDIUM"
    else:
        eligibility = "ELIGIBLE"
        risk_level = "LOW"

    total_mandatory = len(mandatory_results)
    passed_mandatory = sum(1 for r in mandatory_results if r.status == "PASS")
    
    pass_rate = f"{passed_mandatory}/{total_mandatory}" if total_mandatory > 0 else "N/A"

    return {
        "supplier": supplier.name,
        "eligibility": eligibility,
        "risk_level": risk_level,
        "requirements_met": pass_rate,
        "constraints": [r.__dict__ for r in results]
    }