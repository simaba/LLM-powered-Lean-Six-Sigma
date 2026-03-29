# LLM-powered Lean Six Sigma

A structured AI copilot for applying Lean Six Sigma thinking to real projects step by step.

## Why this repository exists

Many projects have messy symptoms, vague problem statements, scattered evidence, and rushed solutions.
This repository is a practical starter system for using AI and LLM workflows to structure Lean Six Sigma reasoning with clear phases, evidence discipline, and reusable artifacts.

## What the system accepts

The user provides:
- project name
- problem statement
- current symptoms
- current metrics
- constraints
- stakeholder concerns

## What the system generates

The system produces structured outputs such as:
- cleaned-up problem statement
- likely CTQs
- SIPOC draft
- possible root causes
- suggested metrics to track
- suggested improvement actions
- control plan draft
- executive summary and action tracker

## Core phases

### Phase 1. LSS project structurer
Takes project input and produces a DMAIC-oriented project structure.

### Phase 2. Root cause assistant
Supports 5 Whys, fishbone categories, bottleneck detection, and issue clustering.

### Phase 3. Improvement prioritizer
Ranks actions by impact, effort, risk, and quick-win potential.

### Phase 4. Control plan generator
Defines owners, metrics, review cadence, and threshold-based triggers.

### Phase 5. Dashboard and reporting layer
Creates leadership summary, action tracker, status narrative, and before-vs-after view.

## Modes

- DMAIC mode
- Kaizen mode
- Root cause mode
- Process waste mode
- Control plan mode

## Design principles

- structured outputs over generic advice
- evidence tags for trustworthiness
- role-aware summaries for different audiences
- persistent project memory for baseline, hypotheses, actions, controls, and risks
- reusable artifacts such as SIPOC, CTQ tree, fishbone draft, control plan, and A3 summary

## Repository structure

- `run_demo.py`
- `src/models.py`
- `src/engine.py`
- `src/phases.py`
- `src/renderers.py`
- `examples/sample_project.json`
- `examples/sample_output.md`
- `docs/architecture.md`
- `docs/modes.md`
- `docs/evidence-discipline.md`
- `templates/project_input_template.json`

## Quick start

```bash
python run_demo.py --input examples/sample_project.json --mode dmaic
```

## Current scope

This repository is a structured MVP and reference implementation. It does not claim to replace human judgment. It is designed to accelerate and discipline Lean Six Sigma reasoning, not automate it blindly.
