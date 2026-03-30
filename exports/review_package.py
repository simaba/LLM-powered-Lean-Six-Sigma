from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


EXPORT_DIR = Path("exports_output")
EXPORT_DIR.mkdir(exist_ok=True)


def export_review_package(project_name: str, payload: dict[str, Any], action_df: pd.DataFrame, control_df: pd.DataFrame) -> dict[str, str]:
    slug = "_".join(project_name.strip().lower().split()) or "untitled_project"
    json_path = EXPORT_DIR / f"{slug}_review_package.json"
    actions_path = EXPORT_DIR / f"{slug}_actions.csv"
    controls_path = EXPORT_DIR / f"{slug}_controls.csv"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    action_df.to_csv(actions_path, index=False)
    control_df.to_csv(controls_path, index=False)

    return {
        "json": str(json_path),
        "actions_csv": str(actions_path),
        "controls_csv": str(controls_path),
    }
