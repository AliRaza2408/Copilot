from dataclasses import dataclass, field

@dataclass
class ExtractionResult:
    facts: list[dict] = field(default_factory=list)
    assumptions: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)