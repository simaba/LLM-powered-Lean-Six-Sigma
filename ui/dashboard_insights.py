from __future__ import annotations

import re
from typing import Any

import altair as alt
import pandas as pd

from src.models import AssessmentResult, ProjectInput

# ── Shared colour palette ─────────────────────────────────────────────────────

_BLUE   = "#4361EE"
_NAVY   = "#1E1B4B"
_GREEN  = "#06D6A0"
_AMBER  = "#FFB703"
_RED    = "#EF233C"
_PURPLE = "#7B2FBE"
_TEAL   = "#0EA5E9"
_GRAY   = "#94A3B8"

_PHASE_COLOURS = {
    "define":  "#3B82F6",
    "measure": "#8B5CF6",
    "analyze": "#F59E0B",
    "improve": "#10B981",
    "control": "#06B6D4",
}


# ── Data builders ─────────────────────────────────────────────────────────────

def _parse_metric_value(raw: str) -> float:
    if raw is None:
        return 0.0
    match = re.search(r"-?\d+(?:\.\d+)?", str(raw).strip())
    return float(match.group()) if match else 0.0


def build_metric_dataframe(project: ProjectInput) -> pd.DataFrame:
    rows = []
    for name, value in project.current_metrics.items():
        numeric = _parse_metric_value(value)
        label = name.replace("_", " ").title()
        # Build a simple projected target: 15% better than current
        target = numeric * 0.85 if numeric else 0.0
        rows.append({"metric": label, "current": numeric, "target": target, "raw": value})
    return pd.DataFrame(rows)


def build_action_dataframe(result: AssessmentResult) -> pd.DataFrame:
    """Assigns heuristic impact/effort scores so the matrix chart always renders."""
    _PRESETS = [
        (8, 2, "Quick Win"),
        (7, 5, "Priority"),
        (9, 7, "Structural"),
        (6, 3, "Quick Win"),
        (5, 6, "Priority"),
        (8, 8, "Structural"),
    ]
    rows: list[dict[str, Any]] = []
    for idx, item in enumerate(result.improvement_actions):
        impact, effort, group = _PRESETS[idx % len(_PRESETS)]
        short = item.statement[:55] + "…" if len(item.statement) > 55 else item.statement
        rows.append({"action": short, "impact": impact, "effort": effort, "group": group})
    return pd.DataFrame(rows)


def build_root_cause_dataframe(result: AssessmentResult) -> pd.DataFrame:
    """Assigns heuristic weights for the Pareto chart."""
    weights = [35, 25, 18, 12, 6, 4]
    rows = []
    for idx, item in enumerate(result.root_causes):
        short = item.statement[:60] + "…" if len(item.statement) > 60 else item.statement
        rows.append({"root_cause": short, "weight": weights[idx % len(weights)]})
    return pd.DataFrame(rows)


def build_evidence_dataframe(result: AssessmentResult) -> pd.DataFrame:
    all_items = (
        result.ctqs
        + result.root_causes
        + result.suggested_metrics
        + result.improvement_actions
        + result.control_plan
        + [item for items in result.dmaic_structure.values() for item in items]
    )
    counts = {"Supported": 0, "Inferred": 0, "Missing": 0}
    for item in all_items:
        if "supported" in item.evidence_tag:
            counts["Supported"] += 1
        elif "missing" in item.evidence_tag:
            counts["Missing"] += 1
        else:
            counts["Inferred"] += 1
    return pd.DataFrame([{"type": k, "count": v} for k, v in counts.items()])


def build_priority_dataframe(result: AssessmentResult) -> pd.DataFrame:
    counts: dict[str, int] = {"High": 0, "Medium": 0, "Low": 0}
    for row in result.action_tracker:
        p = str(row.get("priority", "medium")).strip().title()
        if p in counts:
            counts[p] += 1
    return pd.DataFrame([{"priority": k, "count": v} for k, v in counts.items() if v > 0])


def build_dmaic_coverage_dataframe(result: AssessmentResult) -> pd.DataFrame:
    rows = [
        {"phase": phase.upper(), "items": len(items), "colour": _PHASE_COLOURS.get(phase, _BLUE)}
        for phase, items in result.dmaic_structure.items()
    ]
    return pd.DataFrame(rows)


# ── Charts ────────────────────────────────────────────────────────────────────

def metric_bar_chart(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color=_BLUE)
        .encode(
            x=alt.X("metric:N", title=None, axis=alt.Axis(labelAngle=-20, labelLimit=120)),
            y=alt.Y("current:Q", title="Current value", axis=alt.Axis(grid=True)),
            tooltip=[
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("current:Q", title="Current value"),
                alt.Tooltip("raw:N", title="Original"),
            ],
        )
        .properties(title="Baseline metrics", height=260)
    )


def target_gap_chart(df: pd.DataFrame) -> alt.Chart:
    melted = df.melt(
        id_vars=["metric"], value_vars=["current", "target"],
        var_name="series", value_name="value",
    )
    colour_scale = alt.Scale(
        domain=["current", "target"], range=[_BLUE, _GREEN]
    )
    return (
        alt.Chart(melted)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("metric:N", title=None, axis=alt.Axis(labelAngle=-20, labelLimit=120)),
            y=alt.Y("value:Q", title="Value"),
            xOffset=alt.XOffset("series:N"),
            color=alt.Color("series:N", scale=colour_scale, title="Series"),
            tooltip=["metric:N", "series:N", alt.Tooltip("value:Q", format=".1f")],
        )
        .properties(title="Current vs projected target (-15%)", height=260)
    )


def action_matrix_chart(df: pd.DataFrame) -> alt.Chart:
    """Impact vs Effort scatter with quadrant guides and labels."""
    mid = 5.0

    # Quadrant guideline rules
    v_rule = (
        alt.Chart(pd.DataFrame({"x": [mid]}))
        .mark_rule(color="#D1D5DB", strokeDash=[5, 3], strokeWidth=1.5)
        .encode(x="x:Q")
    )
    h_rule = (
        alt.Chart(pd.DataFrame({"y": [mid]}))
        .mark_rule(color="#D1D5DB", strokeDash=[5, 3], strokeWidth=1.5)
        .encode(y="y:Q")
    )

    # Quadrant labels
    quad_df = pd.DataFrame([
        {"x": 1.8, "y": 9.2, "label": "Quick Wins"},
        {"x": 7.8, "y": 9.2, "label": "Big Bets"},
        {"x": 1.8, "y": 0.8, "label": "Fill-ins"},
        {"x": 7.8, "y": 0.8, "label": "Avoid"},
    ])
    quad_labels = (
        alt.Chart(quad_df)
        .mark_text(color="#CBD5E1", fontSize=10, fontStyle="italic", fontWeight=600)
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[0, 10])),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 10])),
            text="label:N",
        )
    )

    colour_scale = alt.Scale(
        domain=["Quick Win", "Priority", "Structural"],
        range=[_GREEN, _BLUE, _AMBER],
    )
    scatter = (
        alt.Chart(df)
        .mark_circle(opacity=0.88)
        .encode(
            x=alt.X("effort:Q", title="Implementation Effort  →", scale=alt.Scale(domain=[0, 10])),
            y=alt.Y("impact:Q", title="Expected Impact  ↑", scale=alt.Scale(domain=[0, 10])),
            color=alt.Color("group:N", scale=colour_scale, title="Category"),
            size=alt.value(300),
            tooltip=[
                alt.Tooltip("action:N", title="Action"),
                alt.Tooltip("impact:Q", title="Impact score"),
                alt.Tooltip("effort:Q", title="Effort score"),
                alt.Tooltip("group:N", title="Category"),
            ],
        )
    )

    return (
        alt.layer(v_rule, h_rule, quad_labels, scatter)
        .properties(title="Impact vs Effort Matrix", height=320)
    )


def pareto_chart(df: pd.DataFrame) -> alt.Chart:
    ordered = df.sort_values("weight", ascending=False).copy()
    ordered["cumulative"] = ordered["weight"].cumsum() / ordered["weight"].sum() * 100

    bars = (
        alt.Chart(ordered)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color=_BLUE)
        .encode(
            x=alt.X(
                "root_cause:N", sort=None, title=None,
                axis=alt.Axis(labelAngle=-30, labelLimit=140),
            ),
            y=alt.Y("weight:Q", title="Relative weight", axis=alt.Axis(grid=True)),
            tooltip=[
                alt.Tooltip("root_cause:N", title="Root cause"),
                alt.Tooltip("weight:Q", title="Weight"),
                alt.Tooltip("cumulative:Q", title="Cumulative %", format=".0f"),
            ],
        )
    )
    line = (
        alt.Chart(ordered)
        .mark_line(
            point=alt.OverlayMarkDef(color=_RED, size=50, filled=True),
            color=_RED,
            strokeWidth=2,
        )
        .encode(
            x=alt.X("root_cause:N", sort=None),
            y=alt.Y(
                "cumulative:Q",
                title="Cumulative %",
                axis=alt.Axis(grid=False),
            ),
        )
    )
    return (
        alt.layer(bars, line)
        .resolve_scale(y="independent")
        .properties(title="Root Cause Concentration (Pareto)", height=320)
    )


def evidence_distribution_chart(df: pd.DataFrame) -> alt.Chart:
    colour_scale = alt.Scale(
        domain=["Supported", "Inferred", "Missing"],
        range=[_GREEN, _AMBER, _RED],
    )
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=48, outerRadius=80, stroke="white", strokeWidth=2)
        .encode(
            theta=alt.Theta("count:Q", stack=True),
            color=alt.Color(
                "type:N",
                scale=colour_scale,
                legend=alt.Legend(title="Evidence type", orient="right"),
            ),
            tooltip=["type:N", "count:Q"],
        )
        .properties(title="Evidence quality breakdown", height=220)
    )


def dmaic_phase_chart(df: pd.DataFrame) -> alt.Chart:
    colour_scale = alt.Scale(
        domain=["DEFINE", "MEASURE", "ANALYZE", "IMPROVE", "CONTROL"],
        range=[
            _PHASE_COLOURS["define"], _PHASE_COLOURS["measure"],
            _PHASE_COLOURS["analyze"], _PHASE_COLOURS["improve"],
            _PHASE_COLOURS["control"],
        ],
    )
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusEnd=5)
        .encode(
            x=alt.X("items:Q", title="Number of items"),
            y=alt.Y("phase:N", sort=None, title=None),
            color=alt.Color("phase:N", scale=colour_scale, legend=None),
            tooltip=["phase:N", alt.Tooltip("items:Q", title="Items")],
        )
        .properties(title="DMAIC Phase Coverage", height=180)
    )


def priority_distribution_chart(df: pd.DataFrame) -> alt.Chart:
    colour_scale = alt.Scale(
        domain=["High", "Medium", "Low"],
        range=[_RED, _AMBER, _GREEN],
    )
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=48, outerRadius=80, stroke="white", strokeWidth=2)
        .encode(
            theta=alt.Theta("count:Q", stack=True),
            color=alt.Color(
                "priority:N",
                scale=colour_scale,
                legend=alt.Legend(title="Priority", orient="right"),
            ),
            tooltip=["priority:N", "count:Q"],
        )
        .properties(title="Action priority distribution", height=220)
    )


def control_plan_table(result: AssessmentResult) -> pd.DataFrame:
    owners = ["PM", "Process Owner", "Quality Lead", "Operations Lead", "Team Manager"]
    cadence = ["Weekly", "Weekly", "Bi-weekly", "Monthly", "Bi-weekly"]
    triggers = [
        "2 consecutive misses below target",
        "Threshold breach > 10%",
        "Escalation recurrence in same cycle",
        "Missed review for > 4 weeks",
        "Metric trend worsening 3 weeks straight",
    ]
    rows = []
    for idx, item in enumerate(result.control_plan):
        rows.append({
            "Control Item": item.statement,
            "Owner": owners[idx % len(owners)],
            "Cadence": cadence[idx % len(cadence)],
            "Trigger": triggers[idx % len(triggers)],
        })
    return pd.DataFrame(rows)


def executive_bullets(result: AssessmentResult) -> list[str]:
    return [
        f"Problem: {result.cleaned_problem_statement}",
        f"Top root cause: {result.root_causes[0].statement if result.root_causes else 'Not available'}",
        f"Priority action: {result.improvement_actions[0].statement if result.improvement_actions else 'Not available'}",
        f"Key control focus: {result.control_plan[0].statement if result.control_plan else 'Not available'}",
        f"Main unresolved risk: {result.project_memory.get('unresolved_risks', ['Not available'])[0]}",
    ]
