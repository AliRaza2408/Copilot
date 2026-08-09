# models

## Purpose
Data contracts shared across the pipeline — Pydantic models and dataclasses that define the shape of evidence, requirements, suppliers, and results.

## Files
- `approval.py` — `Approval` — human review decision record.
- `conflict.py` — `Conflict` — a detected conflicting field with its values and sources.
- `constraint.py` — `ConstraintResult` — outcome of checking one requirement against one supplier (status PASS/FAIL/UNKNOWN).
- `decision.py` — `DecisionResult` — the full API response for a decision case (requirements, suppliers, evaluations, ranking, conflicts, issues, recommendation).
- `evidence.py` — `Evidence` — a piece of evidence with source, location, content, and confidence.
- `evidence_chunk.py` — `EvidenceChunk` — an indexed text chunk with page and optional supplier/field metadata.
- `extracted_data.py` — `ExtractedField`, `ExtractedRequirement`, `ExtractedSupplier` — LLM extraction outputs.
- `extraction_result.py` — `ExtractionResult` — facts/assumptions/warnings from an extraction run.
- `ranking.py` — `RankingWeights` — quality/lead_time/moq weights.
- `requirements.py` — `Requirement` — a single product requirement (name, operator, required value, mandatory flag).
- `review.py` — `ReviewItem` — a supplier issue requiring human review.
- `supplier.py` — `Supplier` — a supplier profile (MOQ, lead time, certifications, quality score, capability).
- `system_issue.py` — `SystemIssue` — a reliability warning/error (type, severity, message).
- `__init__.py` — package marker.

## How it fits into the pipeline
Produced/consumed by all layers; `DecisionResult` is what the frontend renders in the results dashboard.
