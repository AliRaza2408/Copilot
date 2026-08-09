from dataclasses import dataclass
from typing import Optional

@dataclass
class ConstraintResult:
    requirement_name: str
    supplier_name: str
    status: str  # "PASS", "FAIL", "UNKNOWN"
    required_value: Optional[object]
    actual_value: Optional[object]
    source: Optional[str]
    location: Optional[str]
    explanation: str