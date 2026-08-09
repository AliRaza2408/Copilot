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

def find_missing_requirements(requirements, supplier) -> list[dict]:
    missing = []
    
    for requirement in requirements:
        # Normalize the name so "Quality score" becomes "quality"
        name = normalize_name(requirement.name)
        
        if name == "moq":
            value = supplier.minimum_order_quantity
        elif name == "lead time":
            value = supplier.lead_time_days
        elif name == "quality":
            value = supplier.quality_score
        elif name == "capability":
            value = supplier.manufacturing_capability
        elif name == "certification":
            value = supplier.certifications
        else:
            value = None

        if value is None or value == []:
            missing.append({
                "requirement": requirement.name,
                "source": requirement.source,
                "location": requirement.location,
                "message": "Required supplier information was not found."
            })
            
    return missing