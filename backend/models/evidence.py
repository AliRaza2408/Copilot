from dataclasses import dataclass
from typing import Optional

@dataclass
class Evidence:
    source: str
    location: str
    content: str
    field: Optional[str] = None
    confidence: float = 1.0