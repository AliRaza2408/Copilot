# extraction

## Purpose
Layer 2: turns raw evidence text into structured requirements and supplier profiles. Uses a Groq LLM with strict JSON schemas, with keyword-based regex fallbacks.

## Files
- `document_classifier.py` — classifies a document by keyword heuristics: `product_requirements`, `supplier_profile`, `quotation`, `quality_report`, or `unknown`.
- `llm_extractor.py` — calls Groq (`llama-3.1-8b-instant`, JSON mode) to extract `ExtractedRequirement` / `ExtractedSupplier` objects; returns empty lists if the API is unavailable.
- `requirement_extractor.py` — regex fallback that extracts only the MOQ requirement (used by `api/extract.py`).
- `supplier_extractor.py` — regex fallback that extracts supplier name, MOQ, and lead time.
- `__init__.py` — package marker.

## How it fits into the pipeline
Consumes evidence from `document_processing/`. `decision_service.py` uses `LLMExtractor` for the full pipeline; `api/extract.py` uses the regex extractors. Structured output is converted into `models/` dataclasses for the decision engine.
