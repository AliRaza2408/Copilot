# api

## Purpose
HTTP layer of the backend. Each file is a FastAPI `APIRouter` exposing the REST endpoints that the frontend and external clients call. Routers are mounted in `../main.py` via `app.include_router(...)`.

## Files
- `upload.py` — `POST /api/upload` — saves uploaded files to `uploads/` with a UUID-safe prefix; rejects unsupported extensions.
- `process.py` — `POST /api/process/{filename}` — runs document processing (Layer 1) on a previously uploaded file and returns evidence.
- `extract.py` — `POST /api/extract/{filename}` — runs document processing + regex extraction and returns structured requirements/supplier.
- `decision.py` — `POST /api/decision/process` — orchestrates the full 5-layer pipeline via `DecisionService` for uploaded files (the main demo endpoint).
- `copilot.py` — `POST /api/copilot/ask` — RAG question-answering over ingested evidence; `POST /api/copilot/ingest` — index new evidence.
- `approvals.py` — `POST /api/decision/{case_id}/review` — records the human review decision (in-memory store).
- `analyze.py` — `POST /analyze` — placeholder (not implemented).
- `recommendation.py` — `GET /recommendation` — placeholder (not implemented).
- `suppliers.py` — `GET /suppliers` — placeholder (not implemented).
- `__init__.py` — package marker.

## How it fits into the pipeline
Called directly by the frontend (`frontend/copilot/src/services/api.js`). Routes forward into the 5 processing layers; `decision.py` is the main entry point that ties them together.
