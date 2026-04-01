from __future__ import annotations

from typing import Any, Dict

import json
from pathlib import Path
import streamlit as st

from ui.coaching import render_input_coaching

SAMPLE_PATH = Path("examples/sample_project.json")


def load_sample_project() -> Dict[str, Any] | None:
    if not SAMPLE_PATH.exists():
        return None
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def _join_lines(values: list[str] | None) -> str:
    return "\n".join(values or [])


def _metrics_to_text(metrics: dict[str, str] | None) -> str:
    if not metrics:
        return ""
    return "\n".join(f"{k}={v}" for k, v in metrics.items())


def parse_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_metrics(text: str) -> dict[str, str]:
    metrics: dict[str, str] = {}
    for line in parse_lines(text):
        if "=" in line:
            key, value = line.split("=", 1)
            metrics[key.strip()] = value.strip()
        else:
            metrics[line] = ""
    return metrics


def collect_project_input(defaults: Dict[str, Any] | None = None) -> Dict[str, Any]:
    defaults = defaults or {}

    # ── Row 1: Project name ───────────────────────────────────────────────────
    st.markdown("#### Project identity")
    col_name, col_hint = st.columns([3, 2])
    with col_name:
        project_name = st.text_input(
            "Project name *",
            value=defaults.get("project_name", ""),
            placeholder="e.g. Assembly Line B Defect Rate Reduction — Q3 2025",
            help="A short, descriptive name. Include the area, metric, and quarter/year.",
        )
    with col_hint:
        st.write("")
        render_input_coaching("project_name")

    st.markdown("---")

    # ── Row 2: Problem statement ──────────────────────────────────────────────
    st.markdown("#### Problem statement")
    col_prob, col_prob_coach = st.columns([3, 2])
    with col_prob:
        problem_statement = st.text_area(
            "Problem statement *",
            value=defaults.get("problem_statement", ""),
            height=130,
            placeholder=(
                "e.g. Defect rate on Assembly Line B increased from 2.1% to 4.8% "
                "over the last 3 months, causing rework costs of $45K/month and 2 customer escalations."
            ),
            help="The single most important field. Include: metric, before/after values, timeframe, scope, business impact.",
        )
    with col_prob_coach:
        st.write("")
        render_input_coaching("problem_statement")

    st.markdown("---")

    # ── Row 3: Symptoms & Metrics ─────────────────────────────────────────────
    st.markdown("#### Symptoms and metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.caption("📋 Current symptoms")
        current_symptoms = st.text_area(
            "One observable symptom per line",
            value=_join_lines(defaults.get("current_symptoms", [])),
            height=130,
            placeholder=(
                "Rework volumes up 40% since March\n"
                "3 customer escalations in last 30 days\n"
                "Overtime increased 15 hrs/week"
            ),
            label_visibility="collapsed",
        )
        render_input_coaching("current_symptoms")

    with col2:
        st.caption("📊 Current metrics (name=value)")
        current_metrics_text = st.text_area(
            "One metric per line as name=value",
            value=_metrics_to_text(defaults.get("current_metrics", {})),
            height=130,
            placeholder=(
                "defect_rate_pct=4.8\n"
                "rework_cost_monthly_usd=45000\n"
                "customer_escalations_30d=3"
            ),
            label_visibility="collapsed",
        )
        render_input_coaching("current_metrics")

    st.markdown("---")

    # ── Row 4: Constraints & Stakeholders ─────────────────────────────────────
    st.markdown("#### Context")
    col3, col4 = st.columns(2)

    with col3:
        st.caption("🚧 Constraints (one per line)")
        constraints = st.text_area(
            "Constraints",
            value=_join_lines(defaults.get("constraints", [])),
            height=110,
            placeholder=(
                "No capital approval until Q4\n"
                "Team available 10% FTE max\n"
                "Cannot stop production line"
            ),
            label_visibility="collapsed",
        )
        render_input_coaching("constraints")

    with col4:
        st.caption("👥 Stakeholder concerns (one per line)")
        stakeholder_concerns = st.text_area(
            "Stakeholder concerns",
            value=_join_lines(defaults.get("stakeholder_concerns", [])),
            height=110,
            placeholder=(
                "Plant Manager: shipment delays causing contract risk\n"
                "Finance: rework cost must be under $20K/month by Q4\n"
                "Quality Lead: wants permanent fix, not a workaround"
            ),
            label_visibility="collapsed",
        )
        render_input_coaching("stakeholder_concerns")

    return {
        "project_name":         project_name,
        "problem_statement":    problem_statement,
        "current_symptoms":     parse_lines(current_symptoms),
        "current_metrics":      parse_metrics(current_metrics_text),
        "constraints":          parse_lines(constraints),
        "stakeholder_concerns": parse_lines(stakeholder_concerns),
    }
