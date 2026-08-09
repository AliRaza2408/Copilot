from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Approval:
    decision_id: str
    status: str  # PENDING, APPROVED, REJECTED, NEEDS_REVIEW
    reviewed_at: Optional[datetime] = None
    reviewer_note: Optional[str] = None