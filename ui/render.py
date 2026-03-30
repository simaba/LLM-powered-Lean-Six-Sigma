from __future__ import annotations

import streamlit as st

from src.models import AssessmentResult


def render_header_cards(result: AssessmentResult) -> None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CTQs", len(result.ctqs))
    with col2:
        st.metric("Improvement actions", len(result.improvement_actions))
    with col3:
        st.metric("Control plan items", len(result.control_plan))


def render_assessment_tabs(result: AssessmentResult) -> None:
    tabs = st.tabs(["Overview", "DMAIC", "Root Cause", "Improvements", "Control Plan", "Executive Summary"])

    with tabs[0]:
        st.subheader("Cleaned-up problem statement")
        st.write(result.cleaned_problem_statement)
        st.subheader("Likely CTQs")
        for item in result.ctqs:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.subheader("SIPOC draft")
        st.json(result.sipoc)

    with tabs[1]:
        for phase_name, items in result.dmaic_structure.items():
            st.markdown(f"### {phase_name.title()}")
            for item in items:
                st.write(f"- {item.statement} [{item.evidence_tag}]")

    with tabs[2]:
        st.subheader("Possible root causes")
        for item in result.root_causes:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.subheader("Project memory")
        st.json(result.project_memory)

    with tabs[3]:
        st.subheader("Suggested metrics to track")
        for item in result.suggested_metrics:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.subheader("Suggested improvement actions")
        for item in result.improvement_actions:
            st.write(f"- {item.statement} [{item.evidence_tag}]")
        st.subheader("Action tracker")
        st.table(result.action_tracker)

    with tabs[4]:
        st.subheader("Control plan draft")
        for item in result.control_plan:
            st.write(f"- {item.statement} [{item.evidence_tag}]")

    with tabs[5]:
        st.subheader("Role-aware summary")
        st.write(result.role_summary)
