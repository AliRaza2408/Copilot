from pydantic import BaseModel, Field
from typing import Any, Optional, List

class ExtractedField(BaseModel):
    name: str
    value: Any
    unit: Optional[str] = None
    source: Optional[str] = "Unknown"
    page: Optional[int] = None
    confidence: float = 0.8

class ExtractedRequirement(BaseModel):
    field: str
    operator: Optional[str] = None
    required_value: Any = None
    unit: Optional[str] = None
    mandatory: bool = True
    source: Optional[str] = "Unknown"
    page: Optional[int] = None

class ExtractedSupplier(BaseModel):
    name: str
    moq: Optional[Any] = Field(default=None, alias="minimum_order_quantity") # Changed to Any
    lead_time_days: Optional[Any] = Field(default=None, alias="lead_time") # Changed to Any
    quality_score: Optional[Any] = Field(default=None, alias="quality") # Changed to Any
    certifications: List[str] = []
    capability: Optional[Any] = Field(default=None, alias="manufacturing_capability") # Changed to Any
    source: Optional[str] = "Unknown"
    verification_status: dict = {}  # per-field: field -> "VERIFIED" | "UNVERIFIED"

    class Config:
        populate_by_name = True