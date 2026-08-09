# document_processing

## Purpose
Layer 1: converts raw uploaded files (PDF, Excel, DOCX, CSV, TXT) into a uniform list of "evidence" dicts that every downstream layer consumes.

## Files
- `document_service.py` — routes a file to the correct reader by extension and normalizes every evidence item so it always has a `text` field (`_normalize_evidence` / `evidence_to_text` handles tabular `data` dicts from CSV/Excel).
- `pdf_reader.py` — extracts per-page text with PyMuPDF; flags scanned/no-text pages as `is_scanned: True` (OCR fallback required).
- `excel_reader.py` — reads every sheet as row-level evidence with a `data` dict (Field/Value pairs).
- `docx_reader.py` — reads paragraph-level evidence.
- `csv_reader.py` — reads row-level evidence with a `data` dict.
- `txt_reader.py` — reads the whole file as a single evidence item.
- `__init__.py` — package marker.

## How it fits into the pipeline
Called by `api/process.py`, `api/extract.py`, and `services/decision_service.py`. Output (evidence list) is handed to `extraction/` for classification and to the RAG index for embeddings.
