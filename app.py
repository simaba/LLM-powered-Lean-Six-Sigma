from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from src.engine import run_assessment
from src.models import ProjectInput
from src.renderers import render_markdown_summary


st.set_page_config(page_title="LLM-powered Lean Six Sigma", layout="wide")

st.title("LLM-powered Lean Six Sigma")
st.caption("Turn messy project problems into structured improvement plans.")

with st.sidebar:
    st.header("Settings")
    mode = st.selectbox(
        "Mode",
        ["dmaic", "kaizen", "root_cause", "process_waste", "control_plan"],
        index=0,
    )
    audience = st.selectbox(
        "Audience",
        ["engineer", "pm", "manager", "quality_lead", "executive"],
        index=1,
    )

st.subheader("Project input")

col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input("Project name", value="Audit Preparation Improvement")
    problem_statement = st.text_area(
        "Problem statement",
        value="Audit preparation is late, reactive, and requires repeated rework across teams.",
        height=120,
    )
    current_symptoms = st.text_area(
        "Current symptoms (one per line)",
        value="Repeated last-minute requests\nHigh rework on submitted materials\nUnclear ownership across handoffs",
        height=120,
    )
with col2:
    current_metrics_text = st.text_area(
        "Current metrics (one per line as name=value)",
        value="on_time_completion_rate=62%\nrework_rate=28%\naverage_cycle_time_days=14",
        height=120,
    )
    constraints = st.text_area(
        "Constraints (one per line)",
        value="Limited team capacity\nFixed audit deadlines",
        height=120,
    )
    stakeholder_concerns = st.text_area(
        "Stakeholder concerns (one per line)",
        value="Need clearer accountability\nNeed fewer escalation loops\nNeed more predictable delivery",
        height=120,
    )


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


if st.button("Generate Lean Six Sigma assessment", type="primary"):
    project = ProjectInput(
        project_name=project_name,
        problem_statement=problem_statement,
        current_symptoms=parse_lines(current_symptoms),
        current_metrics=parse_metrics(current_metrics_text),
        constraints=parse_lines(constraints),
        stakeholder_concerns=parse_lines(stakeholder_concerns),
    )

    result = run_assessment(project, mode=mode, audience=audience)
    markdown_output = render_markdown_summary(result)

    overview_tab, dmaic_tab, root_tab, improve_tab, control_tab, exec_tab = st.tabs(
        ["Overview", "DMAIC", "Root Cause", "Improvements", "Control Plan", "Summary"]
    )

    with overview_tab:
        st.markdown("### Cleaned-up problem statement")
        st.write(result.cleaned_problem_statement)
        st.markdown("### Likely CTQs")
        for item in result.ctqs:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.markdown("### SIPOC")
        st.json(result.sipoc)

    with dmaic_tab:
        for phase_name, items in result.dmaic_structure.items():
            st.markdown(f"### {phase_name.title()}")
            for item in items:
                st.write(f"- {item.statement} [{item.evidence_tag}]")

    with root_tab:
        st.markdown("### Possible root causes")
        for item in result.root_causes:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.markdown("### Project memory")
        st.json(result.project_memory)

    with improve_tab:
        st.markdown("### Suggested metrics")
        for item in result.suggested_metrics:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.markdown("### Suggested improvement actions")
        for item in result.improvement_actions:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.markdown("### Action tracker")
        st.table(result.action_tracker)

    with control_tab:
        st.markdown("### Control plan draft")
        for item in result.control_plan:
            st.write(f"- {item.statement} [{item.evidence_tag}]")

    with exec_tab:
        st.markdown("### Role-aware summary")
        st.write(result.role_summary)
        st.download_button(
            "Download markdown summary",
            markdown_output,
            file_name="lean_six_sigma_summary.md",
            mime="text/markdown",
        )

    st.markdown("---")
    st.markdown("### Full markdown output")
    st.code(markdown_output, language="markdown")
