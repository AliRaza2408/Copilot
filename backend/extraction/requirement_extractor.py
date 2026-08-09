import re
from models.requirements import Requirement

def extract_requirements(evidence_items: list[dict]) -> list[Requirement]:
    requirements = []

    for item in evidence_items:
        text = item.get("text", "")
        if not text:
            continue

        source = item.get("source", "")
        page = item.get("page")
        location = f"Page {page}" if page else "Unknown location"

        # Extract MOQ
        moq_match = re.search(
            r"(?:maximum|max|up to).*?MOQ.*?(\d[\d,]*)",
            text,
            re.IGNORECASE
        )
        if moq_match:
            moq = float(moq_match.group(1).replace(",", ""))
            requirements.append(
                Requirement(
                    name="MOQ",
                    requirement_type="numeric",
                    operator="<=",
                    required_value=moq,
                    unit="units",
                    mandatory=True,
                    source=source,
                    location=location,
                    evidence_text=text
                )
            )

    return requirements