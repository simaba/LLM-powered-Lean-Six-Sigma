"""
tollgate.py
===========
Streamlit UI module for DMAIC Tollgate Readiness Checklists.

Renders interactive checklists for each of the five DMAIC phases, scores
readiness, flags risks, and lets the user export a plain-text tollgate summary.

Public API
----------
render_tollgate() -> None
"""
from __future__ import annotations

from datetime import date

import streamlit as st

# ---------------------------------------------------------------------------
# Phase configuration — colour, icon, subtitle, abbreviation
# ---------------------------------------------------------------------------
_PHASES: list[dict] = [
    {
        "name":     "Define",
        "abbrev":   "def",
        "icon":     "📋",
        "color":    "#3B82F6",
        "subtitle": "Gate: Is the problem clearly defined, scoped, and sponsored?",
    },
    {
        "name":     "Measure",
        "abbrev":   "mea",
        "icon":     "📏",
        "color":    "#8B5CF6",
        "subtitle": "Gate: Is the measurement system validated and baseline established?",
    },
    {
        "name":     "Analyze",
        "abbrev":   "ana",
        "icon":     "🔬",
        "color":    "#F59E0B",
        "subtitle": "Gate: Are root causes identified and statistically confirmed?",
    },
    {
        "name":     "Improve",
        "abbrev":   "imp",
        "icon":     "⚙️",
        "color":    "#22C55E",
        "subtitle": "Gate: Is the solution piloted, validated, and ready to implement?",
    },
    {
        "name":     "Control",
        "abbrev":   "ctl",
        "icon":     "🛡️",
        "color":    "#14B8A6",
        "subtitle": "Gate: Is the process handed over with ongoing monitoring in place?",
    },
]

# ---------------------------------------------------------------------------
# Checklist items per phase
# ---------------------------------------------------------------------------
_CHECKLIST: dict[str, list[str]] = {
    "def": [
        "Problem statement written with specific metric and baseline value",
        "Business case / financial impact quantified",
        "Project scope defined (what is IN and OUT of scope)",
        "SIPOC diagram completed",
        "Voice of Customer (VOC) data collected",
        "CTQs (Critical-to-Quality) identified and linked to VOC",
        "Goal statement is SMART (Specific, Measurable, Achievable, Relevant, Time-bound)",
        "Project team defined with roles and % availability",
        "Sponsor/Champion identified and committed",
        "Project charter reviewed and approved by sponsor",
        "Project plan with milestones drafted",
        "Key stakeholders identified and communication plan in place",
    ],
    "mea": [
        "Process map (detailed, current state) completed",
        "Measurement system validated (MSA / Gauge R&R performed)",
        "%GRR is acceptable (< 30% study variation, < 10% for critical measures)",
        "Baseline data collected (minimum 30 data points or 30 days)",
        "Baseline capability calculated (Cp, Cpk, Sigma level, or DPMO)",
        "Process is confirmed stable (SPC chart shows no special causes)",
        "Data collection plan documented (who, what, where, when, how)",
        "Measurement operational definitions documented",
        "Baseline metric validated against financial impact",
        "Stratification analysis completed (by shift, line, product, etc.)",
        "Data integrity verified (no missing values, outliers investigated)",
        "Measure phase tollgate reviewed by Champion",
    ],
    "ana": [
        "Root causes hypothesised from fishbone / 5 Whys",
        "Root cause hypotheses tested with data (not just opinion)",
        "Statistical significance confirmed (hypothesis tests performed)",
        "Vital few Xs identified from the many (Pareto, regression, or DOE)",
        "Root cause verified at gemba (direct observation)",
        "Failure modes reviewed (FMEA started or updated)",
        "Process waste identified and quantified (TIMWOODS or VSM)",
        "Baseline sigma level validated against Measure phase findings",
        "Root causes linked back to the problem statement metric",
        "Team consensus on top 3 root causes documented",
        "Analyze phase tollgate reviewed by Champion",
    ],
    "imp": [
        "Multiple solution options generated (at least 3 considered)",
        "Solutions evaluated against criteria (impact, cost, effort, risk)",
        "Pilot / trial of top solution(s) completed",
        "Pilot results show statistically significant improvement",
        "Improved capability quantified (new Cpk, Sigma level, DPMO)",
        "Risk assessment of solutions completed (FMEA updated with actions)",
        "Implementation plan documented with owners and dates",
        "Financial benefit confirmed with Finance / Sponsor",
        "Solution root cause linkage verified (X→Y relationship confirmed)",
        "Change management plan in place (training, communications)",
        "Improve phase tollgate reviewed by Champion",
    ],
    "ctl": [
        "Control plan documented (metric, method, frequency, owner, response)",
        "Control limits set (UCL/LCL based on improved process data, NOT spec limits)",
        "SPC charts or dashboards implemented and running",
        "Response plan for out-of-control signals defined and tested",
        "Process documentation / SOPs updated",
        "Operators and relevant staff trained on new process",
        "Mistake-proofing (Poka-yoke) implemented where feasible",
        "Handover to process owner completed",
        "Benefits realised and validated with Finance (hard savings confirmed)",
        "30/60/90 day monitoring plan in place",
        "Project closure report completed",
        "Lessons learned documented and shared",
    ],
}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _phase_banner_html(phase: dict) -> str:
    """Return the styled phase header banner as an HTML string."""
    color    = phase["color"]
    icon     = phase["icon"]
    name     = phase["name"]
    subtitle = phase["subtitle"]
    return (
        f'<div style="background:{color}15; border-left: 4px solid {color}; '
        f'border-radius: 0 10px 10px 0; padding: 12px 18px; margin-bottom: 16px;">'
        f'<span style="color:{color}; font-weight:800; font-size:1.1em;">'
        f'{icon} {name} PHASE TOLLGATE</span><br>'
        f'<span style="color:#64748B; font-size:0.88em;">{subtitle}</span>'
        f'</div>'
    )


def _score_card_html(checked: int, total: int, color: str) -> str:
    """Return a styled score card HTML block."""
    pct = int(checked / total * 100) if total else 0

    if pct >= 86:
        traffic = "🟢"
        status  = "Ready to proceed"
        bg      = "#ECFDF5"
        border  = "#6EE7B7"
        text    = "#065F46"
    elif pct >= 60:
        traffic = "🟡"
        status  = "Partially ready"
        bg      = "#FFFBEB"
        border  = "#FCD34D"
        text    = "#92400E"
    else:
        traffic = "🔴"
        status  = "Not ready"
        bg      = "#FEF2F2"
        border  = "#FCA5A5"
        text    = "#991B1B"

    return (
        f'<div style="background:{bg}; border:1px solid {border}; '
        f'border-radius:10px; padding:14px 20px; margin:16px 0;">'
        f'<span style="font-size:1.5rem;">{traffic}</span>'
        f'<span style="font-weight:700; color:{text}; font-size:1rem; margin-left:8px;">'
        f'{status}</span>'
        f'<br>'
        f'<span style="color:#475569; font-size:0.88rem;">'
        f'{checked} of {total} items complete — {pct}% ready</span>'
        f'</div>'
    )


def _unchecked_items_html(items: list[str]) -> str:
    """Return an amber-styled bulleted list of outstanding items."""
    if not items:
        return ""
    bullets = "".join(
        f'<li style="margin:5px 0; font-size:0.87rem; color:#92400E;">{item}</li>'
        for item in items
    )
    return (
        f'<div style="background:#FFFBEB; border:1px solid #FCD34D; '
        f'border-radius:8px; padding:12px 18px; margin-top:8px;">'
        f'<p style="font-weight:700; color:#B45309; font-size:0.85rem; '
        f'text-transform:uppercase; letter-spacing:0.05em; margin:0 0 8px 0;">'
        f'⚠️ Outstanding items below must be resolved before proceeding:</p>'
        f'<ul style="margin:0; padding-left:18px;">{bullets}</ul>'
        f'</div>'
    )


def _phase_score_card_html(phase_name: str, checked: int, total: int, color: str) -> str:
    """Return a compact metric card HTML for the overall summary row."""
    pct = int(checked / total * 100) if total else 0
    if pct >= 86:
        badge, badge_bg, badge_text = "🟢", "#ECFDF5", "#065F46"
    elif pct >= 60:
        badge, badge_bg, badge_text = "🟡", "#FFFBEB", "#92400E"
    else:
        badge, badge_bg, badge_text = "🔴", "#FEF2F2", "#991B1B"

    return (
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; '
        f'border-top:4px solid {color}; border-radius:10px; '
        f'padding:14px 12px; text-align:center; '
        f'box-shadow:0 1px 3px rgba(0,0,0,0.06);">'
        f'<p style="font-weight:700; color:{color}; font-size:0.9rem; margin:0 0 4px 0;">'
        f'{phase_name}</p>'
        f'<p style="font-size:1.6rem; font-weight:800; color:#1E293B; margin:0 0 4px 0;">'
        f'{pct}%</p>'
        f'<span style="background:{badge_bg}; color:{badge_text}; '
        f'font-size:0.78rem; padding:3px 8px; border-radius:12px; font-weight:600;">'
        f'{badge} {checked}/{total}</span>'
        f'</div>'
    )


def _build_export_text(phase_states: list[dict]) -> str:
    """Build the plain-text tollgate summary string."""
    today = date.today().strftime("%Y-%m-%d")
    lines: list[str] = [
        "DMAIC TOLLGATE READINESS SUMMARY",
        f"Generated: {today}",
        "",
    ]

    all_unchecked: list[str] = []
    total_checked = 0
    total_items   = 0

    for ps in phase_states:
        phase_name   = ps["name"]
        n_done       = ps["checked"]
        n_total      = ps["total"]
        score        = int(n_done / n_total * 100) if n_total else 0
        unchecked    = ps["unchecked"]

        total_checked += n_done
        total_items   += n_total
        all_unchecked.extend(unchecked)

        lines.append(f"{phase_name.upper()}: {score}% ({n_done}/{n_total} items)")
        if unchecked:
            for item in unchecked:
                lines.append(f"  ☐ {item}")
        else:
            lines.append("  All items complete.")
        lines.append("")

    overall_pct = int(total_checked / total_items * 100) if total_items else 0
    lines.append(f"OVERALL READINESS: {overall_pct}%")

    if all_unchecked:
        lines.append("OUTSTANDING RISKS:")
        for item in all_unchecked:
            lines.append(f"- {item}")
    else:
        lines.append("OUTSTANDING RISKS: None — all items complete.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-phase tab renderer
# ---------------------------------------------------------------------------

def _render_phase_tab(phase: dict) -> dict:
    """Render all content for one phase tab. Returns state dict."""
    abbrev  = phase["abbrev"]
    items   = _CHECKLIST[abbrev]
    color   = phase["color"]

    # Phase banner
    st.markdown(_phase_banner_html(phase), unsafe_allow_html=True)

    # Checklist
    checked_items:   list[str] = []
    unchecked_items: list[str] = []

    for i, item in enumerate(items):
        key   = f"tg_{abbrev}_{i}"
        value = st.checkbox(item, key=key)
        if value:
            checked_items.append(item)
        else:
            unchecked_items.append(item)

    n_checked = len(checked_items)
    n_total   = len(items)

    # Score card
    st.markdown(_score_card_html(n_checked, n_total, color), unsafe_allow_html=True)

    # Risk list (unchecked items)
    if unchecked_items:
        st.markdown(
            _unchecked_items_html(unchecked_items),
            unsafe_allow_html=True,
        )

    # Phase notes
    st.text_area(
        "Phase notes (optional)",
        placeholder="Add any observations, blockers, or context for this phase gate...",
        key=f"tg_{abbrev}_notes",
        height=90,
    )

    return {
        "name":      phase["name"],
        "abbrev":    abbrev,
        "color":     color,
        "checked":   n_checked,
        "total":     n_total,
        "unchecked": unchecked_items,
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render_tollgate() -> None:
    """Render the DMAIC Tollgate Readiness Checklist page."""

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        '<h2 style="color:#1E293B; margin-bottom:2px;">🚦 DMAIC Tollgate Readiness</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#64748B; font-size:0.93rem; margin-top:0;">'
        'Review your readiness at each phase gate before moving forward. '
        'Unresolved items become risks.</p>',
        unsafe_allow_html=True,
    )

    # ── Phase tabs ───────────────────────────────────────────────────────────
    tab_labels = [p["name"] for p in _PHASES]
    tabs       = st.tabs(tab_labels)

    phase_states: list[dict] = []
    for tab, phase in zip(tabs, _PHASES):
        with tab:
            state = _render_phase_tab(phase)
            phase_states.append(state)

    # ── Overall summary ──────────────────────────────────────────────────────
    st.divider()

    st.markdown(
        '<p style="font-weight:700; color:#1E1B4B; font-size:1rem; margin-bottom:12px;">'
        '📊 Overall Phase Readiness</p>',
        unsafe_allow_html=True,
    )

    summary_cols = st.columns(len(_PHASES))
    for col, ps in zip(summary_cols, phase_states):
        with col:
            st.markdown(
                _phase_score_card_html(
                    ps["name"],
                    ps["checked"],
                    ps["total"],
                    ps["color"],
                ),
                unsafe_allow_html=True,
            )

    # ── Outstanding risks across all phases ─────────────────────────────────
    all_unchecked = [
        (ps["name"], item)
        for ps in phase_states
        for item in ps["unchecked"]
    ]

    with st.expander("⚠️ Outstanding risks across all phases", expanded=bool(all_unchecked)):
        if not all_unchecked:
            st.markdown(
                '<p style="color:#065F46; font-size:0.9rem;">'
                '✅ No outstanding risks — all items across all phases are complete.</p>',
                unsafe_allow_html=True,
            )
        else:
            risk_rows = "".join(
                f'<tr>'
                f'<td style="padding:6px 10px; font-weight:600; color:{next(p["color"] for p in _PHASES if p["name"] == phase_name)}; '
                f'font-size:0.85rem; white-space:nowrap;">{phase_name}</td>'
                f'<td style="padding:6px 10px; font-size:0.85rem; color:#1E293B;">{item}</td>'
                f'</tr>'
                for phase_name, item in all_unchecked
            )
            st.markdown(
                f'<table style="width:100%; border-collapse:collapse; margin-top:4px;">'
                f'<thead><tr>'
                f'<th style="text-align:left; padding:6px 10px; color:#64748B; '
                f'font-size:0.8rem; border-bottom:1px solid #E2E8F0;">Phase</th>'
                f'<th style="text-align:left; padding:6px 10px; color:#64748B; '
                f'font-size:0.8rem; border-bottom:1px solid #E2E8F0;">Outstanding item</th>'
                f'</tr></thead>'
                f'<tbody>{risk_rows}</tbody>'
                f'</table>',
                unsafe_allow_html=True,
            )

    # ── Export ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📄 Export Tollgate Summary", type="primary"):
        export_text = _build_export_text(phase_states)
        st.download_button(
            label="⬇️ Download tollgate_summary.txt",
            data=export_text,
            file_name="tollgate_summary.txt",
            mime="text/plain",
        )
