# services

## Purpose
The orchestration layer that ties the 5 processing layers together into a complete decision case.

## Files
- `decision_service.py` — the main orchestrator. `DecisionService.process_case` runs: process documents → classify → LLM extraction → build Requirement/Supplier models → evaluate constraints → rank → sensitivity analysis → reliability checks → confidence → recommendation, and returns a `DecisionResult`.
- `sensitivity_service.py` — `run_sensitivity_analysis` re-scores all suppliers under each weight scenario in `decision_engine/scenarios.py`.
- `confidence_service.py` — `get_confidence` maps an evidence type (`direct`/`ambiguous`/`inferred`) to a confidence label.
- `evidence_service.py` — placeholder for supplier evidence mapping (Step 17+).
- `ranking_service.py` — placeholder for transparent ranking (Step 18+).
- `supplier_service.py` — placeholder for supplier data loading (Step 18+).
- `__init__.py` — package marker.

## How it fits into the pipeline
Called by `api/decision.py`. It consumes `document_processing/`, `extraction/`, `decision_engine/`, and `reliability/`, plus the shared RAG index, and produces the final `DecisionResult` returned to the frontend.
