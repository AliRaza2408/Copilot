from dataclasses import dataclass
from typing import Optional

@dataclass
class ReviewItem:
    supplier: str
    issue_type: str
    field: str
    message: str
    severity: str
    source: Optional[str] = None
    location: Optional[str] = None