"""
analytics_workbench.py
======================
Streamlit UI for the LSS Black Belt Analytics Workbench.

Provides interactive UIs for all nine analytics modules:
  1. Data Hub         — upload CSV / XLSX, preview, select columns
  2. Capability       — Cp / Cpk / Pp / Ppk / sigma / DPM
  3. MSA / Gauge R&R  — repeatability & reproducibility, NDC
  4. Hypothesis Tests — 7 guided tests with plain-English results
  5. SPC Charts       — I-MR, Xbar-R, p-chart with Nelson rules
  6. FMEA             — RPN builder, risk matrix, Pareto
  7. Regression       — simple & multiple OLS with diagnostics
  8. DOE              — factor definition, design recommendation
  9. Benefits / COPQ  — ROI, payback, NPV, waterfall chart
 10. Lean Flow        — takt time, VSM, bottleneck, PCE, Little's Law

Entry point: call ``render_analytics_workbench()`` from app.py.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st

# ── Analytics imports ────────────────────────────────────────────────────────

from analytics.capability import run_capability, capability_histogram
from analytics.hypothesis_tests import (
    one_sample_t, two_sample_t, paired_t,
    one_proportion, two_proportion,
    chi_square_independence, one_way_anova,
)
from analytics.spc import imr_chart, xbar_r_chart, p_chart
from analytics.msa import run_gauge_rr, gauge_rr_chart
from analytics.fmea import (
    FMEAEntry, new_entry, fmea_to_dataframe,
    fmea_risk_matrix_chart, fmea_pareto_chart,
)
from analytics.benefits import (
    CostOfQualityEntry, run_benefits_analysis,
    copq_waterfall_chart, savings_timeline_chart,
)
from analytics.regression import (
    simple_regression, multiple_regression,
    regression_scatter_chart, residual_plot,
)
from analytics.doe import DOEFactor, recommend_design, design_matrix_chart
from analytics.lean_flow import (
    ProcessStep, run_lean_flow_analysis,
    value_stream_chart, utilisation_chart,
    pce_gauge_html, waste_waterfall_chart,
)


# ── Shared helpers ────────────────────────────────────────────────────────────

def _section(title: str, icon: str = "") -> None:
    prefix = f"{icon} " if icon else ""
    st.markdown(
        f'<h3 style="color:#1E1B4B;font-size:1.15em;font-weight:800;'
        f'margin:0 0 4px 0;letter-spacing:-0.01em">{prefix}{title}</h3>',
        unsafe_allow_html=True,
    )


def _info_card(text: str, colour: str = "#EEF2FF") -> None:
    st.markdown(
        f'<div style="background:{colour};border-radius:10px;padding:12px 16px;'
        f'font-size:0.88em;color:#374151;line-height:1.6;margin-bottom:12px">'
        f'{text}</div>',
        unsafe_allow_html=True,
    )


def _result_metric(label: str, value: str, delta: str = "") -> None:
    """Render a small metric tile."""
    delta_html = (
        f'<span style="font-size:0.78em;color:#64748B;margin-left:6px">{delta}</span>'
        if delta else ""
    )
    st.markdown(
        f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;'
        f'padding:12px 16px;margin-bottom:8px">'
        f'<div style="font-size:0.75em;font-weight:700;color:#64748B;text-transform:uppercase;'
        f'letter-spacing:0.06em;margin-bottom:4px">{label}</div>'
        f'<div style="font-size:1.5em;font-weight:800;color:#1E1B4B">{value}{delta_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _verdict_badge(reject: bool, alpha: float = 0.05) -> None:
    if reject:
        st.markdown(
            '<div style="background:#DCFCE7;border:1px solid #86EFAC;border-radius:10px;'
            'padding:12px 16px;color:#166534;font-weight:700;font-size:0.93em">'
            f'✓ H₀ rejected (α = {alpha}) — statistically significant result'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="background:#FEF9C3;border:1px solid #FDE68A;border-radius:10px;'
            'padding:12px 16px;color:#854D0E;font-weight:700;font-size:0.93em">'
            f'○ H₀ not rejected (α = {alpha}) — insufficient evidence to detect difference'
            '</div>',
            unsafe_allow_html=True,
        )


def _parse_numeric_series(text: str) -> np.ndarray:
    """Parse comma- or newline-separated numbers from a text area."""
    import re
    tokens = re.split(r"[,\n\r\t;]+", text.strip())
    vals = []
    for t in tokens:
        t = t.strip()
        if t:
            try:
                vals.append(float(t))
            except ValueError:
                pass
    return np.array(vals)


def _get_uploaded_df() -> Optional[pd.DataFrame]:
    return st.session_state.get("wb_df")


def _col_select(df: pd.DataFrame, label: str, key: str,
                numeric_only: bool = True) -> Optional[str]:
    cols = df.select_dtypes(include="number").columns.tolist() if numeric_only else df.columns.tolist()
    if not cols:
        st.warning("No suitable columns found in the uploaded data.")
        return None
    return st.selectbox(label, cols, key=key)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Data Hub
# ─────────────────────────────────────────────────────────────────────────────

def _tab_data_hub() -> None:
    _section("Data Hub", "📂")
    _info_card(
        "Upload a <strong>CSV</strong> or <strong>Excel (.xlsx)</strong> file containing your process data. "
        "Once uploaded the data is available across all analytics tabs in this session. "
        "You can also paste raw numbers directly in any tab — no file needed."
    )

    uploaded = st.file_uploader(
        "Drop your data file here",
        type=["csv", "xlsx"],
        key="wb_uploader",
        help="CSV or Excel file. First row should be column headers.",
    )

    if uploaded is not None:
        try:
            if uploaded.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded)
            else:
                df = pd.read_csv(uploaded)

            st.session_state["wb_df"] = df
            st.success(f"✓  Loaded **{uploaded.name}** — {len(df):,} rows × {len(df.columns)} columns")

            st.markdown("#### Preview (first 20 rows)")
            st.dataframe(df.head(20), use_container_width=True)

            num_cols = df.select_dtypes(include="number").columns.tolist()
            cat_cols = df.select_dtypes(exclude="number").columns.tolist()
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Numeric columns ({len(num_cols)})**")
                if num_cols:
                    st.dataframe(df[num_cols].describe().T.round(4), use_container_width=True)
            with c2:
                st.markdown(f"**Categorical / text columns ({len(cat_cols)})**")
                if cat_cols:
                    summary = pd.DataFrame({
                        "Unique": [df[c].nunique() for c in cat_cols],
                        "Top value": [
                            str(df[c].value_counts().index[0]) if df[c].nunique() > 0 else ""
                            for c in cat_cols
                        ],
                    }, index=cat_cols)
                    st.dataframe(summary, use_container_width=True)

        except Exception as exc:
            st.error(f"Could not read file: {exc}")

    elif st.session_state.get("wb_df") is not None:
        df = st.session_state["wb_df"]
        st.info(f"Using previously uploaded data — {len(df):,} rows × {len(df.columns)} columns")
        if st.button("Clear data", key="wb_clear"):
            del st.session_state["wb_df"]
            st.rerun()
    else:
        st.markdown(
            '<div style="border:2px dashed #C7D2FE;border-radius:12px;padding:40px;'
            'text-align:center;color:#94A3B8;background:#F8FAFF">'
            '<div style="font-size:2em;margin-bottom:8px">📊</div>'
            '<div style="font-weight:600">No data uploaded yet</div>'
            '<div style="font-size:0.88em;margin-top:4px">Upload a file above, or paste numbers directly in any analytics tab</div>'
            '</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 2. Process Capability
# ─────────────────────────────────────────────────────────────────────────────

def _tab_capability() -> None:
    _section("Process Capability", "📐")
    _info_card(
        "Computes <strong>Cp, Cpk</strong> (short-term / within sigma) and "
        "<strong>Pp, Ppk</strong> (long-term / overall sigma), plus sigma level and DPM. "
        "Enter your process data and specification limits below."
    )

    df = _get_uploaded_df()
    src = st.radio("Data source", ["Paste numbers", "Uploaded file column"],
                    horizontal=True, key="cap_src")

    data_arr: Optional[np.ndarray] = None

    if src == "Paste numbers":
        raw = st.text_area("Process measurements (comma or newline separated)",
                            height=100, placeholder="e.g.  10.2, 10.5, 9.8, 10.1 …",
                            key="cap_paste")
        if raw.strip():
            data_arr = _parse_numeric_series(raw)
    else:
        if df is not None:
            col = _col_select(df, "Select measurement column", "cap_col")
            if col:
                data_arr = df[col].dropna().to_numpy()
        else:
            st.warning("Upload data in the **Data Hub** tab first, or choose 'Paste numbers'.")

    col1, col2, col3 = st.columns(3)
    with col1:
        lsl_str = st.text_input("Lower Spec Limit (LSL)", value="", key="cap_lsl",
                                 placeholder="leave blank if one-sided")
    with col2:
        usl_str = st.text_input("Upper Spec Limit (USL)", value="", key="cap_usl",
                                 placeholder="leave blank if one-sided")
    with col3:
        tgt_str = st.text_input("Target / nominal", value="", key="cap_tgt",
                                 placeholder="optional")

    lsl = float(lsl_str) if lsl_str.strip() else None
    usl = float(usl_str) if usl_str.strip() else None
    tgt = float(tgt_str) if tgt_str.strip() else None

    if st.button("▶ Run Capability Analysis", type="primary", key="cap_run"):
        if data_arr is None or len(data_arr) < 5:
            st.error("Please provide at least 5 data points.")
            return
        if lsl is None and usl is None:
            st.error("At least one specification limit (LSL or USL) is required.")
            return

        with st.spinner("Calculating …"):
            try:
                result = run_capability(data_arr, lsl=lsl, usl=usl, target=tgt)
            except Exception as e:
                st.error(f"Calculation error: {e}")
                return

        st.markdown("---")
        st.markdown("#### Results")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            _result_metric("Cp",  f"{result.cp:.3f}"  if result.cp  is not None else "—")
            _result_metric("Pp",  f"{result.pp:.3f}"  if result.pp  is not None else "—")
        with m2:
            _result_metric("Cpk", f"{result.cpk:.3f}" if result.cpk is not None else "—")
            _result_metric("Ppk", f"{result.ppk:.3f}" if result.ppk is not None else "—")
        with m3:
            _result_metric("Sigma level",
                           f"{result.sigma_level:.2f}σ" if result.sigma_level is not None else "—")
            _result_metric("DPM", f"{result.dpm:,}")
        with m4:
            _result_metric("Mean", f"{result.mean:.4g}")
            _result_metric("n", str(result.n))

        cpk_val = result.cpk
        if cpk_val is not None:
            if cpk_val >= 1.67:
                label, colour = "World-class (Six Sigma)", "#DCFCE7"
            elif cpk_val >= 1.33:
                label, colour = "Capable — meets specification", "#D1FAE5"
            elif cpk_val >= 1.00:
                label, colour = "Marginally capable — improvement recommended", "#FEF9C3"
            else:
                label, colour = "Not capable — immediate action required", "#FEE2E2"
            st.markdown(
                f'<div style="background:{colour};border-radius:10px;padding:12px 16px;'
                f'font-weight:700;font-size:0.93em;margin:12px 0">'
                f'Capability verdict: {label}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f"**Normality (p = {result.normality_p:.4f}):** "
            + ("data appears normal ✓" if result.is_normal
               else "non-normal distribution ⚠ — interpret indices with caution")
        )

        if result.interpretation:
            st.markdown(
                f'<div class="lss-card-accent" style="margin-top:12px">'
                f'<strong>Interpretation</strong><br>{result.interpretation}</div>',
                unsafe_allow_html=True,
            )

        chart = capability_histogram(data_arr, result)
        st.altair_chart(chart, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. MSA / Gauge R&R
# ─────────────────────────────────────────────────────────────────────────────

def _tab_msa() -> None:
    _section("MSA — Gauge R&R", "🔬")
    _info_card(
        "Measurement System Analysis using the ANOVA method (AIAG MSA-4). "
        "Requires a dataset with <strong>Part</strong>, <strong>Operator</strong>, and "
        "<strong>Measurement</strong> columns (with at least 2 replicates per Part × Operator cell)."
    )

    df = _get_uploaded_df()

    if df is None:
        _info_card(
            "ℹ Upload a file in the <strong>Data Hub</strong> tab first. "
            "Your file should have columns for Part ID, Operator, and the measurement value.",
            colour="#F0F9FF",
        )
        if st.button("Load demo MSA data", key="msa_demo"):
            rng = np.random.default_rng(42)
            parts      = list(range(1, 11)) * 6
            operators  = (["Alice"] * 10 + ["Bob"] * 10 + ["Carol"] * 10) * 2
            true_vals  = {p: rng.normal(100 + p * 2, 0.5) for p in range(1, 11)}
            measurements = [true_vals[p] + rng.normal(0, 0.3) for p in parts]
            st.session_state["wb_df"] = pd.DataFrame({
                "Part": parts, "Operator": operators, "Measurement": measurements,
            })
            st.rerun()
        return

    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include="number").columns.tolist()

    c1, c2, c3 = st.columns(3)
    with c1:
        part_col = st.selectbox("Part column",        all_cols, key="msa_part")
    with c2:
        op_col   = st.selectbox("Operator column",    all_cols, key="msa_op")
    with c3:
        meas_col = st.selectbox("Measurement column", num_cols, key="msa_meas")

    c4, c5 = st.columns(2)
    with c4:
        lsl_str = st.text_input("LSL (optional, for tolerance %GRR)", value="", key="msa_lsl")
    with c5:
        usl_str = st.text_input("USL (optional, for tolerance %GRR)", value="", key="msa_usl")

    lsl = float(lsl_str) if lsl_str.strip() else None
    usl = float(usl_str) if usl_str.strip() else None

    if st.button("▶ Run Gauge R&R", type="primary", key="msa_run"):
        with st.spinner("Running ANOVA …"):
            try:
                result = run_gauge_rr(
                    df,
                    part_col=part_col,
                    operator_col=op_col,
                    measurement_col=meas_col,
                    lsl=lsl,
                    usl=usl,
                )
            except Exception as e:
                st.error(f"Gauge R&R error: {e}")
                return

        st.markdown("---")
        st.markdown("#### Results")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            _result_metric("% GRR (Study)", f"{result.pct_grr_study:.1f}%")
            _result_metric("Repeatability (EV)", f"{result.repeatability_var:.4g}")
        with m2:
            _result_metric("Reproducibility (AV)", f"{result.reproducibility_var:.4g}")
            _result_metric("Part Variation (PV)", f"{result.part_var:.4g}")
        with m3:
            _result_metric("Total Variation (TV)", f"{result.total_var:.4g}")
            _result_metric("NDC", str(result.ndc))
        with m4:
            if result.pct_grr_tolerance > 0:
                _result_metric("% GRR (Tolerance)", f"{result.pct_grr_tolerance:.1f}%")
            _result_metric("Parts", str(result.n_parts))

        grr = result.pct_grr_study
        if grr < 10:
            label, colour = "Excellent — measurement system is adequate", "#DCFCE7"
        elif grr < 30:
            label, colour = "Marginal — may be acceptable depending on application", "#FEF9C3"
        else:
            label, colour = "Unacceptable — measurement system needs improvement", "#FEE2E2"
        st.markdown(
            f'<div style="background:{colour};border-radius:10px;padding:12px 16px;'
            f'font-weight:700;font-size:0.93em;margin:12px 0">'
            f'MSA verdict: {label}</div>',
            unsafe_allow_html=True,
        )

        ndc_colour = "#DCFCE7" if result.ndc >= 5 else "#FEF9C3" if result.ndc >= 2 else "#FEE2E2"
        st.markdown(
            f'<div style="background:{ndc_colour};border-radius:8px;padding:10px 14px;'
            f'font-size:0.88em;margin-bottom:12px">'
            f'<strong>NDC = {result.ndc}</strong> — '
            + ("≥ 5 categories: measurement system can discriminate well between parts." if result.ndc >= 5
               else "< 5 categories: measurement system may not distinguish part-to-part variation.")
            + "</div>",
            unsafe_allow_html=True,
        )

        if result.interpretation:
            st.markdown(f"**Interpretation:** {result.interpretation}")

        try:
            chart = gauge_rr_chart(result, df, part_col, op_col, meas_col)
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.caption(f"Chart unavailable: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Hypothesis Testing
# ─────────────────────────────────────────────────────────────────────────────

_HT_TESTS = {
    "One-sample t-test": "one_sample_t",
    "Two-sample t-test (independent, Welch)": "two_sample_t",
    "Paired t-test": "paired_t",
    "One-proportion z-test": "one_proportion",
    "Two-proportion z-test": "two_proportion",
    "Chi-square independence": "chi_square",
    "One-way ANOVA": "anova",
}


def _tab_hypothesis() -> None:
    _section("Hypothesis Testing", "🧪")
    _info_card(
        "Select a statistical test, enter your data, and receive a plain-English verdict. "
        "Results include the test statistic, p-value, effect size, confidence interval, "
        "assumptions checklist, and a recommended next action."
    )

    test_name = st.selectbox("Select test", list(_HT_TESTS.keys()), key="ht_test")
    alpha = st.select_slider("Significance level (α)", options=[0.01, 0.05, 0.10],
                              value=0.05, key="ht_alpha")

    test_key = _HT_TESTS[test_name]
    result = None

    if test_key == "one_sample_t":
        raw = st.text_area("Sample data (comma / newline separated)", height=80, key="ht_os_data")
        mu0 = st.number_input("Hypothesised mean (μ₀)", value=0.0, key="ht_os_mu")
        if st.button("▶ Run Test", type="primary", key="ht_run_os"):
            arr = _parse_numeric_series(raw)
            if len(arr) < 2:
                st.error("Need at least 2 data points.")
            else:
                with st.spinner("…"):
                    result = one_sample_t(arr, mu0=mu0, alpha=alpha)

    elif test_key == "two_sample_t":
        c1, c2 = st.columns(2)
        with c1:
            raw1 = st.text_area("Group 1 data", height=80, key="ht_ts_d1")
        with c2:
            raw2 = st.text_area("Group 2 data", height=80, key="ht_ts_d2")
        if st.button("▶ Run Test", type="primary", key="ht_run_ts"):
            a1, a2 = _parse_numeric_series(raw1), _parse_numeric_series(raw2)
            if len(a1) < 2 or len(a2) < 2:
                st.error("Need at least 2 data points in each group.")
            else:
                with st.spinner("…"):
                    result = two_sample_t(a1, a2, alpha=alpha)

    elif test_key == "paired_t":
        c1, c2 = st.columns(2)
        with c1:
            raw1 = st.text_area("Before data", height=80, key="ht_pt_d1")
        with c2:
            raw2 = st.text_area("After data", height=80, key="ht_pt_d2")
        if st.button("▶ Run Test", type="primary", key="ht_run_pt"):
            a1, a2 = _parse_numeric_series(raw1), _parse_numeric_series(raw2)
            if len(a1) != len(a2) or len(a1) < 2:
                st.error("Before and After arrays must have the same length (≥ 2).")
            else:
                with st.spinner("…"):
                    result = paired_t(a1, a2, alpha=alpha)

    elif test_key == "one_proportion":
        c1, c2, c3 = st.columns(3)
        with c1:
            x = st.number_input("Successes (x)", min_value=0, value=45, key="ht_op_x")
        with c2:
            n = st.number_input("Sample size (n)", min_value=1, value=100, key="ht_op_n")
        with c3:
            p0 = st.number_input("Hypothesised proportion (p₀)", min_value=0.0, max_value=1.0,
                                   value=0.5, step=0.01, key="ht_op_p0")
        if st.button("▶ Run Test", type="primary", key="ht_run_op"):
            with st.spinner("…"):
                result = one_proportion(int(x), int(n), p0=p0, alpha=alpha)

    elif test_key == "two_proportion":
        c1, c2 = st.columns(2)
        with c1:
            x1 = st.number_input("Group 1 successes (x₁)", min_value=0, value=40, key="ht_tp_x1")
            n1 = st.number_input("Group 1 size (n₁)", min_value=1, value=100, key="ht_tp_n1")
        with c2:
            x2 = st.number_input("Group 2 successes (x₂)", min_value=0, value=55, key="ht_tp_x2")
            n2 = st.number_input("Group 2 size (n₂)", min_value=1, value=100, key="ht_tp_n2")
        if st.button("▶ Run Test", type="primary", key="ht_run_tp"):
            with st.spinner("…"):
                result = two_proportion(int(x1), int(n1), int(x2), int(n2), alpha=alpha)

    elif test_key == "chi_square":
        df_up = _get_uploaded_df()
        if df_up is not None:
            c1, c2 = st.columns(2)
            with c1:
                col_a = _col_select(df_up, "Column A (categorical)", "ht_cs_ca", numeric_only=False)
            with c2:
                col_b = _col_select(df_up, "Column B (categorical)", "ht_cs_cb", numeric_only=False)
            if st.button("▶ Run Test", type="primary", key="ht_run_cs") and col_a and col_b:
                with st.spinner("…"):
                    result = chi_square_independence(df_up[col_a], df_up[col_b], alpha=alpha)
        else:
            st.info("Upload a file in **Data Hub** to use chi-square independence test.")

    elif test_key == "anova":
        n_groups = st.number_input("Number of groups", min_value=2, max_value=8, value=3, key="ht_av_ng")
        groups = []
        cols = st.columns(int(n_groups))
        for i, col in enumerate(cols):
            with col:
                raw = st.text_area(f"Group {i+1}", height=80, key=f"ht_av_g{i}")
                groups.append(raw)
        if st.button("▶ Run Test", type="primary", key="ht_run_av"):
            arrs = [_parse_numeric_series(g) for g in groups]
            if any(len(a) < 2 for a in arrs):
                st.error("Each group needs at least 2 data points.")
            else:
                with st.spinner("…"):
                    result = one_way_anova(*arrs, alpha=alpha)

    if result is not None:
        st.markdown("---")
        st.markdown(f"#### {result.test_name} — Results")

        _verdict_badge(result.reject_h0, alpha)

        m1, m2, m3 = st.columns(3)
        with m1:
            _result_metric("Test statistic", f"{result.statistic:.4f}")
        with m2:
            _result_metric("p-value", f"{result.p_value:.5f}")
        with m3:
            if result.effect_size is not None:
                _result_metric("Effect size", f"{result.effect_size:.4f}")

        if result.confidence_interval:
            lo, hi = result.confidence_interval
            st.markdown(
                f"**{int((1 - alpha) * 100)}% Confidence interval:** [{lo:.4f}, {hi:.4f}]"
            )

        if result.interpretation:
            st.markdown(
                f'<div class="lss-card-accent" style="margin-top:12px">'
                f'<strong>Interpretation</strong><br>{result.interpretation}</div>',
                unsafe_allow_html=True,
            )

        if result.recommended_action:
            st.markdown(
                f'<div style="background:#F0FDF4;border-radius:10px;padding:12px 16px;'
                f'font-size:0.9em;color:#166534;margin-top:8px">'
                f'<strong>→ Recommended next step:</strong> {result.recommended_action}</div>',
                unsafe_allow_html=True,
            )

        if result.assumptions:
            with st.expander("Statistical assumptions"):
                for a in result.assumptions:
                    st.markdown(f"- {a}")

        if result.chart is not None:
            try:
                st.altair_chart(result.chart, use_container_width=True)
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# 5. SPC Charts
# ─────────────────────────────────────────────────────────────────────────────

def _tab_spc() -> None:
    _section("Statistical Process Control", "📈")
    _info_card(
        "Create control charts to detect process instability. "
        "<strong>I-MR</strong> for individual readings; "
        "<strong>Xbar-R</strong> for subgroup data; "
        "<strong>p-chart</strong> for proportion defective. "
        "Out-of-control points and Nelson rule violations are highlighted automatically."
    )

    chart_type = st.radio(
        "Chart type",
        ["I-MR (Individuals + Moving Range)", "Xbar-R (Subgroup mean + Range)", "p-chart (Proportion defective)"],
        horizontal=True,
        key="spc_type",
    )

    df = _get_uploaded_df()

    if "I-MR" in chart_type:
        src = st.radio("Data source", ["Paste numbers", "Uploaded column"],
                        horizontal=True, key="spc_imr_src")
        data_arr = None
        if src == "Paste numbers":
            raw = st.text_area("Individual measurements (comma / newline)", height=80, key="spc_imr_paste")
            if raw.strip():
                data_arr = _parse_numeric_series(raw)
        else:
            if df is not None:
                col = _col_select(df, "Measurement column", "spc_imr_col")
                if col:
                    data_arr = df[col].dropna().to_numpy()
            else:
                st.warning("Upload data in the **Data Hub** tab first.")

        if st.button("▶ Plot I-MR Chart", type="primary", key="spc_imr_run"):
            if data_arr is None or len(data_arr) < 8:
                st.error("Need at least 8 data points for an I-MR chart.")
            else:
                with st.spinner("Building chart …"):
                    try:
                        result, chart = imr_chart(data_arr.tolist())
                        st.altair_chart(chart, use_container_width=True)
                        _spc_summary(result)
                    except Exception as e:
                        st.error(f"SPC error: {e}")

    elif "Xbar-R" in chart_type:
        _info_card(
            "Xbar-R requires data as a flat list of measurements. "
            "They will be grouped into subgroups of the size you specify below.",
            colour="#F0F9FF",
        )
        src = st.radio("Data source", ["Paste numbers", "Uploaded column"],
                        horizontal=True, key="spc_xr_src")
        data_flat = None
        if src == "Paste numbers":
            raw = st.text_area("Measurements (comma / newline)", height=80, key="spc_xr_paste")
            if raw.strip():
                data_flat = _parse_numeric_series(raw)
        else:
            if df is not None:
                num_cols = df.select_dtypes(include="number").columns.tolist()
                meas_col = st.selectbox("Measurement column", num_cols, key="spc_xr_meas")
                data_flat = df[meas_col].dropna().to_numpy()
            else:
                st.warning("Upload data in the **Data Hub** tab first.")

        subgroup_size = st.number_input("Subgroup size (n)", min_value=2, max_value=8,
                                         value=5, key="spc_xr_n")

        if st.button("▶ Plot Xbar-R Chart", type="primary", key="spc_xr_run"):
            if data_flat is None or len(data_flat) < int(subgroup_size) * 4:
                st.error(f"Need at least {int(subgroup_size) * 4} measurements for {int(subgroup_size)} subgroups × 4 minimum.")
            else:
                n = int(subgroup_size)
                # Trim to a multiple of n, then reshape into subgroups
                trimmed = data_flat[:len(data_flat) - (len(data_flat) % n)]
                subgroups = trimmed.reshape(-1, n).tolist()
                with st.spinner("Building chart …"):
                    try:
                        result, chart = xbar_r_chart(subgroups)
                        st.altair_chart(chart, use_container_width=True)
                        _spc_summary(result)
                    except Exception as e:
                        st.error(f"SPC error: {e}")

    elif "p-chart" in chart_type:
        src = st.radio("Data source", ["Paste numbers", "Uploaded columns"],
                        horizontal=True, key="spc_pc_src")
        defectives_arr = None
        sample_sizes_arr = None

        if src == "Paste numbers":
            c1, c2 = st.columns(2)
            with c1:
                raw_def = st.text_area("Defective counts per sample", height=80, key="spc_pc_def")
            with c2:
                raw_n = st.text_area("Sample sizes per subgroup", height=80, key="spc_pc_n")
            if raw_def.strip() and raw_n.strip():
                defectives_arr = _parse_numeric_series(raw_def).astype(int)
                sample_sizes_arr = _parse_numeric_series(raw_n).astype(int)
        else:
            if df is not None:
                num_cols = df.select_dtypes(include="number").columns.tolist()
                c1, c2 = st.columns(2)
                with c1:
                    def_col = st.selectbox("Defectives column", num_cols, key="spc_pc_dc")
                with c2:
                    n_col = st.selectbox("Sample size column", num_cols, key="spc_pc_nc")
                defectives_arr = df[def_col].dropna().to_numpy().astype(int)
                sample_sizes_arr = df[n_col].dropna().to_numpy().astype(int)
            else:
                st.warning("Upload data in the **Data Hub** tab first.")

        if st.button("▶ Plot p-chart", type="primary", key="spc_pc_run"):
            if defectives_arr is None or len(defectives_arr) < 8:
                st.error("Need at least 8 subgroups.")
            else:
                with st.spinner("Building chart …"):
                    try:
                        result, chart = p_chart(
                            defectives_arr.tolist(),
                            sample_sizes_arr.tolist() if sample_sizes_arr is not None else None,
                        )
                        st.altair_chart(chart, use_container_width=True)
                        _spc_summary(result)
                    except Exception as e:
                        st.error(f"SPC error: {e}")


def _spc_summary(result) -> None:
    """Render SPC stability summary."""
    if result.is_in_control:
        st.markdown(
            '<div style="background:#DCFCE7;border-radius:10px;padding:12px 16px;'
            'font-weight:700;font-size:0.93em;margin-top:12px">'
            '✓ Process is in statistical control — no signals detected</div>',
            unsafe_allow_html=True,
        )
    else:
        signals = result.signals or []
        ooc = result.ooc_points or []
        msg_parts = [f"Out-of-control points at indices: {ooc}"] if ooc else []
        msg_parts += [f"Signal: {s}" for s in signals]
        st.markdown(
            '<div style="background:#FEE2E2;border-radius:10px;padding:12px 16px;'
            'font-weight:700;font-size:0.93em;margin-top:12px">⚠ Process signals detected:<br>'
            + "<br>".join(f"• {m}" for m in msg_parts)
            + "</div>",
            unsafe_allow_html=True,
        )

    m1, m2, m3 = st.columns(3)
    with m1:
        _result_metric("Centerline", f"{result.centerline:.4g}")
    with m2:
        _result_metric("UCL", f"{result.ucl:.4g}")
    with m3:
        lcl = result.lcl
        _result_metric("LCL", f"{lcl:.4g}" if lcl is not None and lcl > 0 else "—")

    if result.recommended_action:
        st.markdown(
            f'<div style="background:#F0F9FF;border-radius:8px;padding:10px 14px;'
            f'font-size:0.88em;color:#0369A1;margin-top:8px">'
            f'<strong>→ Action:</strong> {result.recommended_action}</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 6. FMEA
# ─────────────────────────────────────────────────────────────────────────────

def _tab_fmea() -> None:
    _section("FMEA — Failure Mode & Effects Analysis", "⚠️")
    _info_card(
        "Build your FMEA interactively. Rate each failure mode on "
        "<strong>Severity (S)</strong>, <strong>Occurrence (O)</strong>, and "
        "<strong>Detection (D)</strong> using the standard 1–10 scale. "
        "RPN = S × O × D. High-priority items (S ≥ 9 or RPN ≥ 200) are flagged automatically."
    )

    if "fmea_entries" not in st.session_state:
        st.session_state["fmea_entries"] = []

    entries: list[FMEAEntry] = st.session_state["fmea_entries"]

    with st.expander("➕ Add failure mode entry", expanded=not bool(entries)):
        with st.form("fmea_add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                process_step   = st.text_input("Process step")
                failure_mode   = st.text_input("Failure mode")
                failure_effect = st.text_input("Effect of failure")
                failure_cause  = st.text_input("Potential cause")
            with c2:
                controls = st.text_input("Current controls")
                action   = st.text_input("Recommended action")
                owner    = st.text_input("Action owner")
                date     = st.text_input("Target date (YYYY-MM-DD)")

            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                severity   = st.slider("Severity (S)",   1, 10, 5)
            with sc2:
                occurrence = st.slider("Occurrence (O)", 1, 10, 4)
            with sc3:
                detection  = st.slider("Detection (D)",  1, 10, 5)

            if st.form_submit_button("Add entry", type="primary"):
                if process_step and failure_mode:
                    entry = new_entry(
                        process_step=process_step,
                        failure_mode=failure_mode,
                        failure_effect=failure_effect,
                        failure_cause=failure_cause,
                        current_controls=controls,
                        severity=severity,
                        occurrence=occurrence,
                        detection=detection,
                        recommended_action=action,
                        action_owner=owner,
                        target_date=date,
                    )
                    st.session_state["fmea_entries"].append(entry)
                    st.rerun()
                else:
                    st.warning("Process step and Failure mode are required.")

    if not entries:
        st.info("No entries yet — use the form above to add failure modes.")
        return

    df_fmea = fmea_to_dataframe(entries)
    st.markdown(f"**{len(entries)} failure mode(s)** — sorted by RPN (highest first)")

    display_cols = [
        "process_step", "failure_mode", "severity", "occurrence", "detection",
        "rpn", "action_priority", "recommended_action", "action_owner"
    ]
    display_cols = [c for c in display_cols if c in df_fmea.columns]
    st.dataframe(
        df_fmea[display_cols].sort_values("rpn", ascending=False),
        use_container_width=True,
    )

    if st.button("Clear all entries", key="fmea_clear"):
        st.session_state["fmea_entries"] = []
        st.rerun()

    if len(entries) >= 2:
        c1, c2 = st.columns(2)
        with c1:
            try:
                st.altair_chart(fmea_risk_matrix_chart(df_fmea), use_container_width=True)
            except Exception:
                pass
        with c2:
            try:
                st.altair_chart(fmea_pareto_chart(df_fmea), use_container_width=True)
            except Exception:
                pass

    csv_bytes = df_fmea.to_csv(index=False).encode()
    st.download_button("⬇ Download FMEA as CSV", data=csv_bytes,
                        file_name="fmea_output.csv", mime="text/csv", key="fmea_dl")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Regression
# ─────────────────────────────────────────────────────────────────────────────

def _tab_regression() -> None:
    _section("Regression Analysis", "📉")
    _info_card(
        "Run <strong>simple</strong> or <strong>multiple linear regression</strong> using OLS. "
        "Results include R², adjusted R², p-values, coefficient confidence intervals, "
        "and diagnostics (normality, heteroscedasticity, VIF for multicollinearity)."
    )

    df = _get_uploaded_df()
    if df is None:
        st.info("Upload a dataset in **Data Hub** to run regression analysis.")
        return

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(num_cols) < 2:
        st.warning("Need at least 2 numeric columns for regression.")
        return

    reg_type = st.radio("Regression type", ["Simple (one predictor)", "Multiple (several predictors)"],
                         horizontal=True, key="reg_type")

    y_col = st.selectbox("Response / outcome variable (Y)", num_cols, key="reg_y")
    remaining = [c for c in num_cols if c != y_col]

    if "Simple" in reg_type:
        x_col = st.selectbox("Predictor variable (X)", remaining, key="reg_x")
        predictors = [x_col]
    else:
        predictors = st.multiselect("Predictor variables (X)", remaining, key="reg_xs")

    alpha = st.select_slider("Significance level (α)", options=[0.01, 0.05, 0.10],
                              value=0.05, key="reg_alpha")

    if st.button("▶ Run Regression", type="primary", key="reg_run"):
        if not predictors:
            st.error("Select at least one predictor.")
            return

        # Align rows with no missing values
        cols_needed = [y_col] + predictors
        sub = df[cols_needed].dropna()
        if len(sub) < 10:
            st.error("Need at least 10 complete observations (no missing values).")
            return

        y_arr = sub[y_col].to_numpy()
        X_sub = sub[predictors]

        with st.spinner("Fitting model …"):
            try:
                if len(predictors) == 1:
                    result = simple_regression(
                        X_sub[predictors[0]].to_numpy(), y_arr,
                        x_name=predictors[0], y_name=y_col, alpha=alpha,
                    )
                else:
                    result = multiple_regression(X_sub, y_arr, alpha=alpha)
            except Exception as e:
                st.error(f"Regression error: {e}")
                return

        st.markdown("---")
        st.markdown("#### Model summary")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            _result_metric("R²", f"{result.r_squared:.4f}")
        with m2:
            _result_metric("Adj. R²", f"{result.adj_r_squared:.4f}")
        with m3:
            f_str = f"{result.f_statistic:.4f}" if result.f_statistic and not (result.f_statistic != result.f_statistic) else "—"
            _result_metric("F-statistic", f_str)
        with m4:
            fp_str = f"{result.f_p_value:.5f}" if result.f_p_value and not (result.f_p_value != result.f_p_value) else "—"
            _result_metric("Prob(F)", fp_str)

        # Coefficients
        st.markdown("#### Coefficients")
        coef_rows = []
        for name, coef in result.coefficients.items():
            coef_rows.append({
                "Variable": name,
                "Coefficient": round(coef, 5),
                "Std Error": round(result.standard_errors.get(name, float("nan")), 5),
                "p-value": round(result.p_values.get(name, float("nan")), 5),
                "95% CI Lower": round(result.confidence_intervals.get(name, (float("nan"), float("nan")))[0], 5),
                "95% CI Upper": round(result.confidence_intervals.get(name, (float("nan"), float("nan")))[1], 5),
                "Significant": "✓" if name in result.significant_predictors else "",
            })
        st.dataframe(pd.DataFrame(coef_rows), use_container_width=True, hide_index=True)

        # Diagnostics
        st.markdown("#### Diagnostics")
        for check_name, check_text in result.assumptions_checks.items():
            label = check_name.replace("_", " ").title()
            colour = "#DCFCE7" if "Pass" in check_text or "No " in check_text or "acceptable" in check_text else "#FEF9C3"
            st.markdown(
                f'<div style="background:{colour};border-radius:8px;padding:8px 12px;'
                f'font-size:0.87em;margin-bottom:6px">'
                f'<strong>{label}:</strong> {check_text}</div>',
                unsafe_allow_html=True,
            )

        # Charts (simple regression only)
        if len(predictors) == 1:
            x_arr = X_sub[predictors[0]].to_numpy()
            try:
                scatter = regression_scatter_chart(x_arr, y_arr, result, predictors[0], y_col)
                st.altair_chart(scatter, use_container_width=True)
            except Exception:
                pass
            try:
                resid = residual_plot(x_arr, y_arr, result)
                st.altair_chart(resid, use_container_width=True)
            except Exception:
                pass

        if result.interpretation:
            st.markdown(
                f'<div class="lss-card-accent" style="margin-top:12px">'
                f'<strong>Interpretation</strong><br>{result.interpretation}</div>',
                unsafe_allow_html=True,
            )
        if result.recommended_action:
            st.markdown(
                f'<div style="background:#F0FDF4;border-radius:10px;padding:12px 16px;'
                f'font-size:0.9em;color:#166534;margin-top:8px">'
                f'<strong>→ Recommended next step:</strong> {result.recommended_action}</div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# 8. Design of Experiments
# ─────────────────────────────────────────────────────────────────────────────

def _tab_doe() -> None:
    _section("Design of Experiments (DOE)", "🧬")
    _info_card(
        "Define your experimental factors and receive an optimised design matrix. "
        "Supports full factorial (k ≤ 4), half-fraction (k = 5–6), and Plackett-Burman (k ≥ 7). "
        "Design selection follows Montgomery's rules (9th edition)."
    )

    n_factors = st.number_input("Number of factors", min_value=2, max_value=12, value=3, key="doe_nf")
    budget = st.number_input(
        "Maximum number of runs (budget)",
        min_value=4, max_value=256, value=16, key="doe_budget",
        help="DOE will select the most informative design within this run count.",
    )

    st.markdown("#### Define factors")
    st.markdown(
        '<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:8px;'
        'font-weight:700;font-size:0.82em;color:#64748B;text-transform:uppercase;'
        'letter-spacing:0.05em;margin-bottom:6px">'
        '<span>Factor name</span><span>Low level</span><span>High level</span>'
        '<span>Units</span><span>Continuous?</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    factors: list[DOEFactor] = []
    for i in range(int(n_factors)):
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        with c1:
            name = st.text_input("Name", value=f"Factor {i+1}", key=f"doe_name_{i}",
                                  label_visibility="collapsed")
        with c2:
            lo = st.text_input("Low", value="Low", key=f"doe_lo_{i}",
                                label_visibility="collapsed")
        with c3:
            hi = st.text_input("High", value="High", key=f"doe_hi_{i}",
                                label_visibility="collapsed")
        with c4:
            units = st.text_input("Units", value="", key=f"doe_units_{i}",
                                   label_visibility="collapsed")
        with c5:
            is_cont = st.checkbox("", value=True, key=f"doe_cont_{i}")

        try:
            lo_val = float(lo) if is_cont else lo
            hi_val = float(hi) if is_cont else hi
        except ValueError:
            lo_val, hi_val = lo, hi

        factors.append(DOEFactor(
            name=name, low_level=lo_val, high_level=hi_val,
            units=units, is_continuous=is_cont,
        ))

    if st.button("▶ Generate Design", type="primary", key="doe_run"):
        with st.spinner("Building design matrix …"):
            try:
                design = recommend_design(factors, budget_runs=int(budget))
            except Exception as e:
                st.error(f"DOE error: {e}")
                return

        st.markdown("---")
        st.markdown("#### Design recommendation")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            _result_metric("Design type", design.design_type)
        with m2:
            _result_metric("Runs (design)", str(design.n_runs_design))
        with m3:
            _result_metric("Total runs (incl. reps + centre)", str(design.total_runs))
        with m4:
            _result_metric("Resolution", design.resolution if design.resolution else "—")

        if design.interpretation:
            st.markdown(
                f'<div class="lss-card-accent" style="margin-top:12px">'
                f'<strong>Design interpretation</strong><br>{design.interpretation}</div>',
                unsafe_allow_html=True,
            )

        if design.alias_structure:
            with st.expander("Confounding / alias structure"):
                for alias in design.alias_structure:
                    st.markdown(f"- {alias}")

        # Design matrix
        run_matrix = design.randomized_run_matrix
        if run_matrix is not None and not run_matrix.empty:
            st.markdown("#### Design matrix (coded levels: −1 = Low, +1 = High) — randomised run order")
            st.dataframe(run_matrix, use_container_width=True)

            csv_bytes = run_matrix.to_csv(index=False).encode()
            st.download_button(
                "⬇ Download design matrix (CSV)",
                data=csv_bytes,
                file_name="doe_design_matrix.csv",
                mime="text/csv",
                key="doe_dl",
            )

        try:
            dm_chart = design_matrix_chart(design)
            st.altair_chart(dm_chart, use_container_width=True)
        except Exception:
            pass

        if design.recommended_action:
            _info_card(f"<strong>Next step:</strong> {design.recommended_action}", colour="#F0F9FF")


# ─────────────────────────────────────────────────────────────────────────────
# 9. Benefits / COPQ
# ─────────────────────────────────────────────────────────────────────────────

def _tab_benefits() -> None:
    _section("Benefits & COPQ Analysis", "💰")
    _info_card(
        "Quantify the financial impact of your project using the "
        "<strong>Cost of Poor Quality (COPQ)</strong> framework: "
        "Prevention, Appraisal, Internal Failure, External Failure. "
        "Results include hard vs soft savings, ROI, payback period, and 3-year NPV."
    )

    if "copq_entries" not in st.session_state:
        st.session_state["copq_entries"] = []

    entries: list[CostOfQualityEntry] = st.session_state["copq_entries"]

    with st.expander("➕ Add COPQ line item", expanded=not bool(entries)):
        with st.form("copq_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                category = st.selectbox(
                    "Category",
                    ["Internal Failure", "External Failure", "Appraisal", "Prevention"],
                    key="copq_cat",
                )
                description = st.text_input("Description", key="copq_desc")
            with c2:
                annual_cost = st.number_input("Annual cost ($)", min_value=0.0,
                                               value=10000.0, step=1000.0, key="copq_cost")
                is_hard = st.checkbox("Hard saving (verifiable in P&L)", value=True, key="copq_hard")

            if st.form_submit_button("Add line item", type="primary") and description:
                st.session_state["copq_entries"].append(
                    CostOfQualityEntry(
                        category=category,
                        description=description,
                        annual_cost=annual_cost,
                        is_hard_saving=is_hard,
                    )
                )
                st.rerun()

    if not entries:
        st.info("No COPQ items yet — add line items above.")
        return

    copq_df = pd.DataFrame([
        {
            "Category": e.category,
            "Description": e.description,
            "Annual Cost ($)": f"${e.annual_cost:,.0f}",
            "Type": "Hard" if e.is_hard_saving else "Soft",
        }
        for e in entries
    ])
    st.dataframe(copq_df, use_container_width=True, hide_index=True)

    total_copq = sum(e.annual_cost for e in entries)
    st.markdown(f"**Total COPQ: ${total_copq:,.0f} / year**")

    if st.button("Clear all COPQ items", key="copq_clear"):
        st.session_state["copq_entries"] = []
        st.rerun()

    st.markdown("#### ROI & NPV parameters")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        improvement_pct = st.number_input("Expected COPQ improvement (%)",
                                           min_value=1.0, max_value=100.0, value=40.0,
                                           step=5.0, key="ben_imp")
    with c2:
        impl_cost = st.number_input("Implementation cost ($)",
                                     min_value=0.0, value=50000.0, step=5000.0, key="ben_impl")
    with c3:
        discount_rate = st.number_input("Discount rate (%)", min_value=0.0,
                                         max_value=50.0, value=10.0, step=1.0,
                                         key="ben_dr") / 100
    with c4:
        confidence = st.selectbox("Savings confidence", ["High", "Medium", "Low"], key="ben_conf")

    if st.button("▶ Calculate ROI & NPV", type="primary", key="ben_run"):
        with st.spinner("Calculating …"):
            try:
                result = run_benefits_analysis(
                    copq_entries=entries,
                    projected_improvement_pct=improvement_pct,
                    implementation_cost=impl_cost,
                    discount_rate=discount_rate,
                    confidence=confidence,
                )
            except Exception as e:
                st.error(f"Benefits error: {e}")
                return

        st.markdown("---")
        st.markdown("#### Financial results")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            _result_metric("Total projected savings", f"${result.total_projected_savings:,.0f}")
            _result_metric("Hard savings", f"${result.projected_savings_hard:,.0f}")
        with m2:
            _result_metric("Soft savings", f"${result.projected_savings_soft:,.0f}")
            _result_metric("Net year-1 benefit", f"${result.net_benefit_year1:,.0f}")
        with m3:
            _result_metric("ROI", f"{result.roi_pct:.1f}%")
            _result_metric("Payback period", f"{result.payback_months:.1f} months")
        with m4:
            _result_metric("3-year NPV", f"${result.npv_3yr:,.0f}")
            st.caption(f"Confidence: {result.confidence_level}")

        npv = result.npv_3yr
        colour = "#DCFCE7" if npv > 0 else "#FEE2E2"
        verdict = (f"Project is financially justified — 3-year NPV of ${npv:,.0f}"
                   if npv > 0 else
                   f"Project does not recover costs in 3 years — NPV: ${npv:,.0f}")
        st.markdown(
            f'<div style="background:{colour};border-radius:10px;padding:12px 16px;'
            f'font-weight:700;font-size:0.93em;margin:12px 0">{verdict}</div>',
            unsafe_allow_html=True,
        )

        try:
            wf = copq_waterfall_chart(entries)
            st.altair_chart(wf, use_container_width=True)
        except Exception:
            pass
        try:
            tl = savings_timeline_chart(result)
            st.altair_chart(tl, use_container_width=True)
        except Exception:
            pass

        if result.interpretation:
            st.markdown(
                f'<div class="lss-card-accent" style="margin-top:12px">'
                f'<strong>Interpretation</strong><br>{result.interpretation}</div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────────────

def _tab_lean_flow() -> None:
    """Lean Flow / Value Stream Analysis tab."""

    _section("Lean Flow & Value Stream Analysis", "🌊")
    st.caption(
        "Map your process steps, calculate takt time vs cycle time, identify the bottleneck, "
        "quantify waste, and apply Little's Law to understand WIP and lead time."
    )

    st.markdown("---")

    # ── Demand & time parameters ─────────────────────────────────────────────
    st.markdown("#### ⏱ Demand & Available Time")
    c1, c2, c3 = st.columns(3)
    with c1:
        demand_per_day = st.number_input(
            "Customer demand (units/day)",
            min_value=1.0, value=22.0, step=1.0,
            key="lf_demand",
            help="How many units does the customer require per day?",
        )
    with c2:
        available_hrs = st.number_input(
            "Available production time (hrs/day)",
            min_value=0.5, max_value=24.0, value=7.5, step=0.5,
            key="lf_avail_hrs",
            help="Scheduled hours minus planned breaks and maintenance.",
        )
    with c3:
        available_time_min = available_hrs * 60.0
        takt_time_min = available_time_min / demand_per_day
        st.metric("Takt time", f"{takt_time_min:.1f} min/unit",
                  help="Available time ÷ demand — the pace the customer sets.")
        st.metric("Available time", f"{available_time_min:.0f} min/day")

    st.markdown("---")

    # ── Process steps editor ─────────────────────────────────────────────────
    st.markdown("#### 🔢 Process Steps")
    st.caption(
        "Define each step in the value stream. One row per step. "
        "VA = Value-Added (customer pays for it). NVA = waste."
    )

    default_steps = pd.DataFrame({
        "Step name":           ["Order Entry", "Machining", "Assembly", "Quality Check", "Shipping Prep"],
        "Cycle time (min)":    [5.0, 18.0, 12.0, 6.0, 4.0],
        "Wait/queue (min)":    [120.0, 240.0, 60.0, 30.0, 15.0],
        "Value-added?":        [False, True, True, False, True],
        "Defect rate (%)":     [2.0, 4.5, 1.5, 0.5, 0.2],
        "Rework rate (%)":     [0.0, 60.0, 40.0, 0.0, 0.0],
        "Operators":           [1.0, 2.0, 2.0, 1.0, 1.0],
        "Uptime (%)":          [100.0, 88.0, 95.0, 100.0, 100.0],
    })

    if "lf_steps_df" not in st.session_state:
        st.session_state["lf_steps_df"] = default_steps.copy()

    edited_df = st.data_editor(
        st.session_state["lf_steps_df"],
        num_rows="dynamic",
        use_container_width=True,
        key="lf_steps_editor",
        column_config={
            "Step name":         st.column_config.TextColumn("Step name", width="medium"),
            "Cycle time (min)":  st.column_config.NumberColumn("Cycle time (min)", min_value=0.0, format="%.1f"),
            "Wait/queue (min)":  st.column_config.NumberColumn("Wait/queue (min)", min_value=0.0, format="%.1f"),
            "Value-added?":      st.column_config.CheckboxColumn("Value-added?"),
            "Defect rate (%)":   st.column_config.NumberColumn("Defect rate (%)", min_value=0.0, max_value=100.0, format="%.1f"),
            "Rework rate (%)":   st.column_config.NumberColumn("Rework rate (%)", min_value=0.0, max_value=100.0, format="%.1f"),
            "Operators":         st.column_config.NumberColumn("Operators", min_value=0.0, format="%.1f"),
            "Uptime (%)":        st.column_config.NumberColumn("Uptime (%)", min_value=1.0, max_value=100.0, format="%.1f"),
        },
    )
    st.session_state["lf_steps_df"] = edited_df

    run_btn = st.button("▶ Run Lean Flow Analysis", type="primary", key="lf_run_btn")
    if run_btn:
        st.session_state["lf_run"] = True

    if not st.session_state.get("lf_run"):
        st.info("Fill in your process steps above and click **▶ Run Lean Flow Analysis**.")
        return

    # ── Build ProcessStep objects ─────────────────────────────────────────────
    df = st.session_state["lf_steps_df"].dropna(subset=["Step name"])
    if df.empty or len(df) < 2:
        st.warning("Enter at least 2 process steps to run the analysis.")
        return

    try:
        steps = [
            ProcessStep(
                name=str(row["Step name"]),
                cycle_time_min=float(row.get("Cycle time (min)", 5.0) or 5.0),
                wait_time_min=float(row.get("Wait/queue (min)", 0.0) or 0.0),
                defect_rate_pct=float(row.get("Defect rate (%)", 0.0) or 0.0),
                is_value_added=bool(row.get("Value-added?", False)),
                operator_count=float(row.get("Operators", 1.0) or 1.0),
                uptime_pct=float(row.get("Uptime (%)", 100.0) or 100.0),
                rework_pct=float(row.get("Rework rate (%)", 0.0) or 0.0),
            )
            for _, row in df.iterrows()
        ]
        result = run_lean_flow_analysis(
            steps=steps,
            takt_time_min=takt_time_min,
            available_time_min=available_time_min,
            demand_per_day=demand_per_day,
        )
    except Exception as exc:
        st.error(f"Analysis error: {exc}")
        return

    st.markdown("---")
    st.markdown("#### 📊 Key Metrics")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Lead Time",       f"{result.total_lead_time_min:.0f} min",
              help="Total cycle time + total wait time (end-to-end)")
    m2.metric("VA Time",         f"{result.va_time_min:.0f} min",
              help="Sum of value-added cycle times only")
    m3.metric("PCE",             f"{result.process_cycle_efficiency_pct:.1f}%",
              help="Process Cycle Efficiency = VA / Lead Time × 100. World class >25%.")
    m4.metric("Bottleneck",      result.bottleneck_step,
              help="Step with highest effective cycle time (adjusted for uptime)")
    m5.metric("Avg WIP",         f"{result.avg_wip_units:.1f} units",
              help="Little's Law: WIP = Throughput × Lead Time")

    st.markdown("---")

    # ── PCE gauge ─────────────────────────────────────────────────────────────
    st.markdown("#### 🎯 Process Cycle Efficiency")
    st.markdown(pce_gauge_html(result.process_cycle_efficiency_pct), unsafe_allow_html=True)

    st.markdown("---")

    # ── Value stream chart ────────────────────────────────────────────────────
    st.markdown("#### 🗺 Value Stream Map")
    st.caption("Green = value-added cycle time  ·  Amber = NVA cycle time  ·  Red = wait/queue time  ·  Dashed line = takt time")
    try:
        st.altair_chart(value_stream_chart(result), use_container_width=True)
    except Exception as exc:
        st.warning(f"Chart error: {exc}")

    st.markdown("---")

    # ── Utilisation chart ─────────────────────────────────────────────────────
    st.markdown("#### ⚙️ Step Utilisation vs Takt")
    st.caption("Red = overloaded (>90%), Amber = caution (70–90%), Green = OK (<70%)")
    try:
        st.altair_chart(utilisation_chart(result), use_container_width=True)
    except Exception as exc:
        st.warning(f"Chart error: {exc}")

    st.markdown("---")

    # ── Waste waterfall ───────────────────────────────────────────────────────
    st.markdown("#### 🗑 Lead Time Composition")
    st.caption("How total lead time is split between VA, NVA cycle time, wait, and rework")
    try:
        st.altair_chart(waste_waterfall_chart(result), use_container_width=True)
    except Exception as exc:
        st.warning(f"Chart error: {exc}")

    st.markdown("---")

    # ── Step-level detail table ───────────────────────────────────────────────
    st.markdown("#### 📋 Step-Level Detail")
    detail_df = pd.DataFrame(result.step_analysis)
    if not detail_df.empty:
        st.dataframe(detail_df, use_container_width=True)

    st.markdown("---")

    # ── Observations & recommendations ────────────────────────────────────────
    st.markdown("#### 💡 Observations")
    for obs in result.observations:
        st.markdown(f"- {obs}")

    st.markdown("#### ✅ Recommendations")
    for rec in result.recommendations:
        st.markdown(
            f'<div style="background:#F0FDF4;border-left:4px solid #22C55E;'
            f'border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;">'
            f'✅ {rec}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Little's Law explainer ────────────────────────────────────────────────
    with st.expander("📚 Little's Law explainer"):
        st.markdown(
            f"""
**Little's Law:** Lead Time = WIP ÷ Throughput Rate

| Variable | Your value |
|---|---|
| Throughput rate | {result.throughput_units_per_hour:.2f} units/hr |
| Average WIP | {result.avg_wip_units:.1f} units |
| Lead time (Little's Law) | {result.littles_law_lead_time_min:.0f} min |
| Lead time (sum CT+wait) | {result.total_lead_time_min:.0f} min |

**To reduce lead time:** reduce WIP (smaller batches, pull scheduling) or increase throughput (relieve the bottleneck).
"""
        )


def render_analytics_workbench() -> None:
    """
    Render the full Black Belt Analytics Workbench.
    Called from app.py when the user switches to Analytics mode.
    """

    st.markdown(
        '<div class="hero-banner">'
        '<h2>⚡ Black Belt Analytics Workbench</h2>'
        '<p>Advanced quantitative analysis — Capability · MSA · Hypothesis Testing · '
        'SPC · FMEA · Regression · DOE · Benefits & COPQ · Lean Flow</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs([
        "📂 Data Hub",
        "📐 Capability",
        "🔬 MSA / Gauge R&R",
        "🧪 Hypothesis Tests",
        "📈 SPC Charts",
        "⚠️ FMEA",
        "📉 Regression",
        "🧬 DOE",
        "💰 Benefits & COPQ",
        "🌊 Lean Flow",
    ])

    with tabs[0]:
        _tab_data_hub()
    with tabs[1]:
        _tab_capability()
    with tabs[2]:
        _tab_msa()
    with tabs[3]:
        _tab_hypothesis()
    with tabs[4]:
        _tab_spc()
    with tabs[5]:
        _tab_fmea()
    with tabs[6]:
        _tab_regression()
    with tabs[7]:
        _tab_doe()
    with tabs[8]:
        _tab_benefits()
    with tabs[9]:
        _tab_lean_flow()
