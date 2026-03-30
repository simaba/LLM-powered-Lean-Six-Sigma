# Non-Technical UI Guide

This repository includes a Streamlit app so the system can be used without PowerShell or command-line steps.

## Start the app

From the repository folder, run:

```bash
streamlit run app.py
```

Then open the local browser link shown by Streamlit.

## What the app does

The app provides a guided form for entering:
- project name
- problem statement
- current symptoms
- current metrics
- constraints
- stakeholder concerns

It then generates structured Lean Six Sigma outputs through a non-technical interface.

## Main sections in the app

### Overview
Shows the cleaned-up problem statement, likely CTQs, and a SIPOC draft.

### DMAIC
Shows the Define, Measure, Analyze, Improve, and Control structure.

### Root Cause
Shows likely root causes and saved project memory.

### Improvements
Shows suggested metrics, improvement actions, and action tracker.

### Control Plan
Shows the control plan draft including ownership and review logic.

### Summary
Shows the role-aware summary and allows markdown download.

## Best way to use it

1. Start with the sample values.
2. Replace them with your real project details.
3. Generate the assessment.
4. Review the evidence tags carefully.
5. Validate hypotheses before acting on them.
6. Download the markdown summary for sharing.

## Important note

This tool is designed to structure thinking, not replace Lean Six Sigma judgment. It should be used to accelerate analysis and improve consistency, not to automate decisions blindly.
