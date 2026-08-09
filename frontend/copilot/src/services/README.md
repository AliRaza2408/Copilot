# src/services

## Purpose
API client layer that talks to the FastAPI backend.

## Files
- `api.js` — defines `API_BASE_URL = "http://localhost:8000"` and exports four functions:
  - `uploadDocuments(files)` — `POST /api/upload` — sends files as `FormData` under the `files` key.
  - `processDecision(files)` — `POST /api/decision/process` — sends files as `FormData`; returns the full decision case (requirements, suppliers, evaluations, ranking, recommendation).
  - `askCopilot(question)` — `POST /api/copilot/ask` — JSON body `{question}`; returns the RAG answer with facts, recommendation, assumptions, citations.
  - `submitHumanReview(caseId, status, reason)` — `POST /api/decision/{case_id}/review` — JSON body `{case_id, status, reason}`.

## How it fits into the pipeline
`UploadBox.jsx` and `CopilotChat.jsx`/`ResultsDashboard.jsx` import these functions to drive the whole upload → analyze → review flow.
