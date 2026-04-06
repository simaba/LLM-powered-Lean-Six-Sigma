"""
tool_recommender.py
===================
Streamlit UI module providing a "Tool Recommender Wizard" for the
LLM-powered Lean Six Sigma application.

The wizard presents 7 diagnostic questions, then recommends the best-fit
LSS tool or approach plus up to 3 supporting tools — with rationale,
required inputs, expected outputs, effort estimate, and cautions.

Public API
----------
render_tool_recommender() -> None
    Renders the entire tool recommender UI.
"""
from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Colour palette — matches the app's global design system
# ---------------------------------------------------------------------------
_BLUE  = "#4361EE"
_NAVY  = "#1E1B4B"
_GREEN = "#06D6A0"
_AMBER = "#FFB703"
_RED   = "#EF233C"
_GRAY  = "#94A3B8"
_BG    = "#F1F4FB"


# ---------------------------------------------------------------------------
# CSS injection
# ---------------------------------------------------------------------------
_CSS = """
<style>
.rec-primary-card {
    background: #FFFFFF;
    border-left: 5px solid #4361EE;
    border-radius: 12px;
    padding: 24px 28px;
    box-shadow: 0 4px 16px rgba(67, 97, 238, 0.10);
    margin-bottom: 8px;
}
.rec-primary-card h2 {
    font-size: 1.6rem;
    color: #1E1B4B;
    margin: 0 0 10px 0;
}
.rec-primary-card .rationale {
    font-size: 0.95rem;
    color: #374151;
    line-height: 1.6;
    margin-bottom: 16px;
}
.rec-supporting-card {
    background: #F8FAFF;
    border: 1px solid #C7D2FE;
    border-radius: 10px;
    padding: 14px 16px;
    height: 100%;
}
.rec-caution-box {
    background: #FFFBEB;
    border-left: 4px solid #FFB703;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 4px;
}
.rec-effort-badge {
    display: inline-block;
    background: #EEF2FF;
    color: #3730A3;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.83rem;
    font-weight: 600;
    margin-top: 4px;
    margin-bottom: 16px;
}
</style>
"""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _pill(text: str, bg: str, color: str = "#fff") -> str:
    """Return an HTML span styled as a pill badge."""
    return (
        f'<span style="background:{bg};color:{color};padding:6px 12px;'
        f'border-radius:20px;font-size:0.85rem;font-weight:500;'
        f'display:inline-block;margin:4px 0;">{text}</span>'
    )


def _bullet_list_html(items: list[str], color: str = "#1E293B") -> str:
    """Return an HTML unordered list from a list of strings."""
    lis = "".join(
        f'<li style="margin:5px 0;font-size:0.88rem;color:{color};">{item}</li>'
        for item in items
    )
    return f'<ul style="margin:0;padding-left:18px;">{lis}</ul>'


# ---------------------------------------------------------------------------
# Recommendation engine
# ---------------------------------------------------------------------------
def _compute_recommendation(
    q1: str, q2: str, q3: str, q4: str, q5: str, q6: str, q7: str
) -> dict:
    """Pure-Python decision tree that maps diagnostic answers to the best LSS tool.

    Parameters
    ----------
    q1 : Problem type
    q2 : Data availability
    q3 : Scope
    q4 : Speed needed
    q5 : Measurement system confidence
    q6 : Root cause status
    q7 : Team LSS experience level

    Returns
    -------
    dict with keys: primary_tool, primary_icon, primary_rationale,
    what_you_need, what_you_get, supporting_tools, estimated_effort,
    cautions, next_step_in_app, next_step_label.
    """

    # ------------------------------------------------------------------
    # Shared defaults for DMAIC (reused in several branches)
    # ------------------------------------------------------------------
    def _dmaic() -> dict:
        return {
            "primary_tool": "DMAIC Project",
            "primary_icon": "🔄",
            "primary_rationale": (
                "With limited data, a structured DMAIC project is the right approach. "
                "The Measure phase will build your data collection plan and validate the "
                "measurement system before any analysis."
            ),
            "what_you_need": [
                "Problem statement with scope and baseline metric",
                "Process map or SIPOC",
                "Data collection plan",
                "Stakeholder list",
            ],
            "what_you_get": [
                "Structured improvement roadmap",
                "Root cause analysis",
                "Prioritised improvement actions",
                "Control plan",
            ],
            "supporting_tools": [
                {
                    "name": "FMEA",
                    "icon": "⚠️",
                    "why": "Risk-rank potential failure modes before selecting solutions",
                },
                {
                    "name": "MSA / Gauge R&R",
                    "icon": "🎯",
                    "why": "Validate measurement system in the Measure phase",
                },
            ],
            "estimated_effort": "4-12 weeks Green Belt project",
            "cautions": [
                "Don't skip Measure — jumping to solutions is the #1 cause of DMAIC failure",
                "Define the problem scope before starting",
            ],
            "next_step_in_app": "wizard",
            "next_step_label": "Open Project Wizard → select 'DMAIC' mode",
        }

    # ------------------------------------------------------------------
    # Shared defaults for Lean Flow (reused for slow process AND waste)
    # ------------------------------------------------------------------
    def _lean_flow() -> dict:
        return {
            "primary_tool": "Lean Flow / Value Stream Analysis",
            "primary_icon": "🌊",
            "primary_rationale": (
                "Speed problems are almost always caused by non-value-added steps, "
                "excessive wait times, and poor flow. Value stream mapping surfaces the "
                "waste and Little's Law quantifies WIP and throughput."
            ),
            "what_you_need": [
                "List of all process steps",
                "Cycle time for each step",
                "Wait/queue time between steps",
                "Customer demand rate (units/day or week)",
            ],
            "what_you_get": [
                "Value stream map with VA vs NVA time",
                "Process Cycle Efficiency (PCE%)",
                "Bottleneck identification",
                "Takt time vs cycle time comparison",
                "Specific waste elimination recommendations",
            ],
            "supporting_tools": [
                {
                    "name": "SPC Charts",
                    "icon": "📈",
                    "why": "Monitor lead time and cycle time after improvement",
                },
                {
                    "name": "Hypothesis Testing",
                    "icon": "🔬",
                    "why": "Confirm lead time reduction is statistically significant",
                },
            ],
            "estimated_effort": "1-3 weeks (mapping + analysis)",
            "cautions": [
                "Map the current state honestly — don't map the ideal state",
                "Include wait times — they're usually 60-90% of lead time",
            ],
            "next_step_in_app": "workbench",
            "next_step_label": "Open Analytics Workbench → Lean Flow tab",
        }

    # ------------------------------------------------------------------
    # Shared defaults for Control Plan (reused for two q6/q1 branches)
    # ------------------------------------------------------------------
    def _control_plan() -> dict:
        return {
            "primary_tool": "Control Plan",
            "primary_icon": "🛡️",
            "primary_rationale": (
                "You've done the hard work — now the priority is sustaining gains. "
                "A control plan with defined owners, SPC monitoring, and escalation "
                "triggers prevents regression."
            ),
            "what_you_need": [
                "Validated improvement actions",
                "Defined control metrics and limits",
                "Process owners identified",
                "Audit/review schedule",
            ],
            "what_you_get": [
                "Structured control plan document",
                "SPC monitoring setup",
                "Escalation triggers",
                "Sustainability roadmap",
            ],
            "supporting_tools": [
                {
                    "name": "SPC Charts",
                    "icon": "📈",
                    "why": "Monitor key metrics in real-time for out-of-control signals",
                },
                {
                    "name": "Hypothesis Testing",
                    "icon": "🔬",
                    "why": "Confirm the improvement is statistically significant before closing out",
                },
            ],
            "estimated_effort": "1-2 weeks",
            "cautions": [
                "Ensure measurement system is validated before setting control limits",
                "Control limits ≠ specification limits",
            ],
            "next_step_in_app": "wizard",
            "next_step_label": "Open Project Wizard → select 'Control Plan' mode",
        }

    # ------------------------------------------------------------------
    # Decision tree — highest-priority checks first
    # ------------------------------------------------------------------

    # Root cause + solution known → Control Plan
    if q6 == "Root cause and solution are known — need to implement and sustain":
        return _control_plan()

    # Explicit intent to sustain/control
    if q1 == "Need to sustain / control recent gains":
        return _control_plan()

    # Defect/error problem
    if q1 == "Too many defects or errors":
        if q2 in [
            "Good data — months of history, 30+ data points",
            "Lots of data — automated / ongoing process data",
        ]:
            # Check measurement system first
            if q5 != "Measurement system is validated (MSA / Gauge R&R done)":
                return {
                    "primary_tool": "MSA / Gauge R&R",
                    "primary_icon": "🎯",
                    "primary_rationale": (
                        "Before analysing defect data, validate that your measurement "
                        "system is capable. If Gauge R&R is poor (>30% GRR), your defect "
                        "data is unreliable. Fix the measurement before the process."
                    ),
                    "what_you_need": [
                        "2-3 operators",
                        "10 representative parts/samples",
                        "Measurement procedure documented",
                        "Spec limits (USL/LSL)",
                    ],
                    "what_you_get": [
                        "%GRR (target <10% for critical, <30% acceptable)",
                        "Number of distinct categories (NDC ≥ 5)",
                        "Repeatability vs reproducibility breakdown",
                        "Go/no-go on measurement system",
                    ],
                    "supporting_tools": [
                        {
                            "name": "Process Capability",
                            "icon": "📊",
                            "why": (
                                "Run after MSA passes — Cp/Cpk tells you if the "
                                "process itself is capable"
                            ),
                        },
                        {
                            "name": "SPC Charts",
                            "icon": "📈",
                            "why": (
                                "Set up ongoing monitoring once measurement system "
                                "is validated"
                            ),
                        },
                    ],
                    "estimated_effort": "1-3 days for study + 1 day analysis",
                    "cautions": [
                        "Study under real production conditions (not ideal)",
                        "Include all sources of variation (shifts, operators)",
                    ],
                    "next_step_in_app": "workbench",
                    "next_step_label": "Open Analytics Workbench → MSA / Gauge R&R tab",
                }
            else:
                # MSA already done — go straight to capability
                return {
                    "primary_tool": "Process Capability",
                    "primary_icon": "📊",
                    "primary_rationale": (
                        "With validated data, process capability analysis tells you "
                        "exactly how your process compares to specification. Cp/Cpk "
                        "quantifies the gap and Sigma level shows you where you stand "
                        "vs world class."
                    ),
                    "what_you_need": [
                        "30+ measurements from stable process",
                        "Spec limits (USL and/or LSL)",
                        "Validated measurement system",
                    ],
                    "what_you_get": [
                        "Cp, Cpk (within-subgroup capability)",
                        "Pp, Ppk (overall performance)",
                        "Sigma level and DPMO",
                        "Capability histogram with normal overlay",
                    ],
                    "supporting_tools": [
                        {
                            "name": "SPC Charts",
                            "icon": "📈",
                            "why": (
                                "Check process stability before running capability — "
                                "unstable process = meaningless Cpk"
                            ),
                        },
                        {
                            "name": "Hypothesis Testing",
                            "icon": "🔬",
                            "why": (
                                "Compare before vs after capability to confirm "
                                "improvement is real"
                            ),
                        },
                    ],
                    "estimated_effort": "1-2 days with existing data",
                    "cautions": [
                        "Process must be stable (in statistical control) before calculating Cpk",
                        "Check normality — non-normal data needs transformation or non-parametric Ppk",
                    ],
                    "next_step_in_app": "workbench",
                    "next_step_label": "Open Analytics Workbench → Process Capability tab",
                }
        else:
            # Limited data — start a DMAIC project
            return _dmaic()

    # Lead time / speed problem
    if q1 == "Process is too slow / long lead times":
        return _lean_flow()

    # Variation / inconsistency
    if q1 == "Results are inconsistent / too much variation":
        if q2 in [
            "Good data — months of history, 30+ data points",
            "Lots of data — automated / ongoing process data",
        ]:
            return {
                "primary_tool": "SPC Charts",
                "primary_icon": "📈",
                "primary_rationale": (
                    "For variation problems with good data, SPC charts reveal whether "
                    "variation is common cause (inherent to the process) or special cause "
                    "(assignable, fixable). This distinction drives the right response."
                ),
                "what_you_need": [
                    "Time-ordered measurement data (30+ points)",
                    "Subgroup structure (if applicable)",
                    "Measurement system validated",
                ],
                "what_you_get": [
                    "I-MR, Xbar-R, or p-chart depending on data type",
                    "Nelson rule violations flagged",
                    "Common cause vs special cause classification",
                    "Control limits (UCL/LCL)",
                ],
                "supporting_tools": [
                    {
                        "name": "Process Capability",
                        "icon": "📊",
                        "why": "Quantify how much variation exceeds spec limits",
                    },
                    {
                        "name": "Regression",
                        "icon": "📉",
                        "why": "Identify which input variables are driving the output variation",
                    },
                ],
                "estimated_effort": "1-3 days with existing data",
                "cautions": [
                    "SPC requires time-ordered data — don't re-sort it",
                    "Control limits are calculated from the data — don't use spec limits as substitutes",
                ],
                "next_step_in_app": "workbench",
                "next_step_label": "Open Analytics Workbench → SPC Charts tab",
            }
        else:
            # Limited data — start with root cause analysis
            return {
                "primary_tool": "Root Cause Analysis",
                "primary_icon": "🌿",
                "primary_rationale": (
                    "Without solid data, structured root cause analysis is the right "
                    "starting point. A 5 Whys chain and fishbone diagram will guide your "
                    "measurement plan so you collect the right data."
                ),
                "what_you_need": [
                    "Clear problem statement with a specific metric",
                    "Process knowledge from operators",
                    "Any available defect/incident records",
                ],
                "what_you_get": [
                    "5 Whys chain to verified root cause",
                    "Fishbone diagram (6Ms)",
                    "Prioritised hypotheses for validation",
                    "Targeted data collection plan",
                ],
                "supporting_tools": [
                    {
                        "name": "SPC Charts",
                        "icon": "📈",
                        "why": "Set up monitoring once you know what to measure",
                    },
                    {
                        "name": "Hypothesis Testing",
                        "icon": "🔬",
                        "why": "Statistically confirm root cause hypotheses",
                    },
                ],
                "estimated_effort": "1-2 weeks",
                "cautions": [
                    "Stop at the first 'why' that can be validated with data",
                    "Avoid jumping to solutions during root cause analysis",
                ],
                "next_step_in_app": "wizard",
                "next_step_label": "Open Project Wizard → select 'Root Cause' mode",
            }

    # Waste identification
    if q1 == "We know there's waste but can't pinpoint it":
        return _lean_flow()

    # Understanding drivers of an outcome
    if q1 == "Need to understand what's driving an outcome (Y)":
        if q7 in [
            "Green Belt — can run structured projects",
            "Black Belt — full statistical toolkit",
        ]:
            return {
                "primary_tool": "Regression Analysis",
                "primary_icon": "📉",
                "primary_rationale": (
                    "When you have a clear output variable (Y) and suspect multiple input "
                    "variables (Xs), regression quantifies each X's contribution, tests "
                    "significance, and identifies which inputs actually move the needle."
                ),
                "what_you_need": [
                    "Dataset with Y column and at least 2-3 X columns",
                    "20+ data points (more = better)",
                    "X variables that can realistically be changed",
                ],
                "what_you_get": [
                    "Regression equation (Y = b0 + b1X1 + ...)",
                    "R² and adjusted R²",
                    "Statistical significance (p-values) for each X",
                    "Diagnostics (VIF for multicollinearity, residual plots)",
                ],
                "supporting_tools": [
                    {
                        "name": "DOE",
                        "icon": "🧪",
                        "why": (
                            "Confirm cause-and-effect by deliberately varying Xs "
                            "in a controlled experiment"
                        ),
                    },
                    {
                        "name": "Hypothesis Testing",
                        "icon": "🔬",
                        "why": (
                            "Test individual X vs Y relationships before running "
                            "full regression"
                        ),
                    },
                ],
                "estimated_effort": "2-5 days with existing data",
                "cautions": [
                    "Correlation ≠ causation — use DOE to confirm",
                    "Check multicollinearity (VIF > 5 is a warning sign)",
                ],
                "next_step_in_app": "workbench",
                "next_step_label": "Open Analytics Workbench → Regression tab",
            }
        else:
            return {
                "primary_tool": "Hypothesis Testing",
                "primary_icon": "🔬",
                "primary_rationale": (
                    "For teams newer to statistics, hypothesis testing is the right "
                    "starting point. It answers specific yes/no questions: 'Is there a "
                    "difference between shifts?' 'Did the improvement work?' — with "
                    "statistical confidence."
                ),
                "what_you_need": [
                    "Two or more groups/conditions to compare",
                    "Measurement data for each group (15+ per group)",
                    "A specific question to answer",
                ],
                "what_you_get": [
                    "p-value (< 0.05 = statistically significant)",
                    "Confidence intervals",
                    "Plain-English interpretation",
                    "Effect size (practical significance)",
                ],
                "supporting_tools": [
                    {
                        "name": "Regression",
                        "icon": "📉",
                        "why": "Once you know which Xs matter, regression quantifies how much",
                    },
                    {
                        "name": "SPC Charts",
                        "icon": "📈",
                        "why": "Monitor the key driver over time",
                    },
                ],
                "estimated_effort": "1-2 days",
                "cautions": [
                    "Statistical significance ≠ practical significance — check effect size",
                    "Sample size matters — small samples can miss real differences",
                ],
                "next_step_in_app": "workbench",
                "next_step_label": "Open Analytics Workbench → Hypothesis Testing tab",
            }

    # Proactive failure prevention
    if q1 == "Need to prevent future failures":
        return {
            "primary_tool": "FMEA",
            "primary_icon": "⚠️",
            "primary_rationale": (
                "FMEA (Failure Mode & Effects Analysis) is the proactive tool of choice. "
                "It systematically identifies what could go wrong, rates "
                "severity/occurrence/detection, and prioritises risk reduction actions."
            ),
            "what_you_need": [
                "Process steps or product functions listed",
                "Team with process knowledge (3-5 people)",
                "Historical failure data if available (improves Occurrence ratings)",
            ],
            "what_you_get": [
                "Risk Priority Numbers (RPN = S×O×D) for each failure mode",
                "Risk matrix (high/medium/low)",
                "Pareto of top risks",
                "Recommended actions with responsibility and timing",
            ],
            "supporting_tools": [
                {
                    "name": "DOE",
                    "icon": "🧪",
                    "why": "Validate that recommended actions actually reduce failure rates",
                },
                {
                    "name": "SPC Charts",
                    "icon": "📈",
                    "why": "Monitor high-RPN items after control actions are in place",
                },
            ],
            "estimated_effort": "2-5 days (team workshop)",
            "cautions": [
                "Don't do FMEA alone — you'll miss failure modes",
                "Update ratings after implementing actions — re-score the FMEA",
            ],
            "next_step_in_app": "workbench",
            "next_step_label": "Open Analytics Workbench → FMEA tab",
        }

    # "Not sure" or any other / fallback
    return _dmaic()


# ---------------------------------------------------------------------------
# Public render function
# ---------------------------------------------------------------------------
def render_tool_recommender() -> None:
    """Render the Tool Recommender Wizard UI.

    Presents 7 diagnostic questions and, on submission, computes and displays
    a primary LSS tool recommendation plus up to 3 supporting tools.
    """
    # Inject CSS
    st.markdown(_CSS, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------
    st.markdown(
        f'<h2 style="color:{_NAVY};margin-bottom:4px;">🧭 What problem are you solving?</h2>'
        f'<p style="color:{_GRAY};font-size:0.95rem;margin-top:0;margin-bottom:24px;">'
        f'Answer a few questions and we\'ll recommend the best approach for your situation.'
        f'</p>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # Initialise session state keys (avoids KeyError on first run)
    # -----------------------------------------------------------------------
    _defaults: dict[str, object] = {
        "rec_submitted": False,
        "rec_q1": None,
        "rec_q2": None,
        "rec_q3": None,
        "rec_q4": None,
        "rec_q5": None,
        "rec_q6": None,
        "rec_q7": None,
    }
    for key, val in _defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # -----------------------------------------------------------------------
    # Step 1 — Diagnostic questions (shown when not yet submitted)
    # -----------------------------------------------------------------------
if not st.session_state["rec_submitted"]:
    st.radio(
        "What kind of problem are you dealing with?",
        options=[
            "Too many defects or errors",
            "Process is too slow / long lead times",
            "Results are inconsistent / too much variation",
            "We know there's waste but can't pinpoint it",
            "Need to understand what's driving an outcome (Y)",
            "Need to prevent future failures",
            "Need to sustain / control recent gains",
            "Not sure — I just know something is wrong",
        ],
        key="rec_q1",
    )

    st.radio(
        "How much data do you have?",
        options=[
            "None yet — haven't started measuring",
            "Some data — a few weeks / small sample",
            "Good data — months of history, 30+ data points",
            "Lots of data — automated / ongoing process data",
        ],
        key="rec_q2",
    )

    st.radio(
        "What is the scope of the problem?",
        options=[
            "Single machine, station, or step",
            "End-to-end process (multiple steps or departments)",
            "Product or service line",
            "Organisation-wide",
        ],
        key="rec_q3",
    )

    st.radio(
        "How urgently do you need a result?",
        options=[
            "Immediate — something needs fixing this week",
            "Short-term — 1-4 weeks",
            "Medium-term — 1-3 months project",
            "Long-term — formal improvement programme",
        ],
        key="rec_q4",
    )

    st.radio(
        "How confident are you in your measurement system?",
        options=[
            "We have no formal measurement",
            "We measure but haven't validated the measurement system",
            "We've done a basic gauge check",
            "Measurement system is validated (MSA / Gauge R&R done)",
        ],
        key="rec_q5",
    )

    st.radio(
        "Do you know the root cause?",
        options=[
            "No idea — haven't investigated yet",
            "Have some hunches but not confirmed",
            "Root cause is known but solution is unclear",
            "Root cause and solution are known — need to implement and sustain",
        ],
        key="rec_q6",
    )

    st.radio(
        "What is your team's LSS experience level?",
        options=[
            "No prior LSS training",
            "Yellow Belt — familiar with basics",
            "Green Belt — can run structured projects",
            "Black Belt — full statistical toolkit",
        ],
        key="rec_q7",
    )
        st.divider()

        if st.button("🔍 Find my best approach →", type="primary"):
            st.session_state["rec_submitted"] = True
            st.rerun()

        return  # Don't render the output section until submitted

    # -----------------------------------------------------------------------
    # Step 2 — Show recommendation
    # -----------------------------------------------------------------------
    q1 = st.session_state.get("rec_q1", "")
    q2 = st.session_state.get("rec_q2", "")
    q3 = st.session_state.get("rec_q3", "")
    q4 = st.session_state.get("rec_q4", "")
    q5 = st.session_state.get("rec_q5", "")
    q6 = st.session_state.get("rec_q6", "")
    q7 = st.session_state.get("rec_q7", "")

    rec = _compute_recommendation(q1, q2, q3, q4, q5, q6, q7)

    # -----------------------------------------------------------------------
    # Primary recommendation card (HTML)
    # -----------------------------------------------------------------------
    need_html  = _bullet_list_html(rec["what_you_need"])
    get_html   = _bullet_list_html(rec["what_you_get"])

    card_html = (
        f'<div class="rec-primary-card">'
        f'<h2>{rec["primary_icon"]} {rec["primary_tool"]}</h2>'
        f'<p class="rationale">{rec["primary_rationale"]}</p>'
        f'<div style="display:flex;gap:24px;flex-wrap:wrap;">'
        # Left column — what you need
        f'<div style="flex:1;min-width:220px;">'
        f'<p style="font-weight:700;color:{_NAVY};font-size:0.88rem;'
        f'text-transform:uppercase;letter-spacing:0.05em;margin:0 0 6px 0;">'
        f'📋 What you need</p>'
        f'{need_html}'
        f'</div>'
        # Right column — what you get
        f'<div style="flex:1;min-width:220px;">'
        f'<p style="font-weight:700;color:{_NAVY};font-size:0.88rem;'
        f'text-transform:uppercase;letter-spacing:0.05em;margin:0 0 6px 0;">'
        f'✅ What you get</p>'
        f'{get_html}'
        f'</div>'
        f'</div>'
        # Effort badge
        f'<div style="margin-top:18px;">'
        f'<span class="rec-effort-badge">⏱ Estimated effort: {rec["estimated_effort"]}</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # "Open in App" button
    # -----------------------------------------------------------------------
    if st.button(
        f'Open in App → {rec["next_step_label"]}',
        type="primary",
        key="rec_open_in_app",
    ):
        st.session_state["app_mode"] = rec["next_step_in_app"]
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Supporting tools section
    # -----------------------------------------------------------------------
    supporting = rec.get("supporting_tools", [])
    if supporting:
        st.markdown(
            f'<p style="font-weight:700;color:{_NAVY};font-size:1rem;margin-bottom:12px;">'
            f'🔧 Supporting tools to consider</p>',
            unsafe_allow_html=True,
        )

        cols = st.columns(len(supporting))
        for col, tool in zip(cols, supporting):
            with col:
                col.markdown(
                    f'<div class="rec-supporting-card">'
                    f'<p style="font-size:1.5rem;margin:0 0 6px 0;">{tool["icon"]}</p>'
                    f'<p style="font-weight:700;color:{_NAVY};font-size:0.9rem;'
                    f'margin:0 0 4px 0;">{tool["name"]}</p>'
                    f'<p style="font-size:0.82rem;color:#475569;margin:0;">{tool["why"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Cautions section — amber callout
    # -----------------------------------------------------------------------
    cautions = rec.get("cautions", [])
    if cautions:
        caution_items = "".join(
            f'<li style="margin:6px 0;font-size:0.88rem;color:#92400E;">{c}</li>'
            for c in cautions
        )
        st.markdown(
            f'<div class="rec-caution-box">'
            f'<p style="font-weight:700;color:#B45309;font-size:0.88rem;'
            f'margin:0 0 8px 0;text-transform:uppercase;letter-spacing:0.04em;">'
            f'⚠️ Things to check first</p>'
            f'<ul style="margin:0;padding-left:18px;">{caution_items}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Start over button
    # -----------------------------------------------------------------------
    if st.button("↩ Start over", key="rec_start_over"):
        st.session_state["rec_submitted"] = False
        st.rerun()
