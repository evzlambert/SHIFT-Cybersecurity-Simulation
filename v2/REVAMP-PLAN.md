# SHIFT Cybersecurity Simulation — v2 Revamp Plan

**Status:** Plan finalized — ready to build
**Originals preserved in:** `Teaching/SHIFT-Cybersecurity-Simulation/`
**WHO feedback source:** `Administration (Work)/SHIFT Program/WHO-Academy-Feedback-2026.md` — Module 03
**Student feedback:** Movement too limited; urgency not felt; no visible consequence for decisions

---

## Planning Decisions — Locked

| Question | Decision |
|----------|----------|
| Cohort size | 10–20 students = 2–4 teams of 5. Phase 3 ICC briefing: 2–4 Incident Commanders simultaneously. Phase 5 cross-team: 2 working groups of 5–10. |
| Facilitator coverage | Primary facilitator on main floor throughout. Co-facilitator dedicated to ICC floor — delivers Phase 3 Regional Authority briefing, manages intelligence card handoffs, monitors ICC dashboard. |
| HIE app approach | HIE threat view built INTO the ICC dashboard (new `icc_dashboard.py`), not a modification of the existing interoperability lab app. The interoperability lab app is a live teaching tool — don't touch it. ICC HIE view references the same data architecture students know (same table/field names) without connecting to the live app. |
| Audio production | Same approach as v1 — targeted inject audio only (HIE alert, PA system announcement, breaking news clip). No ambient narration. |
| Pre-reading | Role cards distributed the day before. Phase 0 trims to 10 min (saves 5 min absorbed into Phase 3). |

---

## Build Sequence

Build in this order. Each item unblocks the next.

| Order | File | Type | Depends On |
|-------|------|------|------------|
| 1 | `Intelligence-Cards.md` | Print-ready content | Plan only — no code |
| 2 | `icc_dashboard.py` | New Streamlit app | Intelligence Cards (to know what metrics to show) |
| 3 | `Instructor-Facilitation-Guide-v2.md` | Facilitation doc | ICC dashboard spec; intelligence cards |
| 4 | `student_app_v2.py` | Revised Streamlit app | Facilitation guide (to confirm phase content) |
| 5 | `instructor_app_v3.py` | Revised Streamlit app | Student app v2 (shares DB schema) |
| 6 | `Assignment-Cybersecurity-Simulation-v2.md` | Assignment doc | Student app v2 (artifacts drive rubric) |
| 7 | `Narration-Transcripts-v2.md` | Audio scripts | Facilitation guide (inject timing) |
| 8 | `Debrief-Guide-v2.md` | Debrief doc | Assignment v2 (new artifacts need debrief questions) |
| 9 | `build_worksheet_v2.py` | Build script | All content finalized |

---

## Design Philosophy

The v1 simulation is structurally sound — the scenario, regulatory context, and role structure are strong — but it operates as a sequential, homogeneous experience: all teams doing the same thing at the same time in the same place. This creates passive engagement and no felt consequence.

The v2 redesign is built on one central premise: **a real hospital cyberattack distributes decision authority across floors, roles, and organizations simultaneously.** The redesign leverages the WHO Academy's two-floor physical layout as an integral structural element, introduces a consequence architecture that makes prior decisions visibly affect later conditions, and weaves in the SHIFT Literacy and SHIFT Interoperability modules as organic components rather than add-ons.

---

## What Is Being Removed

These elements are cut — either because they duplicate a better experience elsewhere in the simulation, or because they contribute to the laptop-stillness problem.

| Removed | From | Why | Where the Content Goes |
|---------|------|-----|----------------------|
| Digital Paper Records Simulator tab | Phase 2 | Duplicates the physical artifact stations; keeps students on laptops | Physical action stations remain; lesson is preserved |
| Communications Center tab | Phase 2 | Replaced by the literacy inject, which is more rigorous and requires movement | New literacy inject (Phase 2) |
| 3 of 7 Manual Workflow decision areas | Phase 2 | 7 decisions is too many; lower-stakes areas (dietary, housekeeping) generate little analytical tension | Referenced in briefing text; 4 high-stakes areas remain |
| Surgery vs. HIM conflict inject | Phase 4 | Duplicates governance tension handled better in Phase 3 Regional Briefing and Phase 5 cross-team deliberation | Folded into Phase 3 Regional Briefing as background tension |
| Back-Entry Triage tab | Phase 6 | Becomes a section of the new Business Continuity Plan artifact | BCP artifact (Phase 6) |
| Trust Recovery tab | Phase 6 | Covered more effectively in debrief Block 7-8; thin as a standalone tab | One question in after-action summary; debrief Block 7 |
| Break-screen reflection prompts | Break | Phase 3 Regional Briefing (new) serves this function with far more urgency | Phase 3 |
| Ambient continuous audio narration | Throughout | Student feedback: "noise and distraction"; reduces urgency rather than creating it | Replaced by sharp, targeted audio injections at specific moments only |

**Net effect:** Phase 2 loses three tabs and becomes more focused. Phase 6 loses two tabs and consolidates into one stronger deliverable. Phase 4 loses one inject and gets a better one. The simulation is denser and more physical, not longer.

---

## Revised Simulation Structure

| Phase | Clock | Duration | Sim Time | Core Activity | Key Changes from v1 |
|-------|-------|----------|----------|---------------|---------------------|
| **0: Orientation** | 0:00 | 15 min | Pre-breach | Scenario, roles, inter-module briefing | Add: explicit literacy + interoperability connections; ICC concept introduced |
| **1: The Breach** | 0:15 | 25 min | Hour 0–2 | Attack timeline, first decisions | Add: post-decision ICC dispatch; consequence dashboard initializes |
| **2: Downtime Operations** | 0:40 | 40 min | Hour 2–24 | 4 manual workflows, paper stations, HIE inject, literacy inject | Remove: 3 workflow areas, Paper Records Simulator, Comms Center tab; Add: HIE Spread inject, literacy communication inject |
| **3: Regional Briefing** *(NEW)* | 1:20 | 15 min | Hour 24 | Cross-team ICC coordination | Entirely new phase; one rep per team at ICC |
| **BREAK** | 1:35 | 20 min | — | Review Phase 3 intelligence | Moved 15 min later; no app reflection prompts |
| **4: Escalation** | 1:55 | 30 min | Hour 24–48 | Media, families, staff morale, social media | Add: ICC movement for media crisis; literacy-required patient notification; GDHP framing; Remove: surgery/HIM inject |
| **5: Critical Decisions** | 2:25 | 30 min | Hour 48–72 | Ransom, GDPR, restoration | Change: cross-team deliberation format; BCP artifact begins |
| **6: Recovery** | 2:55 | 20 min | Hour 72+ | BCP, GDHP maturity assessment, after-action | Replace: generic radar → GDHP maturity framework; Back-entry + trust folded into BCP |
| **END** | 3:15 | — | — | Export; transition to debrief | +15 min from v1 due to Phase 3 |

*Total: ~3:15 active. If time is tight, Phase 3 can be trimmed to 10 min by cutting the rep-to-rep exchange time at ICC.*

---

## Phase-by-Phase Specification

---

### Phase 0: Orientation (15 min) — Minor Changes

**What changes:**
- Add 3-minute inter-module framing at the top: *"Before we begin, three things connect this simulation to work you've already done. The HIE you built and queried in the interoperability lab appears in this simulation — on the other side of a breach. The health literacy principles from the literacy module appear in your communication obligations under a time-pressured crisis. And the WHO governance frameworks you've been introduced to provide the global standards against which this hospital's preparedness will be measured. These aren't coincidences. They're the point."*
- Introduce the ICC concept: briefly explain the second floor, when students will be dispatched there, and what they'll find
- Role cards should be distributed and read before class if possible; orientation should spend more time on the scenario and less on administrative setup

**What stays:**
- Role assignment structure and team composition
- Ground rules
- Scenario and hospital profile walk-through

---

### Phase 1: The Breach (25 min) — ICC Dispatch Added

**What changes:**
- After the first decision set is complete (approximately 15 min in), **IT Security Lead and HIM Director are dispatched to the ICC.** Instructor announces: *"Your ANSSI alert has triggered an automatic escalation protocol. IT Security and the HIM Director: you are being called to the Incident Command Center. Go now."*
- At ICC, they receive two things:
  1. A physical **ANSSI Advisory Card** (printed) with threat intelligence not yet available to the team — initial scope assessment, attack vector, known affected system list
  2. They see the **ICC Consequence Dashboard** initialized — currently showing mostly green/neutral because decisions just started, but the GDPR clock is already ticking
- They return and brief their team (5 min remaining in Phase 1)
- The information asymmetry is real: they know the scope of the attack; their teammates don't yet

**What stays:**
- Attack timeline delivery (optional read-aloud for dramatic effect)
- All four Phase 1 decisions
- Role-specific first action discussion

**Consequence tracking starts here:**
- Decision 1 (Network Isolation speed) → sets initial **Data Exposure Estimate** on ICC dashboard
- Decision 3 (Staff Communication method) → sets initial **Staff Availability Index**

---

### Phase 2: Downtime Operations (40 min) — Most Changed Phase

**What changes:**

**Manual Workflows tab: 7 areas → 4 areas**
Keep: Medication Administration, Patient Identification, Surgery Decision, IT System Isolation
Remove as decision items: Dietary Services, Housekeeping, Outpatient Scheduling
*(These three appear as background text in the scenario briefing — they're mentioned as challenges without requiring a formal decision)*

**Remove: Paper Records Simulator tab**
Physical artifact stations replace this entirely. Students write actual paper records at stations — they don't simulate writing on a laptop.

**Remove: Communications Center tab**
Replaced by the literacy inject below.

**Add: HIE Spread Inject (approximately 20 min in)**
Audio inject — a brief, sharp audio clip: *"IT Security, urgent message from the HIE Coordinator at the regional exchange. Anomalous data packets detected at two partner hospitals. Possible lateral spread via the exchange network. Requesting guidance immediately."*

**IT Security Lead is dispatched to ICC.** At ICC:
- A separate screen shows a modified view of the HIE threat status — partner hospital connection statuses (red/yellow/green), data packet anomaly log, ANSSI advisory on HIE disconnection
- IT Security Lead receives a physical **HIE Advisory Card** with: what patient data categories flow through this HIE, what happens clinically if the exchange is disconnected, GDPR obligations for notifying HIE partner organizations
- They return and the team must make the HIE disconnection decision together

*This inject requires students to apply interoperability knowledge directly: the same HIE architecture they worked with in the lab is now the attack surface. The question of whether to disconnect invokes every dependency they mapped.*

**Add: Literacy Communication Inject (approximately 30 min in)**
Inject text appears on student app: *"The Communications Officer has been tasked with drafting the first patient-facing advisory. CNIL guidance has flagged that this hospital's catchment area includes 40,000 patients with low health literacy and 22,000 primary speakers of Arabic, Turkish, or Dari. The advisory must meet WHO plain language standards — 6th to 8th grade reading level, clear structure, no medical jargon."*

**Communications Officer physically moves to another team's table** for a 5-minute peer literacy review. They bring their draft. The other team reviews using the plain-language checklist from the literacy module. They return with feedback.

*This is the first cross-team physical interaction. It's purposeful — not just movement for movement's sake — because literacy peer review is the actual activity from the literacy module.*

**What stays:**
- Paper artifact action stations (all of them — this is the richest hands-on element)
- Inject events: medication near-miss, ambulance diversion, shift handoff, paper records crisis (these remain; they're well-designed)

---

### Phase 3: Regional Briefing — NEW PHASE (15 min)

This is the most structurally new element and the one that most directly addresses both the movement problem and the urgency problem.

**Trigger:** At the end of Phase 2, instructor announces: *"The Regional Health Authority has arrived at Sainte-Claire. The Director of Regional Digital Health has called a joint briefing at the Incident Command Center. One representative from each team must go to the ICC immediately. That person is: your Incident Commander."*

**At the ICC (all Incident Commanders, 8–10 min):**

All Incident Commanders from all teams are in the same room together. This is the one moment of cross-team interaction before Phase 5. With a cohort of 10–20 this means 2–4 ICs at ICC simultaneously — an intimate, high-stakes group.

The **co-facilitator** (on ICC floor throughout) delivers a 3-minute live briefing in character as the Regional Health Authority Director:
- The breach has spread to the HIE — three partner hospitals are now monitoring anomalies
- The GDPR 72-hour clock is at Hour 20 — 52 hours remain
- ANSSI has issued an advisory recommending against ransom payment
- A member of the national press has contacted the Regional Authority
- Each Incident Commander receives a **Regional Briefing Card** (physical) with these facts printed plus one piece of team-specific intelligence:
  - Team A: *"Your hospital's DPO has not been formally notified yet — this is a compliance gap"*
  - Team B: *"Your backup server from 48 hours ago has been confirmed clean"*
  - Team C: *"ANSSI has identified your organization as the primary source of the regional spread"*
  - Team D: *"A news crew has been spotted outside the hospital — earlier than anticipated"*
  *(Use the first N cards matching the number of teams running)*

**The 2-minute cross-IC exchange:**
Before returning, Incident Commanders have 2 minutes to talk to each other — informally, in character. With 2–4 ICs this is intimate and intense. They may share or withhold their team-specific intelligence. That choice matters and will surface in Phase 5 deliberation.

**Return and debrief to teams (5 min):**
Each IC returns downstairs and briefs their team. The information asymmetry is now established: teams know different things, and what they do with that shapes Phase 4 and Phase 5.

**What the ICC shows during Phase 3:**
The Consequence Dashboard is now visibly differentiated by team. All six metrics are displayed in a side-by-side team view. Incident Commanders can see — for the first time — how their team compares to others on the dashboard. This is intentionally visible and creates urgency: *"Team 3's GDPR exposure clock is worse than ours. Why? What did they decide that we didn't?"*

---

### BREAK (20 min) — Same Duration, Different Energy

The break now follows a high-intensity ICC coordination moment. Students are debriefing in their teams, processing asymmetric information, and arguing about what their IC brought back.

No app reflection prompts. The break is unstructured recovery time after Phase 3's intensity.

---

### Phase 4: Escalation (30 min) — ICC Movement + Literacy Artifact

**What changes:**

**Remove: surgery vs. HIM conflict inject**
This is folded into Phase 3's Regional Briefing as background intelligence the IC brings back ("surgical teams are pushing to resume elective procedures"). It becomes something teams must already be managing by Phase 4 rather than a fresh surprise.

**Add: ICC dispatch for media crisis**
When the media story inject fires, instructor announces: *"Media is at the front entrance. Press conference in 20 minutes. Incident Commander and Communications Officer: you are needed in the Incident Command Center."*

At ICC: they see the media sentiment board (one section of the Consequence Dashboard — social media post volume, press inquiry count, public perception index). They have 8 minutes to draft the press statement there, using the ICC screen for reference, before returning downstairs.

*This is the second ICC movement. The spatial separation from the team is intentional — in a real crisis, the people managing media are not in the same room as the people managing clinical operations.*

**Add: Literacy-graded patient notification (formalized from Phase 2 draft)**
By Phase 4, the patient notification draft from Phase 2 must be finalized. The final artifact is assessed against plain language criteria. The grading rubric for this artifact explicitly includes: reading level, structural clarity, cultural accessibility, channel equity considerations. This is one of the graded communication deliverables.

**Add: GDHP network notification trigger**
A brief inject in Phase 4: the WHO's Global Digital Health Partnership cybersecurity workstream has issued an alert requesting member organizations report significant ransomware incidents. Teams must decide whether and how to comply. This is a light touch — one decision question — but it introduces the GDHP into the simulation organically.

**What stays:**
- Family confrontation inject
- Staff morale/Marie-Claire voicemail inject
- Social media inject (nurse's family member post)

---

### Phase 5: Critical Decisions (30 min) — Cross-Team Deliberation Format

**What changes:**

**Structural change: cross-team deliberation for ransom and GDPR decisions**
Rather than each team deciding independently, Phase 5 opens with a reconfiguration:

Instructor announces: *"In a real regional incident of this scale, hospitals coordinate their response with ANSSI, the Regional Health Authority, and legal counsel. For the next 30 minutes, you are no longer operating as individual hospitals. You are operating as the regional incident coordination group. Reconfigure into two working groups — Teams 1-4 at one table cluster, Teams 5-8 at another."*

Each working group must reach a coordinated recommendation on:
1. The ransom demand (pay, refuse, or negotiate — and do all hospitals align or can they differ?)
2. The GDPR notification timing and scope
3. System restoration strategy

This creates genuine argumentation — teams who made different decisions in Phases 1-4 will have different information and different consequences on the dashboard, which means they will argue from genuinely different positions.

The individual team's decision is still what gets graded — but the deliberation is cross-team. After 20 minutes of deliberation, teams return to their own laptops to record their individual decision and justification (10 min).

**Add: BCP artifact begins**
During Phase 5 (last 10 min, after deliberation), teams begin the Business Continuity Plan. This is a structured template (in the app) with the first sections covering: incident containment record, downtime operations log, recovery sequencing priorities. They will complete it in Phase 6.

**What stays:**
- All three critical decision frameworks (ransom ethics, GDPR mechanics, restoration options) — these are the best content in the simulation
- CNIL notification station

---

### Phase 6: Recovery (20 min) — Consolidated and Upgraded

**What changes:**

**Replace generic preparedness radar → GDHP Cybersecurity Maturity Assessment**
The existing radar chart is replaced by a structured assessment against the WHO/GDHP cybersecurity governance dimensions:
1. Governance accountability and leadership
2. Incident detection and response protocols
3. Data recovery and resilience
4. Staff training and awareness culture
5. Digital trust architecture and data governance
6. Business continuity planning

Teams self-assess Sainte-Claire's posture on each dimension (1-5 scale) based on what they've just experienced. The assessment generates a radar chart but it's anchored to WHO/GDHP criteria rather than generic categories.

**Remove: Back-Entry Triage tab → Section 3 of BCP**
The BCP artifact (started in Phase 5) now includes a back-entry section. Teams complete the record reconciliation prioritization as part of the BCP rather than a standalone tab.

**Remove: Trust Recovery tab → after-action summary**
One after-action question asks: *"Which stakeholder group will be hardest to regain trust with, and what specific action — not a general strategy — would you take in the first 30 days?"* This is more focused than the standalone tab.

**Add: WHO responsible data governance framing to CNIL reflection**
The CNIL reflection question is expanded: teams must connect their notification decisions to the broader principle of responsible data governance — not just legal compliance, but institutional trust and patient dignity. Reference language from WHO data principles is provided as a prompt.

**What stays:**
- After-Action Summary (5 questions)
- Export function

---

## Movement Architecture — Summary

| Dispatch | Who | Phase | Direction | What They Receive |
|----------|-----|-------|-----------|-------------------|
| ANSSI briefing | IT Security + HIM Director | Phase 1 (post-decisions) | Up to ICC | ANSSI Advisory Card; see dashboard initialize |
| HIE Spread | IT Security | Phase 2 (~20 min) | Up to ICC | HIE Advisory Card; see HIE threat status screen |
| Literacy peer review | Communications Officer | Phase 2 (~30 min) | To another team's table | Peer feedback on plain-language notification draft |
| Regional Briefing | Incident Commander (all teams) | Phase 3 (new) | Up to ICC simultaneously | Regional Briefing Card (team-specific); see team-comparison dashboard; peer IC exchange |
| Media crisis | Incident Commander + Comms Officer | Phase 4 (media inject) | Up to ICC | See media sentiment board; draft press statement there |
| Cross-team deliberation | All students | Phase 5 | Reconfigure floor seating | Ransom/GDPR/restoration debate in two working groups |

Six distinct movement events. Each is purposeful — triggered by narrative logic, not just for physical variety.

---

## Consequence Architecture

The ICC dashboard reflects three tracked decision dimensions. These are read from the student app database (which already stores decisions) and rendered as live metrics.

### Dimension 1: Containment Speed
- **Tracked from:** Phase 1 decisions (network isolation timing, initial response priority)
- **Metric:** Data Exposure Estimate (expressed as a range: e.g., "12,000–40,000 patient records at risk")
- **Effect:** Fast isolation → lower estimate → Phase 5 ransom calculus is cleaner. Slow isolation → higher estimate → ransom decision is harder; GDPR notification scope is larger.

### Dimension 2: Communication Quality
- **Tracked from:** Phase 1 staff communication decision + Phase 2 communications
- **Metric:** Staff Availability Index (percentage, e.g., "74% of expected staff present")
- **Effect:** Good staff communication → metric higher → Phase 4 morale crisis is less severe. Poor or delayed → metric lower → Phase 4 Marie-Claire event hits harder; staffing for paper workflows is constrained.

### Dimension 3: Regulatory Posture
- **Tracked from:** Phase 2 GDPR-related decisions + Phase 3 IC briefing follow-through
- **Metric:** GDPR Compliance Window (hours remaining, displayed as a countdown)
- **Effect:** Teams that have begun GDPR preparation have more time to complete the CNIL notification properly. Teams that haven't are racing the clock by Phase 5.

### Additional ICC Dashboard Metrics (atmosphere/information, not directly tracked)
- **Financial Burn Rate:** Revenue loss accumulation (set by scenario constants, not team decisions — shown to reinforce stakes)
- **Media Pressure Index:** Grows over time regardless of decisions (mirrors real media escalation)
- **HIE Network Status:** Shows partner hospital connection statuses; updated by instructor when HIE inject fires

---

## Integration Touchpoints

### SHIFT Literacy Module
| Where | What | Connection |
|-------|------|------------|
| Phase 2 literacy inject | Plain-language patient notification draft | Readability principles, WHO plain language standards |
| Phase 2 cross-team review | Communications Officer peer review | Comparative analysis skill from literacy activity |
| Phase 4 notification finalization | Graded literacy artifact | Health literacy levels, cultural accessibility, channel equity |
| Assignment rubric | New literacy criterion in Crisis Communication | Formalizes literacy as a graded competency |

### SHIFT Interoperability Lab
| Where | What | Connection |
|-------|------|------------|
| Phase 2 HIE Spread inject | HIE attack vector decision | The shared HIE database as attack surface |
| ICC HIE dashboard | Threat status visualization | HIE architecture and data dependencies |
| HIE Advisory Card | Disconnection decision | Clinical consequences of severing data exchange |
| Phase 5 GDPR | Cross-organizational notification | Partner hospital data obligations through shared HIE |
| Debrief Block 6 | HIM perspective discussion | Data integrity cascade from HIE compromise |

### WHO Module 03 Alignment
| Feedback Item | Where Addressed |
|---------------|----------------|
| Reference GDHP cybersecurity workstream | Phase 4 GDHP notification inject; Phase 6 maturity assessment |
| WHO guidance on cybersecurity and digital trust | Phase 6 GDHP maturity framework; Assignment rubric framing |
| Business continuity planning | Phase 5-6 BCP artifact |
| Data recovery and resilience | Phase 6 maturity dimension 3 |
| Crisis communication (patient safety framing) | Phase 2 literacy inject; Phase 4 notification artifact |
| Cybersecurity maturity assessments | Phase 6 GDHP assessment (replaces generic radar) |
| Responsible data governance framing | Phase 6 CNIL reflection; Assignment rubric |
| Governance accountability mechanisms | Phase 3 Regional Briefing; Phase 5 cross-team deliberation |

---

## Physical Artifacts — Full Inventory

These are all printed/handwritten materials. New items added in v2 are marked.

| Artifact | Phase | Who Produces | Graded? |
|----------|-------|-------------|---------|
| Emergency Downtime MAR | Phase 2 Station | Team | Yes (Criterion 1) |
| Staff Communication Bulletin | Phase 2 Station | Team | Yes (Criterion 4) |
| Emergency Patient ID Wristband | Phase 2 Station | Team | Yes (Criterion 1) |
| Shift Handoff Tool | Phase 2 Station | Team | Yes (Criterion 1) |
| Paper Patient Record | Phase 2 Station | Team | Yes (Criterion 1) |
| **Literacy-Graded Patient Notification** *(new)* | Phase 2 → finalized Phase 4 | Comms Officer + peer review | Yes (Criterion 4 expanded) |
| Press Statement | Phase 4 Station | Team | Yes (Criterion 4) |
| Family Information Sheet | Phase 4 Station | Team | Yes (Criterion 4) |
| Board Recommendation Memo | Phase 5 Station | Team | Yes (Criteria 2 & 4) |
| CNIL Breach Notification | Phase 5 Station | Team | Yes (Criterion 3) |
| **Business Continuity Plan** *(new)* | Phase 5-6 | Team | Yes (new Criterion 5 component) |
| After-Action Summary | Phase 6 | Individual | Yes (Criterion 5) |
| **ANSSI Advisory Card** *(new — instructor-produced)* | Phase 1 ICC | Instructor → IT Security/HIMD | No — intelligence prop |
| **HIE Advisory Card** *(new — instructor-produced)* | Phase 2 ICC | Instructor → IT Security | No — intelligence prop |
| **Regional Briefing Card** *(new — instructor-produced)* | Phase 3 ICC | Instructor → each IC | No — intelligence prop |

---

## ICC Dashboard — Technical Specification

**What it is:** A new Streamlit page (`icc_dashboard.py`) deployed separately from the student app. Reads from the same SQLite database the student app writes to.

**Display:** One large screen on the ICC floor. Students who go up read it — they do not interact with it on individual devices.

**Content — per team view (side-by-side panels, one per team):**
```
┌─────────────────────────────┐
│  TEAM [NAME]                │
│                             │
│  DATA EXPOSURE ESTIMATE     │
│  ████████░░  12,000–40,000  │
│                             │
│  STAFF AVAILABILITY         │
│  ██████████  87%            │
│                             │
│  GDPR CLOCK                 │
│  52:14 remaining            │
│                             │
│  MEDIA PRESSURE             │
│  ████░░░░░░  Moderate       │
│                             │
│  HIE STATUS                 │
│  ● Connected [ALERT]        │
│                             │
│  FINANCIAL BURN             │
│  €28,400 / hour             │
└─────────────────────────────┘
```

**Data sources:**
- Data Exposure Estimate: derived from Phase 1 network isolation decision (stored in student app DB)
- Staff Availability: derived from Phase 1 communication decision
- GDPR Clock: real-time countdown from simulation start (fixed scenario constant)
- Media Pressure: scenario constant that escalates on a fixed schedule
- HIE Status: instructor-toggled (flips to ALERT when HIE inject fires)
- Financial Burn: scenario constant (not team-decision-dependent — shown for atmosphere)

**Build complexity:** Low. This is a read-only dashboard pulling from an existing database. No new data entry. Estimated 150–200 lines of Streamlit code.

---

## Revised Rubric Changes

The v2 assignment rubric reflects three changes:

**Criterion 4 (Crisis Communication) — expanded**
Add a literacy sub-criterion: the patient notification artifact is now explicitly assessed for plain language compliance (reading level, cultural accessibility, channel equity). The criterion weight stays at 32 points but the descriptor expands.

**Criterion 5 (Recovery Planning) — restructured**
The Business Continuity Plan replaces the back-entry workflow as the primary recovery artifact. The BCP encompasses back-entry prioritization as one section. Points remain at 20 but the descriptor is updated.

**Add: Criterion 6 — Interoperability and System Interdependency (new, 20 points)**
This is the only point change — add 20 points to reflect the HIE decision as a graded component. Teams are assessed on: whether their HIE disconnection decision was justified, whether they correctly identified clinical dependencies, and whether their GDPR obligations to HIE partner organizations were addressed. Total moves from 200 to 220 points.

---

## Files to Build

| File | Type | Status | Notes |
|------|------|--------|-------|
| `REVAMP-PLAN.md` | Planning doc | ✅ This document | |
| `icc_dashboard.py` | New Streamlit app | Not started | Reads from student app DB; ~200 lines |
| `student_app_v2.py` | Revised Streamlit app | Not started | Port from `student_app.py`; remove 3 tabs, add 2 injects, add BCP, add GDHP maturity |
| `instructor_app_v3.py` | Revised Streamlit app | Not started | Port from `instructor_app_v2.py`; add ICC dashboard trigger, HIE status toggle |
| `Assignment-Cybersecurity-Simulation-v2.md` | Assignment doc | Not started | Add Criterion 6; expand Criterion 4 literacy section; update BCP in Criterion 5 |
| `Instructor-Facilitation-Guide-v2.md` | Facilitation doc | Not started | Full rewrite of Phase-by-Phase section; add Phase 3 script; movement protocols |
| `Debrief-Guide-v2.md` | Debrief doc | Not started | Add literacy and interoperability debrief questions; connect to new artifacts |
| `Intelligence-Cards.md` | Print-ready content | Not started | ANSSI Advisory, HIE Advisory, Regional Briefing Card — print-ready text for all |
| `Narration-Transcripts-v2.md` | Audio scripts | Not started | Trim ambient; write targeted inject audio only (HIE alert, media break, PA system) |
| `build_worksheet_v2.py` | Build script | Not started | Regenerate student worksheet to reflect BCP and literacy artifacts |

---

## Open Questions — All Closed

All planning questions resolved. See **Planning Decisions — Locked** table above.
