from __future__ import annotations

from typing import Any


def intake_validation(project_data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not project_data.get("project_name", "").strip():
        issues.append("Project name is missing.")
    if not project_data.get("problem_statement", "").strip():
        issues.append("Problem statement is missing.")
    if not project_data.get("current_symptoms"):
        issues.append("At least one current symptom is required.")
    if not project_data.get("current_metrics"):
        issues.append("At least one current metric is required.")
    if not project_data.get("stakeholder_concerns"):
        issues.append("At least one stakeholder concern is recommended.")
    return issues


def review_payload(
    confirmed_ctqs: list[str],
    root_cause_labels: dict[str, str],
    refined_actions: list[str],
) -> dict[str, Any]:
    return {
        "confirmed_ctqs": confirmed_ctqs,
        "root_cause_labels": root_cause_labels,
        "refined_actions": refined_actions,
    }
