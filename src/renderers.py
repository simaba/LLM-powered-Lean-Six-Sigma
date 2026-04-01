from __future__ import annotations

from src.models import AssessmentResult, EvidenceItem


# ── Shared helpers ────────────────────────────────────────────────────────────

def _render_items_md(items: list[EvidenceItem]) -> str:
    return "\n".join(f"- {item.statement} [{item.evidence_tag}]" for item in items)


_TAG_COLOURS = {
    "directly_supported_by_input": ("#d4edda", "#155724"),
    "supported_by_input": ("#d4edda", "#155724"),
    "inferred_hypothesis": ("#fff3cd", "#856404"),
    "missing_evidence": ("#f8d7da", "#721c24"),
}

_TAG_LABELS = {
    "directly_supported_by_input": "supported",
    "supported_by_input": "supported",
    "inferred_hypothesis": "inferred",
    "missing_evidence": "missing",
}


def _tag_badge(tag: str) -> str:
    bg, fg = _TAG_COLOURS.get(tag, ("#e9ecef", "#495057"))
    label = _TAG_LABELS.get(tag, tag)
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 7px;border-radius:4px;'
        f'font-size:0.75em;font-weight:700;white-space:nowrap">{label}</span>'
    )


def _render_items_html(items: list[EvidenceItem]) -> str:
    lines = []
    for item in items:
        lines.append(f"<li>{item.statement} &nbsp;{_tag_badge(item.evidence_tag)}</li>")
    return "<ul>" + "".join(lines) + "</ul>"


def _render_table_html(rows: list[dict]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for row in rows:
        td = "".join(f"<td>{row.get(h, '')}</td>" for h in headers)
        body += f"<tr>{td}</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>"


# ── Markdown renderer ─────────────────────────────────────────────────────────

def render_markdown_summary(result: AssessmentResult) -> str:
    sections = [
        f"# {result.project_name}",
        "",
        f"**Mode:** {result.mode}  |  **Audience:** {result.audience}",
        "",
        "---",
        "",
        "## Cleaned-up problem statement",
        result.cleaned_problem_statement,
        "",
        "## Critical-to-Quality (CTQs)",
        _render_items_md(result.ctqs),
        "",
        "## SIPOC",
        f"- **Suppliers:** {', '.join(result.sipoc.get('suppliers', []))}",
        f"- **Inputs:** {', '.join(result.sipoc.get('inputs', []))}",
        f"- **Process:** {', '.join(result.sipoc.get('process', []))}",
        f"- **Outputs:** {', '.join(result.sipoc.get('outputs', []))}",
        f"- **Customers:** {', '.join(result.sipoc.get('customers', []))}",
        "",
        "## DMAIC structure",
    ]

    for phase_name, items in result.dmaic_structure.items():
        sections.append(f"### {phase_name.title()}")
        sections.append(_render_items_md(items))
        sections.append("")

    sections.extend([
        "## Possible root causes",
        _render_items_md(result.root_causes),
        "",
        "## Suggested metrics to track",
        _render_items_md(result.suggested_metrics),
        "",
        "## Suggested improvement actions",
        _render_items_md(result.improvement_actions),
        "",
        "## Control plan",
        _render_items_md(result.control_plan),
        "",
        "## Action tracker",
    ])

    for row in result.action_tracker:
        sections.append(
            f"- {row.get('action', '')} | owner: {row.get('owner', '')} "
            f"| priority: {row.get('priority', '')} | status: {row.get('status', '')}"
        )

    sections.extend(["", "## Project memory"])
    for key, values in result.project_memory.items():
        sections.append(f"### {key.replace('_', ' ').title()}")
        sections.extend(f"- {v}" for v in values)
        sections.append("")

    sections.extend(["## Role-aware summary", result.role_summary])
    return "\n".join(sections)


# ── HTML renderer ─────────────────────────────────────────────────────────────

_HTML_CSS = """
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         font-size: 14px; color: #212529; background: #fff; margin: 0; padding: 0; }
  .wrapper { max-width: 900px; margin: 0 auto; padding: 40px 32px; }
  h1 { font-size: 1.9em; font-weight: 700; margin-bottom: 4px; }
  h2 { font-size: 1.2em; font-weight: 700; color: #1a1a2e;
       border-bottom: 2px solid #e9ecef; padding-bottom: 6px; margin-top: 36px; }
  h3 { font-size: 1em; font-weight: 700; color: #333; margin-top: 20px; margin-bottom: 6px; }
  .meta { color: #6c757d; font-size: 0.9em; margin-bottom: 32px; }
  .problem-box { background: #f0f4ff; border-left: 4px solid #4361ee;
                 padding: 14px 18px; border-radius: 6px; margin: 12px 0; }
  ul { margin: 6px 0 12px 0; padding-left: 20px; line-height: 1.7; }
  li { margin-bottom: 6px; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9em; }
  th { background: #f8f9fa; text-align: left; padding: 8px 10px;
       border: 1px solid #dee2e6; font-weight: 600; }
  td { padding: 7px 10px; border: 1px solid #dee2e6; vertical-align: top; }
  tr:nth-child(even) td { background: #f8f9fa; }
  .summary-box { background: #e8f4fd; border-left: 4px solid #0ea5e9;
                 padding: 14px 18px; border-radius: 6px; margin: 12px 0; }
  .sipoc-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 10px; }
  .sipoc-col { background: #f8f9fa; border-radius: 6px; padding: 10px; }
  .sipoc-col strong { display: block; margin-bottom: 6px; color: #4361ee; font-size: 0.85em;
                      text-transform: uppercase; letter-spacing: 0.05em; }
  .sipoc-col ul { margin: 0; padding-left: 14px; }
  footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #e9ecef;
           color: #adb5bd; font-size: 0.8em; text-align: center; }
"""


def render_html_summary(result: AssessmentResult) -> str:
    sipoc = result.sipoc

    sipoc_html = '<div class="sipoc-grid">'
    for col in ["suppliers", "inputs", "process", "outputs", "customers"]:
        items_html = "".join(f"<li>{v}</li>" for v in sipoc.get(col, []))
        sipoc_html += f'<div class="sipoc-col"><strong>{col}</strong><ul>{items_html}</ul></div>'
    sipoc_html += "</div>"

    dmaic_html = ""
    for phase, items in result.dmaic_structure.items():
        dmaic_html += f"<h3>{phase.upper()}</h3>{_render_items_html(items)}"

    memory_html = ""
    for key, values in result.project_memory.items():
        label = key.replace("_", " ").title()
        items_html = "".join(f"<li>{v}</li>" for v in values)
        memory_html += f"<h3>{label}</h3><ul>{items_html}</ul>"

    action_table = _render_table_html(result.action_tracker)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{result.project_name} — LSS Report</title>
<style>{_HTML_CSS}</style>
</head>
<body>
<div class="wrapper">

  <h1>{result.project_name}</h1>
  <div class="meta">
    Mode: <strong>{result.mode.upper()}</strong> &nbsp;|&nbsp;
    Audience: <strong>{result.audience.replace('_', ' ').title()}</strong>
  </div>

  <h2>Problem Statement</h2>
  <div class="problem-box">{result.cleaned_problem_statement}</div>

  <h2>Critical-to-Quality (CTQs)</h2>
  {_render_items_html(result.ctqs)}

  <h2>SIPOC</h2>
  {sipoc_html}

  <h2>DMAIC Structure</h2>
  {dmaic_html}

  <h2>Root Causes</h2>
  {_render_items_html(result.root_causes)}

  <h2>Suggested Metrics</h2>
  {_render_items_html(result.suggested_metrics)}

  <h2>Improvement Actions</h2>
  {_render_items_html(result.improvement_actions)}

  <h2>Control Plan</h2>
  {_render_items_html(result.control_plan)}

  <h2>Action Tracker</h2>
  {action_table}

  <h2>Project Memory</h2>
  {memory_html}

  <h2>Role-Aware Summary</h2>
  <div class="summary-box">{result.role_summary}</div>

  <footer>Generated by LSS Copilot &mdash; Lean Six Sigma AI assistant</footer>
</div>
</body>
</html>"""
