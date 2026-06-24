# SHIFT Cybersecurity Simulation — Intelligence Cards
## Facilitator Print Guide

**Print settings:** A4 (or Letter) paper, single-sided. Two cards per sheet using the horizontal rules as cut lines. Laminate if reusing across cohorts.

**Total cards:** 6 — one ANSSI Advisory, one HIE Advisory, four Regional Briefing variants (3A–3D).

**Do not distribute in advance.** Cards are handed to specific students at specific ICC dispatch moments only.

---
---

## CARD 1 — ANSSI Advisory
### Dispatch: Phase 1 — after decision set is complete
**Hand to:** IT Security Lead AND HIM Director when instructor announces the Phase 1 ICC dispatch

---

```
╔═══════════════════════════════════════════════════════════════╗
║       ANSSI — AGENCE NATIONALE DE LA SÉCURITÉ DES SI          ║
║   TECHNICAL ADVISORY — RESTRICTED — INCIDENT COMMAND ONLY     ║
╚═══════════════════════════════════════════════════════════════╝

Incident Reference: FR-2025-HOSP-0847
Classification:     RESTRICTED — Do not forward to uncleared staff
Issued:             Hour 1 — Immediate dissemination authorized

THREAT ACTOR ASSESSMENT
LockBit 3.0 ransomware. Known TTPs include lateral movement via
unpatched SMB shares and data exfiltration 11–18 days before
encryption trigger. You are likely NOT seeing the initial intrusion —
you are seeing the detonation.

CURRENT SCOPE ASSESSMENT (Hour 1)
Confirmed encrypted:   EHR main server, PACS, billing server,
                       3 radiology workstations
Status uncertain:      Backup server, pharmacy system, LIS
Likely clean:          Isolated clinical devices (ventilators,
                       infusion pumps — on isolated VLAN)

EXFILTRATION LIKELIHOOD: HIGH
Evidence of data staging in system logs from the past 3 days.
Assume breach of patient records until forensics confirm otherwise.

ANSSI GUIDANCE
1. Do NOT restart or attempt to decrypt any encrypted system
2. Isolate backup server immediately if not already done
3. Contact Regional HIE Coordinator — anomalous data packets
   detected at two partner institutions
4. File CNIL breach notification within 72 hours of discovery
   → Breach discovered: 06:12 today → Deadline: 06:12 Thursday

GDPR CLOCK STATUS: Hour 1 of 72
```

---
---

## CARD 2 — HIE Advisory
### Dispatch: Phase 2 — when the HIE Spread audio inject fires (~20 min in)
**Hand to:** IT Security Lead when instructor announces the Phase 2 ICC dispatch

---

```
╔═══════════════════════════════════════════════════════════════╗
║    REGIONAL HIE — URGENT INCIDENT NOTIFICATION                 ║
║    Auvergne-Rhône-Alpes Regional Health Authority             ║
╚═══════════════════════════════════════════════════════════════╝

To:   Sainte-Claire IT Security Lead
From: HIE Technical Coordinator, Regional Health Authority
Time: Hour 14 — URGENT

SITUATION
Anomalous outbound data packets detected from Sainte-Claire's
HIE node beginning approximately Hour 8. Two partner hospitals
are reporting unusual query patterns originating from your
institution's HIE credentials.

CURRENT PARTNER HOSPITAL STATUS
  ● CHU de Grenoble:    Monitoring (no isolation yet)
  ● Clinique du Parc:   Monitoring (no isolation yet)
  ● CH de Valence:      Normal — no anomaly detected
  ● Sainte-Claire:      ⚠ ALERT — source of anomaly

WHAT FLOWS THROUGH THIS HIE
  • Active patient demographics (MPI-matched)
  • Medication reconciliation records
  • Lab result forwarding (outpatient continuity)
  • Discharge summary exchange

CLINICAL CONSEQUENCE OF HIE DISCONNECTION
If Sainte-Claire is disconnected from the HIE, your institution
loses automatic medication reconciliation for transferred patients.
ED physicians will need to call partner hospitals for records.
Discharge summaries will require manual fax or courier.

GDPR NOTE
If the attackers accessed records via the HIE connection,
your GDPR notification obligations extend to partner hospitals'
patient data. This may significantly expand your notification scope.

YOUR DECISION (bring back to your team):
Do you request the Regional Health Authority to isolate
Sainte-Claire from the HIE network — and on what timeline?
```

---
---

## CARD 3A — Regional Briefing Card (Team A)
### Dispatch: Phase 3 — all Incident Commanders simultaneously
**Hand to:** Team A's Incident Commander at Phase 3 ICC briefing

---

```
╔═══════════════════════════════════════════════════════════════╗
║   REGIONAL HEALTH AUTHORITY — INCIDENT BRIEFING               ║
║   CONFIDENTIAL — INCIDENT COMMANDER EYES ONLY                 ║
╚═══════════════════════════════════════════════════════════════╝

Issued: Hour 20 · Delivered at Incident Command Center

REGIONAL STATUS — ALL HOSPITALS
• Sainte-Claire identified as likely origin of HIE anomalies
  affecting two partner hospitals
• ANSSI advisory issued: recommends against ransom payment
• Le Monde has contacted the Regional Authority —
  national press coverage is imminent
• GDPR 72-hour clock: 52 hours remaining

────────────────────────────────────────────────────────────────
INTELLIGENCE SPECIFIC TO YOUR HOSPITAL
────────────────────────────────────────────────────────────────

Your hospital's Data Protection Officer (DPO) has not yet been
formally notified of the breach.

Under GDPR Article 37–39 and CNIL guidance, the DPO must be
involved in preparing and filing the breach notification. Filing
without DPO involvement is a procedural compliance gap that
regulators have cited in post-incident reviews.

This is not a minor detail — it is documentation the CNIL
will ask about.

QUESTION TO BRING BACK TO YOUR TEAM:
How will your team close this gap before the 72-hour window
closes? Who is responsible? What does the DPO need to review?
```

---
---

## CARD 3B — Regional Briefing Card (Team B)
### Dispatch: Phase 3 — all Incident Commanders simultaneously
**Hand to:** Team B's Incident Commander at Phase 3 ICC briefing

---

```
╔═══════════════════════════════════════════════════════════════╗
║   REGIONAL HEALTH AUTHORITY — INCIDENT BRIEFING               ║
║   CONFIDENTIAL — INCIDENT COMMANDER EYES ONLY                 ║
╚═══════════════════════════════════════════════════════════════╝

Issued: Hour 20 · Delivered at Incident Command Center

REGIONAL STATUS — ALL HOSPITALS
• Sainte-Claire identified as likely origin of HIE anomalies
  affecting two partner hospitals
• ANSSI advisory issued: recommends against ransom payment
• Le Monde has contacted the Regional Authority —
  national press coverage is imminent
• GDPR 72-hour clock: 52 hours remaining

────────────────────────────────────────────────────────────────
INTELLIGENCE SPECIFIC TO YOUR HOSPITAL
────────────────────────────────────────────────────────────────

Your IT team has confirmed that the hospital's backup server —
created 48 hours before the breach — is intact and unencrypted.

This is your cleanest restoration option. It survived because
it was on an isolated network segment.

However: 48 hours of pre-breach clinical activity will be absent
from this backup. Approximately 180 patient encounters, 14 surgical
cases, and 3 days of lab results from that window will need to be
reconstructed from paper records.

QUESTION TO BRING BACK TO YOUR TEAM:
How does the confirmed backup change your restoration strategy?
Which clinical data from those 48 missing hours is most critical
to reconstruct first — and how will you do it?
```

---
---

## CARD 3C — Regional Briefing Card (Team C)
### Dispatch: Phase 3 — all Incident Commanders simultaneously
**Hand to:** Team C's Incident Commander at Phase 3 ICC briefing

---

```
╔═══════════════════════════════════════════════════════════════╗
║   REGIONAL HEALTH AUTHORITY — INCIDENT BRIEFING               ║
║   CONFIDENTIAL — INCIDENT COMMANDER EYES ONLY                 ║
╚═══════════════════════════════════════════════════════════════╝

Issued: Hour 20 · Delivered at Incident Command Center

REGIONAL STATUS — ALL HOSPITALS
• Sainte-Claire identified as likely origin of HIE anomalies
  affecting two partner hospitals
• ANSSI advisory issued: recommends against ransom payment
• Le Monde has contacted the Regional Authority —
  national press coverage is imminent
• GDPR 72-hour clock: 52 hours remaining

────────────────────────────────────────────────────────────────
INTELLIGENCE SPECIFIC TO YOUR HOSPITAL
────────────────────────────────────────────────────────────────

ANSSI forensics have identified Sainte-Claire as the PRIMARY
point of entry for what appears to be a coordinated regional
attack on healthcare infrastructure.

Your institution is not only a victim — it is the origin point
through which the attack spread to partner hospitals. The Regional
Health Authority will expect you to take a leadership role in
coordinating the regional response.

CHU de Grenoble and Clinique du Parc are waiting for Sainte-Claire
to share forensic findings with their IT security teams.

QUESTION TO BRING BACK TO YOUR TEAM:
What obligations does Sainte-Claire now have to the partner
hospitals? What do you share with them, when, and through
what channel? Does this change your CNIL filing?
```

---
---

## CARD 3D — Regional Briefing Card (Team D)
### Dispatch: Phase 3 — all Incident Commanders simultaneously
**Hand to:** Team D's Incident Commander at Phase 3 ICC briefing

---

```
╔═══════════════════════════════════════════════════════════════╗
║   REGIONAL HEALTH AUTHORITY — INCIDENT BRIEFING               ║
║   CONFIDENTIAL — INCIDENT COMMANDER EYES ONLY                 ║
╚═══════════════════════════════════════════════════════════════╝

Issued: Hour 20 · Delivered at Incident Command Center

REGIONAL STATUS — ALL HOSPITALS
• Sainte-Claire identified as likely origin of HIE anomalies
  affecting two partner hospitals
• ANSSI advisory issued: recommends against ransom payment
• Le Monde has contacted the Regional Authority —
  national press coverage is imminent
• GDPR 72-hour clock: 52 hours remaining

────────────────────────────────────────────────────────────────
INTELLIGENCE SPECIFIC TO YOUR HOSPITAL
────────────────────────────────────────────────────────────────

A news crew has been spotted outside Sainte-Claire's main entrance.
Arrival is significantly earlier than your communications plan
anticipated.

The journalist is Sophie Marin from Le Monde — the same journalist
who broke the CH de Rouen ransomware story in 2019. She has
documented sources inside French hospitals and is known for
obtaining internal communications.

She has not yet asked for a statement. She is observing.

QUESTION TO BRING BACK TO YOUR TEAM:
Does your current media strategy still hold given her early arrival?
If your press conference is not until tomorrow, what do you say —
or not say — to her today? What is the risk of saying nothing?
```

---
---

## Facilitator Notes

### Phase 3 ICC Briefing Protocol (15 minutes)

**Timing:** Immediately after Phase 2 is complete.

**Announcement (main floor, all teams hear this):**
> "The Regional Health Authority has arrived at Sainte-Claire. The Director of Regional Digital Health has called a joint briefing at the Incident Command Center. Incident Commander from each team: you are needed at the ICC immediately. Everyone else: stay at your table and review your Phase 2 decisions."

**At the ICC (co-facilitator leads, playing the Regional Authority Director):**

1. **3-minute regional briefing** (co-facilitator delivers, in character):
   - The breach has spread via the HIE to two partner hospitals
   - GDPR clock: 52 hours remaining
   - ANSSI recommends against ransom payment
   - National media contact imminent
   
2. **Card distribution:** Hand each IC their team-specific card. Give them 2 minutes to read silently.

3. **2-minute IC exchange:** Announce — *"You have two minutes before you return to your teams. In a real regional incident, Incident Commanders consult each other. Use this time."* Step back and observe. Do NOT facilitate. Note what gets shared and what doesn't.

4. **ICs return to teams** — they have approximately 5 minutes to brief before Phase 3 closes and the Break begins.

---

### Adapting for Fewer Than 4 Teams

| Teams | Use These Cards |
|-------|----------------|
| 2 teams | 3A (DPO gap) + 3B (clean backup confirmed) |
| 3 teams | 3A + 3B + 3D (media urgency) |
| 4 teams | 3A + 3B + 3C + 3D |

Cards 3A and 3B represent the most common real-world gaps and produce the most productive team discussions. Card 3C (primary origin point) is the highest-stakes card and should go to the team that appears most engaged and analytically strong. Card 3D adds urgency to the communications track without changing technical decisions.

---

### What to Watch For

- **Information sharing at ICC:** Do ICs share their team-specific intelligence? Withhold it? This reveals real-world information politics.
- **DPO card (3A):** Most teams won't have thought about the DPO. This card surfaces a genuine, common compliance gap.
- **Backup card (3B):** Watch how teams revise their restoration strategy. Some will go all-in on the clean backup; others will argue for hybrid.
- **Origin point card (3C):** This creates moral weight — the team must consider obligations beyond their own hospital.
- **Media card (3D):** Creates urgency without giving them a clear right answer. No decision is safe.
