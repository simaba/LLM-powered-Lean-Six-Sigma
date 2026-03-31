from __future__ import annotations

from typing import Iterable


def build_leadership_deck_markdown(
    project_name: str,
    status_narrative: str,
    leadership_summary: Iterable[str],
    top_actions: Iterable[str],
    top_risks: Iterable[str],
) -> str:
    summary = '\n'.join(f'- {item}' for item in leadership_summary)
    actions = '\n'.join(f'- {item}' for item in top_actions)
    risks = '\n'.join(f'- {item}' for item in top_risks)
    return f"""# {project_name}

## Slide 1. Executive snapshot

{status_narrative}

## Slide 2. Leadership summary

{summary}

## Slide 3. Priority actions

{actions}

## Slide 4. Top risks

{risks}

## Slide 5. Recommended next step

- Validate the highest-priority action with stakeholders.
- Confirm control ownership and review cadence.
- Pilot one change before broader rollout.
"""
