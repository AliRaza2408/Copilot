# src/pages

## Purpose
Page-level composition of components. Currently contains a single page.

## Files
- `Dashboard.jsx` — **UNUSED / dead code.** It assembles `FileUpload`, `RequirementTable`, `SupplierTable`, `RecommendationCard`, `SensitivityAnalysis`, `ConflictPanel`, and `ReviewPanel`, but is never imported anywhere. `App.jsx` uses `ResultsDashboard` instead. It only sets hardcoded mock data and must not be shown in demos.

## How it fits into the pipeline
Not wired into the app. The live UI path is `App.jsx` → `UploadBox` → `ResultsDashboard`.
