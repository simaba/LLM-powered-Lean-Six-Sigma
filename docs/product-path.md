# Product Path

This document describes the intended productized architecture for the repository.

## Canonical architecture

### Backend
- `src/canonical_phases.py`
- `src/engine_canonical.py`
- `src/models.py`
- `src/renderers.py`

### UI
- `app_product.py`

### Persistence
- `storage/projects.py`
- `storage/reviews.py`

### UI support
- `ui/forms.py`
- `ui/render.py`
- `ui/dashboard_insights.py`
- `ui/scoring.py`
- `ui/narrative.py`
- `ui/wizard.py`

### Exports
- `exports/review_package.py`
- `exports/briefing_html.py`
- `exports/pdf_briefing.py`
- `exports/leadership_deck.py`

## Product goals

This path is intended to provide:
- one clear backend flow
- one flagship app
- one guided user experience
- one export path for leadership-ready outputs

## Product workflow

The flagship app uses a five-step guided workflow:
1. Intake
2. Generate
3. Dashboard
4. Review
5. Export

## Exports currently supported

- markdown summary
- HTML briefing
- PDF briefing
- leadership deck markdown
- reviewed package JSON and CSV files

## Legacy files

Older prototypes remain in the repository for reference, but they should not be treated as the main product path.
