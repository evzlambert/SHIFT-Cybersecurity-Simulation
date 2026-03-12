# Cybersecurity Breach Simulation — Instructor Facilitation Guide

## SHIFT Program — Saint-Etienne, France

**Duration:** 3 hours (160 min active + 20 min break)
**Debrief:** 2 hours (separate session)
**Format:** Streamlit-based interactive simulation with team decision-making
**Students:** Mixed — Health Sciences, Healthcare Administration, Health Informatics & Information Management (undergraduate and graduate)

---

## Overview

This simulation immerses students in a ransomware attack on a French regional hospital (Centre Hospitalier Sainte-Claire, 350 beds). Students experience the breach from assigned organizational roles and must manage downtime procedures, manual workflows, communication, stakeholder pressure, regulatory compliance, and executive-level decisions across a simulated 72+ hour timeline compressed into 3 hours.

The simulation is delivered through a Streamlit web application with an interactive admin dashboard, progressive inject events, paper records simulation, communication drafting, financial impact projections, and structured after-action planning.

---

## Learning Objectives

1. Describe how a cybersecurity breach disrupts clinical, administrative, and operational workflows in a healthcare setting
2. Apply downtime procedures including paper-based documentation, manual patient identification, and alternative communication
3. Evaluate trade-offs in crisis decision-making across patient safety, regulatory compliance, financial impact, and reputation
4. Draft crisis communications for multiple audiences (staff, patients, regulators, media, families)
5. Assess data integrity challenges of transitioning between electronic and manual processes
6. Navigate inter-departmental conflict and stakeholder pressure during sustained crisis operations
7. Analyze ethical dimensions of ransomware response (payment, disclosure, privacy)
8. Reflect on how professional discipline shapes crisis response perspectives

---

## Simulation Structure

| Phase | Clock | Duration | Sim Hours | Content |
|-------|-------|----------|-----------|---------|
| **0: Setup & Orientation** | 0:00 | 15 min | Pre-breach | Scenario, roles, briefings, systems review |
| **1: The Breach** | 0:15 | 25 min | Hour 0–2 | Attack timeline, role-specific first actions, 4 team decisions |
| **2: Downtime Operations** | 0:40 | 40 min | Hour 2–24 | Manual workflows (7 areas), paper records sim, comms center, 4 inject events |
| **BREAK** | 1:20 | 20 min | — | Pause; decision log review |
| **4: Escalation & Pressure** | 1:40 | 30 min | Hour 24–48 | Media story, family confrontation, staff morale, social media, dept. conflict |
| **5: Critical Decisions** | 2:10 | 30 min | Hour 48–72 | Ransom demand, GDPR deadline, system restoration strategy |
| **6: Recovery Planning** | 2:40 | 20 min | Hour 72+ | Back-entry triage, trust recovery, preparedness radar, after-action summary |
| **END** | 3:00 | — | — | Export reports; transition to debrief |

---

## Before the Session

### Technical Setup
- Launch: `pip3 install -r requirements.txt && python3 -m streamlit run app.py`
- Test on projector/screen AND on student devices (each team needs one device)
- Prepare backup: printed decision sheets in case of technical issues

### Room Setup
- **Teams of 5** (one per role). If fewer than 5 per team, double up the Communications & Compliance Officer with another role, or assign one student as a "floating advisor."
- Each team needs: one laptop/tablet for the Streamlit app, scratch paper, pens
- Post the simulation timeline visibly (board or projected)

### Team Composition
- **Mix disciplines intentionally**: each team should include students from different backgrounds
- **Role assignment strategy**: place students in roles matching their discipline first, then cross-assign in debrief discussion
  - HIM students → HIM Director
  - Healthcare admin students → Incident Commander
  - Health sciences/clinical students → Clinical Operations Lead
  - Informatics students → IT Security & Informatics Lead
  - Graduate students → Communications & Compliance Officer (most nuanced regulatory reasoning)

---

## Facilitation Guide by Phase

### Phase 0: Setup & Orientation (15 min)

**Instructor actions:**
- Walk teams through the scenario and hospital profile
- Help with role selection; ensure balanced teams
- Have students read their role briefing carefully — it sets their perspective for the entire simulation
- Emphasize ground rules: stay in role, document decisions, no perfect answers

**Key message to students:**
> "You are about to experience what real hospital leaders go through during a cyberattack. This is not a technical exercise — it is a leadership, communication, and organizational resilience exercise. Your professional perspective matters. Stay in your role."

### Phase 1: The Breach (25 min)

**Instructor actions:**
- Optional: read the breach timeline aloud for dramatic effect, pacing events every 30-60 seconds
- After the timeline, give teams 2-3 minutes to discuss their role-specific first action individually before team decisions
- Circulate and prompt teams that are stuck: "What is your FIRST action? Not your plan — your action."
- Push teams to decide, not endlessly debate. Time pressure is the point.

**Facilitation prompts:**
- "Your pharmacy cabinets are locked. ICU patients need drips. What do you do RIGHT NOW?"
- "400 staff are arriving. They know nothing. Rumors are spreading. How do you communicate?"
- "There are 8 women in labor. The nearest alternative maternity unit is 50 minutes away."
- "The attackers got in 11 days ago. What does that tell you about what they might have taken?"

### Phase 2: Downtime Operations (40 min)

**This is the richest phase — 40 minutes.** Direct teams to work through all four tabs:

1. **Manual Workflows (10-12 min):** Teams must make decisions for 7 workflow areas. Encourage them to read the risk notes. Ask: "What breaks first?"
2. **Paper Records Simulator (8-10 min):** Require teams to enter at least 2 patient records. The experience of manual documentation IS the lesson. Then review the back-entry cost estimator — the numbers are sobering.
3. **Communication Center (8-10 min):** Teams should draft at least 2 communications to different audiences. Push them to write actual messages, not bullet points.
4. **Inject Events (10-12 min):** Four events: medication near-miss, ambulance diversion, shift handoff, paper records crisis. Each requires a team decision with role-specific considerations.

**Facilitation prompts:**
- "How confident are you that the paper record you just entered is complete? What's missing?"
- "It's 19:00. Your day shift has been working 13 hours. Evening staff know nothing about paper processes. Go."
- "11% of your paper records can't be matched to a patient. That's 350 orphaned documents. What do you do?"
- "A pregnant woman at 36 weeks is in the ambulance. You're on diversion. What do you tell the paramedics?"

### BREAK (20 min)

**Instructor actions:**
- Encourage teams to review their decision log during the break
- Casually plant seeds: "When you come back, the media will be involved." "Think about who hasn't heard from you yet."
- The app has a break screen with reflection prompts

### Phase 4: Escalation & Stakeholder Pressure (30 min)

**This is the most emotionally intense phase.** Five inject events with immersive content (news tickers, voicemails, social media posts):

1. **Media Story (5 min):** The story breaks on local TV. Press conference or written statement?
2. **Family Confrontation (5 min):** An angry family member in the lobby. Who responds? How?
3. **Staff Morale Crisis (5 min):** A charge nurse voicemail about burnout and near-misses. This is a patient safety issue.
4. **Social Media Firestorm (5-7 min):** Multiple posts including one from a nurse's family member. Do you engage?
5. **Inter-Department Conflict (5-8 min):** Surgery vs. HIM on resuming elective procedures. The Incident Commander must decide.

**Facilitation prompts:**
- "The man in the lobby represents hundreds of families with the same question. Your answer sets the template."
- "Marie-Claire is one of your best charge nurses. If she breaks, the unit breaks. What do you do for her?"
- "The Chief of Surgery says 'We operated for decades before computers.' Is he right? Is the HIM Director right? Or is the answer somewhere else?"
- "A nurse's family member posted on social media. Do you discipline the nurse? That's a morale disaster during a crisis. Do you ignore it? That's an information security issue."

### Phase 5: Critical Decisions (30 min)

**The three hardest decisions in the simulation:**

1. **Ransom Demand (10 min):** €2.5M demand, €1M insurance cap, ANSSI says don't pay. Genuine ethical debate. Push teams to consider: patient data exposure, criminal funding, insurance implications, legal landscape (Loi LOPMI 2023).
2. **GDPR Notification (10 min):** 72-hour clock with incomplete information. Push teams on the tension between transparency and liability. Discuss: how do you notify 180,000 people that their health data may have been stolen?
3. **System Restoration (10 min):** Four options with different risk/speed/data trade-offs. Every role has a different preference. Make them negotiate.

**Facilitation prompts:**
- "The ransom is €2.5M. But the GDPR fine for a breach of this magnitude could be €10-20M. Does that change your calculus?"
- "You have 14 hours left on the GDPR clock. You don't know the full scope. Do you file now or wait?"
- "Option A loses 48 hours of clinical data. That data is on paper somewhere in the hospital. Somewhere."
- "Who decides the restoration strategy? Is this a technical decision? A clinical decision? A financial decision? A data integrity decision?"

### Phase 6: Recovery Planning (20 min)

**Shift to strategic thinking.** Four tabs:

1. **Back-Entry Triage (7 min):** Prioritize 8 categories of paper records for back-entry. Reveals different priorities by role.
2. **Trust Recovery (5 min):** Strategy for 5 different audiences. The hardest: patients with stolen mental health records.
3. **Preparedness Assessment (4 min):** Radar chart — a good visual for cross-team comparison during debrief.
4. **After-Action Summary (4 min):** 5 reflection questions to prime the debrief.

**Key message:**
> "Recovery is not just technical. It's organizational, reputational, emotional, and financial. The systems may come back in days. The trust takes months."

---

## Cross-Disciplinary Discussion Points

### For Health Sciences Students
- Patient safety during downtime: the five rights without barcodes
- The medication near-miss and the math error from manual dose calculation
- Clinical decision-making without electronic decision support
- Staff fatigue and its impact on clinical judgment

### For Healthcare Administration Students
- Financial modeling: revenue loss, overtime, back-entry costs, insurance, potential GDPR fines
- Organizational communication strategy across 7+ audiences
- Governance: who has authority to make which decisions?
- The ransom as a business decision with ethical dimensions

### For Health Informatics & Information Management Students
- Data integrity across electronic → paper → electronic transitions
- The 11% orphaned records problem and reconciliation planning
- Coding backlog and revenue cycle cascade effects
- GDPR mechanics: what exactly goes in the CNIL notification?
- Back-entry workflow design and quality assurance

### For Graduate Students (All Disciplines)
- Strategic preparedness and organizational resilience
- Ethical analysis of ransomware payment
- The intersection of cybersecurity policy, healthcare regulation, and operations
- Leadership under uncertainty — deciding with incomplete information

---

## Connecting to Other SHIFT Modules

| Module | Connection |
|--------|------------|
| **Project Management** | Crisis response uses incident command (a PM structure). Recovery is a project with scope, timeline, budget, stakeholders. The PM simulation's "disruption" concept maps directly to the breach injects. |
| **Interoperability** | Interconnected systems create cascading failures. PACS goes down → can't compare prior imaging. LIS goes down → can't get lab alerts. Interoperability is a strength AND a vulnerability. |
| **Data Analytics** | Data integrity issues from downtime create downstream analytics problems. How do you trust population health data that includes manually entered crisis records? |
| **Ethics** | Ransom ethics, patient notification equity, privacy vs. transparency, staff surveillance (social media), consent during crisis. |
| **Hackathon** | Students may propose cybersecurity resilience solutions as hackathon projects. The preparedness radar identifies specific gaps. |

---

## Real-World Context (Optional Talking Points)

- **Centre Hospitalier de Versailles (2022):** French hospital, ransomware, forced patient transfers, months of disruption
- **Centre Hospitalier de Corbeil-Essonnes (2022):** 11GB of patient data published after ransom refusal
- **WannaCry / NHS (2017):** 80 hospital trusts, 19,000 appointments canceled, £92M cost
- **CommonSpirit Health (2022):** 140 US hospitals, weeks of EHR downtime
- **ANSSI reports:** France experienced a 400% increase in ransomware attacks 2020-2022; healthcare is the 3rd most targeted sector
- **Loi LOPMI (2023):** New French law requiring police report within 72h of ransom payment for insurance eligibility

---

## Assessment Rubric

| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|-----------|--------------|----------------|-----------------|----------------|
| **Role Engagement** | Consistently advocated from role with nuance and depth | Mostly in role with clear advocacy | Occasionally referenced role | Did not engage with role |
| **Decision Quality** | Well-justified with multi-stakeholder awareness | Justified with trade-off awareness | Made but limited justification | Reactive or unjustified |
| **Communication** | Audience-appropriate, correct tone, complete content | Mostly appropriate, minor gaps | Generic or missing key elements | Did not draft communications |
| **Interdisciplinary Awareness** | Actively sought and integrated other perspectives | Acknowledged others when prompted | Aware but limited integration | Focused only on own role |
| **Stakeholder Management** | Sophisticated handling of competing pressures | Addressed stakeholders adequately | Acknowledged but did not fully address | Ignored external stakeholders |
| **Ethical Reasoning** | Articulated ethical dimensions with nuance | Identified key ethical issues | Mentioned ethics superficially | Did not consider ethics |
| **Reflection Depth** | Insightful connections to broader healthcare challenges | Thoughtful with some connections | Descriptive only | Minimal or surface-level |

---

## Troubleshooting

- **Streamlit won't launch:** Check Python 3.8+, run `pip3 install -r requirements.txt`
- **Students stuck on a phase:** Phases are sequential but the sidebar allows navigating back. You can verbally tell a team to skip ahead.
- **One student dominates:** Explicitly redirect: "Nurse, what does this mean for your patients?" "HIM Director, what about the paper records?"
- **Students want the 'right answer':** "There are no right answers. There are only trade-offs. Name yours."
- **Time pressure:** Phase 2 (40 min) and Phase 4 (30 min) can each absorb 5 min of slack. If running behind, Phase 6 can be shortened to 15 min by focusing on the After-Action Summary tab only.
- **Low-tech backup:** If Streamlit fails, the inject events and decisions can be read aloud and discussed with paper worksheets. The simulation works as a tabletop exercise without the technology.
