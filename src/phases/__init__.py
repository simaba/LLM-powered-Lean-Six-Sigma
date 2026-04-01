from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from src.models import AssessmentResult, EvidenceItem, ProjectInput


# ── Evidence helpers ──────────────────────────────────────────────────────────

def _supported(statement: str) -> EvidenceItem:
    return EvidenceItem(statement=statement, evidence_tag="directly_supported_by_input")


def _inferred(statement: str) -> EvidenceItem:
    return EvidenceItem(statement=statement, evidence_tag="inferred_hypothesis")


def _missing(statement: str) -> EvidenceItem:
    return EvidenceItem(statement=statement, evidence_tag="missing_evidence")


def _parse_items(raw: List[Dict]) -> List[EvidenceItem]:
    return [
        EvidenceItem(statement=i.get("statement", ""), evidence_tag=i.get("evidence_tag", "inferred_hypothesis"))
        for i in raw
        if i.get("statement")
    ]


def _parse_dmaic(raw: Dict) -> Dict[str, List[EvidenceItem]]:
    return {phase: _parse_items(items) for phase, items in raw.items()}


# ── Mode-specific prompt instructions ─────────────────────────────────────────

_MODE_INSTRUCTIONS: Dict[str, str] = {
    "dmaic": (
        "Apply the full DMAIC methodology rigorously across all five phases. "
        "Define: frame the problem precisely. Measure: identify what is and is not known about the current state. "
        "Analyze: identify root causes with evidence discipline. Improve: propose specific, prioritised actions. "
        "Control: define how gains will be monitored and sustained."
    ),
    "kaizen": (
        "Apply a Kaizen lens. Focus on rapid, small-batch improvements and short learning cycles. "
        "Improvement actions must be immediately actionable (can start within days), low-overhead, and team-led. "
        "De-emphasise structural overhauls. Prioritise visible quick wins, waste elimination, and incremental change. "
        "Flag opportunities for daily stand-ups, visual management boards, and short improvement sprints."
    ),
    "root_cause": (
        "Conduct a deep root cause investigation. This is the primary focus of the output. "
        "Apply 5 Whys reasoning: starting from the first symptom, ask 'why' iteratively, "
        "building a causal chain of at least 4 levels deep until you reach a systemic root cause. "
        "Show the chain as separate root cause items labelled Why-1 through Why-4+. "
        "Also apply fishbone (Ishikawa) thinking across six categories: "
        "People, Process, Environment, Materials, Machines, Measurements. "
        "Generate at least one specific root cause candidate per relevant category. "
        "Distinguish clearly between supported evidence and hypotheses."
    ),
    "process_waste": (
        "Focus the analysis on waste identification using the TIMWOODS framework: "
        "Transportation (unnecessary movement of information or work), "
        "Inventory (work piling up between steps), "
        "Motion (unnecessary steps or handoffs), "
        "Waiting (delays between process steps), "
        "Overproduction (doing more than needed), "
        "Over-processing (more effort than required), "
        "Defects (errors and rework), "
        "Skills underutilisation (not using people's full capability). "
        "Identify which waste types are present, how each manifests in this specific project, "
        "and propose one targeted countermeasure per identified waste type. "
        "Rank the top three waste categories by business impact."
    ),
    "control_plan": (
        "Focus primarily on the Control phase. Build a detailed, actionable control plan. "
        "Each control plan item must include: a specific metric to monitor, a named owner role, "
        "a concrete review cadence (daily/weekly/bi-weekly/monthly), "
        "a threshold trigger that defines when corrective action is required, "
        "and the escalation response when that trigger fires. "
        "Populate the action_tracker with control-oriented actions (monitoring setup, owner assignment, review scheduling). "
        "Expand the project_memory control_metrics section to be the richest section."
    ),
}

# ── Audience-specific prompt instructions ──────────────────────────────────────

_AUDIENCE_INSTRUCTIONS: Dict[str, str] = {
    "executive": (
        "Write role_summary for a senior executive. Lead with business impact and strategic risk. "
        "Use plain, jargon-free language. Cover: what problem is being solved, what the financial or "
        "operational risk is if it is not resolved, what decision or resource commitment is needed now, "
        "and what the expected outcome of the improvement is. Maximum 4 sentences."
    ),
    "manager": (
        "Write role_summary for an operations or process manager. "
        "Focus on team accountability, the top 3 prioritised actions, and review cadence. "
        "Name specific owner roles for the top actions. State clearly what must happen in the next 30 days "
        "and what the manager needs to unblock or decide."
    ),
    "quality_lead": (
        "Write role_summary for a quality professional or LSS practitioner. "
        "Focus on CTQ alignment, measurement system integrity, evidence gaps that need filling, "
        "and control plan rigor. Reference specific metrics and flag where evidence is inferred vs. proven. "
        "Mention what additional data collection is needed before the analysis can be considered validated."
    ),
    "engineer": (
        "Write role_summary for a process engineer or analyst. "
        "Focus on process mapping gaps, measurement system opportunities, observable bottlenecks, "
        "and the most technically specific improvement actions. "
        "Suggest what data to collect, what to map, and where to instrument the process."
    ),
    "pm": (
        "Write role_summary for a project manager. "
        "Focus on stakeholder alignment needs, open action items that need owners, milestone clarity, "
        "and risk tracking. Provide a direct 'next 3 actions' directive. "
        "Flag any assumptions that need stakeholder validation."
    ),
}

# ── System prompt ──────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are a world-class Lean Six Sigma Master Black Belt and structured reasoning expert.
Your role is to take messy, incomplete project inputs and transform them into rigorous, \
insightful, and actionable Lean Six Sigma improvement outputs.

Evidence discipline — follow these rules without exception:
- Label every output item with exactly one evidence_tag from this set:
    "directly_supported_by_input"  — the statement is directly grounded in the project data provided
    "inferred_hypothesis"          — a logical inference that is plausible but not yet proven
    "missing_evidence"             — something important is absent and needs investigation
- Never blend assumptions with facts. If you are inferring, say so.
- When project input is vague or incomplete, use missing_evidence items rather than fabricating specifics.
- Prioritise specificity: use the actual project name, symptoms, metrics, and concerns in your statements,
  not generic Lean Six Sigma boilerplate.

Output format: return a single valid JSON object with exactly the structure specified in the user message.
No text before or after the JSON. No markdown code fences. Raw JSON only.\
"""


# ── User message builder ───────────────────────────────────────────────────────

def _build_user_message(project: ProjectInput, mode: str, audience: str) -> str:
    mode_instruction = _MODE_INSTRUCTIONS.get(mode, _MODE_INSTRUCTIONS["dmaic"])
    audience_instruction = _AUDIENCE_INSTRUCTIONS.get(audience, _AUDIENCE_INSTRUCTIONS["pm"])

    return f"""\
Project name: {project.project_name}
Problem statement: {project.problem_statement}
Current symptoms: {json.dumps(project.current_symptoms)}
Current metrics: {json.dumps(project.current_metrics)}
Constraints: {json.dumps(project.constraints)}
Stakeholder concerns: {json.dumps(project.stakeholder_concerns)}

Mode instruction: {mode_instruction}

Audience instruction for role_summary: {audience_instruction}

Return a single JSON object with this exact structure (all fields required):
{{
  "cleaned_problem_statement": "One to two sentences naming the process, the measurable gap, and the business impact.",
  "ctqs": [
    {{"statement": "...", "evidence_tag": "directly_supported_by_input|inferred_hypothesis|missing_evidence"}}
  ],
  "sipoc": {{
    "suppliers": ["..."],
    "inputs": ["..."],
    "process": ["step 1", "step 2", "step 3", "step 4", "step 5"],
    "outputs": ["..."],
    "customers": ["..."]
  }},
  "dmaic_structure": {{
    "define":   [{{"statement": "...", "evidence_tag": "..."}}],
    "measure":  [{{"statement": "...", "evidence_tag": "..."}}],
    "analyze":  [{{"statement": "...", "evidence_tag": "..."}}],
    "improve":  [{{"statement": "...", "evidence_tag": "..."}}],
    "control":  [{{"statement": "...", "evidence_tag": "..."}}]
  }},
  "root_causes": [
    {{"statement": "...", "evidence_tag": "..."}}
  ],
  "suggested_metrics": [
    {{"statement": "...", "evidence_tag": "..."}}
  ],
  "improvement_actions": [
    {{"statement": "...", "evidence_tag": "..."}}
  ],
  "control_plan": [
    {{"statement": "...", "evidence_tag": "..."}}
  ],
  "action_tracker": [
    {{"action": "...", "owner": "...", "priority": "high|medium|low", "status": "proposed"}}
  ],
  "project_memory": {{
    "baseline": ["..."],
    "root_cause_hypotheses": ["..."],
    "chosen_actions": ["..."],
    "control_metrics": ["..."],
    "unresolved_risks": ["..."]
  }},
  "role_summary": "..."
}}

Quality requirements:
- cleaned_problem_statement: specific to this project, not generic
- ctqs: 4-6 items tied to what stakeholders and customers actually care about
- sipoc: realistic to this specific project and industry context
- dmaic_structure: 2-4 items per phase, each specific and actionable for this project
- root_causes: 4-7 items; in root_cause mode expand with 5 Whys chain and fishbone categories
- suggested_metrics: 4-6 items with specific measurement approaches and targets where possible
- improvement_actions: 4-6 items ordered by priority, each naming a specific action and expected effect
- control_plan: 4-5 items each with owner role, cadence, and threshold trigger
- action_tracker: 4-5 rows with realistic owner roles and priorities derived from the improvement actions
- project_memory: 3-5 items per section, capturing what is known, hypothesised, and unknown
- role_summary: 3-5 sentences tailored exactly to the audience instruction above
"""


# ── Deterministic fallback ────────────────────────────────────────────────────

def _deterministic_fallback(project: ProjectInput, mode: str, audience: str) -> AssessmentResult:
    """
    High-quality structured fallback used when no API key is available or the LLM call fails.
    Produces evidence-tagged outputs using the project inputs directly.
    """
    root_causes = [
        _inferred("Problem framing may be too vague, causing teams to address symptoms instead of underlying systemic issues."),
        _inferred("Role or handoff ambiguity is a likely driver of delay and rework based on the reported symptoms."),
        _inferred("Current measurement may not fully reflect the true Critical-to-Quality factors."),
        _inferred("Stakeholder alignment may be insufficient at key decision or handoff points."),
    ]
    if project.constraints:
        root_causes.append(_supported(f"Active constraint influencing process performance: {project.constraints[0]}"))
    if len(project.current_symptoms) > 1:
        root_causes.append(_supported(f"Symptom pattern suggesting systemic cause: {project.current_symptoms[1]}"))

    if mode == "root_cause":
        first_symptom = project.current_symptoms[0] if project.current_symptoms else project.problem_statement
        root_causes = [
            _supported(f"Why-1: {first_symptom}"),
            _inferred("Why-2: The process lacks clear ownership at the point where this symptom occurs."),
            _inferred("Why-3: Ownership is unclear because roles and responsibilities were never formally defined for this workflow."),
            _inferred("Why-4: Roles were never defined because the process grew informally without a structured design phase."),
            _inferred("Root cause (Why-5): No formal process design or governance was established when the workflow was introduced."),
            _inferred("Fishbone — People: Insufficient training or unclear accountability for process participants."),
            _inferred("Fishbone — Process: Steps are ad hoc, undocumented, or inconsistently followed."),
            _inferred("Fishbone — Measurements: No leading indicators are tracked; issues are only visible after the fact."),
            _inferred("Fishbone — Environment: Competing priorities or deadlines create pressure that bypasses standard process."),
        ]

    if mode == "process_waste":
        root_causes = [
            _inferred("Waste — Waiting: Delays between process steps due to unclear handoff triggers or unavailable approvers."),
            _inferred("Waste — Defects: Rework and error correction consuming capacity that should go to value-adding work."),
            _inferred("Waste — Over-processing: More review cycles, sign-offs, or documentation than the output requires."),
            _inferred("Waste — Motion: Unnecessary escalation loops and information routing adding non-value steps."),
            _inferred("Waste — Skills underutilisation: Team members spending time on administrative tasks instead of expertise-led work."),
        ]

    improvement_actions = [
        _inferred("Clarify ownership and decision rights at the major handoff points identified in the SIPOC."),
        _inferred("Standardise intake and prioritisation criteria to reduce ambiguity at process entry."),
        _inferred("Pilot a reduced-scope improvement with explicit acceptance criteria before broad rollout."),
        _inferred("Introduce a visible action tracker with named owner, due date, and status for each open issue."),
    ]

    if mode == "kaizen":
        improvement_actions = [
            _inferred("Quick win: create a one-page process map showing current state and agreed next steps — complete within one week."),
            _inferred("Quick win: hold a 30-minute team standup to agree on the top three pain points and assign an owner to each."),
            _inferred("Quick win: implement a simple status board (physical or digital) to make work-in-progress visible."),
            _inferred("Short cycle: run a two-week improvement sprint on the highest-frequency defect or delay."),
        ]

    control_plan = [
        _inferred("Assign a named owner to each critical metric and confirm accountability formally."),
        _inferred("Review leading indicators weekly during the first stabilisation period (minimum 4 weeks)."),
        _inferred("Trigger escalation when a core metric breaches its target threshold on two consecutive review cycles."),
        _inferred("Document unresolved risks and review them at each status checkpoint to prevent drift."),
    ]

    if mode == "control_plan":
        control_plan = [
            _inferred("Metric: on-time completion rate — Owner: PM — Cadence: weekly — Trigger: drops below target for 2 consecutive weeks — Response: root cause review with sponsor."),
            _inferred("Metric: rework rate — Owner: Quality Lead — Cadence: bi-weekly — Trigger: exceeds 15% — Response: immediate process audit."),
            _inferred("Metric: cycle time — Owner: Process Owner — Cadence: weekly — Trigger: increases more than 20% from baseline — Response: bottleneck analysis."),
            _inferred("Metric: escalation volume — Owner: Manager — Cadence: monthly — Trigger: more than 3 escalations per cycle — Response: ownership and criteria review."),
        ]

    owners = ["PM", "Process owner", "Quality lead", "Analyst"]
    priorities = ["high", "high", "medium", "medium"]
    tracker = [
        {"action": item.statement[:120], "owner": owners[i], "priority": priorities[i], "status": "proposed"}
        for i, item in enumerate(improvement_actions[:4])
    ]

    _audience_summaries: Dict[str, str] = {
        "executive": (
            f"Executive summary: {project.project_name} has a confirmed performance gap — "
            f"{project.problem_statement.strip()} "
            "If unaddressed, this will continue to drive rework, missed deadlines, and stakeholder dissatisfaction. "
            "A structured improvement with clear ownership and measurable targets is recommended as the next step."
        ),
        "manager": (
            f"Manager summary for {project.project_name}: the immediate priorities are ownership clarity, "
            "a controlled pilot of the top improvement action, and a weekly metric review cadence. "
            "Assign named owners to the top three actions within the next 5 business days."
        ),
        "quality_lead": (
            f"Quality summary: the CTQs for {project.project_name} need to be validated against stakeholder expectations. "
            "Current metrics provide a partial baseline but historical trend data is missing. "
            "Measurement system integrity should be confirmed before improvement actions are finalised."
        ),
        "engineer": (
            f"Engineer summary: map the current-state process for {project.project_name} to identify the "
            "specific steps where handoff failures, delays, and rework occur. "
            "Instrument at least two measurement points to create an observable baseline before piloting changes."
        ),
        "pm": (
            f"PM summary: validate the problem statement for {project.project_name} with key stakeholders, "
            "confirm CTQs, assign owners to the top improvement actions, and schedule a pilot with defined success criteria. "
            "Three immediate actions: (1) stakeholder alignment meeting, (2) baseline data collection, (3) pilot scope definition."
        ),
    }

    return AssessmentResult(
        project_name=project.project_name,
        mode=mode,
        audience=audience,
        cleaned_problem_statement=(
            f"{project.project_name} has a measurable performance gap: {project.problem_statement.strip()} "
            f"Key symptoms include: {'; '.join(project.current_symptoms[:3])}."
        ),
        ctqs=[
            *[_supported(f"CTQ linked to reported metric: {name} (current: {val})")
              for name, val in list(project.current_metrics.items())[:3]],
            _inferred("CTQ: cycle time or lead time through the core process steps"),
            _inferred("CTQ: defect, rework, or reopening rate as a signal of first-time quality"),
        ],
        sipoc={
            "suppliers": ["upstream teams", "data source owners", "requesting stakeholders"],
            "inputs": [project.problem_statement[:80], *project.current_symptoms[:2]],
            "process": ["define scope", "measure current state", "analyse root causes", "improve process", "control outcomes"],
            "outputs": ["improved process performance", "reduced rework", "clear ownership and control plan"],
            "customers": ["project sponsor", "process owner", "downstream teams and end users"],
        },
        dmaic_structure={
            "define": [
                _supported(f"Problem confirmed: {project.problem_statement.strip()}"),
                _supported(f"Stakeholder concerns: {', '.join(project.stakeholder_concerns[:3])}"),
            ],
            "measure": [
                _supported(f"Available metrics: {', '.join(f'{k}={v}' for k, v in project.current_metrics.items())}"),
                _missing("Historical trend data and variance analysis are not yet provided and must be collected."),
            ],
            "analyze": [
                _inferred("Root cause cluster likely involves handoff or ownership ambiguity."),
                _inferred("Waste cluster likely involves waiting, rework, or unclear prioritisation criteria."),
            ],
            "improve": [
                _inferred("Pilot one high-impact change before broad rollout to contain risk."),
                _inferred("Standardise intake, triage, and acceptance criteria to reduce entry-point ambiguity."),
            ],
            "control": [
                _inferred("Define control owner, review cadence, and threshold triggers per metric."),
                _inferred("Track recurrence rate and open risks at each post-implementation checkpoint."),
            ],
        },
        root_causes=root_causes,
        suggested_metrics=[
            *[_supported(f"Track existing metric: {k} = {v} — establish target and trend")
              for k, v in list(project.current_metrics.items())[:3]],
            _inferred("Track cycle time by major workflow stage to isolate where time is lost."),
            _inferred("Track first-pass yield or rework rate as the primary quality signal."),
            _inferred("Track escalation volume and recurrence rate as a control metric."),
        ],
        improvement_actions=improvement_actions,
        control_plan=control_plan,
        action_tracker=tracker,
        project_memory={
            "baseline": [f"{k}: {v}" for k, v in project.current_metrics.items()],
            "root_cause_hypotheses": [item.statement for item in root_causes[:4]],
            "chosen_actions": [item.statement[:100] for item in improvement_actions[:3]],
            "control_metrics": [item.statement[:100] for item in control_plan[:3]],
            "unresolved_risks": [
                "Historical trend and variance data are not yet available",
                "Stakeholder alignment across all affected teams has not been confirmed",
                f"Constraint impact not yet fully quantified: {project.constraints[0] if project.constraints else 'none stated'}",
            ],
        },
        role_summary=_audience_summaries.get(audience, _audience_summaries["pm"]),
    )


# ── LLM-powered assessment ────────────────────────────────────────────────────

def run_llm_assessment(project: ProjectInput, mode: str, audience: str) -> AssessmentResult:
    """
    Primary entry point. Calls the Anthropic API when ANTHROPIC_API_KEY is set.
    Falls back to the deterministic implementation automatically on any failure.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return _deterministic_fallback(project, mode, audience)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_user_message(project, mode, audience)}],
        )

        raw = message.content[0].text.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            if raw.endswith("```"):
                raw = raw[: raw.rfind("```")]
            raw = raw.strip()

        data: Dict[str, Any] = json.loads(raw)

        return AssessmentResult(
            project_name=project.project_name,
            mode=mode,
            audience=audience,
            cleaned_problem_statement=data["cleaned_problem_statement"],
            ctqs=_parse_items(data["ctqs"]),
            sipoc=data["sipoc"],
            dmaic_structure=_parse_dmaic(data["dmaic_structure"]),
            root_causes=_parse_items(data["root_causes"]),
            suggested_metrics=_parse_items(data["suggested_metrics"]),
            improvement_actions=_parse_items(data["improvement_actions"]),
            control_plan=_parse_items(data["control_plan"]),
            action_tracker=data["action_tracker"],
            project_memory=data["project_memory"],
            role_summary=data["role_summary"],
        )

    except Exception:
        return _deterministic_fallback(project, mode, audience)
