from dataclasses import dataclass
from typing import Optional

@dataclass
class Requirement:
    name: str
    requirement_type: str
    operator: Optional[str]
    required_value: Optional[object]
    unit: Optional[str]
    mandatory: bool
    source: str
    location: str
    evidence_text: str