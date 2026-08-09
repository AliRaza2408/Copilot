from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/decision", tags=["Approvals"])

# In-memory store for the hackathon prototype. 
# In production, this would be a database table.
APPROVAL_STORE = {}

class ReviewPayload(BaseModel):
    case_id: str
    status: str # "REVIEWED" or "REJECTED"
    reason: Optional[str] = None

@router.post("/{case_id}/review")
async def submit_review(case_id: str, payload: ReviewPayload):
    # Save the human decision
    APPROVAL_STORE[case_id] = {
        "status": payload.status,
        "reason": payload.reason
    }
    print(f"\n[Human Review] Case {case_id} updated: {payload.status} - {payload.reason}")
    return {"status": "success", "data": APPROVAL_STORE[case_id]}