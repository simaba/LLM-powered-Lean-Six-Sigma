from __future__ import annotations

from typing import Dict, List

from src.models import EvidenceItem, ProjectInput


def _tag_supported(statement: str) -> EvidenceItem:
    return EvidenceItem(statement=statement, evidence_tag="supported_by_input")


def _tag_inferred(statement: str) -> EvidenceItem:
    return EvidenceItem(statement=statement, evidence_tag="inferred_hypothesis")


def _tag_missing(statement: str) -> EvidenceItem:
    return EvidenceItem(statement=statement, evidence_tag="missing_evidence")


def cleaned_problem_statement(project: ProjectInput) -> str:
    symptom_summary = "; ".join(project.current_symptoms[:3])
    return (
        f"{project.project_name} is experiencing a performance problem in which {symptom_summary}. "
        f"The current project concern is: {project.problem_statement.strip()}"
    )


def generate_ctqs(project: ProjectInput) -> List[EvidenceItem]:
    ctqs: List[EvidenceItem] = []
    for metric_name in list(project.current_metrics.keys())[:3]:
        ctqs.append(_tag_supported(f"Critical metric to quality: {metric_name}"))
    ctqs.append(_tag_inferred("Critical metric to quality: cycle time or lead time"))
    ctqs.append(_tag_inferred("Critical metric to quality: defect or rework rate"))
    return ctqs


def generate_sipoc(project: ProjectInput) -> Dict[str, List[str]]:
    return {
        "suppliers": ["project team", "upstream stakeholders", "data source owners"],
        "inputs": [project.problem_statement, *project.current_symptoms[:2], *list(project.current_metrics.keys())[:2]],
        "process": ["define problem", "measure current state", "analyze causes", "improve process", "control results"],
        "outputs": ["improved process performance", "reduced waste or rework", "clearer control plan"],
        "customers": ["project sponsor", "process owner", "end users or downstream teams"],
    }


def generate_dmaic(project: ProjectInput) -> Dict[str, List[EvidenceItem]]:
    return {
        "define": [
            _tag_supported(cleaned_problem_statement(project)),
            _tag_supported(f"Key stakeholder concerns: {', '.join(project.stakeholder_concerns[:3])}"),
        ],
        "measure": [
            _tag_supported(f"Current metrics available: {', '.join(project.current_metrics.keys())}"),
            _tag_missing("Baseline variance and historical trend are not yet provided."),
        ],
        "analyze": [
            _tag_inferred("Potential issue in handoffs, prioritization, or unclear decision ownership."),
            _tag_inferred("Potential process waste in waiting, rework, or unnecessary escalation."),
        ],
        "improve": [
            _tag_inferred("Pilot one high-impact process change before scaling broadly."),
            _tag_inferred("Clarify ownership, thresholds, and standard work for critical decisions."),
        ],
        "control": [
            _tag_inferred("Define monitoring cadence and threshold-based triggers for regression."),
            _tag_inferred("Assign control owners and escalation paths for sustained performance."),
        ],
    }


def generate_root_causes(project: ProjectInput) -> List[EvidenceItem]:
    causes = [
        _tag_inferred("Unclear problem framing causes teams to solve symptoms instead of root issues."),
        _tag_inferred("Weak handoff or ownership design may be driving delays and rework."),
        _tag_inferred("Current measurement may be incomplete or not tied to CTQs."),
        _tag_inferred("Stakeholder alignment may be insufficient at key decision points."),
    ]
    if project.constraints:
        causes.append(_tag_supported(f"Constraint pressure may be influencing outcomes: {project.constraints[0]}"))
    return causes


def generate_metrics(project: ProjectInput) -> List[EvidenceItem]:
    metrics = [_tag_supported(f"Track current metric: {k} = {v}") for k, v in list(project.current_metrics.items())[:4]]
    metrics.extend(
        [
            _tag_inferred("Track cycle time or lead time by workflow stage."),
            _tag_inferred("Track defect, rework, or reopening rate."),
            _tag_inferred("Track escalation volume and root-cause recurrence."),
        ]
    )
    return metrics


def generate_improvements(project: ProjectInput) -> List[EvidenceItem]:
    return [
        _tag_inferred("Clarify process ownership and decision rights at major handoff points."),
        _tag_inferred("Standardize intake and triage criteria to reduce ambiguity."),
        _tag_inferred("Pilot a reduced-scope workflow with explicit acceptance thresholds."),
        _tag_inferred("Introduce a simple action tracker with owner and due date for key issues."),
    ]


def generate_control_plan(project: ProjectInput) -> List[EvidenceItem]:
    return [
        _tag_inferred("Assign a process owner for each critical metric."),
        _tag_inferred("Review performance weekly during the first stabilization period."),
        _tag_inferred("Trigger escalation if a core metric breaches its threshold twice in one cycle."),
        _tag_inferred("Document unresolved risks and review them at each status checkpoint."),
    ]


def generate_action_tracker() -> List[Dict[str, str]]:
    return [
        {"action": "Validate problem statement with stakeholders", "owner": "PM", "priority": "high"},
        {"action": "Confirm baseline metrics and missing data", "owner": "Analyst", "priority": "high"},
        {"action": "Pilot one improvement action", "owner": "Process owner", "priority": "medium"},
        {"action": "Define control thresholds", "owner": "Quality lead", "priority": "medium"},
    ]


def generate_project_memory(project: ProjectInput, root_causes: List[EvidenceItem], controls: List[EvidenceItem]) -> Dict[str, List[str]]:
    return {
        "baseline": [f"{k}: {v}" for k, v in project.current_metrics.items()],
        "root_cause_hypotheses": [item.statement for item in root_causes],
        "chosen_actions": ["Validate CTQs", "Pilot one improvement", "Create control review cadence"],
        "control_metrics": [item.statement for item in controls],
        "unresolved_risks": ["Missing historical trend data", "Potential stakeholder misalignment"],
    }
