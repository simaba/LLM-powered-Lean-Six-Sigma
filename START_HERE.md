# Start Here

This file defines the recommended product path for this repository.

## Use this path

### Canonical backend
- `src/canonical_phases.py`
- `src/engine_canonical.py`
- `src/models.py`
- `src/renderers.py`

### Flagship app
- `app_product.py`

## Recommended command

```bash
py -m streamlit run app_product.py
```

## Guided workflow inside the flagship app

1. Intake
2. Generate
3. Dashboard
4. Review
5. Export

## Supported outputs

- markdown summary
- HTML briefing
- PDF briefing
- leadership deck markdown
- reviewed package export

## Saved state

The flagship path supports:
- saved project snapshots
- saved reviewed states

## Legacy files

Older app files remain in the repository as prototypes and historical versions:
- `app.py`
- `app_v2.py`
- `app_v3.py`
- `app_v4.py`
- `app_v5.py`
- `app_v6.py`
- `app_v7.py`

Older backend paths also remain for historical reasons:
- `src/phases.py`
- `src/phases/__init__.py`

For product testing, do not start with those files.
Start with `app_product.py`.
