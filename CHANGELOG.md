# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] — Foundation release

### Added

- Streamlit application for AI-assisted Lean Six Sigma project structuring.
- Project Wizard for generating structured DMAIC-style outputs from informal problem descriptions.
- Analytics Workbench covering process capability, MSA / Gauge R&R, hypothesis testing, SPC charts, FMEA, regression, DOE, and benefits / COPQ analysis.
- Export support for PDF, Word, Excel, HTML, and Markdown project packages.
- CLI demo path through `run_demo.py`.
- Structured fallback mode so the repo can run without an API key.
- Sample project input at `templates/sample_project.json`.
- Smoke tests for the documented fallback path.
- CI checks for imports, tests, and the documented CLI fallback run.

### Notes

This is a working application, not just a framework repo. The main remaining technical debt is app modularity: `app.py` still carries too much responsibility and should be split into smaller testable surfaces over time.

### Next

- Refactor `app.py` into clearer UI, state, routing, and orchestration modules.
- Add deeper tests for export paths and analytics calculations.
- Add more sample project inputs across different process-improvement contexts.
