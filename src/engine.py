from __future__ import annotations

from src.models import AssessmentResult, ProjectInput
from src.phases import run_llm_assessment


def run_assessment(project: ProjectInput, mode: str, audience: str) -> AssessmentResult:
    return run_llm_assessment(project, mode, audience)
