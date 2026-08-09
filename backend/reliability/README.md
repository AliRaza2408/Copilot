# reliability

## Purpose
Layer 4: trustworthiness checks — confidence scoring, conflict detection, claim validation, and prompt-injection protection for the AI output.

## Files
- `confidence.py` — `calculate_confidence` returns LOW/MEDIUM/HIGH based on conflicts, failures, unknown constraints, and missing info.
- `conflict_handler.py` — `detect_supplier_conflicts` flags the same supplier with differing field values across documents; `detect_unknown_constraints` flags constraints that couldn't be verified (status UNKNOWN).
- `claim_validator.py` — `validate_claims` checks that numbers in the AI answer actually appear in the retrieved evidence; flags unsupported claims.
- `safety_guard.py` — `sanitize_prompt` wraps the RAG prompt with system safety rules to prevent prompt injection from untrusted document text.
- `__init__.py` — package marker.

## How it fits into the pipeline
Consumes evaluations from `decision_engine/` and the RAG answer. Its findings (SystemIssue list + confidence level) are surfaced in `DecisionResult` and drive the human-review flag.
