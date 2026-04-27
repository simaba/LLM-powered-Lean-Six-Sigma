from __future__ import annotations

from pathlib import Path

from run_demo import load_input
from src.engine import run_assessment
from src.renderers import render_markdown_summary


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "templates" / "sample_project.json"


def test_sample_project_loads() -> None:
    project = load_input(SAMPLE)
    assert project.project_name == "Supplier Change Request Intake"
    assert len(project.current_symptoms) >= 3
    assert "average_cycle_time_days" in project.current_metrics


def test_fallback_assessment_generates_markdown(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    project = load_input(SAMPLE)
    result = run_assessment(project, mode="dmaic", audience="pm")
    markdown = render_markdown_summary(result)

    assert result.project_name == project.project_name
    assert result.mode == "dmaic"
    assert result.audience == "pm"
    assert result.ctqs
    assert result.root_causes
    assert result.improvement_actions
    assert "# Supplier Change Request Intake" in markdown
    assert "## Critical-to-Quality (CTQs)" in markdown
    assert "## Suggested improvement actions" in markdown
