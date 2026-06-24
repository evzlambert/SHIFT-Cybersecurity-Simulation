# Cybersecurity Breach Simulation — Instructor Facilitation Guide v2
## SHIFT Program — WHO Academy, Lyon

**Duration:** 3 hours 10–15 minutes active + 20 min break
**Debrief:** 2 hours (separate session, see Debrief-Guide-v2.md)
**Format:** Streamlit-based simulation with two-floor physical movement
**Students:** Mixed disciplines — Health Sciences, Healthcare Administration, HIIM (UG and grad)
**Teams:** 2–4 teams of 5 students

**Tech setup:** See `WHO-Setup-Guide.md` — do not duplicate those steps here.

---

## What Is Different in v2

| v1 | v2 |
|----|----|
| All teams stationary throughout | Six purposeful ICC floor dispatches |
| No cross-team interaction | Phase 3 Regional Briefing + Phase 5 cross-team deliberation |
| Paper Records Simulator tab | Physical artifact stations only (tab removed) |
| Communications Center tab | Replaced by literacy inject with peer review movement |
| Generic preparedness radar | GDHP cybersecurity maturity assessment |
| Surgery/HIM conflict inject | Folded into Phase 3 intelligence card |
| Back-entry and trust recovery tabs | Consolidated into Business Continuity Plan artifact |
| 7 manual workflow decision areas | 4 high-stakes areas (3 trimmed) |
| Ambient continuous audio narration | Targeted audio injections at specific moments only |
| No inter-module framing | Explicit literacy + interoperability integration |

---

## Learning Objectives

1. Describe how a ransomware breach disrupts clinical, administrative, and operational workflows in a healthcare setting
2. Apply downtime procedures including paper documentation, manual patient identification, and alternative communication
3. Evaluate trade-offs in crisis decision-making across patient safety, regulatory compliance, financial impact, and reputation
4. Draft crisis communications that meet WHO plain language standards for diverse patient populations *(literacy integration)*
5. Assess how health information exchange architecture creates both data-sharing benefits and attack surface vulnerability *(interoperability integration)*
6. Apply GDHP cybersecurity governance dimensions to assess institutional preparedness
7. Navigate GDPR Article 33 notification obligations under time pressure and incomplete information
8. Analyze the ethical dimensions of ransomware response — payment, disclosure, patient harm
9. Apply business continuity planning principles to a real-time healthcare crisis

---

## Simulation Structure

| Phase | Clock | Duration | Sim Time | Key Change from v1 |
|-------|-------|----------|----------|--------------------|
| **0: Orientation** | 0:00 | 10 min | Pre-breach | Inter-module framing added; ICC intro; role cards pre-read |
| **1: The Breach** | 0:10 | 25 min | Hour 0–2 | ICC dispatch after decision set |
| **2: Downtime Operations** | 0:35 | 40 min | Hour 2–24 | HIE inject + ICC; literacy inject + cross-team movement |
| **3: Regional Briefing** *(NEW)* | 1:15 | 15 min | Hour 20 | All ICs to ICC simultaneously; asymmetric intelligence |
| **BREAK** | 1:30 | 20 min | — | Moved later; no app prompts |
| **4: Escalation** | 1:50 | 30 min | Hour 24–48 | ICC dispatch for media; literacy artifact finalized; GDHP inject |
| **5: Critical Decisions** | 2:20 | 30 min | Hour 48–72 | Cross-team deliberation; BCP artifact begins |
| **6: Recovery** | 2:50 | 20 min | Hour 72+ | GDHP maturity assessment; BCP completed |
| **END** | 3:10 | — | — | PDF export; transition to debrief |

---

## Movement Architecture — Master Reference

Use this as your dispatch cue card. Keep it visible during the simulation.

| # | Phase | Trigger | Who Goes Up | Duration | Card | Return cue |
|---|-------|---------|------------|----------|------|------------|
| 1 | Phase 1 — after decisions | "ANSSI dispatch" | IT Security + HIM Director (one team) | 8 min | ANSSI Advisory (Card 1) | "Return and brief your team" |
| 2 | Phase 2 — ~20 min in | HIE audio inject | IT Security (one team) | 8 min | HIE Advisory (Card 2) | "Return and decide together" |
| 3 | Phase 2 — ~30 min in | Literacy inject fires | Comms Officer | 5 min | None — peer review | "Return with feedback" |
| 4 | Phase 3 | "Regional Briefing" | All ICs simultaneously | 12 min | Cards 3A–3D | Auto — ICs brief teams |
| 5 | Phase 4 — media inject | "Media dispatch" | IC + Comms Officer (one team) | 8 min | None — view ICC screen | "Return with press statement" |
| 6 | Phase 5 — start | "Regional coordination" | All students reconfigure | 20 min | None — floor discussion | After deliberation, return to own laptops |

*Dispatch #6 is a floor reconfiguration, not an ICC floor movement.*

---

## Facilitation Guide by Phase

---

### Phase 0: Orientation (10 min)

**Before students arrive:** Role cards have been distributed the day before. Students arrive having read them.

**Instructor script (adapt to your voice):**

> *"Before we begin, three things you've already done in this program are going to appear in this simulation. In the interoperability lab, you built and queried an HIE — today you'll encounter that same HIE as an attack surface. In the literacy module, you analyzed plain language communication — today you'll have to produce it under time pressure. And the WHO governance frameworks you've been introduced to provide the standards against which this hospital's preparedness will be judged. These aren't coincidences. They're the point of building a curriculum that connects."*

**Cover in 10 minutes:**
1. Scenario and hospital profile (3 min) — Centre Hospitalier Sainte-Claire, 350-bed French regional hospital, Monday 06:12
2. ICC floor intro (2 min) — explain the second floor, that students will be dispatched there during the simulation, and that the screen up there shows real-time data from all teams
3. Role confirmation (2 min) — confirm assignments, ensure each team has all five roles
4. Ground rules (3 min) — stay in role; no perfect answers; document decisions; if you're dispatched, go immediately

**Key message:**
> *"This is not a technical exercise. It is a leadership, communication, and data governance exercise. Your professional perspective matters. When you go upstairs, you will see how your decisions compare to other teams — in real time."*

---

### Phase 1: The Breach (25 min) — ICC Dispatch #1

**Opening:** Optional — read the breach timeline aloud for dramatic effect, pacing events 30–60 seconds apart. Students listen, then begin Phase 1 in the app.

**Facilitation prompts while teams work:**
- *"Your pharmacy cabinets are locked. ICU patients need drips. What do you do right now — not in five minutes."*
- *"400 staff are arriving for the 07:00 shift. They know nothing. Rumors are spreading in the parking lot."*
- *"The attackers got in 11 days ago. What does that tell you about what they may have already taken?"*
- *"There are 8 women in labor. The nearest alternative maternity unit is 50 minutes away."*

**After the decision set is complete (~20 min into Phase 1):**

**ICC Dispatch #1 — ANSSI Briefing**

Announce to the room (pick one team if running multiple):
> *"IT Security Lead and HIM Director from [Team name]: you are being called to the Incident Command Center. ANSSI has triggered an escalation protocol. Go now — your team continues without you."*

Co-facilitator on ICC floor:
- Hands Card 1 (ANSSI Advisory) to both students
- Points to the ICC dashboard — they can see their team's metrics initializing
- After 6–7 minutes: *"You need to get back downstairs and brief your team."*

**What students bring back:** Threat scope intelligence not yet visible to the rest of the team. Watch how they brief — does the IC immediately change plans based on the new information?

---

### Phase 2: Downtime Operations (40 min) — ICC Dispatches #2 and #3

**Phase 2 has four components. Unlike v1, there is no Paper Records Simulator tab and no Communications Center tab.** The physical artifact stations replace the first; the literacy inject replaces the second.

#### 2A: Manual Workflows (~10 min)

Direct teams to the Manual Workflows tab. Four decision areas remain (from seven in v1):
- Medication administration
- Patient identification
- Surgery decision
- IT system isolation

**Why four, not seven:** Dietary services, housekeeping, and outpatient scheduling are referenced in the scenario briefing as ongoing challenges — they don't require a formal decision point. Focus teams on the four areas with real clinical and safety stakes.

**Facilitation prompts:**
- *"What breaks first — and whose problem is it?"*
- *"The charge nurse on Unit 3 is asking if she can restart the medication cabinet. Who answers her? What do you say?"*

#### 2B: Physical Artifact Stations (~15 min)

Direct teams to the physical supply table. They rotate through the stations they haven't completed:
- Emergency Downtime MAR
- Emergency Patient ID Wristband
- Shift Handoff Tool
- Paper Patient Record (Marie DUPONT, 74)

**Instructor role during stations:** Circulate and observe quality. Do not help. If a team finishes fast, ask: *"Swap that record with another team member. Can they read it? What's missing?"*

#### 2C: HIE Spread Inject (~20 min into Phase 2) — ICC Dispatch #2

When approximately 20 minutes of Phase 2 have elapsed, play the HIE audio inject:

> *"IT Security, urgent message from the HIE Coordinator at the regional exchange. Anomalous data packets detected at two partner hospitals. Possible lateral spread via the exchange network. Requesting guidance immediately."*

Announce immediately:
> *"IT Security Lead from [Team]: urgent escalation at the ICC. Go immediately."*

**ICC Co-facilitator:** Toggle ICC dashboard HIE status to **"Compromised"**. Hand Card 2 (HIE Advisory) to the student.

**Why this matters (what to watch for):** The student must decide whether to request HIE disconnection. The clinical consequences (losing medication reconciliation, discharge summaries) directly reference what they built in the interoperability lab. If they disconnect, the co-facilitator toggles ICC to **"Isolated"** and students downstairs lose automatic reconciliation — this affects subsequent clinical decisions.

**When student returns:** Team deliberates the disconnection decision together. Log in app.

#### 2D: Literacy Inject (~30 min into Phase 2) — Cross-Table Movement #3

Display or announce the literacy inject text:

> *"The Communications Officer has been tasked with drafting the first patient-facing advisory. CNIL guidance has flagged that this hospital's catchment area includes 40,000 patients with low health literacy and 22,000 primary speakers of Arabic, Turkish, or Dari. The advisory must meet WHO plain language standards — 6th to 8th grade reading level, clear structure, no medical jargon."*

**Instruction to Communications Officers only:**
> *"Communications Officers: you have 8 minutes to draft a first version on paper. When you're done, take your draft to another team's table for peer review. They will give you feedback using the plain language checklist from your literacy module work. You will return with their feedback and revise. The final version is due at the end of Phase 4."*

**Facilitation note:** This is the first cross-team physical interaction. It is purposeful — literacy peer review IS the activity from the literacy module, applied under pressure. Other team members keep working on artifact stations while their Communications Officer is away.

---

### Phase 3: Regional Briefing — NEW (15 min) — ICC Dispatch #4

**This is the structural centerpiece of the v2 redesign.** All teams pause simultaneously. All Incident Commanders go upstairs together.

**Announce to the full room:**
> *"The Regional Health Authority has arrived at Sainte-Claire. The Director of Regional Digital Health has called a joint briefing at the Incident Command Center. Incident Commander from every team: you are needed at the ICC right now. Everyone else: stay at your table and review your Phase 2 decisions. What would you do differently?"*

**At the ICC — Co-Facilitator delivers the Regional Briefing (3 min, in character):**

See `Intelligence-Cards.md` Facilitator Notes for the full script. Key points to hit:
- HIE spread confirmed at two partner hospitals
- GDPR clock at Hour 20 — 52 hours remaining
- ANSSI recommends against ransom payment
- Le Monde has contacted the Regional Authority
- National press coverage is imminent

**Card handoff:** Give each IC their team-specific Regional Briefing Card (3A, 3B, 3C, or 3D). Two minutes to read silently.

**The IC exchange (2 min):**
> *"You have two minutes before you return to your teams. In a real regional incident, Incident Commanders talk to each other. Use this time."*

Step back. Do not facilitate. Observe: What do they share? What do they withhold? Who takes charge of the group? This exchange is debriefable material.

**ICs return (5 min):** Each IC briefs their team. Teams now have asymmetric information. The IC exchange may have increased or decreased that asymmetry depending on what was shared.

**ICC Dashboard note:** During Phase 3, the dashboard shows all teams' metrics side by side for the first time. ICs will see how their team compares. This is intentional. If Team B has a far better staff availability metric than Team A, Team A's IC knows — and carries that back.

**Transition to Break:**
> *"Take 20 minutes. When you come back, the story breaks on TV."*

---

### BREAK (20 min)

No app reflection prompts in v2. Teams are already debriefing — the Phase 3 ICC exchange and their IC's debrief have given them plenty to discuss. Let it happen organically.

**If teams ask what to do:** *"Review your Phase 2 decisions and your IC's briefing. Think about what you'd change."*

**Instructor/co-facilitator during break:**
- Check submissions folder on instructor laptop — confirm all team JSON files are updating
- Review ICC dashboard to note which teams are ahead/behind on metrics
- Brief co-facilitator on Phase 4 media dispatch timing

---

### Phase 4: Escalation (30 min) — ICC Dispatch #5

**Phase 4 opens with all teams back at their tables.**

**Removed from v1:** Surgery vs. HIM conflict inject. This tension has been seeded in Phase 3 intelligence cards and in the scenario briefing — it is background pressure, not a decision point. Removing it keeps Phase 4 focused on the communication and media crisis.

**Phase 4 sequence:**

#### 4A: Media Story (~5 min)

Play the media inject (TV news audio). Teams make their media decision in the app.

**ICC Dispatch #5 — Media Crisis:**
> *"Incident Commander and Communications Officer from [Team]: the media are at the front entrance. A press conference is in 20 minutes. You need to be at the Incident Command Center now."*

**At ICC:** Both students see the media pressure index on the ICC dashboard. They have 8 minutes to draft their press statement there, using the screen as context. Co-facilitator does not script this — just present the environment.

**Why separate them from their team:** In a real crisis, the people managing media are not in the same room as the people managing clinical operations. The spatial separation creates the communication challenge the inject is designed to surface.

#### 4B: Family Confrontation (~5 min)
No change from v1. Teams handle this at their tables.

**Facilitation prompt:**
> *"The man in the lobby represents 287 families with the same question. Your answer to him is your template for all of them."*

#### 4C: Staff Morale Crisis (~5 min)
No change from v1. Play the Marie-Claire voicemail audio inject.

**Facilitation prompt:**
> *"Marie-Claire is one of your best charge nurses. If she breaks, Unit 3 breaks. What does your role specifically allow you to do for her — right now, today?"*

#### 4D: Social Media (~5 min)
No change from v1.

#### 4E: Literacy Artifact — Final Draft (~5 min)

At the end of Phase 4, Communications Officers finalize their patient notification draft incorporating the peer feedback from Phase 2. This is a graded artifact. Prompt:

> *"Communications Officers: your patient notification draft is due before Phase 5. Incorporate your peer feedback. This will be assessed for plain language compliance — reading level, structure, cultural accessibility, and channel equity."*

#### 4F: GDHP Notification Trigger (~2 min)

Brief inject — display or read aloud:

> *"The WHO's Global Digital Health Partnership cybersecurity workstream has issued a regional alert requesting member organizations report significant ransomware incidents. Your institution's national authority has forwarded the request."*

Teams log one decision: comply now, comply after GDPR filing, or defer. This is light — one decision question, not a full inject sequence. Its purpose is to introduce the GDHP before Phase 6's maturity assessment.

---

### Phase 5: Critical Decisions (30 min) — Cross-Team Deliberation

**This phase has a structural change.** Teams do not work independently. They reconfigure for deliberation.

**Announce:**
> *"In a real regional incident of this scale, hospitals do not make the ransom, GDPR, and restoration decisions in isolation. They coordinate with ANSSI, the Regional Health Authority, and legal counsel. For the next 20 minutes, you are the regional incident coordination group. Teams 1 and 2, pull your tables together. Teams 3 and 4 — same."*

*(If only 2 teams: everyone pulls together into one group.)*

**What the working groups deliberate (20 min):**
1. The ransom demand — pay, refuse, or negotiate? Do all hospitals align, or can they diverge?
2. GDPR notification timing and scope — file now or at the deadline?
3. System restoration strategy — which option, and does the group coordinate?

**Facilitation role during deliberation:** Circulate between groups. Do not adjudicate. If a group reaches consensus too fast, ask: *"Team B's IC came back from the ICC with different intelligence than Team A. Does that change anything?"*

**After 20 minutes — return to individual laptops (10 min):**
> *"Return to your own tables. You have 10 minutes to record your individual team's decision and justification. Your team's decision is yours — the deliberation informed it, but you own it."*

Teams also begin the Business Continuity Plan artifact in the app (first three sections: incident containment record, downtime operations log, recovery sequencing priorities).

**Facilitation prompts during Phase 5:**
- *"The ransom is €2.5M. The GDPR fine for a breach of this magnitude could be €10–20M. Does that change the calculus?"*
- *"You have 14 hours on the GDPR clock. You don't know the full scope. Filing now protects you legally. Waiting gives you more accuracy. Which matters more?"*
- *"Who decides restoration strategy? IT? Clinical? Finance? Data governance? The answer tells you something about your hospital's actual governance structure."*

---

### Phase 6: Recovery (20 min)

**Two components replace the three tabs from v1.**

#### 6A: GDHP Cybersecurity Maturity Assessment (~12 min)

Teams self-assess Sainte-Claire against six WHO/GDHP governance dimensions. They rate what they've just experienced — not an abstract exercise.

The six dimensions:
1. Governance accountability and leadership
2. Incident detection and response protocols
3. Data recovery and resilience
4. Staff training and awareness culture
5. Digital trust architecture and data governance
6. Business continuity planning

**Facilitation prompt:**
> *"You have just spent three hours inside this hospital's incident response. You know exactly which of these dimensions failed and which held. Your ratings should reflect that — not what the hospital wished it had, but what it actually had."*

**Note:** The radar chart will generate from these ratings. Useful for cross-team comparison in debrief — different teams will have experienced the same scenario and rated it differently based on their decisions.

#### 6B: Business Continuity Plan — Completion (~5 min)

Teams complete the BCP artifact started in Phase 5. The final two sections:
- Back-entry prioritization (replaces the standalone tab from v1)
- Responsible data governance declaration (WHO data principles framing)

For the governance declaration prompt:
> *"Your CNIL notification addressed legal compliance. This section asks a different question: beyond what the law requires, what do you owe your patients — in terms of transparency, dignity, and trust — in how you communicate about the breach and recover from it? Reference WHO data principles in your response."*

#### 6C: After-Action Summary (~3 min)

Five reflection questions — same as v1. These prime the debrief.

---

## Cross-Disciplinary Discussion Points

### Health Sciences Students
- Patient safety during downtime: the five rights without barcodes or barcode scanners
- The medication near-miss and the math error risk in manual dose calculation
- Clinical decision-making without electronic decision support
- Staff fatigue and its cascade effect on clinical judgment

### Healthcare Administration Students
- Financial modeling: revenue loss, overtime costs, back-entry costs, insurance coverage, potential GDPR fines
- Organizational communication strategy across 7+ audiences simultaneously
- Governance: who has authority to make which decisions under incident command?
- The ransom as a governance decision with ethical, financial, and reputational dimensions

### HIIM Students
- Data integrity cascade: electronic → paper → electronic
- The 11% orphaned records problem and what it means for back-entry reconciliation
- GDPR Article 33 mechanics: exactly what goes into a CNIL notification — and what doesn't yet
- HIE architecture as both a clinical asset and an attack surface
- Back-entry workflow design and quality assurance under resource constraints

### Graduate Students (All Disciplines)
- GDHP cybersecurity workstream and global governance for healthcare cybersecurity
- WHO responsible data governance principles applied to crisis disclosure
- Strategic preparedness and organizational resilience
- Ethical analysis of ransomware payment (ANSSI guidance, Loi LOPMI 2023, patient harm calculus)

---

## Connecting to SHIFT Modules

| Module | Connection in v2 |
|--------|-----------------|
| **Project Management** | Incident command is a PM structure. The BCP artifact is a project deliverable with scope, timeline, and governance. The regional coordination in Phase 5 mirrors multi-stakeholder PM. |
| **Interoperability** | Phase 2 HIE inject: the same HIE students queried in the lab is now the attack surface. HIE disconnection decision applies data dependency mapping directly. The FHIR-based architecture makes the clinical consequences concrete. |
| **Literacy** | Phase 2 literacy inject and Phase 4 final draft: plain language patient communication under crisis pressure. Peer review between teams mirrors the literacy module activity format. |
| **Ethics** | Ransom ethics, patient notification equity (literacy and cultural access), privacy vs. transparency, staff surveillance (social media post), consent during crisis, responsible data governance declaration. |
| **Data Quality / Analytics** | Downtime data creates integrity gaps that affect downstream analytics. Manually entered crisis records are low-quality inputs into population health databases. The back-entry reconciliation problem is a data quality problem at scale. |

---

## WHO Module 03 Alignment Notes

| WHO Feedback Item | Where Addressed |
|------------------|----------------|
| Reference GDHP cybersecurity workstream | Phase 4 GDHP inject; Phase 6 maturity assessment |
| WHO cybersecurity and digital trust guidance | Phase 6 BCP responsible governance declaration |
| Business continuity planning | Phase 5–6 BCP artifact (graded) |
| Data recovery and resilience | Phase 6 GDHP dimension 3; maturity assessment |
| Crisis communication | Phase 2 literacy inject; Phase 4 patient notification artifact |
| Cybersecurity maturity assessments | Phase 6 GDHP assessment (replaces generic radar) |
| Responsible data governance framing | Phase 6 CNIL reflection; BCP governance declaration |
| Governance accountability mechanisms | Phase 3 Regional Briefing; Phase 5 cross-team deliberation |

---

## Real-World Context

- **Centre Hospitalier de Versailles (2022):** Ransomware, forced patient transfers, months of disruption — French context
- **Centre Hospitalier de Corbeil-Essonnes (2022):** 11GB of patient data published after ransom refusal — ANSSI case
- **WannaCry / NHS (2017):** 80 UK hospital trusts, 19,000 appointments canceled, £92M cost — scale reference
- **CommonSpirit Health (2022):** 140 US hospitals, weeks of EHR downtime — US comparison
- **GDHP Cybersecurity Workstream:** Active WHO partnership tracking national ransomware response policies
- **Loi LOPMI (2023):** French law requiring police report within 72h of ransom payment for insurance eligibility
- **ANSSI statistics:** France 400% increase in ransomware attacks 2020–2022; healthcare is 3rd most targeted sector

---

## Assessment Reference

The full rubric is in `Assignment-Cybersecurity-Simulation-v2.md`. Summary of criteria:

| Criterion | Points | What to Watch During Simulation |
|-----------|--------|--------------------------------|
| Clinical Downtime Management | 40 | Artifact station quality; decision justifications in Phase 1–2 |
| Regulatory Compliance | 40 | GDPR decisions; CNIL station; BCP governance declaration |
| Organizational Leadership | 40 | Stakeholder decisions Phase 4; Phase 3 IC briefing back to team |
| Crisis Communication | 40 | Literacy artifact quality; press statement; Phase 4 communications |
| Interoperability Response | 20 | HIE disconnection decision; justification; GDPR implications addressed |
| Business Continuity Planning | 20 | BCP artifact completeness; back-entry prioritization |
| **Total** | **200** | |

---

## Facilitation Tips — New Challenges in v2

**When ICC dispatches cause team anxiety:**
Some teams will be frustrated that key roles leave at critical moments. That is the point. Say: *"In a real incident, the people making decisions are not all in the same room. Manage it."*

**When cross-team deliberation in Phase 5 stalls:**
If a working group is not engaging substantively, name the asymmetry: *"Team B's IC came back from the ICC with different information than Team A's IC. Does anyone know what it was? Does it matter that you don't?"*

**When Communications Officers resist the literacy peer review:**
Remind them: *"The literacy module told you what makes health communication work. This is you proving you can apply it under pressure. That's the assessment."*

**When teams ask what the 'right answer' is:**
*"There are no right answers. There are trade-offs. Name yours and own it."*

**Time pressure — where to compress:**
- Phase 2 can absorb or donate 5 min (trim manual workflow discussion)
- Phase 3 can trim to 10 min by reducing IC exchange to 1 min
- Phase 6 can be shortened by skipping the maturity assessment ratings and going straight to BCP completion + after-action
- Do not cut Phase 5 deliberation — it is the most pedagogically distinctive element of v2

**Low-tech backup:**
If Streamlit fails entirely, the inject events and decisions can be read aloud and discussed as a facilitated tabletop. The physical artifact stations require no technology. The simulation works without the apps — it just loses the consequence tracking and the ICC dashboard feed.

---

## Troubleshooting

**A dispatched student refuses to go upstairs:**
Gently insist: *"The exercise requires it — go now, your team will manage."* Do not let this slide; the movement is structural, not optional.

**ICC dashboard isn't updating:**
Have the co-facilitator click "Refresh Now" in the sidebar. If still stale, have one team do a manual save in the student app. See `WHO-Setup-Guide.md` for deeper troubleshooting.

**One student dominates:**
Redirect explicitly: *"Nurse, what does this mean for your patients on Unit 3?" "HIM Director, what does the paper record situation look like from where you sit?"*

**Phase 3 Regional Briefing runs long:**
Tighten the IC exchange. The minimum viable Phase 3 is: 2-min briefing (skip narrative detail, hit the four bullet points) → hand cards → 1-min IC exchange → dismiss. That is 8 minutes. The 15-minute version is richer; the 8-minute version still delivers the core value.

**Teams at very different decision counts when Phase 3 starts:**
Announce: *"Before ICs go upstairs, each team should have completed at least the first three decisions in Phase 2. If you haven't, take three minutes now."* Then dispatch.
