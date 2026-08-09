# Manufacturing Decision Copilot — Frontend

React + Vite frontend for the Manufacturing Decision Copilot. Users upload supplier documents, the backend runs the decision pipeline, and the UI shows ranked suppliers with confidence scores and review flags.

## Structure

- `src/` — application source
  - `components/` — UI components (file upload, copilot chat)
  - `services/` — `api.js`, the single client that calls the backend
  - `pages/` — page components
- `index.html`, `vite.config.js`, `package.json` — build tooling
- `dist/` — build output (git-ignored)

## Backend API calls

The frontend talks to the backend via `src/services/api.js`, which only calls:

- `POST /api/upload`
- `POST /api/decision/process`
- `POST /api/copilot/ask`
- `POST /api/decision/{case_id}/review`

## Running

```bash
cd frontend/copilot
npm install
npm run dev
```

Vite dev server runs at `http://localhost:5173`.

## Production build

```bash
npm run build
```

## Lint

```bash
npm run lint   # oxlint
```

## Notes

- The backend must be running on `127.0.0.1:8000` (CORS allows this origin).
- `node_modules/` and `dist/` are git-ignored.
