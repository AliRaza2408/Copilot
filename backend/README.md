# Manufacturing Decision Copilot — Backend

FastAPI backend for the Manufacturing Decision Copilot: it ingests supplier documents (PDF, DOCX, CSV, XLSX, TXT), extracts requirements and supplier evidence, then runs a 5-layer decision pipeline to score suppliers and flag review requirements.

## Architecture

The backend is organised as a 5-layer pipeline:

| Layer | Package | Role |
|-------|---------|------|
| 1. Document processing | `document_processing/` | Normalise every evidence item to a `text` field; extract text from PDF/DOCX/CSV/XLSX/TXT |
| 2. Extraction | `extraction/` | Regex-based extraction of requirements and supplier fields |
| 3. Decision engine | `decision_engine/` | `evaluate_supplier` + `rank_suppliers` scoring (`quality`, `lead_time`, `moq`) |
| 4. Reliability | `reliability/` | Confidence/hallucination checks; flags scanned PDFs and missing fields |
| 5. RAG | `rag/` | Embedding (all-MiniLM-L6-v2) + Groq LLM for question answering |

`services/decision_service.py` orchestrates the full pipeline. `models/` holds the Pydantic schemas (including `DecisionResult.issues` which surfaces processing errors instead of silently dropping them).

## API endpoints

- `GET /health` — liveness check
- `POST /api/upload` — upload files (multi-file supported), rejects unsupported extensions
- `POST /api/process/{filename}` — Layer 1 document processing only
- `POST /api/extract/{filename}` — processing + extraction
- `POST /api/decision/process` — full 5-layer decision pipeline (main demo endpoint)
- `POST /api/copilot/ask` — RAG + LLM question answering
- `POST /api/copilot/ingest` — index new evidence into the vector store
- `POST /api/decision/{case_id}/review` — record the human review decision

## Setup

```bash
cd backend
python -m venv venv                 # or use the existing venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment

Create `backend/.env` with `GROQ_API_KEY=...` (used by the RAG layer). This file is git-ignored and must never be committed.

### Running the server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Frontend expects the backend at `http://127.0.0.1:8000` (CORS allows `http://localhost:5173`).

## Tests

```bash
python test_document_processing.py
python test_decision_engine.py
python test_phase7.py
```

## Known limitations

- Scanned/image-only PDFs have no OCR; they are flagged as `is_scanned` and may lead the LLM to guess supplier names.
- `api/suppliers.py`, `api/analyze.py`, `api/recommendation.py` are placeholder routers that are not registered in `main.py`.
