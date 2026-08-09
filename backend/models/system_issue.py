from pydantic import BaseModel
from typing import Optional

class SystemIssue(BaseModel):
    type: str
    severity: str
    message: str
    source: Optional[str] = None
    page: Optional[int] = None
    requires_review: bool = False