# LSS Copilot — LLM-powered Lean Six Sigma

An AI copilot that turns messy project descriptions into rigorous, evidence-tagged Lean Six Sigma improvement packages — and a full Black Belt analytics workbench with statistical tools for data-driven analysis.

---

## What you get

### 📋 Project Wizard (5-step guided workflow)
Describe your project → receive a complete structured improvement package:

| Output | What it is |
|---|---|
| **Cleaned problem statement** | Rewritten to be specific, measurable, and scoped |
| **CTQs** | Critical-to-Quality characteristics tied to customer requirements |
| **SIPOC** | Suppliers → Inputs → Process → Outputs → Customers map |
| **Full DMAIC structure** | Define / Measure / Analyze / Improve / Control — all five phases |
| **Root cause analysis** | 5 Whys chain, fishbone structure (mode-dependent) |
| **Suggested metrics** | What to measure and how |
| **Improvement actions** | Prioritised, specific actions with effort/impact context |
| **Control plan** | Owners, review cadence, escalation triggers |
| **Action tracker** | Tabled by priority |
| **Role-aware summary** | Framed for your audience (Engineer, PM, Manager, Quality Lead, Executive) |

Every output item is tagged with one of three evidence labels so you always know what's fact, what's inference, and what's missing.

### ⚡ Black Belt Analytics Workbench (9 tools)
Upload your data and run quantitative analysis directly in the app:

| Tool | What it does |
|---|---|
| **Process Capability** | Cp, Cpk, Pp, Ppk, sigma level, DPMO, capability histogram |
| **MSA / Gauge R&R** | Repeatability, reproducibility, %GRR, NDC (ANOVA method, AIAG MSA-4) |
| **Hypothesis Testing** | One-sample t, two-sample t, paired t, proportion tests, chi-square, ANOVA |
| **SPC Charts** | I-MR, Xbar-R, p-chart — Nelson rules, out-of-control detection |
| **FMEA** | RPN builder, risk matrix, Pareto — fully interactive |
| **Regression** | Simple and multiple OLS with diagnostics (VIF, Breusch-Pagan, Durbin-Watson) |
| **DOE** | Factor definition, design recommendation (full factorial / fractional / Plackett-Burman) |
| **Benefits & COPQ** | ROI, payback period, 3-year NPV, waterfall and timeline charts |

---

## How to install

### Step 1 — Make sure Python is installed

Open a terminal (Windows: press **Win + R**, type `cmd`, press Enter) and run:

```
python --version
```

You need Python **3.10 or later**. If you see an error, download Python from [python.org](https://www.python.org/downloads/) and install it. Tick **"Add Python to PATH"** during installation.

---

### Step 2 — Download the project

If you have Git:
```
git clone https://github.com/simaba/LLM-powered-Lean-Six-Sigma.git
cd LLM-powered-Lean-Six-Sigma
```

Or download the ZIP from GitHub → click **Code → Download ZIP** → extract it → open a terminal in that folder.

---

### Step 3 — Install dependencies

In the terminal, run:
```
pip install -r requirements.txt
```

This installs Streamlit, the Anthropic SDK, all statistical libraries (NumPy, SciPy, statsmodels), and the export libraries (fpdf2, python-docx, openpyxl).

> **If `pip` is not found:** try `pip3 install -r requirements.txt` or `python -m pip install -r requirements.txt`

---

### Step 4 — Add your API key (optional but recommended)

Without an API key the app runs in **structured fallback mode** — it still produces high-quality, evidence-tagged outputs based on your inputs, but without LLM reasoning.

With a Claude API key you get **fully AI-powered, project-specific analysis**.

**Windows:**
```
set ANTHROPIC_API_KEY=your_key_here
```

**Mac / Linux:**
```
export ANTHROPIC_API_KEY=your_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com).

---

### Step 5 — Launch the app

```
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## First project in 5 minutes

1. **Open the app** — you land on the Project Intake screen.
2. **Click "Load sample project"** to pre-fill a working example.
3. **Click "Next: Configure"** and choose a methodology mode (start with **DMAIC**) and audience (start with **PM**).
4. **Click "Next: Generate"** then **"▶ Run Assessment"**. The analysis takes 5–15 seconds.
5. **Explore the Dashboard** — six tabs: Overview, DMAIC, Root Cause, Improvements, Control Plan, Summary.
6. **Click "Export"** and download a PDF, Word, Excel, or HTML file.

---

## Using the Analytics Workbench

Click **⚡ Analytics** in the sidebar (replaces the wizard).

- Start in the **📂 Data Hub** tab — upload a CSV or Excel file.
- Switch to any analytics tab (Capability, SPC, etc.) — the uploaded data is available across all tabs.
- You can also **paste numbers directly** in any tab without uploading a file.
- The **FMEA** and **Benefits/COPQ** tools build tables interactively — no data file needed.

---

## Methodology modes

| Mode | When to use |
|---|---|
| **DMAIC** | Structured improvement projects with a clear before/after goal |
| **Kaizen** | Quick wins, rapid improvement cycles, small-scope issues |
| **Root Cause** | When the cause is unclear — produces 5 Whys chain + fishbone |
| **Process Waste** | Flow and efficiency problems — TIMWOODS waste taxonomy |
| **Control Plan** | Sustaining gains — control items with owners and triggers |

---

## Audience modes

| Audience | What changes |
|---|---|
| **Engineer** | Process detail, measurement systems, technical bottlenecks |
| **Project Manager** | Actions, owners, milestones, risk tracking |
| **Manager** | Team accountability, top priorities, 30-day action list |
| **Quality Lead** | CTQ alignment, measurement integrity, control plan rigor |
| **Executive** | Business impact, plain language, decision-ready — no jargon |

---

## Evidence discipline

Every output item carries one of three tags:

| Tag | Meaning |
|---|---|
| ✓ **directly_supported_by_input** | Statement is grounded in the data you provided |
| ~ **inferred_hypothesis** | Logical inference — plausible but not yet proven |
| ! **missing_evidence** | Important data is absent — this needs investigation |

This ensures the system never presents assumptions as facts. The evidence quality chart in the Dashboard shows the breakdown across all outputs.

---

## Export formats

| Format | Best for |
|---|---|
| **PDF** | Printing, emailing leadership, formal submissions |
| **Word (.docx)** | Editing, customising, adding to existing documents |
| **Excel (.xlsx)** | 6-sheet workbook — data tables, action tracking |
| **HTML** | Browser viewing, sharing via link, embedding in portals |
| **Markdown** | Notion, Confluence, GitHub, any text editor |

---

## CLI usage

For automated or batch runs:

```bash
python run_demo.py --input examples/sample_project.json --mode dmaic --audience pm
```

---

## Repository structure

```
app.py                          ← Flagship Streamlit application (wizard + workbench)
run_demo.py                     ← CLI entry point
requirements.txt

src/
  models.py                     ← ProjectInput, EvidenceItem, AssessmentResult dataclasses
  engine.py                     ← Assessment orchestrator
  phases/
    __init__.py                 ← LLM-powered phase logic with structured fallback
  renderers.py                  ← Markdown and HTML export renderers
  exporters.py                  ← PDF, Word, and Excel export

ui/
  forms.py                      ← Project input form components
  render.py                     ← Tab rendering components
  dashboard_insights.py         ← Chart builders and executive signals
  analytics_workbench.py        ← Black Belt Analytics Workbench (9 tools)

analytics/
  capability.py                 ← Cp / Cpk / Pp / Ppk / sigma / DPMO
  msa.py                        ← Gauge R&R (ANOVA method, AIAG MSA-4)
  hypothesis_tests.py           ← 7 statistical tests with plain-English output
  spc.py                        ← I-MR, Xbar-R, p-chart with Nelson rules
  fmea.py                       ← FMEA builder, RPN, risk matrix, Pareto
  regression.py                 ← Simple and multiple OLS with diagnostics
  doe.py                        ← DOE design assistant (factorial / fractional / PB)
  benefits.py                   ← COPQ, ROI, payback, 3-year NPV

storage/
  projects.py                   ← Save and load project snapshots (JSON)

examples/
  sample_project.json
  sample_output.md

templates/
  project_input_template.json
```

---

## Troubleshooting

**"ModuleNotFoundError"**
→ Run `pip install -r requirements.txt` again. If a specific module fails, install it directly: `pip install <module-name>`

**"streamlit: command not found"**
→ Try `python -m streamlit run app.py`

**PDF download produces garbled characters**
→ The PDF exporter auto-converts special characters to ASCII. If you see issues, switch to Word or HTML export.

**App loads but "Claude AI connected" doesn't appear**
→ Your API key may not be set in this terminal session. Set it and restart the app.

**API key is set but results seem generic**
→ Make sure the key is valid and your account has API credits. The app falls back to structured mode automatically if the API call fails.

**On Windows: `set` command doesn't persist between sessions**
→ Set the key permanently: System Properties → Environment Variables → New → `ANTHROPIC_API_KEY`

---

## Design principles

- **Evidence discipline** — every output is tagged supported / inferred / missing
- **Structured outputs** over free-form advice
- **Role-aware summaries** for different audiences
- **Mode-specific reasoning** (DMAIC, Kaizen, Root Cause, Waste, Control)
- **Black Belt analytics** — full quantitative toolkit embedded alongside the wizard
- **Graceful degradation** — fully functional without an API key
- **One canonical backend** — one engine, one phase logic source, one flagship app
