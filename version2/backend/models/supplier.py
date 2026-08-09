from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Supplier:
    name: str
    location: Optional[str] = None
    manufacturing_capability: Optional[str] = None
    minimum_order_quantity: Optional[float] = None
    lead_time_days: Optional[float] = None
    certifications: list[str] = field(default_factory=list)
    quality_score: Optional[float] = None
    capacity: Optional[float] = None
    sustainability_score: Optional[float] = None