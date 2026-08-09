# decision_engine

## Purpose
Layer 3: the deterministic core that evaluates supplier eligibility against requirements, ranks suppliers, detects missing data and conflicts.

## Files
- `constraint_engine.py` — evaluates each requirement against a supplier and returns PASS/FAIL/UNKNOWN per constraint (`check_requirement`) plus a per-supplier evaluation dict (`evaluate_supplier`). `safe_float` strips units (`%`, `days`, `units`, commas) before numeric comparison; `normalize_operator` and `normalize_name` map LLM phrasing to canonical forms. Eligibility: any mandatory FAIL → INELIGIBLE, any mandatory UNKNOWN → REQUIRES_REVIEW, else ELIGIBLE.
- `ranking.py` — scores only ELIGIBLE suppliers and sorts them. Formula per supplier: `score = min(quality,100)*w_quality + max(0,100-lead_time)*w_lead_time + max(0,100-(moq/100))*w_moq`.
- `scenarios.py` — defines the 4 priority weight sets (balanced, quality_focused, speed_focused, cost_focused) used for sensitivity analysis.
- `missing_data.py` — reports which required fields a supplier is missing.
- `conflict_detector.py` — groups facts by field and flags a CONFLICT when the same field has multiple distinct values across sources.
- `__init__.py` — package marker.

## How it fits into the pipeline
Consumes structured `models/Requirement` + `models/Supplier` from `extraction/`. Output feeds `reliability/` (confidence, conflict checks) and `services/decision_service.py` (recommendation).
