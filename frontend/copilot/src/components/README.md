# src/components

## Purpose
Reusable React UI pieces. Presentational components receive data as props; a few (UploadBox, CopilotChat, ResultsDashboard) call the backend API and manage their own state.

## Files
- `Header.jsx` — app title/branding bar.
- `HeroSection.jsx` — landing hero copy on the upload screen.
- `ChallengePack.jsx` — section wrapper that hosts the upload box.
- `UploadBox.jsx` — drag-drop/file input UI; calls `processDecision` and passes the result up via `onUploadSuccess`.
- `FileUpload.jsx` — simpler upload form (calls `/api/upload`); used by the dead `pages/Dashboard.jsx`.
- `SystemStatus.jsx` — shows whether evidence was received.
- `RequirementTable.jsx` — renders a requirements table from props.
- `SupplierTable.jsx` — renders a supplier comparison table from props.
- `RecommendationCard.jsx` — renders the top recommendation (supplier, score, confidence).
- `SensitivityAnalysis.jsx` — renders ranking under each weight scenario.
- `ConflictPanel.jsx` — lists detected evidence conflicts.
- `ReviewPanel.jsx` — lists supplier items needing human review.
- `EvidencePanel.jsx` — displays retrieved evidence chunks.
- `SafetyPanel.jsx` — shows safety/confidence status of the recommendation.
- `CopilotChat.jsx` — AI chat box; calls `/api/copilot/ask` and shows facts, recommendation, assumptions, citations.
- `ResultsDashboard.jsx` — main results view (recommendation, supplier table, constraint breakdown, sensitivity, conflicts, missing info, Copilot chat, human review buttons). This is the component `App.jsx` renders.

## How it fits into the pipeline
`App.jsx` shows the upload flow, then swaps to `ResultsDashboard` once a decision case is returned from the backend.
