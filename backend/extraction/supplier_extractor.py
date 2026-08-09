import re
from models.supplier import Supplier

def extract_supplier_from_text(evidence_items: list[dict]) -> Supplier | None:
    combined_text = "\n".join(
        item.get("text", "")
        for item in evidence_items
        if item.get("text")
    )

    if not combined_text:
        return None

    name_match = re.search(
        r"(?:Supplier Name|Supplier|Company Name)\s*:\s*(.+)",
        combined_text,
        re.IGNORECASE
    )
    supplier_name = name_match.group(1).strip() if name_match else "Unknown Supplier"

    moq_match = re.search(
        r"(?:MOQ|Minimum Order Quantity)\s*:\s*(\d[\d,]*)",
        combined_text,
        re.IGNORECASE
    )
    moq = float(moq_match.group(1).replace(",", "")) if moq_match else None

    lead_time_match = re.search(
        r"(?:Lead Time|Production Lead Time)\s*:\s*(\d+(?:\.\d+)?)\s*days?",
        combined_text,
        re.IGNORECASE
    )
    lead_time = float(lead_time_match.group(1)) if lead_time_match else None

    return Supplier(
        name=supplier_name,
        minimum_order_quantity=moq,
        lead_time_days=lead_time
    )