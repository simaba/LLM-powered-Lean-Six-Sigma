"""
project_library.py
==================
A curated library of 12 realistic Lean Six Sigma example project definitions,
used as a coaching and learning tool within the LLM-powered LSS Streamlit app.

Each project entry is a fully populated dict containing problem statements,
current metrics, weak/strong input examples, common mistakes, and next steps.
The library covers six domains and six problem types across three complexity
levels, giving practitioners and students concrete reference material when
learning to frame, scope, and execute improvement projects.

Usage
-----
    from examples.project_library import PROJECT_LIBRARY, get_project_by_id

    project = get_project_by_id("mfg_defect_rate")
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Project library
# ---------------------------------------------------------------------------

PROJECT_LIBRARY: list[dict] = [
    # -----------------------------------------------------------------------
    # 1. Manufacturing – defects / errors
    # -----------------------------------------------------------------------
    {
        "id": "mfg_defect_rate",
        "title": "Manufacturing Defect Rate Reduction – Assembly Line B",
        "domain": "Manufacturing",
        "problem_type": "defects / errors",
        "complexity": "Practitioner",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Pareto Chart",
            "Fishbone / Ishikawa",
            "Measurement System Analysis (MSA)",
            "Hypothesis Test (2-proportion)",
            "Control Chart (p-chart)",
            "FMEA",
        ],
        "project_name": "Assembly Line B Defect Rate Reduction",
        "problem_statement": (
            "The defect rate on Assembly Line B increased from 2.1% to 4.8% "
            "over the past 4 months (October–January), causing an estimated "
            "$186,000 in scrap and rework costs and pushing the line 12% below "
            "its throughput target."
        ),
        "current_symptoms": [
            "Visual inspection failures spiking on connector sub-assembly station 4",
            "Scrap bins at station 4 and station 7 consistently over capacity",
            "Rework loop cycle time increased from 8 min to 21 min per unit",
            "Customer returns citing intermittent connection faults up 31% QoQ",
            "Line supervisor logging daily stoppages for quality holds",
        ],
        "current_metrics": {
            "Defect Rate (Line B)": "4.8% (baseline: 2.1%)",
            "Monthly Scrap Cost": "$46,500 (baseline: $18,200)",
            "Rework Rate": "11.3% of units require rework loop",
            "Throughput": "1,840 units/day (target: 2,090 units/day)",
            "Customer Return Rate": "1.9% (baseline: 1.1%)",
        },
        "constraints": [
            "Line cannot be shut down for more than 4 hours in any single week",
            "No capital expenditure approved; solutions must use existing equipment",
            "Engineering change freeze until Q2 product review board",
            "Team of two quality engineers and one process engineer available part-time",
        ],
        "stakeholder_concerns": [
            "Plant Manager: throughput impact on shipping commitments",
            "Quality Director: risk of customer escalation and potential recall",
            "Finance: scrap and rework cost trending toward $560K annualised",
            "Operators: unclear whether the issue is tooling, materials, or training",
        ],
        "weak_input_example": (
            "We have too many defects on the assembly line. "
            "Quality is getting worse and we need to fix it."
        ),
        "strong_input_example": (
            "The defect rate on Assembly Line B increased from 2.1% to 4.8% "
            "over the past 4 months (October–January), causing an estimated "
            "$186,000 in scrap and rework costs and pushing the line 12% below "
            "its throughput target."
        ),
        "common_mistakes": [
            "Jumping to solutions (e.g., retraining operators) before measuring defect stratification",
            "Not validating the measurement system — gauge repeatability can mask real signals",
            "Treating all defect types as one population instead of stratifying by station, shift, and part number",
            "Ignoring the 4-month timeline — changes in supplier, tooling, or staffing around October are key clues",
            "Setting a target ('reduce to 2%') without a defined timeline or confidence interval",
        ],
        "what_good_output_looks_like": (
            "A DMAIC charter with a quantified goal (e.g., reduce defect rate to ≤2.1% "
            "within 90 days), a stratified Pareto identifying the top 2-3 defect modes "
            "by station, a fishbone with at least 4 confirmed root causes supported by "
            "data, a hypothesis test result (p < 0.05) linking at least one X to the "
            "defect rate increase, and a control plan specifying p-chart limits and "
            "reaction plan at station 4."
        ),
        "next_steps": [
            "Stratify defect data by type, station, shift, and operator for the past 6 months",
            "Run an MSA (Gauge R&R) on the visual inspection process at station 4",
            "Overlay defect trend with change log: supplier lot changes, tooling PM dates, new hires",
            "Conduct 5 Whys workshops with station 4 and 7 operators",
            "Run a 2-proportion hypothesis test comparing defect rates before and after October",
            "Develop and implement a corrective action plan targeting top root causes",
            "Implement p-chart on Line B with control limits and daily review cadence",
        ],
        "tags": ["assembly", "scrap", "rework", "connector", "p-chart", "MSA", "FMEA"],
    },

    # -----------------------------------------------------------------------
    # 2. Supply Chain – delays / cycle time
    # -----------------------------------------------------------------------
    {
        "id": "delivery_delay",
        "title": "Supply Chain On-Time Delivery Recovery",
        "domain": "Supply Chain",
        "problem_type": "delays / cycle time",
        "complexity": "Practitioner",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Value Stream Map",
            "Pareto Chart",
            "Regression Analysis",
            "Run Chart",
            "Root Cause Analysis (5 Whys)",
            "SIPOC",
        ],
        "project_name": "On-Time Delivery Improvement – Distribution Network",
        "problem_statement": (
            "On-time delivery (OTD) across the North America distribution network "
            "declined from 94% to 78% over 6 months (July–December), resulting in "
            "$2.3M in contractual penalty charges and the loss of two key accounts "
            "representing $8.7M in annual revenue."
        ),
        "current_symptoms": [
            "Carrier on-time performance reports showing consistent late departures from DC-3",
            "Order confirmation to pick-ticket release averaging 26 hours vs 4-hour SLA",
            "Backlog of 340+ open orders aged beyond 5 days in the WMS queue",
            "Customer escalations to account management up 58% in Q4",
            "Weekend and holiday shipments experiencing 2-3 day additional delays",
        ],
        "current_metrics": {
            "On-Time Delivery Rate": "78% (baseline: 94%)",
            "Order-to-Ship Cycle Time": "4.2 days (target: 2.0 days)",
            "Penalty Charges (6-month)": "$2.3M",
            "Carrier On-Time Pick-up Rate": "82% (baseline: 96%)",
            "Backlogged Orders > 5 Days": "340 orders (3.4% of volume)",
        },
        "constraints": [
            "Cannot change primary carrier contracts until renewal in Q3",
            "WMS upgrade is 9 months out; no system changes approved until then",
            "DC-3 operates with fixed staffing — no headcount additions approved",
            "International shipments excluded from scope (handled by separate team)",
        ],
        "stakeholder_concerns": [
            "VP Supply Chain: penalty charges and account retention are top priorities",
            "Sales: two at-risk accounts requesting weekly OTD dashboards",
            "DC-3 Operations Manager: staffing model and shift handover gaps",
            "IT: WMS configuration change requests require 3-week approval cycle",
            "Finance: $2.3M penalty reserve impacting quarterly operating income",
        ],
        "weak_input_example": (
            "Our deliveries are late and customers are complaining. "
            "We need to improve our supply chain."
        ),
        "strong_input_example": (
            "On-time delivery across the North America distribution network "
            "declined from 94% to 78% over 6 months (July–December), resulting in "
            "$2.3M in contractual penalty charges and the loss of two key accounts "
            "representing $8.7M in annual revenue."
        ),
        "common_mistakes": [
            "Focusing exclusively on carrier performance while ignoring internal pick/pack delays",
            "Not segmenting OTD by DC, carrier, product category, and customer tier",
            "Confusing 'ship date' with 'delivery date' in measurement — align definitions first",
            "Treating this as a carrier problem rather than a systemic handoff problem",
            "Not establishing a baseline process map before proposing solutions",
        ],
        "what_good_output_looks_like": (
            "A DMAIC charter targeting ≥91% OTD within 120 days, a current-state VSM "
            "highlighting the order confirmation bottleneck, a stratified Pareto of delay "
            "reasons (internal vs. carrier vs. customer-caused), a regression model "
            "identifying the top 2 predictors of late delivery, and a corrective action "
            "log with owners and due dates tied to each root cause."
        ),
        "next_steps": [
            "Map the end-to-end order-to-delivery process with swim lanes to identify handoff gaps",
            "Stratify late deliveries by DC, carrier, day-of-week, and product category",
            "Perform a detailed time study on the order release process at DC-3",
            "Conduct root cause interviews with DC-3 shift supervisors and carrier reps",
            "Run regression to identify strongest predictors of late delivery",
            "Implement interim controls: daily OTD scorecard, expedite queue for aged orders",
            "Define and pilot revised shift handover checklist at DC-3",
        ],
        "tags": ["logistics", "OTD", "distribution", "carrier", "WMS", "penalty", "cycle time"],
    },

    # -----------------------------------------------------------------------
    # 3. Customer Support – delays / cycle time
    # -----------------------------------------------------------------------
    {
        "id": "call_handle_time",
        "title": "Call Center Average Handle Time Reduction Post-Migration",
        "domain": "Customer Support",
        "problem_type": "delays / cycle time",
        "complexity": "Beginner",
        "recommended_mode": "kaizen",
        "typical_tools": [
            "5 Whys",
            "Time Study / Work Sampling",
            "Spaghetti Diagram",
            "Pareto Chart",
            "Standard Work",
            "Run Chart",
        ],
        "project_name": "AHT Reduction – Customer Service Center Post-CRM Migration",
        "problem_statement": (
            "Average handle time (AHT) in the customer service center increased by 35% "
            "from 4.8 minutes to 6.5 minutes following the CRM platform migration in "
            "March, resulting in a 22% increase in customer queue wait times and an "
            "annualised labour cost overrun of $410,000."
        ),
        "current_symptoms": [
            "Agents visibly navigating multiple screens to locate account history",
            "Post-call wrap-up time increased from 45 seconds to 2.3 minutes",
            "Escalation rate to Tier 2 up from 8% to 14% since migration",
            "Agent satisfaction survey scores dropped 18 points on 'system usability'",
            "Average speed to answer (ASA) now 3.1 minutes vs 1.4-minute SLA",
        ],
        "current_metrics": {
            "Average Handle Time": "6.5 min (baseline: 4.8 min)",
            "Post-Call Wrap-Up Time": "2.3 min (baseline: 45 sec)",
            "Average Speed to Answer": "3.1 min (SLA: 1.4 min)",
            "Tier 2 Escalation Rate": "14% (baseline: 8%)",
            "Agent System Usability Score": "51/100 (baseline: 74/100)",
        },
        "constraints": [
            "CRM platform cannot be rolled back — migration is permanent",
            "Agent scheduling is fixed for the next 8 weeks",
            "IT system configuration changes require change-management approval (2-week SLA)",
            "Call recording system captures audio only — no screen capture available",
        ],
        "stakeholder_concerns": [
            "Contact Centre Director: SLA breach and potential penalty from outsource contract",
            "HR / Workforce Management: overtime costs driven by longer handle times",
            "IT: concerned about scope creep requests for CRM reconfiguration",
            "Agents: frustrated with new system navigation; morale risk",
            "Customers: NPS survey comments citing long hold times as top complaint",
        ],
        "weak_input_example": (
            "Agents are taking too long on calls since we upgraded the system. "
            "We need to train them better."
        ),
        "strong_input_example": (
            "Average handle time in the customer service center increased by 35% "
            "from 4.8 minutes to 6.5 minutes following the CRM platform migration in "
            "March, resulting in a 22% increase in customer queue wait times and an "
            "annualised labour cost overrun of $410,000."
        ),
        "common_mistakes": [
            "Jumping to retraining without measuring where in the call the time is being lost",
            "Not separating talk time from hold time from wrap-up time in the data",
            "Assuming all agents are equally affected — segment by experience level and call type",
            "Blaming the technology without analysing the workflow and navigation patterns",
            "Setting AHT targets so low that quality and customer satisfaction suffer",
        ],
        "what_good_output_looks_like": (
            "A Kaizen event report identifying the top 3 time-wasting steps in the new CRM "
            "workflow (supported by time study data), standard work documentation for the "
            "revised navigation sequence, a before/after AHT run chart showing improvement, "
            "and a 30-day sustainment plan with weekly AHT tracking by agent cohort."
        ),
        "next_steps": [
            "Conduct a time study: break AHT into talk time, hold time, and wrap-up time",
            "Shadow 10+ calls per agent tier to observe CRM navigation patterns",
            "Identify the top 5 call types driving the longest handle times",
            "Run a 5 Whys session with agents on wrap-up time increase",
            "Design and pilot optimised CRM screen layout / navigation shortcuts",
            "Create standard work job aids for top 5 call types in new CRM",
            "Implement weekly AHT dashboard by agent and call type",
        ],
        "tags": ["call center", "AHT", "CRM", "migration", "wrap-up", "standard work", "NPS"],
    },

    # -----------------------------------------------------------------------
    # 4. Finance – delays / cycle time
    # -----------------------------------------------------------------------
    {
        "id": "invoice_cycle",
        "title": "Finance Invoice Processing Cycle Time Reduction",
        "domain": "Finance",
        "problem_type": "delays / cycle time",
        "complexity": "Beginner",
        "recommended_mode": "process_waste",
        "typical_tools": [
            "Value Stream Map",
            "8 Wastes Analysis",
            "Swimlane Process Map",
            "5 Whys",
            "Spaghetti Diagram",
            "SIPOC",
        ],
        "project_name": "Accounts Payable Invoice Cycle Time Reduction",
        "problem_statement": (
            "The accounts payable invoice processing cycle time averages 14 days from "
            "receipt to payment authorisation against a 5-day internal target and a "
            "10-day contractual SLA, resulting in $312,000 in early-payment discount "
            "losses and 47 supplier escalations in the past fiscal quarter."
        ),
        "current_symptoms": [
            "Invoice approval queue backlog regularly exceeds 200 documents",
            "Manual data entry from paper invoices taking 8–12 minutes per invoice",
            "Approvers spending 30+ minutes per week chasing missing PO numbers",
            "14% of invoices returned to suppliers for correction (wrong entity, missing GL code)",
            "Month-end close delayed by 2 days due to unprocessed invoice backlog",
        ],
        "current_metrics": {
            "Invoice Cycle Time (avg)": "14 days (target: 5 days)",
            "Early-Payment Discount Capture Rate": "31% (target: 85%)",
            "Invoice Exception Rate": "14% (target: < 3%)",
            "Invoices Processed per FTE per Day": "38 (benchmark: 72)",
            "Supplier Escalations (last quarter)": "47",
        },
        "constraints": [
            "ERP upgrade is 14 months away — no system automation available now",
            "Team of 6 AP clerks; no additional headcount approved",
            "Supplier portal adoption project is separate and out of scope",
            "Month-end close date is immovable",
        ],
        "stakeholder_concerns": [
            "CFO: discount capture loss is a direct P&L impact; supplier relationship risk",
            "AP Manager: team is overloaded and working overtime at month-end",
            "Procurement: supplier complaints about late payment affecting contract negotiations",
            "Audit: manual workarounds creating segregation-of-duty control gaps",
            "IT: any process change must be documented for SOX compliance review",
        ],
        "weak_input_example": (
            "Our invoices take too long to process and suppliers keep complaining. "
            "We need to speed up accounts payable."
        ),
        "strong_input_example": (
            "The accounts payable invoice processing cycle time averages 14 days from "
            "receipt to payment authorisation against a 5-day internal target and a "
            "10-day contractual SLA, resulting in $312,000 in early-payment discount "
            "losses and 47 supplier escalations in the past fiscal quarter."
        ),
        "common_mistakes": [
            "Mapping only the 'happy path' and missing the exception and rework loops",
            "Not calculating value-added vs. non-value-added time in the current process",
            "Focusing on headcount instead of waste elimination and error-proofing",
            "Ignoring the upstream root cause: poor PO discipline from requisitioners",
            "Not involving approvers in the process map — their wait time is often the biggest waste",
        ],
        "what_good_output_looks_like": (
            "A current-state VSM showing value-added time (<1 hour) versus total cycle time "
            "(14 days), an 8-Wastes analysis identifying the top 3 waste categories, a "
            "future-state VSM targeting 5-day cycle time, and a prioritised improvement "
            "backlog with quick wins (e.g., digital routing, PO matching rules) that can "
            "be implemented without ERP changes."
        ),
        "next_steps": [
            "Map the complete invoice lifecycle from receipt to payment with timestamps",
            "Measure and categorise time spent at each step (value-added vs. waiting)",
            "Stratify exception invoices by error type, supplier, and business unit",
            "Identify top 3 causes of rework and approver bottlenecks",
            "Implement electronic routing with auto-escalation for approvals over 48 hours",
            "Create an invoice submission checklist for top 20 suppliers",
            "Define and monitor a daily invoice cycle time control chart",
        ],
        "tags": ["AP", "invoice", "accounts payable", "VSM", "waste", "discount", "cycle time"],
    },

    # -----------------------------------------------------------------------
    # 5. Software – defects / errors
    # -----------------------------------------------------------------------
    {
        "id": "software_bug_escape",
        "title": "Software Release Defect Escape Rate Reduction",
        "domain": "Software",
        "problem_type": "defects / errors",
        "complexity": "Black Belt",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Defect Concentration Diagram",
            "Regression Analysis",
            "Hypothesis Test (chi-square)",
            "FMEA",
            "Control Charts (c-chart)",
            "Cause-and-Effect Matrix",
            "Measurement System Analysis",
        ],
        "project_name": "Post-Restructure QA Defect Escape Rate Reduction",
        "problem_statement": (
            "The production defect escape rate for software releases increased from 1.2% "
            "to 3.7% of stories per sprint over 5 months following the Q3 team restructure, "
            "causing 3 Severity-1 production incidents, a 19% increase in customer-reported "
            "bugs, and an estimated $640,000 in incident response and remediation costs."
        ),
        "current_symptoms": [
            "Regression test coverage dropped from 84% to 61% post-restructure",
            "3 Sev-1 production incidents in 5 months (vs. 0 in prior 12 months)",
            "Average time-to-detect for escaped defects now 4.2 days (was 0.8 days)",
            "QA engineers reporting unclear ownership of integration testing after restructure",
            "Code review turnaround time increased from 2 hours to 18 hours",
        ],
        "current_metrics": {
            "Defect Escape Rate": "3.7% of stories (baseline: 1.2%)",
            "Regression Test Coverage": "61% (baseline: 84%)",
            "Sev-1 Incidents (5 months)": "3 (prior 12-month period: 0)",
            "Mean Time to Detect (escaped)": "4.2 days (baseline: 0.8 days)",
            "Code Review Turnaround": "18 hours (baseline: 2 hours)",
        },
        "constraints": [
            "Cannot slow release cadence — biweekly sprint schedule is contractually committed",
            "Test automation framework is in mid-migration; stable tooling available Q2",
            "Team is distributed across 3 time zones — synchronous testing windows limited",
            "No additional QA headcount until next fiscal year",
        ],
        "stakeholder_concerns": [
            "CTO: Sev-1 incidents are a reputational and SLA risk with enterprise clients",
            "Engineering VP: restructure ROI is under scrutiny; defect rate adds pressure",
            "QA Lead: team roles and ownership of integration layer are ambiguous",
            "Product Management: sprint velocity is being impacted by rework cycles",
            "Customer Success: 3 enterprise clients have raised formal escalations",
        ],
        "weak_input_example": (
            "Since we reorganised the engineering team, bugs keep slipping into production. "
            "QA needs to do a better job of testing before releases."
        ),
        "strong_input_example": (
            "The production defect escape rate for software releases increased from 1.2% "
            "to 3.7% of stories per sprint over 5 months following the Q3 team restructure, "
            "causing 3 Severity-1 production incidents, a 19% increase in customer-reported "
            "bugs, and an estimated $640,000 in incident response and remediation costs."
        ),
        "common_mistakes": [
            "Attributing all defect escapes to 'insufficient testing' without stratifying by type, component, or team",
            "Not measuring the measurement system itself — defect classification inconsistency inflates escape rates",
            "Treating the restructure as the root cause rather than the trigger — dig into what changed specifically",
            "Focusing on test coverage percentage without validating test effectiveness",
            "Ignoring the code review bottleneck as a contributing factor to rushed merges",
        ],
        "what_good_output_looks_like": (
            "A DMAIC charter with a SMART goal (e.g., reduce escape rate to ≤1.5% within "
            "3 sprints), a defect stratification analysis by component/team/sprint showing "
            "the 80/20 concentration, a chi-square test confirming the association between "
            "restructure-related X factors and escape rate, an updated FMEA for the release "
            "pipeline with revised RPN scores, and a c-chart control plan for ongoing "
            "defect escape rate monitoring."
        ),
        "next_steps": [
            "Stratify escaped defects by sprint, component, team, and defect type for the past 5 months",
            "Map the end-to-end QA process and identify gaps introduced by the restructure",
            "Conduct an ownership RACI workshop for integration testing responsibilities",
            "Measure regression test suite effectiveness (mutation testing or fault injection)",
            "Run hypothesis test: are defect escape rates significantly higher for restructured teams?",
            "Design and pilot a 'shift-left' testing protocol for the top-risk components",
            "Implement c-chart for escape rate per sprint with control limits",
        ],
        "tags": ["QA", "release", "defect escape", "Sev-1", "restructure", "regression", "FMEA"],
    },

    # -----------------------------------------------------------------------
    # 6. HR / Internal – delays / cycle time
    # -----------------------------------------------------------------------
    {
        "id": "onboarding_time",
        "title": "Employee Onboarding Cycle Time Reduction",
        "domain": "HR / Internal",
        "problem_type": "delays / cycle time",
        "complexity": "Beginner",
        "recommended_mode": "process_waste",
        "typical_tools": [
            "Swimlane Process Map",
            "8 Wastes Analysis",
            "5 Whys",
            "SIPOC",
            "Voice of the Customer (survey)",
            "Standard Work",
        ],
        "project_name": "New Hire Onboarding Cycle Time Reduction",
        "problem_statement": (
            "Employee onboarding cycle time from offer acceptance to fully productive "
            "new hire averages 22 days against a 10-day benchmark and an 8-day internal "
            "target, causing an estimated $95,000 per quarter in delayed time-to-productivity "
            "and a 28-point drop in new hire satisfaction scores over the past 6 months."
        ),
        "current_symptoms": [
            "IT equipment provisioning averaging 9 days — new hires sitting idle in first week",
            "Background check vendor turnaround time varying from 3 to 14 days with no visibility",
            "Hiring manager onboarding tasks (buddy assignment, 30-day plan) completed late 62% of the time",
            "New hire paperwork still paper-based — DocuSign available but not yet adopted",
            "Access permissions for core systems requiring manual requests to 4 separate IT queues",
        ],
        "current_metrics": {
            "Onboarding Cycle Time (avg)": "22 days (target: 8 days; benchmark: 10 days)",
            "IT Equipment Ready on Day 1": "38% of new hires (target: 95%)",
            "New Hire Satisfaction (30-day survey)": "58/100 (baseline: 86/100)",
            "Hiring Manager Task Completion Rate": "38% on time (target: 90%)",
            "System Access Ready on Day 1": "21% of new hires",
        },
        "constraints": [
            "Background check vendor contract cannot be renegotiated until Q4",
            "HRIS system has no workflow automation capability — upgrade planned for next year",
            "HR team of 4 supports a 600-person organisation with 15+ hires per month",
            "Legal and compliance review required for any changes to offer letter or I-9 process",
        ],
        "stakeholder_concerns": [
            "CHRO: new hire experience is directly linked to 90-day retention rates",
            "Hiring Managers: delayed productivity impacts team OKRs and delivery timelines",
            "IT: provisioning queue is a shared resource across all departments",
            "Finance: delayed productivity has a measurable cost per unfilled productive day",
            "New Hires: first-impression effect — poor onboarding correlates with early attrition",
        ],
        "weak_input_example": (
            "Onboarding takes way too long and new employees aren't happy. "
            "HR needs to make the process faster."
        ),
        "strong_input_example": (
            "Employee onboarding cycle time from offer acceptance to fully productive "
            "new hire averages 22 days against a 10-day benchmark and an 8-day internal "
            "target, causing an estimated $95,000 per quarter in delayed time-to-productivity "
            "and a 28-point drop in new hire satisfaction scores over the past 6 months."
        ),
        "common_mistakes": [
            "Mapping only HR's steps and ignoring IT, Facilities, and Hiring Manager parallel workstreams",
            "Treating background check delay as uncontrollable — SLA management and vendor escalation paths exist",
            "Not differentiating onboarding cycle time by role, department, or location",
            "Confusing 'first day' readiness with 'fully productive' — define the endpoint clearly",
            "Automating a broken process — map and fix the process before applying technology",
        ],
        "what_good_output_looks_like": (
            "A swimlane process map showing all parallel workstreams (HR, IT, Hiring Manager, "
            "Facilities) with handoff delays highlighted, an 8-Wastes analysis identifying "
            "waiting and over-processing as the top waste categories, a standard work "
            "checklist triggering IT provisioning 10 days before start date, and a 90-day "
            "control plan with weekly cycle time tracking."
        ),
        "next_steps": [
            "Map the full onboarding process including all parallel workstreams with actual timestamps",
            "Measure wait time vs. work time at each step for the past 20 hires",
            "Identify top 3 causes of day-1 unreadiness (IT, access, paperwork)",
            "Implement pre-boarding trigger: send IT provisioning request at offer acceptance",
            "Pilot DocuSign for all offer and onboarding paperwork",
            "Create a hiring manager onboarding task checklist with automated reminders",
            "Track onboarding cycle time on a monthly run chart by department",
        ],
        "tags": ["HR", "onboarding", "new hire", "IT provisioning", "cycle time", "satisfaction"],
    },

    # -----------------------------------------------------------------------
    # 7. Customer Support – customer dissatisfaction
    # -----------------------------------------------------------------------
    {
        "id": "customer_complaints",
        "title": "Customer Complaint Volume Reduction and CSAT Recovery",
        "domain": "Customer Support",
        "problem_type": "customer dissatisfaction",
        "complexity": "Practitioner",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Pareto Chart",
            "Affinity Diagram",
            "Kano Model",
            "Regression Analysis",
            "Voice of the Customer (VoC)",
            "Control Chart (u-chart)",
            "Hypothesis Test",
        ],
        "project_name": "CSAT Recovery and Complaint Reduction Programme",
        "problem_statement": (
            "Customer complaint volume increased by 42% over 3 consecutive quarters "
            "(Q2–Q4), while CSAT scores declined from 4.2 to 3.6 out of 5.0, breaching "
            "the contractual threshold of 3.8 with two enterprise clients and creating "
            "an estimated $1.1M revenue-at-risk from contract penalty clauses."
        ),
        "current_symptoms": [
            "Billing error complaints represent 38% of all complaint volume — up from 11% prior year",
            "First-contact resolution (FCR) rate dropped from 74% to 58% over 3 quarters",
            "Average complaint resolution time now 8.3 days vs. 3-day SLA",
            "Social media negative sentiment index increased 67% in Q4",
            "Two enterprise clients issued formal performance cure notices citing CSAT breach",
        ],
        "current_metrics": {
            "CSAT Score": "3.6 / 5.0 (contractual threshold: 3.8; baseline: 4.2)",
            "Monthly Complaint Volume": "2,840 (baseline: 2,000; +42%)",
            "First-Contact Resolution Rate": "58% (baseline: 74%)",
            "Complaint Resolution Time": "8.3 days (SLA: 3 days)",
            "Billing Error Complaint Share": "38% of volume (baseline: 11%)",
        },
        "constraints": [
            "Billing system replacement is 18 months away — bug fixes only available now",
            "Customer-facing communication changes require Legal approval (5-day SLA)",
            "CX team headcount frozen for the remainder of the fiscal year",
            "Enterprise client contracts limit corrective action timeline to 90 days",
        ],
        "stakeholder_concerns": [
            "CEO: two enterprise cure notices are a board-level visibility item",
            "CX Director: team is reactive and has no capacity for root cause analysis",
            "Finance: $1.1M revenue-at-risk plus potential SLA penalty payments",
            "Sales: complaint volume is being used by competitors in renewal conversations",
            "Legal: cure notice response letters require accurate data commitments",
        ],
        "weak_input_example": (
            "Customers are not happy and we are getting more complaints. "
            "We should improve our customer service."
        ),
        "strong_input_example": (
            "Customer complaint volume increased by 42% over 3 consecutive quarters "
            "(Q2–Q4), while CSAT scores declined from 4.2 to 3.6 out of 5.0, breaching "
            "the contractual threshold of 3.8 with two enterprise clients and creating "
            "an estimated $1.1M revenue-at-risk from contract penalty clauses."
        ),
        "common_mistakes": [
            "Treating CSAT as a single number rather than disaggregating by interaction type and channel",
            "Focusing on complaint handling speed without addressing root causes of complaints",
            "Using complaint volume alone — complaints are a lagging indicator; look for leading signals",
            "Not weighting complaints by revenue impact — 38% billing errors likely affect highest-value accounts",
            "Committing to improvement targets in cure-notice responses without a defined roadmap",
        ],
        "what_good_output_looks_like": (
            "A stratified Pareto showing billing errors account for >60% of CSAT impact, "
            "a VoC affinity diagram summarising the top 5 customer pain themes, a regression "
            "model confirming that billing errors are the strongest predictor of CSAT decline, "
            "a 90-day corrective action plan addressing billing error root causes, and a "
            "u-chart control plan for monthly complaint volume with alert thresholds."
        ),
        "next_steps": [
            "Stratify complaint data by type, channel, product, and customer segment",
            "Conduct VoC interviews with 10–15 dissatisfied enterprise customers",
            "Map the billing error end-to-end process to identify upstream error injection points",
            "Run hypothesis test comparing CSAT for billing-complaint vs. non-billing customers",
            "Engage billing system team to identify and fix top 3 billing error root causes",
            "Implement a complaint early-warning dashboard with weekly trending",
            "Design and track CSAT improvement milestones for the cure-notice response plan",
        ],
        "tags": ["CSAT", "complaints", "billing", "FCR", "enterprise", "VoC", "Pareto"],
    },

    # -----------------------------------------------------------------------
    # 8. Manufacturing – variation / instability
    # -----------------------------------------------------------------------
    {
        "id": "warranty_returns",
        "title": "Field Warranty Return Rate Reduction – Product Line X",
        "domain": "Manufacturing",
        "problem_type": "variation / instability",
        "complexity": "Black Belt",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "FMEA (Design and Process)",
            "Regression Analysis",
            "DOE (Design of Experiments)",
            "Capability Analysis (Cpk)",
            "Control Charts (Xbar-R)",
            "Fault Tree Analysis",
            "Warranty Data Mining",
        ],
        "project_name": "Product Line X Warranty Return Rate Reduction",
        "problem_statement": (
            "The field warranty return rate for Product Line X doubled from 1.4% to 2.9% "
            "in Q3, driven by a specific motor overheating failure mode, resulting in "
            "$1.8M in warranty claim costs, 2,400 affected units in field, and a formal "
            "customer quality review with the top 3 OEM accounts."
        ),
        "current_symptoms": [
            "Motor overheating failure mode accounts for 71% of Q3 warranty claims",
            "Field failure analysis showing thermal paste application inconsistency in returned units",
            "Warranty claims concentrated in units from production weeks 28–34",
            "Process capability (Cpk) for thermal paste weight at 0.61 — well below 1.33 target",
            "Three OEM customers have placed Product Line X on 'conditional approval' status",
        ],
        "current_metrics": {
            "Warranty Return Rate": "2.9% (Q3; baseline: 1.4%)",
            "Warranty Claim Cost (Q3)": "$1.8M",
            "Motor Overheating Failure Share": "71% of Q3 claims",
            "Thermal Paste Cpk": "0.61 (target: ≥ 1.33)",
            "Affected Units in Field": "~2,400 units (weeks 28–34)",
        },
        "constraints": [
            "Product design changes require OEM customer re-qualification (6–9 month cycle)",
            "Production weeks 28–34 coincided with new thermal paste supplier introduction",
            "Field replacement parts are limited — 400 units in service stock",
            "Recall decision requires VP-level approval and regulatory notification in some markets",
        ],
        "stakeholder_concerns": [
            "VP Quality: OEM conditional approval status is a revenue risk of $12M annually",
            "Engineering: design FMEA for thermal management was rated low risk — needs revision",
            "Service / Field: replacement logistics and technician scheduling for 2,400 units",
            "Procurement: new thermal paste supplier performance and qualification status",
            "Legal / Regulatory: potential notification obligations in EU and North America markets",
        ],
        "weak_input_example": (
            "We have too many products being returned under warranty. "
            "The quality of Product Line X needs to improve."
        ),
        "strong_input_example": (
            "The field warranty return rate for Product Line X doubled from 1.4% to 2.9% "
            "in Q3, driven by a specific motor overheating failure mode, resulting in "
            "$1.8M in warranty claim costs, 2,400 affected units in field, and a formal "
            "customer quality review with the top 3 OEM accounts."
        ),
        "common_mistakes": [
            "Treating all warranty returns as one defect type — stratify by failure mode first",
            "Not correlating warranty data with production lot data to find the signal in time/batch",
            "Running DOE on the process without first confirming the measurement system is capable",
            "Assuming the new supplier is the root cause before conducting a side-by-side capability study",
            "Delaying containment action on field units while root cause investigation continues",
        ],
        "what_good_output_looks_like": (
            "A fault tree analysis confirming thermal paste application as the critical failure "
            "path, a DOE identifying the optimal paste weight and application method with "
            "confirmed Cpk ≥ 1.33, a revised process FMEA with updated RPN scores, a "
            "containment/field action plan for the 2,400 affected units, and a control plan "
            "with Xbar-R charts on thermal paste weight per shift."
        ),
        "next_steps": [
            "Isolate all returned units from weeks 28–34 for detailed teardown and failure analysis",
            "Conduct capability study comparing old vs. new thermal paste supplier application process",
            "Run DOE on thermal paste weight, application method, and cure time",
            "Update process FMEA with new failure mode data and revised detection controls",
            "Implement containment: enhanced 100% thermal test on all current production units",
            "Develop field action plan for 2,400 units with prioritisation by customer risk level",
            "Establish Xbar-R control chart on thermal paste weight with operator certification",
        ],
        "tags": ["warranty", "thermal", "DOE", "Cpk", "FMEA", "OEM", "supplier", "motor"],
    },

    # -----------------------------------------------------------------------
    # 9. Supply Chain – waste / inefficiency
    # -----------------------------------------------------------------------
    {
        "id": "procurement_delay",
        "title": "Procurement Order Lead Time Reduction",
        "domain": "Supply Chain",
        "problem_type": "waste / inefficiency",
        "complexity": "Practitioner",
        "recommended_mode": "process_waste",
        "typical_tools": [
            "Value Stream Map",
            "8 Wastes Analysis",
            "Swimlane Process Map",
            "Pareto Chart",
            "5 Whys",
            "Kanban / Pull System Design",
        ],
        "project_name": "Strategic Procurement Order Lead Time Reduction",
        "problem_statement": (
            "Procurement order lead time for indirect materials averages 18 days from "
            "requisition approval to goods receipt against a 7-day internal standard, "
            "causing production schedule disruptions on 34% of planned orders and "
            "an estimated $220,000 quarterly cost in expedite fees and emergency sourcing."
        ),
        "current_symptoms": [
            "34% of purchase orders arriving after the production schedule need date",
            "Procurement team spending 40% of time on expediting rather than strategic sourcing",
            "Supplier quote collection averaging 6 days for standard catalogue items",
            "Approval workflow requiring 3 sequential approvers with average 24-hour turnaround each",
            "Goods receipt process at the dock taking 3.5 hours per delivery due to manual inspection logs",
        ],
        "current_metrics": {
            "Procurement Lead Time (avg)": "18 days (standard: 7 days)",
            "On-Time PO Fulfilment Rate": "66% (target: 95%)",
            "Expedite Fee Cost (quarterly)": "$220,000",
            "Time Spent Expediting (% of team capacity)": "40%",
            "Quote Collection Time (standard items)": "6 days (target: 1 day)",
        },
        "constraints": [
            "ERP procurement module cannot be reconfigured without IT change management approval",
            "Supplier renegotiation is limited to a 6-month window starting Q3",
            "Approval authority matrix is governed by Finance policy — changes require CFO sign-off",
            "Procurement team of 8 has no capacity for parallel workstreams",
        ],
        "stakeholder_concerns": [
            "COO: production disruptions are the top operational constraint this quarter",
            "Procurement Director: team is reactive; no bandwidth for supplier development",
            "Finance: expedite fees are unbudgeted and growing quarter-on-quarter",
            "Production Planning: 34% late POs make scheduling unreliable",
            "Suppliers: receiving unclear specifications in RFQs, causing revision cycles",
        ],
        "weak_input_example": (
            "Procurement is too slow and we keep running out of materials. "
            "We need to order things faster."
        ),
        "strong_input_example": (
            "Procurement order lead time for indirect materials averages 18 days from "
            "requisition approval to goods receipt against a 7-day internal standard, "
            "causing production schedule disruptions on 34% of planned orders and "
            "an estimated $220,000 quarterly cost in expedite fees and emergency sourcing."
        ),
        "common_mistakes": [
            "Mapping only the procurement team's steps and ignoring requisitioner and approver wait time",
            "Treating all categories of spend the same — lead time drivers differ for catalogue vs. custom items",
            "Focusing on supplier delivery speed without analysing internal processing waste",
            "Not quantifying the value-added vs. non-value-added time split (typically >90% is waiting)",
            "Implementing a quick fix (e.g., more expediting) that treats symptoms, not root causes",
        ],
        "what_good_output_looks_like": (
            "A current-state VSM showing the 18-day lead time broken into component steps, "
            "with value-added time likely under 4 hours, an 8-Wastes analysis identifying "
            "waiting and motion as primary waste, a future-state VSM targeting 7-day lead "
            "time, and a quick-win list including pre-approved supplier catalogues, parallel "
            "approval routing, and automated goods receipt for certified suppliers."
        ),
        "next_steps": [
            "Map the end-to-end procurement process with timestamps from last 50 POs",
            "Stratify lead time by category, supplier, and approval tier",
            "Quantify value-added vs. non-value-added time at each process step",
            "Identify top 3 waste categories and root causes with 5 Whys",
            "Pilot a pre-approved supplier catalogue for top 20 catalogue SKUs",
            "Redesign approval workflow to allow parallel routing for orders under threshold",
            "Implement lead time run chart tracked weekly by procurement category",
        ],
        "tags": ["procurement", "lead time", "indirect", "VSM", "expedite", "approval", "kanban"],
    },

    # -----------------------------------------------------------------------
    # 10. Supply Chain – variation / instability
    # -----------------------------------------------------------------------
    {
        "id": "forecast_accuracy",
        "title": "Demand Forecast Accuracy Improvement",
        "domain": "Supply Chain",
        "problem_type": "variation / instability",
        "complexity": "Black Belt",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Regression Analysis",
            "Time Series Analysis",
            "Hypothesis Test",
            "Multi-vari Study",
            "Measurement System Analysis",
            "Control Charts (CUSUM)",
            "Capability Analysis",
        ],
        "project_name": "Demand Forecast Accuracy Improvement – Consumer Products Division",
        "problem_statement": (
            "Demand forecast accuracy in the Consumer Products Division declined from 88% "
            "to 67% MAPE over 8 months (January–August), causing $3.4M in excess inventory "
            "write-downs and $780,000 in lost sales from stockouts across 14 SKUs."
        ),
        "current_symptoms": [
            "Forecast bias is consistently negative (under-forecast) on seasonal SKUs — on average -18%",
            "14 SKUs experienced stockout events in Q2, with an average 9-day out-of-stock duration",
            "Excess inventory on 22 SKUs exceeds 90-day forward cover — $3.4M write-down risk",
            "Sales team overrides to forecast model account for 43% of all submitted forecasts",
            "Forecasting process uses a single Excel-based model with no statistical baseline",
        ],
        "current_metrics": {
            "Forecast Accuracy (MAPE)": "67% accuracy (baseline: 88%)",
            "Forecast Bias": "-18% (systematic under-forecast on seasonal SKUs)",
            "SKUs with Stockout Events (Q2)": "14 of 220 active SKUs",
            "Excess Inventory Value": "$3.4M (>90-day forward cover)",
            "Sales Override Rate": "43% of all submitted forecasts",
        },
        "constraints": [
            "Advanced planning system (APS) implementation is 12 months away",
            "Historical sales data has gaps due to a system migration in year 2",
            "Demand planning team of 3 covers 220 active SKUs across 4 categories",
            "S&OP process reform is a parallel workstream — cannot change meeting cadence now",
        ],
        "stakeholder_concerns": [
            "Supply Chain VP: inventory write-downs are eroding gross margin targets",
            "Sales: stockouts on key SKUs are being used to justify missing revenue targets",
            "Finance: $3.4M write-down is a material variance — auditor attention expected",
            "Demand Planning: team capacity is overwhelmed; model confidence is low",
            "Category Management: promotional forecast accuracy is the biggest driver of variance",
        ],
        "weak_input_example": (
            "Our demand forecasts are often wrong and we either have too much or too little stock. "
            "We need a better forecasting process."
        ),
        "strong_input_example": (
            "Demand forecast accuracy in the Consumer Products Division declined from 88% "
            "to 67% MAPE over 8 months (January–August), causing $3.4M in excess inventory "
            "write-downs and $780,000 in lost sales from stockouts across 14 SKUs."
        ),
        "common_mistakes": [
            "Using MAPE as the only accuracy metric — also track bias, which reveals systematic error",
            "Treating all SKUs as one population — segment by ABC/XYZ classification first",
            "Not separating baseline demand forecast error from promotional uplift error",
            "Assuming better software will fix a process and data quality problem",
            "Not measuring the measurement system: is the actual sales data clean and complete?",
        ],
        "what_good_output_looks_like": (
            "A multi-vari study decomposing forecast error by SKU category, time horizon, "
            "and planner, a regression model identifying promotional events and seasonality "
            "coefficients as the top drivers of error, a CUSUM chart detecting systematic "
            "forecast bias, and a redesigned forecasting process incorporating statistical "
            "baselines, promotional adjustment protocols, and a weekly bias review."
        ),
        "next_steps": [
            "Stratify forecast error by SKU, category, planner, and time horizon",
            "Conduct MSA on the demand data quality (gaps, returns, promotions stripping)",
            "Build a multi-vari chart to decompose variance components",
            "Run regression of forecast error against key drivers: promotions, seasonality, lead time",
            "Pilot statistical baseline models (exponential smoothing) for top 50 SKUs",
            "Design a structured promotional forecast protocol with sales input governance",
            "Implement weekly MAPE and bias control charts by category",
        ],
        "tags": ["forecast", "MAPE", "bias", "inventory", "stockout", "S&OP", "demand planning"],
    },

    # -----------------------------------------------------------------------
    # 11. Service – defects / errors
    # -----------------------------------------------------------------------
    {
        "id": "rework_rate",
        "title": "Claims Processing Rework Rate Reduction",
        "domain": "Service",
        "problem_type": "defects / errors",
        "complexity": "Practitioner",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Pareto Chart",
            "Fishbone / Ishikawa",
            "Error Proofing (Poka-yoke)",
            "Hypothesis Test (2-proportion)",
            "Control Chart (p-chart)",
            "Standard Work",
            "MSA (Attribute Agreement Analysis)",
        ],
        "project_name": "Insurance Claims Processing Rework Rate Reduction",
        "problem_statement": (
            "The rework rate in the insurance claims processing centre is 23% of all "
            "submitted claims against an 8% industry benchmark and a 10% internal target, "
            "resulting in $1.2M annual rework labour cost, an average 6-day increase in "
            "claims settlement time, and a 31% increase in customer complaints related "
            "to claims delays over the past 12 months."
        ),
        "current_symptoms": [
            "Missing supporting documentation is cited in 41% of rework cases",
            "Adjudicator interpretive inconsistency: same claim coded differently by different staff in 29% of sampled cases",
            "Rework rate varies from 12% to 36% across the 4 processing teams — wide variation in performance",
            "Rework loop averaging 6.2 additional days added to settlement time",
            "Customer inquiry volume about claim status up 31% — driven by rework delays",
        ],
        "current_metrics": {
            "Rework Rate": "23% (target: 10%; benchmark: 8%)",
            "Rework Labour Cost (annual)": "$1.2M",
            "Rework Cycle Time Penalty": "+6.2 days per reworked claim",
            "Rework Rate Range (by team)": "12%–36% across 4 teams",
            "Missing Documentation Rate": "41% of rework cases",
        },
        "constraints": [
            "Claims system is legacy — field-level validation rules cannot be added without IT project approval",
            "Regulatory requirement mandates acknowledgement of all claims within 5 business days",
            "Adjudicator caseloads are at capacity — no bandwidth for extended training programmes",
            "Union agreement governs performance management approach for adjudicators",
        ],
        "stakeholder_concerns": [
            "Operations Director: rework is consuming 23% of team capacity — a major throughput drag",
            "Compliance: rework-related delays are approaching regulatory settlement time limits",
            "Finance: $1.2M annual rework cost is the largest controllable cost in the centre",
            "HR: performance variation across teams raises fairness concerns for adjudicators",
            "Customers: 31% complaint increase is feeding into regulator complaints data",
        ],
        "weak_input_example": (
            "Too many claims need to be redone. Staff need better training to "
            "get it right the first time."
        ),
        "strong_input_example": (
            "The rework rate in the insurance claims processing centre is 23% of all "
            "submitted claims against an 8% industry benchmark and a 10% internal target, "
            "resulting in $1.2M annual rework labour cost, an average 6-day increase in "
            "claims settlement time, and a 31% increase in customer complaints related "
            "to claims delays over the past 12 months."
        ),
        "common_mistakes": [
            "Attributing rework to 'human error' without stratifying by error type and root cause",
            "Not conducting an attribute agreement analysis — adjudicator inconsistency may be the real problem",
            "Measuring rework rate at the end of the process rather than at point of creation",
            "Assuming training will fix process design problems like missing documentation gates",
            "Treating the 12% team as the benchmark without understanding what they do differently",
        ],
        "what_good_output_looks_like": (
            "A Pareto of rework causes showing missing documentation and coding inconsistency "
            "account for >70% of rework, an attribute agreement analysis (Kappa ≥ 0.70 target) "
            "quantifying adjudicator inconsistency, a 2-proportion test confirming team-level "
            "rework rate differences are statistically significant, standard work guidelines "
            "for the top 5 claim types, and a p-chart control plan with monthly rework "
            "rate tracking by team."
        ),
        "next_steps": [
            "Stratify rework by error type, team, claim type, and adjudicator for 6-month period",
            "Conduct attribute agreement analysis across all adjudicators on 30 sample claims",
            "Benchmark the 12%-rework team: observe their process and document differences",
            "Implement a documentation completeness checklist at point of claim intake",
            "Design adjudication decision tree for top 5 complex claim types",
            "Pilot error-proofed intake form with mandatory fields for missing documentation types",
            "Track rework rate weekly by team on p-chart",
        ],
        "tags": ["claims", "rework", "insurance", "adjudicator", "documentation", "p-chart", "Poka-yoke"],
    },

    # -----------------------------------------------------------------------
    # 12. Manufacturing – waste / inefficiency
    # -----------------------------------------------------------------------
    {
        "id": "yield_loss",
        "title": "First-Pass Yield Improvement – Production Line 3",
        "domain": "Manufacturing",
        "problem_type": "waste / inefficiency",
        "complexity": "Black Belt",
        "recommended_mode": "dmaic",
        "typical_tools": [
            "Rolled Throughput Yield (RTY) Analysis",
            "Capability Analysis (Ppk/Cpk)",
            "DOE (Design of Experiments)",
            "FMEA",
            "Control Charts (Xbar-S)",
            "Hypothesis Test (ANOVA)",
            "Regression Analysis",
        ],
        "project_name": "Line 3 First-Pass Yield Improvement",
        "problem_statement": (
            "First-pass yield (FPY) on Production Line 3 declined from 92% to 71% over "
            "6 months (Q1–Q2), causing $890,000 in scrap costs, 340 hours of unplanned "
            "overtime for rework, and the line running at only 77% of its scheduled "
            "output capacity."
        ),
        "current_symptoms": [
            "Rolled throughput yield analysis identifies station 6 (solder reflow) as contributing 58% of yield loss",
            "Solder joint defect rate at station 6 varying from 4% to 19% across shifts — wide variation",
            "Oven temperature profile at station 6 showing Cpk of 0.48 — highly incapable",
            "Scrap cost tracking showing $148,000 in the most recent month alone",
            "Overtime authorisations for rework crew averaging 57 hours per week",
        ],
        "current_metrics": {
            "First-Pass Yield (Line 3)": "71% (target: 92%)",
            "Scrap Cost (monthly)": "$148,000",
            "Overtime Hours (rework, weekly avg)": "57 hours",
            "Station 6 Solder Defect Rate": "4%–19% (shift variation)",
            "Solder Reflow Oven Temp Cpk": "0.48 (target: ≥ 1.33)",
        },
        "constraints": [
            "Line 3 cannot be offline for more than 8 hours per week for trials",
            "Replacement oven equipment would require $220,000 capex — needs VP approval",
            "Current production schedule requires Line 3 to hit 85% capacity within 60 days",
            "Process engineers are shared with Lines 1 and 2 — limited dedicated availability",
        ],
        "stakeholder_concerns": [
            "Plant Director: scrap and overtime costs are the top two items on the plant P&L review",
            "Process Engineering: oven temperature variation has been flagged before but not resolved",
            "Maintenance: oven is due for a major PM — requesting approval to advance the schedule",
            "Production Supervisor: rework crew morale is low after 6 months of systematic overtime",
            "Finance: annualised scrap run rate of $1.78M requires controller-level reporting",
        ],
        "weak_input_example": (
            "Line 3 has bad yields and we're scrapping too many parts. "
            "We need to fix the solder process and reduce waste."
        ),
        "strong_input_example": (
            "First-pass yield on Production Line 3 declined from 92% to 71% over "
            "6 months (Q1–Q2), causing $890,000 in scrap costs, 340 hours of unplanned "
            "overtime for rework, and the line running at only 77% of its scheduled "
            "output capacity."
        ),
        "common_mistakes": [
            "Jumping to the oven as root cause without first confirming it with RTY decomposition",
            "Not running an MSA on the solder inspection process — false reject rate inflates apparent FPY loss",
            "Running a DOE on the oven without first stabilising the process (eliminate assignable causes first)",
            "Treating all shifts as equivalent — the 4%–19% variation range screams a shift-level X variable",
            "Requesting capex for a new oven before exhausting process optimisation options",
        ],
        "what_good_output_looks_like": (
            "A full RTY waterfall confirming station 6 as the dominant contributor, an MSA "
            "verifying the solder inspection system is adequate (Gauge R&R < 10%), a "
            "multi-vari chart confirming shift as a significant factor, a DOE identifying "
            "the optimal oven temperature profile (peak temp, dwell time, ramp rate) with "
            "Cpk ≥ 1.33 confirmed, an ANOVA showing shift differences explained by profile "
            "deviation, and an Xbar-S control plan for oven temperature monitoring per batch."
        ),
        "next_steps": [
            "Conduct RTY analysis across all Line 3 stations to confirm yield loss distribution",
            "Run MSA (Gauge R&R) on the solder joint inspection process",
            "Perform multi-vari study on solder defect rate across shift, operator, and oven zone",
            "Advance preventive maintenance on the solder reflow oven (heating element check, calibration)",
            "Run a full-factorial DOE on reflow profile parameters during planned downtime window",
            "Establish Xbar-S control charts on peak temperature and dwell time per batch",
            "Train all shift technicians on the optimised reflow profile and reaction plan",
        ],
        "tags": ["FPY", "yield", "solder", "reflow", "DOE", "Cpk", "RTY", "station 6", "scrap"],
    },
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_project_by_id(project_id: str) -> dict | None:
    """Return the project dict matching the given id, or None."""
    for project in PROJECT_LIBRARY:
        if project["id"] == project_id:
            return project
    return None


def get_projects_by_domain(domain: str) -> list[dict]:
    """Return all projects matching the given domain."""
    return [p for p in PROJECT_LIBRARY if p["domain"] == domain]


def get_projects_by_complexity(complexity: str) -> list[dict]:
    """Return all projects matching the given complexity level."""
    return [p for p in PROJECT_LIBRARY if p["complexity"] == complexity]


def get_all_domains() -> list[str]:
    """Return sorted list of unique domain values."""
    return sorted({p["domain"] for p in PROJECT_LIBRARY})


def get_all_problem_types() -> list[str]:
    """Return sorted list of unique problem_type values."""
    return sorted({p["problem_type"] for p in PROJECT_LIBRARY})
