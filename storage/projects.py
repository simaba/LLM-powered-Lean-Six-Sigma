from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path("saved_projects")
BASE_DIR.mkdir(exist_ok=True)


def _safe_name(name: str) -> str:
    cleaned = "_".join(name.strip().lower().split())
    return cleaned or "untitled_project"


def save_project_snapshot(project_data: Dict[str, Any]) -> str:
    path = BASE_DIR / f"{_safe_name(project_data.get('project_name', 'untitled_project'))}.json"
    path.write_text(json.dumps(project_data, indent=2), encoding="utf-8")
    return str(path)


def load_project_snapshot(path_str: str) -> Dict[str, Any]:
    path = Path(path_str)
    return json.loads(path.read_text(encoding="utf-8"))


def list_saved_projects() -> list[str]:
    return sorted(str(path) for path in BASE_DIR.glob("*.json"))
