from dataclasses import dataclass
from typing import Optional

@dataclass
class EvidenceChunk:
    id: str
    source: str
    page: Optional[int]
    text: str
    supplier: Optional[str] = None
    field: Optional[str] = None