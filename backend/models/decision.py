from pydantic import BaseModel
from typing import Any

class DecisionResult(BaseModel):
    case_id: str
    status: str
    requirements: list[Any] = []
    suppliers: list[Any] = []
    evaluations: list[Any] = []
    ranking: list[Any] = []
    sensitivity_analysis: dict = {}
    conflicts: list[Any] = []
    issues: list[Any] = []
    missing_information: list[Any] = []
    evidence: list[Any] = []
    recommendation: Any = None
    review_required: bool = False