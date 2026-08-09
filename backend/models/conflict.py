from dataclasses import dataclass

@dataclass
class Conflict:
    field: str
    values: list
    sources: list
    severity: str
    explanation: str