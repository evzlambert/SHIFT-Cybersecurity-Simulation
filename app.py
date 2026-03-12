"""
SHIFT Program — Cybersecurity Breach Simulation
Saint-Etienne, France

A Streamlit-based immersive simulation of a ransomware attack on a regional
hospital system.  Students experience the breach from multiple organizational
perspectives and must manage downtime procedures, communication, manual
workflows, and recovery decision-making.

Duration: 3 hours (160 min active + 20 min break)
Separate 2-hour debrief follows.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SHIFT Cybersecurity Breach Simulation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .alert-critical {
        background-color: #ff4b4b; color: white; padding: 20px;
        border-radius: 10px; margin: 10px 0; font-weight: bold;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0%{opacity:1} 50%{opacity:0.7} 100%{opacity:1} }
    .alert-warning {
        background-color: #ffa726; color: white; padding: 15px;
        border-radius: 10px; margin: 10px 0;
    }
    .alert-info {
        background-color: #29b6f6; color: white; padding: 15px;
        border-radius: 10px; margin: 10px 0;
    }
    .alert-break {
        background-color: #7e57c2; color: white; padding: 25px;
        border-radius: 10px; margin: 20px 0; font-size: 1.2em;
        text-align: center;
    }
    .phase-header {
        border-bottom: 3px solid #ff4b4b;
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .news-ticker {
        background-color: #1a1a2e; color: #e94560; padding: 12px 20px;
        border-radius: 8px; font-family: monospace; margin: 8px 0;
        border-left: 4px solid #e94560;
    }
    .email-container {
        background-color: #f5f5f5; color: #333; padding: 20px;
        border-radius: 8px; margin: 10px 0; border: 1px solid #ddd;
    }
    .email-header {
        border-bottom: 1px solid #ddd; padding-bottom: 8px; margin-bottom: 12px;
        font-size: 0.9em; color: #666;
    }
    .voicemail-box {
        background-color: #fff3e0; color: #333; padding: 15px;
        border-radius: 8px; margin: 8px 0; border-left: 4px solid #ff9800;
        font-style: italic;
    }
    .social-media-post {
        background-color: #e3f2fd; color: #333; padding: 15px;
        border-radius: 8px; margin: 8px 0; border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HOSPITAL_NAME = "Centre Hospitalier Sainte-Claire"
HOSPITAL_DESC = (
    "A 350-bed regional hospital in southeastern France serving urban and rural "
    "communities. The hospital runs a modern EHR (DPI), integrated laboratory and "
    "radiology systems, an active patient portal (*Mon Espace Sante*), and a "
    "telehealth program for chronic disease follow-ups. 1,200 staff across "
    "clinical, administrative, and support services. The hospital is the primary "
    "trauma center for the region and hosts an active maternity unit averaging "
    "8 deliveries per day."
)

NUM_PHASES = 7  # 0-6

ROLES = {
    "Incident Commander (Hospital Administrator)": {
        "icon": "👔",
        "color": "#5c6bc0",
        "focus": "Executive decision-making, resource allocation, organizational communication",
        "background": "Healthcare Administration",
        "tasks": [
            "Activate the Hospital Incident Command System (HICS)",
            "Authorize downtime procedures and resource reallocation",
            "Coordinate with external agencies (police, ANSSI, ARS, insurance)",
            "Make go/no-go decisions on system recovery and ransom",
            "Manage media and public communication strategy",
            "Report to hospital board and regional health authority",
        ],
        "briefing": (
            "You are the most senior decision-maker in this crisis. Every major "
            "action requires your authorization. You must balance patient safety, "
            "financial impact, regulatory obligations, staff welfare, and public "
            "trust. You will be the one who ultimately faces the board, the media, "
            "and the regulator. Think about: What information do you need? Who do "
            "you trust? When do you escalate?"
        ),
    },
    "Health Information Manager (HIM Director)": {
        "icon": "📋",
        "color": "#26a69a",
        "focus": "Medical records, coding, data integrity, regulatory compliance, privacy",
        "background": "Health Informatics & Information Management",
        "tasks": [
            "Activate paper-based documentation procedures across all units",
            "Ensure patient identification protocols without barcodes",
            "Plan for back-entry of manual records once systems restore",
            "Track record completeness and data integrity risks in real-time",
            "Manage coding backlog and downstream revenue cycle impact",
            "Assess data breach scope for GDPR notification",
        ],
        "briefing": (
            "You are the guardian of the hospital's data. Right now, your data is "
            "both encrypted (inaccessible) and potentially exfiltrated (stolen). "
            "You must simultaneously manage the transition to paper, ensure data "
            "quality during downtime, and prepare for the massive reconciliation "
            "effort when systems return. Every paper form with missing data is a "
            "future problem. Think about: What data is most critical? How do you "
            "maintain integrity when everyone is stressed and rushing?"
        ),
    },
    "Clinical Operations Lead (Chief Nursing Officer)": {
        "icon": "🩺",
        "color": "#ef5350",
        "focus": "Patient safety, clinical workflows, staff coordination and welfare",
        "background": "Health Sciences / Clinical",
        "tasks": [
            "Implement manual medication verification (five rights without barcodes)",
            "Coordinate patient tracking on whiteboards across all units",
            "Manage nurse and clinical staff scheduling during extended crisis",
            "Maintain patient safety reporting without electronic systems",
            "Coordinate with pharmacy on manual medication dispensing",
            "Monitor staff fatigue and psychological well-being",
        ],
        "briefing": (
            "Patient safety is your north star. Without electronic safeguards, "
            "every medication administration, every patient transfer, every "
            "handoff is higher risk. Your staff are the ones physically doing the "
            "work — they are exhausted, scared, and working without their usual "
            "tools. You must keep patients safe AND keep your staff functional. "
            "Think about: Where are the highest-risk patients right now? What is "
            "most likely to go wrong in the next hour?"
        ),
    },
    "IT Security & Informatics Lead": {
        "icon": "💻",
        "color": "#42a5f5",
        "focus": "Technical response, system forensics, recovery planning",
        "background": "Health Informatics / Information Technology",
        "tasks": [
            "Isolate affected systems and contain the breach",
            "Coordinate with external cybersecurity forensics team",
            "Assess which systems are compromised vs. clean",
            "Determine data exfiltration scope (what did the attackers take?)",
            "Develop and execute system restoration plan with recovery priorities",
            "Document technical timeline for regulatory and legal reporting",
        ],
        "briefing": (
            "You are working two problems simultaneously: containment (stopping "
            "the attack from spreading) and forensics (understanding what happened "
            "and what was taken). Everyone will pressure you for timelines — 'When "
            "will the EHR be back?' — but premature restoration risks reinfection. "
            "You must communicate technical realities to non-technical leaders "
            "clearly and honestly. Think about: What can you verify as clean? "
            "What is your evidence threshold before restoring?"
        ),
    },
    "Communications & Compliance Officer": {
        "icon": "📢",
        "color": "#ab47bc",
        "focus": "Internal/external communications, regulatory notifications, legal exposure",
        "background": "Healthcare Administration / Legal",
        "tasks": [
            "Draft and manage all internal staff communications",
            "Manage patient and family notifications and inquiries",
            "Assess and execute GDPR breach notification (72-hour rule to CNIL)",
            "Coordinate with legal counsel on liability exposure",
            "Prepare and deliver media holding statements",
            "Monitor and respond to social media activity",
        ],
        "briefing": (
            "Information is your currency and your weapon. Too little "
            "communication breeds panic and rumor. Too much reveals details that "
            "could increase legal exposure or help the attackers. You must craft "
            "the right message for the right audience at the right time. You are "
            "also the one watching the GDPR clock — 72 hours from breach "
            "awareness to CNIL notification. Think about: What does each "
            "audience need to hear? What must you NOT say?"
        ),
    },
}

PHASES = [
    {"name": "Setup & Orientation",       "time": "15 min",  "sim_hours": "Pre-Breach",
     "description": "Learn the scenario, select roles, review hospital systems, read your role briefing."},
    {"name": "The Breach",                "time": "25 min",  "sim_hours": "Hour 0–2",
     "description": "The attack hits. Systems go down. Immediate triage and first response actions."},
    {"name": "Downtime Operations",       "time": "40 min",  "sim_hours": "Hour 2–24",
     "description": "Running a hospital on paper. Manual workflows, data entry, shift handoff, communication."},
    {"name": "BREAK",                     "time": "20 min",  "sim_hours": "—",
     "description": "Pause. Regroup. The crisis continues when you return."},
    {"name": "Escalation & Pressure",     "time": "30 min",  "sim_hours": "Hour 24–48",
     "description": "External pressure mounts: media, families, regulators, staff morale, inter-department conflict."},
    {"name": "Critical Decisions",        "time": "30 min",  "sim_hours": "Hour 48–72",
     "description": "Ransom demand, GDPR deadline, system restoration strategy. The hardest choices."},
    {"name": "Recovery Planning",         "time": "20 min",  "sim_hours": "Hour 72+",
     "description": "After-action planning, back-entry triage, trust rebuilding, and preparedness assessment."},
]

BREACH_EVENTS = [
    {"time": "06:12", "event": "Night-shift nurse reports EHR is 'frozen' on 3 workstations in the ICU.", "severity": "warning"},
    {"time": "06:15", "event": "A second nurse reports the same issue in the maternity unit. Midwife cannot access patient birth plans.", "severity": "warning"},
    {"time": "06:18", "event": "IT help desk receives 12 simultaneous calls. Lab system (LIS) shows error messages.", "severity": "warning"},
    {"time": "06:22", "event": "Pharmacy technician reports automated dispensing cabinets are unresponsive.", "severity": "warning"},
    {"time": "06:24", "event": "Radiology PACS displays a ransom message: 'Your files are encrypted. Contact us for decryption key. You have 72 hours.'", "severity": "critical"},
    {"time": "06:26", "event": "Night IT administrator attempts to restart servers — same ransom message appears on 4 of 6 core servers.", "severity": "critical"},
    {"time": "06:30", "event": "Pharmacy dispensing system confirmed offline. Automated medication cabinets locked hospital-wide.", "severity": "critical"},
    {"time": "06:33", "event": "Patient portal (*Mon Espace Sante*) goes dark. 47 telehealth appointments scheduled today.", "severity": "critical"},
    {"time": "06:35", "event": "Scheduling system unresponsive. 142 outpatient appointments for today cannot be confirmed.", "severity": "critical"},
    {"time": "06:38", "event": "Billing and revenue cycle system encrypted. No claims can be submitted.", "severity": "critical"},
    {"time": "06:40", "event": "IT Security confirms: ransomware (LockBit variant) has encrypted servers across EHR, LIS, PACS, pharmacy, and billing.", "severity": "critical"},
    {"time": "06:42", "event": "Forensic log review suggests initial access occurred 11 days ago via a phishing email to a radiology technician.", "severity": "critical"},
    {"time": "06:45", "event": "Email servers compromised. Internal communication now limited to phone, in-person, and personal devices.", "severity": "critical"},
    {"time": "06:48", "event": "Nurse call system functioning but degraded — some units report delays.", "severity": "warning"},
    {"time": "06:50", "event": "Badge access system intermittent. Some restricted areas (pharmacy, server room) cannot be secured electronically.", "severity": "warning"},
    {"time": "06:55", "event": "07:00 shift change begins. 400+ day-shift staff arriving to a hospital in crisis. Most have no information yet.", "severity": "info"},
    {"time": "07:00", "event": "Hospital Incident Command System (HICS) activated by on-call administrator.", "severity": "info"},
    {"time": "07:05", "event": "ANSSI (national cyber agency) contacted. They estimate a forensics team can arrive in 6-8 hours.", "severity": "info"},
]

# Phase 1 additional decision: role-specific first actions
ROLE_FIRST_ACTIONS = {
    "Incident Commander (Hospital Administrator)": {
        "prompt": "You have just activated HICS. What are your first three directives?",
        "options": [
            "1) Lock down all network connections, 2) Convene leadership in the command center, 3) Authorize downtime procedures",
            "1) Contact ANSSI and cyber insurance, 2) Brief department heads by phone, 3) Postpone all elective procedures",
            "1) Authorize downtime procedures, 2) Contact the hospital board chair, 3) Prepare a staff-wide communication",
            "1) Convene leadership, 2) Request a full damage assessment from IT before any other action, 3) Contact legal counsel",
        ],
    },
    "Health Information Manager (HIM Director)": {
        "prompt": "Paper forms are locked in the HIM office. The HIM office does not open until 08:00. What do you do?",
        "options": [
            "Call the HIM on-call staff to open the office now and begin distributing paper form kits to every unit",
            "Direct nursing stations to use blank paper with standardized headers until forms arrive",
            "Pull the emergency downtime binder (if it exists) from the nursing supervisor's office and photocopy forms",
            "Focus first on the patient master index — print the last census from the backup server if accessible",
        ],
    },
    "Clinical Operations Lead (Chief Nursing Officer)": {
        "prompt": "You have 15 ICU patients on IV drips managed by smart pumps that just lost their drug library connection. What is your immediate action?",
        "options": [
            "Switch all pumps to manual mode with nurse-verified rates from the last known settings",
            "Call pharmacy to send a pharmacist to ICU immediately to verify every drip manually",
            "Pause all non-critical drips, maintain only life-sustaining infusions, and await pharmacy verification",
            "Ask ICU charge nurse to photograph current pump settings on every bed before any changes are made",
        ],
    },
    "IT Security & Informatics Lead": {
        "prompt": "You've confirmed ransomware on core servers. The EHR vendor is asking if they should attempt a remote connection to assess damage. What do you do?",
        "options": [
            "Deny remote access — isolate the network completely until forensics arrives",
            "Allow read-only access through a segmented connection to assess backup integrity",
            "Deny vendor access but ask them to prepare a clean restoration environment on standby",
            "Allow access — the vendor knows the system best and every hour of downtime costs patient safety",
        ],
    },
    "Communications & Compliance Officer": {
        "prompt": "It is 07:10. A local radio journalist calls the main hospital line asking about 'reports of a computer problem.' What do you do?",
        "options": [
            "Provide a brief holding statement: 'We are experiencing a technology disruption and patient care continues safely'",
            "Decline to comment — 'We have no information to share at this time'",
            "Redirect to a written statement that you will email within 2 hours (but email is down...)",
            "Provide full transparency: 'We are experiencing a ransomware attack and are working with national authorities'",
        ],
    },
}

# Phase 2 downtime injects
DOWNTIME_INJECTS = [
    {
        "id": "inject_med_error",
        "title": "Near-Miss Medication Event",
        "time": "Hour 4",
        "description": (
            "A nurse on the medical-surgical floor reports a near-miss: without barcode "
            "scanning, a patient with a similar name (MARTIN, Jean-Pierre vs. MARTIN, "
            "Jean-Paul) was almost given the wrong medication. The manual five-rights "
            "check caught it, but staff are shaken and requesting additional safety protocols."
        ),
        "question": "How does your team respond to prevent actual medication errors during downtime?",
        "options": [
            "Implement buddy-system double-checks for all medication administration",
            "Restrict medication dispensing to charge nurses only",
            "Deploy printed patient wristbands with photos from the last backup and add a third identifier",
            "Halt all non-emergency medication administration until a safety protocol is confirmed",
        ],
        "considerations": {
            "Incident Commander (Hospital Administrator)": "What are the liability implications if an actual error occurs? How do you communicate this near-miss to the board without causing panic?",
            "Health Information Manager (HIM Director)": "How do you track this near-miss event without an electronic incident reporting system? What paper form captures it?",
            "Clinical Operations Lead (Chief Nursing Officer)": "What staffing adjustments are needed for double-checks? Your nurses are already stretched. How does this affect morale?",
            "IT Security & Informatics Lead": "Can you recover the patient identification database independently of the full EHR? Is that data on a clean server?",
            "Communications & Compliance Officer": "Is this a reportable patient safety event under French healthcare regulations? What documentation is required?",
        },
    },
    {
        "id": "inject_ambulance",
        "title": "Ambulance Diversion Request",
        "time": "Hour 8",
        "description": (
            "The Emergency Department is overwhelmed. Without electronic triage tools, "
            "patient tracking boards, or access to prior medical histories, ED wait "
            "times have tripled. The ED Medical Director requests ambulance diversion "
            "to neighbouring hospitals. However, the nearest Level 1 trauma center is "
            "45 minutes away, and your hospital is the only facility with a neonatal "
            "ICU in the region."
        ),
        "question": "Do you approve ambulance diversion? What conditions do you set?",
        "options": [
            "Approve full diversion — redirect all incoming ambulances to nearby facilities",
            "Approve partial diversion — accept only life-threatening, trauma, cardiac, stroke, and obstetric emergencies",
            "Deny diversion — implement manual triage protocols and request additional staffing from the regional health authority (ARS)",
            "Approve temporary diversion (4 hours) while establishing manual tracking systems, then reassess",
        ],
        "considerations": {
            "Incident Commander (Hospital Administrator)": "Diversion affects regional emergency capacity. The ARS (regional health authority) must be notified. What is the reputational risk?",
            "Health Information Manager (HIM Director)": "How do you maintain records for ED patients without electronic registration? What about unidentified trauma patients?",
            "Clinical Operations Lead (Chief Nursing Officer)": "A pregnant woman at 36 weeks is in the ambulance right now. The nearest alternative maternity unit is 50 minutes away. What do you tell the paramedics?",
            "IT Security & Informatics Lead": "Can you stand up an isolated laptop with a spreadsheet for basic ED patient tracking? What is the security risk?",
            "Communications & Compliance Officer": "How do you communicate diversion to the public without revealing the cyber attack as the cause? Or do you disclose?",
        },
    },
    {
        "id": "inject_shift_handoff",
        "title": "The 19:00 Shift Handoff",
        "time": "Hour 13",
        "description": (
            "The evening shift is arriving. Day-shift staff have been managing the crisis "
            "for 13 hours — many since before the 07:00 shift change. Evening staff have "
            "received minimal information. You must hand off:\n"
            "- Current patient status for 287 inpatients (all on paper)\n"
            "- Active downtime procedures and which workflows are in place\n"
            "- Outstanding issues (the medication near-miss, ambulance diversion status)\n"
            "- Location of all paper records generated today\n"
            "- Emotional state of day-shift staff (several nurses are in tears)"
        ),
        "question": "How do you structure the shift handoff without any electronic tools?",
        "options": [
            "Unit-by-unit bedside handoff with both outgoing and incoming nurses at each patient, plus a centralized briefing from the charge nurse",
            "Centralized all-hands briefing in the cafeteria (15 minutes) followed by unit-level handoffs",
            "Written handoff packets prepared by each unit's charge nurse, supplemented by phone availability of day-shift staff for questions",
            "Staggered handoff: keep day-shift charge nurses for 2 extra hours to overlap with evening shift and mentor through paper processes",
        ],
        "considerations": {
            "Incident Commander (Hospital Administrator)": "Day-shift staff have been working 13+ hours in crisis mode. Keeping them longer is overtime and a fatigue risk. But losing institutional knowledge is dangerous.",
            "Health Information Manager (HIM Director)": "Every piece of paper generated today must be accounted for. How do you audit completeness during handoff? What about records that are 'in transit' between departments?",
            "Clinical Operations Lead (Chief Nursing Officer)": "Evening staff have never used these paper forms. They need training AND a handoff. You have maybe 30 minutes. What do you prioritize?",
            "IT Security & Informatics Lead": "You need to brief the evening IT skeleton crew. They need to monitor for reinfection, maintain network isolation, and prepare for the ANSSI forensics team arriving overnight.",
            "Communications & Compliance Officer": "Evening staff will have questions. Some may post on social media. How do you get ahead of that? What talking points do you provide?",
        },
    },
    {
        "id": "inject_data_backlog",
        "title": "Paper Records Crisis",
        "time": "Hour 18",
        "description": (
            "After 18 hours of downtime, the HIM department estimates 3,200 pages of "
            "handwritten clinical notes, medication records, lab orders, and nursing "
            "assessments have accumulated across the hospital. A quality audit of a "
            "sample of 50 paper records reveals:\n"
            "- 34% are missing the patient's date of birth\n"
            "- 22% have no allergies documented (blank — not 'NKDA')\n"
            "- 18% have illegible handwriting in at least one section\n"
            "- 11% cannot be matched to a specific patient with certainty\n"
            "- 4 records appear to be duplicates for the same patient\n\n"
            "An overnight back-entry team will need to reconcile everything once "
            "systems are restored — if they can read it."
        ),
        "question": "How do you manage the growing paper backlog while maintaining data integrity?",
        "options": [
            "Designate a centralized paper records staging area with HIM staff organizing, stamping, and auditing in real-time",
            "Prioritize critical documentation only (medications, allergies, vitals) — issue a directive to defer progress notes",
            "Deploy HIM students/staff to each unit as embedded scribes to improve real-time documentation quality",
            "Begin photographing paper records with a dedicated hospital camera (not personal phones) for digital backup",
        ],
        "considerations": {
            "Incident Commander (Hospital Administrator)": "The back-entry effort will cost an estimated €45,000-€80,000 in overtime and temporary staff. Where does this money come from?",
            "Health Information Manager (HIM Director)": "11% of records cannot be matched to a patient. That means ~350 clinical documents are 'orphaned.' What is your reconciliation plan?",
            "Clinical Operations Lead (Chief Nursing Officer)": "Nursing staff are documenting for patient safety, not for coding. If you ask them to add identifiers and improve legibility, that takes time away from patient care.",
            "IT Security & Informatics Lead": "When systems come back, what is the data entry workflow? Can you create a simplified intake interface? How long before normal EHR workflows resume?",
            "Communications & Compliance Officer": "Photographing patient records — even on a hospital camera — creates a secondary data store. What are the GDPR implications?",
        },
    },
]

# Phase 4: Escalation & Stakeholder Pressure injects
ESCALATION_INJECTS = [
    {
        "id": "inject_media_story",
        "title": "The Story Breaks",
        "time": "Hour 26",
        "type": "media",
        "description": "A local television station runs a story at noon.",
        "content": (
            '<div class="news-ticker">'
            "<strong>BREAKING — France 3 Auvergne-Rhone-Alpes</strong><br><br>"
            '"Centre Hospitalier Sainte-Claire has been operating without its computer '
            "systems for over 24 hours following what sources describe as a "
            "'major cyberattack.' Ambulances have been diverted from the hospital's "
            "emergency department since yesterday morning. A hospital spokesperson "
            "confirmed a 'technology disruption' but declined to provide details. "
            "Patient advocacy groups are demanding transparency. The regional health "
            'authority (ARS) says it is \'monitoring the situation.\'"'
            "</div>"
        ),
        "question": "The hospital's phone lines are now receiving calls from patients, families, and other media outlets. How do you respond?",
        "options": [
            "Hold a press conference within 2 hours — control the narrative with transparency",
            "Issue a written press release only — no live questions, no press conference",
            "Provide an updated holding statement and schedule a press conference for tomorrow when you have more information",
            "Go fully transparent: post a detailed update on the hospital website (once IT can bring up a static page) and social media",
        ],
    },
    {
        "id": "inject_family_confrontation",
        "title": "A Family Demands Answers",
        "time": "Hour 28",
        "type": "stakeholder",
        "description": "",
        "content": (
            '<div class="voicemail-box">'
            "<strong>Scene: Hospital Main Lobby</strong><br><br>"
            "A man approaches the information desk. He is visibly upset. His mother, "
            "82 years old, was admitted three days ago for pneumonia. He has been unable "
            "to reach anyone by phone. The patient portal is down. He drove 90 minutes "
            "to get here.<br><br>"
            '"I cannot access my mother\'s records. I don\'t know what medications she\'s '
            "on. The nurse told me they are using PAPER. Paper! What year is this? "
            'I want to know if my mother\'s personal information has been stolen. '
            "I want to speak to whoever is in charge. And if I don't get answers, "
            'I am calling my lawyer and the press."'
            "</div>"
        ),
        "question": "How do you handle this family member? Who responds, and what do they say?",
        "options": [
            "The Incident Commander meets with him personally, acknowledges the situation, and provides a factual but limited briefing",
            "The Communications Officer meets him with a prepared family information sheet and a direct phone number for updates",
            "The Clinical Operations Lead (CNO) walks him to his mother's bedside, introduces the care team, and addresses clinical concerns directly",
            "A patient advocate escorts him to a private room, provides a written FAQ, and schedules a follow-up call with administration",
        ],
    },
    {
        "id": "inject_staff_revolt",
        "title": "Staff Morale Crisis",
        "time": "Hour 32",
        "type": "internal",
        "description": "",
        "content": (
            '<div class="voicemail-box">'
            "<strong>Voicemail from the Day Shift Charge Nurse, Medical-Surgical Unit 3B</strong><br><br>"
            '"This is Marie-Claire on 3B. I need to tell you that my nurses are done. '
            "We have been working 14-hour shifts on paper for two days. Three of my "
            "nurses called in sick today — I think they're not actually sick, they just "
            "can't take it anymore. The ones who are here are making mistakes. "
            "Small ones so far. But I'm scared. We had another near-miss today — wrong "
            "dose calculated by hand because we don't have the EHR doing the math for us. "
            "I need more staff, I need someone to acknowledge what we're going through, "
            'and I need to know when this is going to end. Please call me back."'
            "</div>"
        ),
        "question": "Staff burnout is becoming a patient safety issue. What is your immediate response?",
        "options": [
            "Activate mutual aid: request temporary nursing staff from neighbouring hospitals through the ARS emergency protocol",
            "Reduce patient census: begin transferring stable patients to partner facilities to lighten the workload",
            "Deploy crisis support: bring in a critical incident stress management (CISM) team and provide mental health resources",
            "All of the above, plus: shorten shifts to 8 hours (accepting that you need 3 shifts instead of 2 per day), provide meals and rest areas",
        ],
    },
    {
        "id": "inject_social_media",
        "title": "Social Media Firestorm",
        "time": "Hour 34",
        "type": "media",
        "description": "Multiple social media posts are circulating.",
        "content": (
            '<div class="social-media-post">'
            "<strong>@HealthWatchFR</strong> (12,400 followers)<br>"
            '"THREAD: My aunt is a nurse at Sainte-Claire. She says they\'ve been '
            "writing EVERYTHING by hand for 2 days. No access to patient histories. "
            "No medication barcodes. She's terrified of making an error. This is a "
            'patient safety EMERGENCY and no one is talking about it. 1/7"'
            "</div>"
            '<div class="social-media-post">'
            "<strong>@PatientRightsFR</strong> (34,200 followers)<br>"
            '"If Centre Hospitalier Sainte-Claire has had 180,000 patient records '
            "stolen, where is the CNIL notification? Where is the patient notification? "
            "GDPR requires transparency. Silence is not acceptable. "
            '#DataBreach #GDPR #SanteNumerique"'
            "</div>"
            '<div class="social-media-post">'
            "<strong>Dr. Laurent M.</strong> (verified physician, not affiliated)<br>"
            '"The Sainte-Claire situation is exactly what we\'ve been warning about. '
            "French hospitals are chronically under-invested in cybersecurity. The "
            'average hospital IT security budget is a fraction of what it should be. '
            'This will happen again. And next time, patients may die."'
            "</div>"
        ),
        "question": "Social media is shaping the public narrative. What is your response strategy?",
        "options": [
            "Post an official hospital statement on social media: factual, empathetic, and transparent about what you know",
            "Do not engage on social media — respond only through official channels (press releases, hospital website)",
            "Identify the nurse's relative post and ask the employee (through HR) to remove it, as it may violate confidentiality policies",
            "Engage a professional crisis communications firm (your insurance may cover this) to manage the social media response",
        ],
    },
    {
        "id": "inject_department_conflict",
        "title": "Inter-Department Conflict",
        "time": "Hour 36",
        "type": "internal",
        "description": "",
        "content": (
            '<div class="voicemail-box">'
            "<strong>Scene: Incident Command Center</strong><br><br>"
            "The Chief of Surgery and the HIM Director are in a heated argument. "
            "Surgery wants to resume elective procedures tomorrow morning — they have "
            "patients who have been waiting and are at medical risk from delay. The HIM "
            "Director insists that without electronic surgical checklists, specimen "
            "labeling systems, and proper consent documentation workflows, resuming "
            "surgery on paper is an unacceptable risk to patient safety and regulatory "
            "compliance.<br><br>"
            "The Chief of Surgery says: <em>'We operated for decades before computers. "
            "I am not letting a computer problem endanger my patients by delaying their "
            "care.'</em><br><br>"
            "The HIM Director responds: <em>'And we had higher error rates for decades "
            "before computers. We are not going backward. Every mislabeled specimen is "
            "a potential catastrophe.'</em>"
            "</div>"
        ),
        "question": "How do you resolve this conflict?",
        "options": [
            "Side with surgery: resume elective cases with enhanced manual safety protocols (dedicated surgical safety officer in each OR)",
            "Side with HIM: delay elective surgery until at least basic electronic surgical safety systems are restored",
            "Compromise: resume only low-risk, short-duration elective procedures with dedicated HIM staff in the OR; defer complex cases",
            "Convene an emergency clinical governance meeting with surgery, HIM, nursing, and anesthesia to develop consensus criteria",
        ],
    },
]

# Phase 5: Critical Decisions
CRITICAL_INJECTS = [
    {
        "id": "inject_ransom",
        "title": "The Ransom Demand",
        "time": "Hour 50",
        "description": (
            "The attackers have made formal contact through an encrypted channel. "
            "Their demands:\n\n"
            "- **€2.5 million** in cryptocurrency within 48 hours\n"
            "- They claim to have exfiltrated **180,000 patient records** including "
            "diagnoses, medications, national identification numbers (NIR), and "
            "in some cases, mental health and HIV status records\n"
            "- They provide a sample of 500 records as 'proof' — your IT team confirms "
            "these are genuine\n"
            "- They threaten to **publish all data on the dark web** if payment is not received\n"
            "- They offer a 'discount' to €1.8 million if you pay within 24 hours\n\n"
            "**Your cyber insurance** policy has a **€1 million ransomware coverage limit**.\n\n"
            "**ANSSI** (France's national cybersecurity agency) officially advises against "
            "paying: *'Payment does not guarantee data deletion, funds criminal "
            "enterprises, and makes you a target for future attacks.'*\n\n"
            "**Your legal counsel** notes that under French law, paying a ransom is "
            "not illegal, but insurance reimbursement for ransom payments requires "
            "a police report filed within 72 hours of payment (Loi LOPMI, 2023)."
        ),
        "question": "What is your recommendation to the hospital board?",
        "options": [
            "Do not pay — follow ANSSI guidance, focus on restoration from backups, accept the data exposure risk",
            "Negotiate through a professional ransomware negotiator (covered by insurance) — try to reduce the price and confirm data deletion",
            "Pay the reduced amount (€1.8M) immediately — the exposure of mental health and HIV records would be catastrophic for patients",
            "Escalate to the Ministry of Health — request emergency government intervention and defer the decision",
        ],
        "follow_up": (
            "Regardless of your choice, discuss as a team: **What are the ethical "
            "dimensions of this decision?** Consider: Is it ethical to use hospital "
            "funds to pay criminals? Is it ethical NOT to pay if patient data will be "
            "exposed? Who bears the harm in each scenario?"
        ),
    },
    {
        "id": "inject_gdpr",
        "title": "GDPR 72-Hour Notification Deadline",
        "time": "Hour 58",
        "description": (
            "Under **GDPR Article 33**, you must notify the **CNIL** (French data "
            "protection authority) within 72 hours of becoming aware of a personal "
            "data breach. The clock started when the breach was confirmed at **06:40 "
            "on Day 1**. You are now at **hour 58**. You have **14 hours remaining**.\n\n"
            "The forensics team has established:\n"
            "- Attackers had network access for **11 days** before encryption\n"
            "- During that time, **large data transfers** occurred to external servers\n"
            "- They cannot yet confirm the exact number of records exfiltrated\n"
            "- The 500-record sample provided by attackers is confirmed genuine\n"
            "- The breach likely includes: patient demographics, diagnoses, "
            "medications, lab results, and for some patients, mental health records\n\n"
            "**GDPR Article 34** requires notifying affected individuals 'without "
            "undue delay' if the breach is likely to result in a 'high risk to the "
            "rights and freedoms' of those individuals."
        ),
        "question": "How do you handle the GDPR notification with incomplete information?",
        "options": [
            "File an initial notification to CNIL NOW with what you know, clearly marking it as preliminary, and supplement as forensics progresses",
            "Wait until the 72-hour mark, file the most complete report possible, and request an extension for supplementary details",
            "File the CNIL notification AND begin notifying all 180,000 potentially affected patients simultaneously via postal mail",
            "File the CNIL notification now and notify only the patients whose records appeared in the attacker's 500-record proof sample",
        ],
        "follow_up": (
            "Discuss: **How do you notify 180,000 patients that their health data "
            "may have been stolen?** Consider literacy levels, elderly patients, "
            "patients with mental health records who may face stigma, patients in "
            "domestic violence situations whose address is now potentially exposed."
        ),
    },
    {
        "id": "inject_partial_restore",
        "title": "System Restoration Strategy",
        "time": "Hour 64",
        "description": (
            "The IT team presents three restoration options to the Incident Commander:\n\n"
            "**Option A: Restore from Backup (48 hours old)**\n"
            "- EHR can be operational in 12-18 hours\n"
            "- Loses 48 hours of pre-breach data + all downtime data (on paper)\n"
            "- Backup integrity verified — clean of malware\n"
            "- Back-entry of paper records estimated at 3-4 weeks\n\n"
            "**Option B: Decrypt and Clean Current Systems**\n"
            "- Could take 5-10 additional days\n"
            "- Preserves all pre-breach data\n"
            "- Risk of residual malware: estimated 15-20% chance of reinfection\n"
            "- Forensics team recommends against this option\n\n"
            "**Option C: New Clean Instance**\n"
            "- Fresh EHR installation on new hardware\n"
            "- Operational in 24-36 hours\n"
            "- Requires manual entry of ALL active patient data\n"
            "- Historical data available only after Option A backup is loaded later\n"
            "- Most secure option — zero reinfection risk\n\n"
            "**Option D: Hybrid Phased Approach**\n"
            "- Phase 1 (24h): Stand up Option C for active inpatients only\n"
            "- Phase 2 (1 week): Restore Option A backup in parallel environment\n"
            "- Phase 3 (2-4 weeks): Merge, reconcile, and back-enter paper records\n"
            "- Most complex, but balances speed, data preservation, and security"
        ),
        "question": "Which restoration strategy do you recommend?",
        "options": [
            "Option A: Restore 48-hour backup — fastest return to electronic operations, accept the data gap",
            "Option B: Decrypt and clean — preserve data, accept extended downtime and reinfection risk",
            "Option C: New clean instance — most secure, accept massive data entry effort",
            "Option D: Hybrid phased approach — most complex but most balanced",
        ],
        "follow_up": (
            "Discuss: **Who decides the restoration strategy?** Is this a technical "
            "decision (IT), a clinical decision (patient safety), a financial decision "
            "(administration), or a data integrity decision (HIM)? How do you weigh "
            "these competing priorities?"
        ),
    },
]

# Phase 2 workflow areas
WORKFLOW_AREAS = {
    "Medication Administration": {
        "normal": "Barcode scan → EHR allergy check → Smart pump drug library → Electronic MAR documentation",
        "downtime_options": [
            "Manual five-rights check with buddy system + paper MAR",
            "Charge nurse verifies all medications + paper MAR",
            "Pharmacist stationed on each floor verifies + paper MAR",
            "Limit to pre-packaged unit-dose medications only + paper MAR",
        ],
        "risk_note": "Without barcode scanning, medication error rates increase 2-5x. The buddy system adds safety but halves throughput.",
    },
    "Patient Identification": {
        "normal": "Barcode wristband scan → EHR photo verification → Electronic allergy/alert display",
        "downtime_options": [
            "Verbal two-identifier check (name + DOB) + paper allergy bands",
            "Handwritten wristbands from last printed census + verbal verification",
            "Photo ID from admission (if available in paper chart) + verbal verification",
            "Color-coded paper wristbands by unit + two-identifier verbal check",
        ],
        "risk_note": "Similar names (MARTIN, Jean-Pierre vs. MARTIN, Jean-Paul) are a known risk. The hospital has 14 patients named Martin.",
    },
    "Lab Orders & Results": {
        "normal": "Electronic CPOE → LIS processing → Results auto-populate in EHR → Critical value alerts",
        "downtime_options": [
            "Paper requisition forms → Phone results to ordering provider → Provider documents on paper",
            "Paper requisition forms → Fax results to unit (if fax is operational)",
            "Paper requisition → Runner delivers printed results to unit",
            "Limit to STAT/critical labs only until systems restore",
        ],
        "risk_note": "Without electronic critical value alerts, abnormal results may sit unreviewed. A missed critical potassium level can be fatal.",
    },
    "Patient Tracking & Bed Management": {
        "normal": "Electronic bed board → Automated ADT notifications → Real-time census → Discharge planning",
        "downtime_options": [
            "Whiteboard tracking at each nursing station + hourly phone updates to admitting",
            "Central paper bed board in the command center + runners for updates",
            "Charge nurse maintains paper census + calls admitting for every change",
            "Designate one person per unit as 'bed tracker' with dedicated phone line",
        ],
        "risk_note": "Without real-time tracking, bed turnover slows. This directly affects ED boarding, surgical scheduling, and ambulance diversion.",
    },
    "Surgical Services": {
        "normal": "Electronic consent → EHR surgical checklist → Automated specimen labeling → Electronic op notes",
        "downtime_options": [
            "Paper consent forms + manual surgical safety checklist + handwritten specimen labels",
            "Emergency-only operations with full manual documentation protocol",
            "Paper-based with dedicated surgical HIM clerk in the OR for real-time documentation support",
            "Pre-printed surgical packets for common procedures + manual documentation",
        ],
        "risk_note": "Mislabeled surgical specimens can lead to wrong-site surgery or incorrect pathology results. This is a 'never event.'",
    },
    "Radiology & Imaging": {
        "normal": "Electronic order → PACS image capture → Radiologist reads on screen → Report auto-populates in EHR",
        "downtime_options": [
            "Paper orders only → Images captured but stored locally on modality → Radiologist reads on modality screen → Paper report dictated and faxed",
            "Portable X-ray and ultrasound only (CT/MRI offline) → Paper reports delivered by runner",
            "Emergency imaging only → Results communicated by phone directly to ordering physician",
            "Redirect non-emergency imaging to a partner facility with functioning PACS",
        ],
        "risk_note": "Without PACS, prior imaging comparisons are impossible. A radiologist reading a chest X-ray cannot see the one from last week.",
    },
    "Pharmacy & Formulary": {
        "normal": "Electronic prescribing → Automated drug interaction check → Robotic dispensing → Barcode verification",
        "downtime_options": [
            "Paper prescriptions → Manual pharmacist review for interactions → Manual cabinet override → Paper dispensing log",
            "Pharmacists stationed on each floor for real-time order verification and dispensing from floor stock",
            "Restrict formulary to a pre-approved downtime medication list (50 most common drugs) to simplify manual checking",
            "Transfer all high-risk medications (chemotherapy, anticoagulants, insulin) to pharmacy-only dispensing with direct delivery",
        ],
        "risk_note": "Without automated drug interaction checking, the pharmacist is the last safety net. A single pharmacist cannot review 400+ orders manually at the same speed.",
    },
}

# Communication audiences and templates
COMM_AUDIENCES = {
    "All Hospital Staff (Internal)": {
        "channels": ["PA Announcement", "Printed Bulletin", "Text/SMS", "In-Person Briefing"],
        "template": (
            "Suggested elements: Current situation status, which systems are affected, "
            "what staff should do RIGHT NOW, where to get paper forms, who to contact "
            "with questions, next scheduled update time, acknowledgment of staff effort."
        ),
    },
    "Patients & Families Currently in Hospital": {
        "channels": ["Printed Bulletin", "In-Person Briefing", "Written Letter"],
        "template": (
            "Suggested elements: Reassurance of safety, plain-language explanation "
            "(no jargon), what this means for their care today, how to reach their "
            "care team, what you are doing to protect their personal information."
        ),
    },
    "Outpatients with Upcoming Appointments": {
        "channels": ["Phone Tree", "Text/SMS", "Social Media Post", "Written Letter"],
        "template": (
            "Suggested elements: Appointment status (canceled/rescheduled?), how to "
            "reschedule, medication refill instructions, emergency contact number, "
            "when to expect systems to return."
        ),
    },
    "Media / Press Inquiry": {
        "channels": ["Written Statement", "Press Conference", "Social Media Post"],
        "template": (
            "Suggested elements: Brief factual statement, patient safety emphasis, "
            "cooperation with authorities (ANSSI, police), commitment to transparency, "
            "NO technical details about the attack vector or ransom. Remember: "
            "anything you say may be quoted."
        ),
    },
    "CNIL / Regulatory Authority (GDPR)": {
        "channels": ["Formal Report", "Secure Portal Submission"],
        "template": (
            "Required elements (GDPR Art. 33): Nature of the breach, categories and "
            "approximate number of data subjects affected, categories of personal data "
            "records concerned, name and contact of DPO, likely consequences, measures "
            "taken or proposed to address the breach."
        ),
    },
    "Hospital Board of Directors": {
        "channels": ["Written Report", "Emergency Board Call", "In-Person Briefing"],
        "template": (
            "Suggested elements: Full situation briefing with timeline, financial "
            "impact estimate (current and projected), legal exposure assessment, "
            "insurance coverage status, recovery timeline and options, strategic "
            "decisions requiring board authorization (ransom, public disclosure level)."
        ),
    },
    "Regional Health Authority (ARS)": {
        "channels": ["Formal Report", "Phone Call", "Written Letter"],
        "template": (
            "Suggested elements: Nature and scope of operational disruption, impact "
            "on emergency services and patient capacity, mutual aid requests (staffing, "
            "patient transfers), ambulance diversion status, estimated recovery timeline."
        ),
    },
}

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
DEFAULTS = {
    "current_phase": 0,
    "team_name": "",
    "team_role": "Not Selected",
    "decisions_log": [],
    "phase_unlocked": [True] + [False] * (NUM_PHASES - 1),
    "systems_status": {
        "EHR (DPI)": "Operational", "Lab System (LIS)": "Operational",
        "Radiology (PACS)": "Operational", "Pharmacy": "Operational",
        "Patient Portal": "Operational", "Email": "Operational",
        "Scheduling": "Operational", "Billing/Revenue Cycle": "Operational",
        "Nurse Call System": "Operational", "Badge Access": "Operational",
    },
    "manual_entries": [],
    "communication_log": [],
    "sim_started": False,
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val if not isinstance(val, (list, dict)) else type(val)(val)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def update_systems_breach():
    st.session_state.systems_status = {
        "EHR (DPI)": "Down", "Lab System (LIS)": "Down",
        "Radiology (PACS)": "Down", "Pharmacy": "Down",
        "Patient Portal": "Down", "Email": "Down",
        "Scheduling": "Down", "Billing/Revenue Cycle": "Down",
        "Nurse Call System": "Degraded", "Badge Access": "Degraded",
    }

def update_systems_day2():
    st.session_state.systems_status = {
        "EHR (DPI)": "Down", "Lab System (LIS)": "Down",
        "Radiology (PACS)": "Down", "Pharmacy": "Down",
        "Patient Portal": "Down", "Email": "Down",
        "Scheduling": "Down", "Billing/Revenue Cycle": "Down",
        "Nurse Call System": "Operational", "Badge Access": "Operational",
    }

def update_systems_day3():
    st.session_state.systems_status = {
        "EHR (DPI)": "Down", "Lab System (LIS)": "Down",
        "Radiology (PACS)": "Down", "Pharmacy": "Down",
        "Patient Portal": "Down", "Email": "Degraded",
        "Scheduling": "Down", "Billing/Revenue Cycle": "Down",
        "Nurse Call System": "Operational", "Badge Access": "Operational",
    }

def update_systems_recovery():
    st.session_state.systems_status = {
        "EHR (DPI)": "Degraded", "Lab System (LIS)": "Degraded",
        "Radiology (PACS)": "Down", "Pharmacy": "Degraded",
        "Patient Portal": "Down", "Email": "Operational",
        "Scheduling": "Degraded", "Billing/Revenue Cycle": "Down",
        "Nurse Call System": "Operational", "Badge Access": "Operational",
    }

def get_status_color(status):
    return {"Operational": "#66bb6a", "Degraded": "#ffa726", "Down": "#ff4b4b"}.get(status, "#999")

def render_systems_dashboard():
    st.subheader("Hospital Systems Status")
    cols = st.columns(5)
    for i, (system, status) in enumerate(st.session_state.systems_status.items()):
        col = cols[i % 5]
        color = get_status_color(status)
        col.markdown(
            f'<div style="background-color:{color};color:white;padding:12px;'
            f'border-radius:8px;text-align:center;margin:4px 0;font-size:0.85em;">'
            f"<strong>{system}</strong><br>{status}</div>",
            unsafe_allow_html=True,
        )

def log_decision(phase, context, choice, justification=""):
    st.session_state.decisions_log.append({
        "phase": phase, "context": context, "choice": choice,
        "justification": justification,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })

def render_decision_log():
    if not st.session_state.decisions_log:
        st.info("No decisions recorded yet.")
        return
    for i, d in enumerate(st.session_state.decisions_log, 1):
        with st.expander(f"Decision {i}: {d['context']}", expanded=False):
            st.write(f"**Phase:** {d['phase']}")
            st.write(f"**Choice:** {d['choice']}")
            if d["justification"]:
                st.write(f"**Justification:** {d['justification']}")

def advance_phase():
    nxt = st.session_state.current_phase + 1
    if nxt < NUM_PHASES:
        st.session_state.current_phase = nxt
        st.session_state.phase_unlocked[nxt] = True
        st.rerun()

# ---------------------------------------------------------------------------
# PHASE 0 — Setup & Orientation (15 min)
# ---------------------------------------------------------------------------
def render_phase_0():
    st.markdown('<h2 class="phase-header">Phase 0: Setup & Orientation</h2>', unsafe_allow_html=True)
    st.caption("Estimated time: 15 minutes")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {HOSPITAL_NAME}")
        st.markdown(HOSPITAL_DESC)
        st.markdown("### The Scenario")
        st.markdown(
            "It is **Monday, 06:12 AM**. Your team is the hospital's senior "
            "leadership crisis response team. In moments, you will receive reports "
            "of system anomalies that will escalate into a full-scale ransomware "
            "attack.\n\n"
            "Over the next **3 hours of simulation time** (representing **72+ hours** "
            "of hospital time), you will manage the crisis from your assigned role's "
            "perspective. There will be a **20-minute break** at the midpoint. A "
            "**2-hour debrief** will follow the simulation."
        )
        st.markdown("### Simulation Timeline")
        timeline_data = []
        for p in PHASES:
            timeline_data.append({"Phase": p["name"], "Duration": p["time"],
                                  "Simulated Time": p["sim_hours"], "Description": p["description"]})
        st.dataframe(pd.DataFrame(timeline_data), use_container_width=True, hide_index=True)

        st.markdown("### Your Objectives")
        st.markdown("""
1. **Protect patient safety** above all else
2. **Maintain hospital operations** using downtime procedures
3. **Manage communication** to staff, patients, regulators, and the public
4. **Make defensible decisions** about ransom, recovery, and compliance
5. **Navigate stakeholder pressure** from media, families, staff, and regulators
6. **Document your reasoning** — you will debrief and reflect afterward
        """)

        st.markdown("### Simulation Rules")
        st.markdown("""
1. **Stay in your role.** Advocate from your role's perspective, even if you personally disagree.
2. **There are no perfect answers.** Every decision involves trade-offs. Make deliberate, justified choices.
3. **Respond to inject events as a team.** When new information arrives, pause and address it together.
4. **Document your decisions and reasoning.** Use the app to record choices and justifications.
5. **Time pressure is intentional.** You will not have enough time. That is realistic.
6. **The crisis evolves.** Your earlier decisions will shape later scenarios.
        """)

    with col2:
        st.markdown("### Team Setup")
        team = st.text_input("Team Name", value=st.session_state.team_name, key="team_name_input")
        if team:
            st.session_state.team_name = team

        st.markdown("### Select Your Role")
        role = st.selectbox(
            "Your individual role:",
            ["Not Selected"] + list(ROLES.keys()),
            index=(["Not Selected"] + list(ROLES.keys())).index(st.session_state.team_role),
            key="role_select",
        )
        st.session_state.team_role = role

        if role != "Not Selected":
            r = ROLES[role]
            st.markdown(f"### {r['icon']} Your Role")
            st.markdown(f"**Focus:** {r['focus']}")
            st.markdown(f"**Background:** {r['background']}")
            st.markdown("**Your key tasks during this crisis:**")
            for t in r["tasks"]:
                st.markdown(f"- {t}")
            st.markdown("---")
            st.markdown("#### Your Role Briefing")
            st.markdown(f"*{r['briefing']}*")

    st.markdown("---")
    st.markdown("### All Roles in This Simulation")
    role_cols = st.columns(len(ROLES))
    for i, (rname, rinfo) in enumerate(ROLES.items()):
        with role_cols[i]:
            st.markdown(
                f'<div style="border:2px solid {rinfo["color"]};border-radius:10px;'
                f'padding:12px;text-align:center;min-height:200px;">'
                f'<span style="font-size:2em;">{rinfo["icon"]}</span><br>'
                f'<strong style="font-size:0.82em;">{rname}</strong><br>'
                f'<em style="font-size:0.75em;">{rinfo["background"]}</em><br>'
                f'<span style="font-size:0.72em;color:#888;">{rinfo["focus"]}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Pre-Breach Systems Status")
    render_systems_dashboard()

    st.markdown("---")
    if st.session_state.team_name and st.session_state.team_role != "Not Selected":
        if st.button("Begin Simulation — The Breach Starts Now", type="primary", use_container_width=True):
            st.session_state.sim_started = True
            update_systems_breach()
            advance_phase()
    else:
        st.warning("Enter your team name and select a role to begin.")


# ---------------------------------------------------------------------------
# PHASE 1 — The Breach (25 min)
# ---------------------------------------------------------------------------
def render_phase_1():
    st.markdown('<h2 class="phase-header">Phase 1: The Breach (Hour 0–2)</h2>', unsafe_allow_html=True)
    st.caption("Estimated time: 25 minutes | Simulated time: 06:12 – 08:00")

    st.markdown(
        '<div class="alert-critical">ALERT: CYBERSECURITY INCIDENT IN PROGRESS — '
        "HOSPITAL INCIDENT COMMAND ACTIVATED</div>",
        unsafe_allow_html=True,
    )

    render_systems_dashboard()

    # --- Incident Timeline ---
    st.markdown("---")
    st.markdown("### Incident Timeline")
    st.markdown("*Read aloud as a team. Each event arrives in real time.*")

    for evt in BREACH_EVENTS:
        icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}[evt["severity"]]
        st.markdown(f"{icon} **{evt['time']}** — {evt['event']}")

    # --- Role-Specific First Action ---
    st.markdown("---")
    st.markdown("### Role-Specific First Action")
    st.markdown(
        "Before the team discusses together, each role has an **immediate, "
        "role-specific decision** to make. Answer from YOUR role's perspective."
    )

    role = st.session_state.team_role
    if role in ROLE_FIRST_ACTIONS:
        action = ROLE_FIRST_ACTIONS[role]
        st.markdown(f"#### {ROLES[role]['icon']} {role}")
        response = st.radio(action["prompt"], action["options"], key="role_first_action", index=None)
        st.text_area("Your reasoning:", key="role_first_action_just", height=80)

    # --- Team Decisions ---
    st.markdown("---")
    st.markdown("### Team Decisions")
    st.markdown("*Now discuss as a full team. Each person advocates from their role.*")

    st.markdown("---")
    st.markdown("#### Decision 1: First 15 Minutes — Dual Priorities")
    st.markdown(
        "The EHR is down. Pharmacy cabinets are locked. Lab results cannot be "
        "transmitted electronically. You have patients who need medications "
        "**right now**. But the ransomware may still be spreading."
    )
    st.radio(
        "What is your FIRST priority action?",
        [
            "Activate downtime procedures immediately — distribute paper forms and medication reference sheets while IT contains the breach in parallel",
            "Focus on network isolation first — prevent further spread before activating downtime (accept 30-60 min additional delay for clinical operations)",
            "Split the team: IT isolates the network while clinical leadership activates downtime simultaneously — accept coordination complexity",
            "Convene a 10-minute emergency leadership huddle before any action — align on priorities, then execute",
        ],
        key="d1_breach", index=None,
    )
    st.text_area("Team justification:", key="d1_justify", height=80)

    st.markdown("---")
    st.markdown("#### Decision 2: Communication Under Fire")
    st.markdown(
        "Email is down. The phone system is overwhelmed. 400+ day-shift staff "
        "are arriving for the 07:00 shift change. Most have no information. "
        "Rumors are already spreading via personal phones."
    )
    st.radio(
        "How do you communicate to staff?",
        [
            "Overhead PA announcement with instructions to report to unit charge nurses for briefing",
            "Runners with printed bulletins to every unit and department (takes 20-30 min to reach everyone)",
            "Mass text via personal cell phones (WhatsApp/SMS) — fast but informal and potentially insecure",
            "Hold arriving day-shift staff at main entrances for a 5-minute all-hands verbal briefing before they enter units",
        ],
        key="d2_comm", index=None,
    )
    st.text_area("Team justification:", key="d2_justify", height=80)

    st.markdown("---")
    st.markdown("#### Decision 3: Patient Safety — The Critical First Hour")
    st.markdown(
        "There are **287 inpatients**. **42** are in the ICU. **15** are on IV "
        "medication drips managed by smart pumps linked to the pharmacy system "
        "(now offline). **8 women** are in active labor or post-partum in the "
        "maternity unit. **12 surgeries** are scheduled for the next 2 hours."
    )
    st.radio(
        "What is your patient safety strategy?",
        [
            "Cancel all elective surgeries; continue only emergency/life-saving procedures with manual verification; maternity continues with midwife-led manual protocols",
            "Cancel ALL surgeries and halt new admissions until every clinical system is individually assessed for safety",
            "Proceed case-by-case: surgical team and anesthesia assess each scheduled patient individually; maternity continues; ICU on manual pump management",
            "Continue all procedures — clinical staff are trained professionals who can work without computers. Focus IT resources on restoring clinical systems first.",
        ],
        key="d3_safety", index=None,
    )
    st.text_area("Team justification:", key="d3_justify", height=80)

    st.markdown("---")
    st.markdown("#### Decision 4: External Notification — Who Do You Call First?")
    st.markdown(
        "ANSSI has been notified but cannot send a forensics team for 6-8 hours. "
        "You have not yet contacted the police, the ARS (regional health "
        "authority), your cyber insurance carrier, or the hospital board chair."
    )
    st.radio(
        "In what order do you contact external parties?",
        [
            "1) Cyber insurance (they provide forensics, legal, and crisis PR), 2) Police (required for insurance claim), 3) ARS, 4) Board chair",
            "1) Police (criminal investigation), 2) ARS (regulatory obligation), 3) Cyber insurance, 4) Board chair",
            "1) Board chair (governance obligation), 2) Cyber insurance, 3) ARS, 4) Police",
            "1) ARS (patient safety regulator, can authorize mutual aid), 2) Cyber insurance, 3) Police, 4) Board chair",
        ],
        key="d4_external", index=None,
    )
    st.text_area("Team justification:", key="d4_justify", height=80)

    st.markdown("---")
    if st.button("Lock in Phase 1 Decisions & Proceed to Downtime Operations", type="primary", use_container_width=True):
        # Log role-specific action
        if st.session_state.get("role_first_action"):
            log_decision("Phase 1: The Breach", f"Role First Action ({role})",
                         st.session_state["role_first_action"],
                         st.session_state.get("role_first_action_just", ""))
        for label, kc, kj in [
            ("First Priority Action", "d1_breach", "d1_justify"),
            ("Staff Communication", "d2_comm", "d2_justify"),
            ("Patient Safety Strategy", "d3_safety", "d3_justify"),
            ("External Notification Order", "d4_external", "d4_justify"),
        ]:
            c = st.session_state.get(kc)
            j = st.session_state.get(kj, "")
            if c:
                log_decision("Phase 1: The Breach", label, c, j)
        advance_phase()


# ---------------------------------------------------------------------------
# PHASE 2 — Downtime Operations (40 min)
# ---------------------------------------------------------------------------
def render_phase_2():
    st.markdown('<h2 class="phase-header">Phase 2: Downtime Operations (Hour 2–24)</h2>', unsafe_allow_html=True)
    st.caption("Estimated time: 40 minutes | Simulated time: 08:00 – 06:00 next day")

    st.markdown(
        '<div class="alert-warning">DOWNTIME PROCEDURES ACTIVE — ALL CLINICAL SYSTEMS OPERATING MANUALLY</div>',
        unsafe_allow_html=True,
    )
    render_systems_dashboard()
    st.markdown("---")

    tabs = st.tabs([
        "Manual Workflows",
        "Paper Records Simulator",
        "Communication Center",
        "Inject Events (4)",
    ])

    # --- Tab 1: Manual Workflows ---
    with tabs[0]:
        st.markdown("### Manual Workflow Conversion Board")
        st.markdown(
            "Without electronic systems, **every** clinical and administrative "
            "process must switch to a manual alternative. For each workflow area, "
            "review the normal electronic process, select your downtime procedure, "
            "and note the risk."
        )
        for area, info in WORKFLOW_AREAS.items():
            with st.expander(f"**{area}**", expanded=False):
                st.markdown("**Normal Electronic Process:**")
                st.code(info["normal"], language=None)
                st.warning(f"**Risk Note:** {info['risk_note']}")
                st.markdown("**Select your downtime procedure:**")
                st.radio(f"Approach for {area}:", info["downtime_options"],
                         key=f"wf_{area}", index=None, label_visibility="collapsed")
                st.text_input(f"Custom modifications or notes:", key=f"wf_notes_{area}")

    # --- Tab 2: Paper Records Simulator ---
    with tabs[1]:
        st.markdown("### Paper Records Simulation")
        st.markdown(
            "Experience the challenges of manual documentation. Enter at least "
            "**2 sample patient records** to understand what staff are dealing with."
        )

        st.markdown("#### Downtime Patient Documentation Form")
        with st.form("paper_form"):
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                pt_name = st.text_input("Patient Name (Last, First)")
                pt_dob = st.date_input("Date of Birth", value=datetime(1955, 3, 15))
                pt_mrn = st.text_input("MRN (if known — may not be available)")
                pt_room = st.text_input("Room / Bed Number")
                pt_allergies = st.text_area("Known Allergies (or write NKDA)", height=50)
                pt_code_status = st.selectbox("Code Status", ["Unknown", "Full Code", "DNR", "DNI", "Comfort Care Only"])
            with pcol2:
                pt_dx = st.text_input("Primary Diagnosis")
                pt_vitals = st.text_area("Current Vitals (manual entry)", height=50,
                                          placeholder="BP: ___/___ HR: ___ RR: ___ Temp: ___ SpO2: ___")
                pt_meds = st.text_area("Current Medications (from bedside MAR or memory)", height=70)
                pt_notes = st.text_area("Clinical Notes / Assessment", height=70)
                pt_nurse = st.text_input("Documenting Nurse (name)")
                pt_time = st.text_input("Time of Documentation", value=datetime.now().strftime("%H:%M"))

            submitted = st.form_submit_button("Submit Paper Record", type="primary")
            if submitted:
                fields = [pt_name, True, pt_mrn, pt_room, pt_allergies, pt_dx, pt_vitals, pt_meds, pt_nurse, pt_code_status != "Unknown"]
                completeness = sum(1 for v in fields if v) / len(fields) * 100
                record = {
                    "name": pt_name, "dob": str(pt_dob), "mrn": pt_mrn,
                    "room": pt_room, "allergies": pt_allergies, "dx": pt_dx,
                    "vitals": pt_vitals, "meds": pt_meds, "notes": pt_notes,
                    "nurse": pt_nurse, "code_status": pt_code_status,
                    "doc_time": pt_time,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "completeness": completeness,
                }
                st.session_state.manual_entries.append(record)
                st.success("Record submitted.")

        if st.session_state.manual_entries:
            st.markdown("#### Submitted Records")
            for i, rec in enumerate(st.session_state.manual_entries, 1):
                c = rec["completeness"]
                color = "#66bb6a" if c > 80 else "#ffa726" if c > 50 else "#ff4b4b"
                st.markdown(
                    f"**Record {i}** — {rec['name'] or 'UNNAMED'} | Room: {rec['room'] or '??'} "
                    f"| Code: {rec.get('code_status','?')} "
                    f"| Completeness: <span style='color:{color}'>{c:.0f}%</span>",
                    unsafe_allow_html=True,
                )
            avg = sum(r["completeness"] for r in st.session_state.manual_entries) / len(st.session_state.manual_entries)
            st.markdown(f"**Average Completeness: {avg:.0f}%**")
            if avg < 70:
                st.warning("Low completeness creates patient safety risks and back-entry nightmares.")

        st.markdown("---")
        st.markdown("#### Back-Entry Cost Estimator")
        bcol1, bcol2, bcol3 = st.columns(3)
        with bcol1:
            hours_down = st.number_input("Hours of downtime", 1, 168, 24)
        with bcol2:
            recs_per_hour = st.number_input("Paper records per hour", 10, 500, 100)
        with bcol3:
            entry_min = st.number_input("Minutes to back-enter one record", 1, 30, 8)

        total_recs = hours_down * recs_per_hour
        entry_hours = (total_recs * entry_min) / 60
        fte_days = entry_hours / 8
        cost = fte_days * 8 * 35

        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Total Paper Records", f"{total_recs:,}")
        mcol2.metric("Back-Entry Hours", f"{entry_hours:,.0f}")
        mcol3.metric("Staff-Days Needed", f"{fte_days:,.0f}")
        mcol4.metric("Est. Overtime Cost", f"€{cost:,.0f}")

    # --- Tab 3: Communication Center ---
    with tabs[2]:
        st.markdown("### Communication Center")
        st.markdown("Draft and send communications to different audiences. Each communication is logged.")

        audience = st.selectbox("Audience:", list(COMM_AUDIENCES.keys()), key="comm_aud")
        aud_info = COMM_AUDIENCES[audience]
        channel = st.selectbox("Channel:", aud_info["channels"], key="comm_ch")
        st.info(aud_info["template"])

        message = st.text_area(f"Draft your message to **{audience}** via **{channel}**:",
                               height=150, key="comm_msg")

        if st.button("Send Communication", key="send_comm"):
            if message:
                st.session_state.communication_log.append({
                    "audience": audience, "channel": channel, "message": message,
                    "time": datetime.now().strftime("%H:%M:%S"),
                })
                st.success(f"Sent to {audience} via {channel}.")
            else:
                st.error("Draft a message first.")

        if st.session_state.communication_log:
            st.markdown("---")
            st.markdown(f"#### Communication Log ({len(st.session_state.communication_log)} messages)")
            for i, c in enumerate(st.session_state.communication_log, 1):
                with st.expander(f"Msg {i}: {c['audience']} via {c['channel']}"):
                    st.write(c["message"])

    # --- Tab 4: Inject Events ---
    with tabs[3]:
        st.markdown("### Inject Events — Expect the Unexpected")
        st.markdown("New problems emerge while you manage existing ones. Respond to **each inject** as a team.")

        for inject in DOWNTIME_INJECTS:
            st.markdown("---")
            st.markdown(f"### {inject['title']} — {inject['time']}")
            st.markdown(inject["description"])
            role = st.session_state.team_role
            if role != "Not Selected" and role in inject["considerations"]:
                st.info(f"**From your role ({role}):** {inject['considerations'][role]}")
            st.radio(inject["question"], inject["options"], key=f"inj_{inject['id']}", index=None)
            st.text_area("Team justification:", key=f"inj_j_{inject['id']}", height=80)

    st.markdown("---")
    if st.button("Lock in Phase 2 & Proceed to Break", type="primary", use_container_width=True):
        for inj in DOWNTIME_INJECTS:
            c = st.session_state.get(f"inj_{inj['id']}")
            j = st.session_state.get(f"inj_j_{inj['id']}", "")
            if c:
                log_decision("Phase 2: Downtime", inj["title"], c, j)
        advance_phase()


# ---------------------------------------------------------------------------
# PHASE 3 — BREAK (20 min)
# ---------------------------------------------------------------------------
def render_phase_3():
    st.markdown('<h2 class="phase-header">Break</h2>', unsafe_allow_html=True)

    st.markdown(
        '<div class="alert-break">'
        "<strong>20-MINUTE BREAK</strong><br><br>"
        "The crisis does not pause, but you can.<br>"
        "When you return, it will be <strong>Hour 24</strong> of the incident.<br>"
        "External pressure is about to intensify."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### While You're on Break, Consider...")
    st.markdown("""
- What has gone well so far? What is your team most worried about?
- Which role has had the hardest time? Why?
- What information do you wish you had?
- What decisions from Part 1 might come back to haunt you in Part 2?
    """)

    st.markdown("---")
    st.markdown("### Status Check")
    st.markdown(f"**Decisions logged so far:** {len(st.session_state.decisions_log)}")
    st.markdown(f"**Communications sent:** {len(st.session_state.communication_log)}")
    st.markdown(f"**Paper records entered:** {len(st.session_state.manual_entries)}")

    render_decision_log()

    st.markdown("---")
    if st.button("Resume Simulation — Enter Day 2", type="primary", use_container_width=True):
        update_systems_day2()
        advance_phase()


# ---------------------------------------------------------------------------
# PHASE 4 — Escalation & Stakeholder Pressure (30 min)
# ---------------------------------------------------------------------------
def render_phase_4():
    st.markdown('<h2 class="phase-header">Phase 4: Escalation & Stakeholder Pressure (Hour 24–48)</h2>', unsafe_allow_html=True)
    st.caption("Estimated time: 30 minutes | Simulated time: Day 2")

    st.markdown(
        '<div class="alert-warning">DAY 2: EXTERNAL PRESSURE MOUNTING — MEDIA, FAMILIES, REGULATORS, STAFF</div>',
        unsafe_allow_html=True,
    )
    render_systems_dashboard()

    st.markdown("---")
    st.markdown("### Situation Update — 24 Hours In")
    icol1, icol2, icol3, icol4 = st.columns(4)
    icol1.metric("Hours of Downtime", "24")
    icol2.metric("Paper Records", "~3,200")
    icol3.metric("Surgeries Canceled", "23")
    icol4.metric("Patients Diverted", "14")

    icol5, icol6, icol7, icol8 = st.columns(4)
    icol5.metric("Revenue Loss (est.)", "€240,000")
    icol6.metric("Staff Overtime Hours", "360")
    icol7.metric("Patient Complaints", "36")
    icol8.metric("Media Inquiries", "4")

    st.markdown("---")
    st.markdown(
        "### The Pressure Mounts\n"
        "In this phase, you will face escalating pressure from **outside** the "
        "hospital (media, families, regulators) and from **inside** (staff morale, "
        "inter-department conflict). Each inject requires a team decision."
    )

    for inject in ESCALATION_INJECTS:
        st.markdown("---")
        st.markdown(f"### {inject['title']} — {inject['time']}")
        if inject.get("description"):
            st.markdown(inject["description"])
        if inject.get("content"):
            st.markdown(inject["content"], unsafe_allow_html=True)

        role = st.session_state.team_role
        if role != "Not Selected":
            # Role-specific prompts for escalation events
            role_prompts = {
                "inject_media_story": {
                    "Incident Commander (Hospital Administrator)": "You will likely be the face of the press conference. What are you willing to say publicly?",
                    "Health Information Manager (HIM Director)": "The media is asking about patient data theft. What can you confirm? What must you withhold pending CNIL notification?",
                    "Clinical Operations Lead (Chief Nursing Officer)": "A nurse's family member may have been the source. How do you address this with staff without creating a witch hunt?",
                    "IT Security & Informatics Lead": "Journalists will ask technical questions. What is safe to disclose? What gives the attackers an advantage if revealed?",
                    "Communications & Compliance Officer": "This is your moment. What is the key message? What is the one thing you absolutely cannot say?",
                },
                "inject_family_confrontation": {
                    "Incident Commander (Hospital Administrator)": "This man represents hundreds of families with the same concerns. Your response sets the template.",
                    "Health Information Manager (HIM Director)": "He wants to know about his mother's records and whether her data was stolen. What can you tell him under GDPR?",
                    "Clinical Operations Lead (Chief Nursing Officer)": "His mother is your patient. Her care is being delivered on paper. How do you reassure him about clinical quality?",
                    "IT Security & Informatics Lead": "He may ask when the portal will be back. What is your honest answer?",
                    "Communications & Compliance Officer": "He is threatening to call his lawyer and the press. How do you de-escalate without making promises you can't keep?",
                },
                "inject_staff_revolt": {
                    "Incident Commander (Hospital Administrator)": "If nurses keep calling in sick, you face a staffing crisis on top of a cyber crisis. What resources can you mobilize?",
                    "Health Information Manager (HIM Director)": "Fatigued staff make more documentation errors. How does this affect your data integrity concerns?",
                    "Clinical Operations Lead (Chief Nursing Officer)": "Marie-Claire is one of your best charge nurses. If she breaks, the unit breaks. What do you do for her specifically?",
                    "IT Security & Informatics Lead": "Is there anything you can bring back online quickly that would reduce staff burden? Even one system?",
                    "Communications & Compliance Officer": "Staff are posting on social media. Some posts reveal operational details. How do you address this?",
                },
                "inject_social_media": {
                    "Incident Commander (Hospital Administrator)": "Social media is now driving the narrative. Do you engage or stay above it?",
                    "Health Information Manager (HIM Director)": "The data breach claims on social media may be premature — you haven't confirmed the scope. But silence looks like a cover-up.",
                    "Clinical Operations Lead (Chief Nursing Officer)": "Your nurses are being portrayed as working in unsafe conditions. This affects recruitment, morale, and public trust.",
                    "IT Security & Informatics Lead": "Some posts contain technical details that could help other attackers. Is there a way to request removal without censorship?",
                    "Communications & Compliance Officer": "You are now managing communications on platforms you don't control. What is your strategy?",
                },
                "inject_department_conflict": {
                    "Incident Commander (Hospital Administrator)": "Both sides have valid points. You must make the call. Either way, someone will be unhappy. How do you maintain team unity?",
                    "Health Information Manager (HIM Director)": "Your professional judgment says paper-based surgery is high risk. Are you willing to be overruled?",
                    "Clinical Operations Lead (Chief Nursing Officer)": "You've seen surgical errors. You've also seen patients harmed by surgical delay. Where is the line?",
                    "IT Security & Informatics Lead": "Could you restore just the surgical safety checklist system independently? How long would that take?",
                    "Communications & Compliance Officer": "If a surgical error occurs during downtime, the hospital's legal exposure is enormous. If a patient is harmed by delay, same thing.",
                },
            }
            prompts = role_prompts.get(inject["id"], {})
            if role in prompts:
                st.info(f"**From your role ({role}):** {prompts[role]}")

        st.radio(inject["question"], inject["options"], key=f"esc_{inject['id']}", index=None)
        st.text_area("Team justification:", key=f"esc_j_{inject['id']}", height=100)

    st.markdown("---")
    if st.button("Lock in Escalation Decisions & Proceed to Critical Decisions", type="primary", use_container_width=True):
        for inj in ESCALATION_INJECTS:
            c = st.session_state.get(f"esc_{inj['id']}")
            j = st.session_state.get(f"esc_j_{inj['id']}", "")
            if c:
                log_decision("Phase 4: Escalation", inj["title"], c, j)
        update_systems_day3()
        advance_phase()


# ---------------------------------------------------------------------------
# PHASE 5 — Critical Decisions (30 min)
# ---------------------------------------------------------------------------
def render_phase_5():
    st.markdown('<h2 class="phase-header">Phase 5: Critical Decisions (Hour 48–72)</h2>', unsafe_allow_html=True)
    st.caption("Estimated time: 30 minutes | Simulated time: Day 3")

    st.markdown(
        '<div class="alert-critical">DAY 3: MAJOR DECISIONS REQUIRED — RANSOM DEADLINE & REGULATORY CLOCK TICKING</div>',
        unsafe_allow_html=True,
    )
    render_systems_dashboard()

    st.markdown("---")

    # Updated impact dashboard
    st.markdown("### Incident Impact Dashboard — 48 Hours")
    icol1, icol2, icol3, icol4 = st.columns(4)
    icol1.metric("Hours of Downtime", "48", delta="+24", delta_color="inverse")
    icol2.metric("Paper Records", "~6,400", delta="+3,200")
    icol3.metric("Surgeries Canceled", "38", delta="+15")
    icol4.metric("Patients Diverted", "24", delta="+10")

    icol5, icol6, icol7, icol8 = st.columns(4)
    icol5.metric("Revenue Loss", "€480,000", delta="-€240K")
    icol6.metric("Overtime Hours", "720", delta="+360")
    icol7.metric("Patient Complaints", "89", delta="+53")
    icol8.metric("Media Stories", "7", delta="+3")

    # Financial projection
    st.markdown("### Financial Impact Projection")
    days = list(range(1, 22))
    daily = [85000 * (1 if d <= 3 else 0.7 if d <= 7 else 0.3 if d <= 14 else 0.1) for d in days]
    cumul = []
    t = 0
    for v in daily:
        t += v
        cumul.append(t)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=days, y=daily, name="Daily Revenue Loss", marker_color="#ff4b4b"))
    fig.add_trace(go.Scatter(x=days, y=cumul, name="Cumulative Loss", line=dict(color="#ffa726", width=3), yaxis="y2"))
    fig.update_layout(
        title="Projected Financial Impact Over 21 Days",
        xaxis_title="Day Since Breach", yaxis_title="Daily Loss (€)",
        yaxis2=dict(title="Cumulative Loss (€)", overlaying="y", side="right"),
        height=350, legend=dict(orientation="h", y=1.15),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    for inject in CRITICAL_INJECTS:
        st.markdown(f"### {inject['title']} — {inject['time']}")
        st.markdown(inject["description"])
        st.radio(inject["question"], inject["options"], key=f"crit_{inject['id']}", index=None)
        st.text_area("Team justification (consider ALL role perspectives):", key=f"crit_j_{inject['id']}", height=120)
        if inject.get("follow_up"):
            with st.expander("Discussion Prompt"):
                st.markdown(inject["follow_up"])
        st.markdown("---")

    if st.button("Lock in Critical Decisions & Proceed to Recovery Planning", type="primary", use_container_width=True):
        for inj in CRITICAL_INJECTS:
            c = st.session_state.get(f"crit_{inj['id']}")
            j = st.session_state.get(f"crit_j_{inj['id']}", "")
            if c:
                log_decision("Phase 5: Critical Decisions", inj["title"], c, j)
        update_systems_recovery()
        advance_phase()


# ---------------------------------------------------------------------------
# PHASE 6 — Recovery Planning (20 min)
# ---------------------------------------------------------------------------
def render_phase_6():
    st.markdown('<h2 class="phase-header">Phase 6: Recovery Planning (Hour 72+)</h2>', unsafe_allow_html=True)
    st.caption("Estimated time: 20 minutes | Simulated time: Day 4 onward")

    st.markdown(
        '<div class="alert-info">DAY 4+: PARTIAL RESTORATION IN PROGRESS — PLANNING FOR RECOVERY</div>',
        unsafe_allow_html=True,
    )
    render_systems_dashboard()

    st.markdown("---")

    tabs = st.tabs([
        "Back-Entry Triage Plan",
        "Trust & Reputation Recovery",
        "Preparedness Assessment",
        "Team After-Action Summary",
    ])

    # --- Tab 1: Back-Entry Triage ---
    with tabs[0]:
        st.markdown("### Back-Entry Triage Plan")
        st.markdown(
            "Systems are coming back online. You have an estimated **6,400+ paper "
            "records** to reconcile and enter. You cannot do everything at once. "
            "**Prioritize.**"
        )

        record_types = [
            ("Medication Administration Records (MARs)", "Patient safety — validates what was actually given during downtime"),
            ("Allergy documentation", "Patient safety — critical for ongoing care decisions"),
            ("Vital signs and nursing assessments", "Clinical continuity — needed for trending and discharge decisions"),
            ("Lab orders and results", "Clinical decisions — some results may not have been communicated"),
            ("Surgical documentation (consents, op notes, specimen labels)", "Legal and compliance — incomplete surgical records are high liability"),
            ("Progress notes (physician and nursing)", "Clinical completeness — important but lower immediate risk"),
            ("Admission/discharge/transfer records", "Revenue cycle — needed for billing and census reconciliation"),
            ("Patient identification and demographic verification", "Data integrity — resolves the 11% 'orphaned' records"),
        ]

        st.markdown("**Drag to reorder these record types by back-entry priority (1 = highest):**")
        st.markdown("*Since drag-and-drop isn't available, assign a priority number to each:*")

        priorities = {}
        for rt, rationale in record_types:
            col1, col2 = st.columns([1, 3])
            with col1:
                priorities[rt] = st.number_input(f"Priority", 1, 8, key=f"pri_{rt}", label_visibility="collapsed")
            with col2:
                st.markdown(f"**{rt}**  \n*{rationale}*")

        st.markdown("---")
        st.markdown("#### Back-Entry Staffing Plan")
        st.text_area(
            "How will you staff the back-entry effort? Consider: Who does the data entry? "
            "How do you handle illegible records? What is your quality check process? "
            "What is your timeline?",
            key="backentry_plan", height=120,
        )

    # --- Tab 2: Trust Recovery ---
    with tabs[1]:
        st.markdown("### Trust & Reputation Recovery")
        st.markdown("The technical recovery is only half the battle. You must rebuild trust with multiple audiences.")

        audiences = [
            ("Patients whose data may have been stolen",
             "180,000 people need to be notified. Many will be frightened, angry, or confused. Some have sensitive records (mental health, HIV, reproductive health)."),
            ("Current inpatients and their families",
             "They experienced the crisis firsthand. Some had surgeries delayed, medications disrupted, or care delivered on paper. They want to know it won't happen again."),
            ("Hospital staff",
             "They worked through the crisis. Many are burned out, some are angry at leadership, some feel unsupported. Retention is at risk."),
            ("The public and media",
             "The hospital's reputation has been damaged. Community trust is shaken. Future patients may choose other facilities."),
            ("Regulators (CNIL, ARS)",
             "You must demonstrate compliance, transparency, and a credible plan to prevent recurrence."),
        ]

        for aud, context in audiences:
            with st.expander(f"**{aud}**"):
                st.markdown(f"*{context}*")
                st.text_area(f"Your trust recovery strategy for {aud}:", key=f"trust_{aud}", height=100)

    # --- Tab 3: Preparedness Assessment ---
    with tabs[2]:
        st.markdown("### Cybersecurity Preparedness Assessment")
        st.markdown("Rate the hospital's preparedness in each area based on what you experienced. Then recommend ONE improvement.")

        prep_areas = [
            "Downtime procedures (paper forms, manual processes)",
            "Staff training on manual/downtime operations",
            "Communication plan (internal and external)",
            "Data backup and recovery strategy",
            "Incident response team readiness",
            "GDPR breach notification preparedness",
            "Cybersecurity insurance and financial resilience",
            "Patient communication and trust management",
            "Cybersecurity awareness training (phishing prevention)",
            "Inter-department coordination during crisis",
        ]

        ratings = {}
        for area in prep_areas:
            c1, c2 = st.columns([1, 2])
            with c1:
                ratings[area] = st.slider(area, 1, 5, 2, key=f"prep_{area}",
                                           help="1 = Not prepared, 5 = Fully prepared")
            with c2:
                st.text_input(f"Recommendation:", key=f"prep_rec_{area}")

        if any(v > 0 for v in ratings.values()):
            st.markdown("#### Preparedness Radar")
            cats = [a[:35] + "..." if len(a) > 35 else a for a in prep_areas]
            vals = list(ratings.values())
            vals.append(vals[0])
            cats.append(cats[0])
            fig = go.Figure(data=go.Scatterpolar(
                r=vals, theta=cats, fill="toself",
                line_color="#ff4b4b", fillcolor="rgba(255,75,75,0.2)",
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                height=450, title="Preparedness Assessment",
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Tab 4: After-Action Summary ---
    with tabs[3]:
        st.markdown("### Team After-Action Summary")
        st.markdown("Complete this as a team before the debrief session.")

        st.markdown("#### Decision Timeline Review")
        render_decision_log()

        st.markdown("---")
        st.markdown("#### Key Takeaways")
        st.text_area(
            "1. What was the single most important decision your team made? Why?",
            key="aa_q1", height=100,
        )
        st.text_area(
            "2. What decision would you change if you could do it over? What would you do differently?",
            key="aa_q2", height=100,
        )
        st.text_area(
            "3. Which role had the most difficult job in this simulation? Why?",
            key="aa_q3", height=100,
        )
        st.text_area(
            "4. What is one thing about cybersecurity in healthcare that you did not appreciate before this simulation?",
            key="aa_q4", height=100,
        )
        st.text_area(
            "5. If you were advising a hospital CEO on cybersecurity preparedness, what would your top 3 recommendations be?",
            key="aa_q5", height=100,
        )

    st.markdown("---")

    # Export
    if st.button("Export Full Simulation Report", type="primary"):
        report = {
            "team_name": st.session_state.team_name,
            "role": st.session_state.team_role,
            "decisions": st.session_state.decisions_log,
            "communications": st.session_state.communication_log,
            "manual_records_count": len(st.session_state.manual_entries),
            "after_action": {
                f"q{i}": st.session_state.get(f"aa_q{i}", "") for i in range(1, 6)
            },
        }
        st.download_button(
            "Download Report (JSON)",
            data=json.dumps(report, indent=2, ensure_ascii=False),
            file_name=f"cybersecurity_sim_{st.session_state.team_name}.json",
            mime="application/json",
        )

    st.markdown("---")
    st.markdown(
        '<div class="alert-info" style="text-align:center;">'
        "<strong>End of Simulation</strong><br>"
        "Thank you for your work. The 2-hour debrief will follow."
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown("## SHIFT Cybersecurity Simulation")
        st.markdown(f"**{HOSPITAL_NAME}**")

        if st.session_state.team_name:
            st.markdown(f"**Team:** {st.session_state.team_name}")
        if st.session_state.team_role != "Not Selected":
            r = ROLES[st.session_state.team_role]
            st.markdown(f"**Role:** {r['icon']} {st.session_state.team_role}")

        st.markdown("---")
        st.markdown("### Simulation Phases")
        for i, phase in enumerate(PHASES):
            if i == st.session_state.current_phase:
                st.markdown(f"**>> {phase['name']}** ({phase['time']})")
            elif st.session_state.phase_unlocked[i]:
                if st.button(f"{phase['name']}", key=f"nav_{i}"):
                    st.session_state.current_phase = i
                    st.rerun()
            else:
                st.markdown(f"*{phase['name']}* (locked)")

        st.markdown("---")
        st.markdown("### Quick Reference")
        with st.expander("Downtime Essentials"):
            st.markdown("""
- **Paper forms**: HIM office + each nursing station
- **Medication reference**: Printed formulary in pharmacy
- **Phone tree**: Posted at each charge nurse desk
- **Runner system**: Volunteers at command center
- **Patient ID**: Verbal two-identifier (name + DOB)
- **Specimen labeling**: Handwritten with 2 identifiers
- **Code status**: Paper band on wristband
            """)
        with st.expander("GDPR Key Points"):
            st.markdown("""
- **72-hour notification** to CNIL after breach awareness
- **Document everything**: timeline, scope, response
- **Patient notification** if high risk to rights/freedoms
- **Right to be forgotten** still applies in crisis
- **DPO** must be involved in all decisions
- **Loi LOPMI (2023)**: Police report within 72h of ransom payment for insurance reimbursement
            """)
        with st.expander("Key Contacts (Scenario)"):
            st.markdown("""
- **ANSSI** (Cyber): +33 1 XX XX XX XX
- **CNIL** (Data Protection): notification portal
- **Cyber Insurance**: Policy #HC-2026-4471
- **EHR Vendor**: 24/7 emergency line
- **Legal Counsel**: On retainer
- **ARS** (Regional Health): Emergency line
- **Police**: Commissariat local
            """)
        with st.expander("Hospital Quick Facts"):
            st.markdown("""
- **350 beds**, 287 current inpatients
- **42** ICU patients, **8** maternity
- **1,200** staff (3 shifts)
- **14** patients named Martin
- **47** telehealth appointments today
- **142** outpatient appointments today
- **12** scheduled surgeries (pre-breach)
- **Neonatal ICU**: only one in region
            """)

        st.markdown("---")
        st.markdown(f"**Decisions:** {len(st.session_state.decisions_log)}")
        st.markdown(f"**Communications:** {len(st.session_state.communication_log)}")
        st.markdown(f"**Paper records:** {len(st.session_state.manual_entries)}")

        st.markdown("---")
        if st.button("Reset Simulation", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
PHASE_RENDERERS = {
    0: render_phase_0,
    1: render_phase_1,
    2: render_phase_2,
    3: render_phase_3,
    4: render_phase_4,
    5: render_phase_5,
    6: render_phase_6,
}

def main():
    render_sidebar()
    renderer = PHASE_RENDERERS.get(st.session_state.current_phase)
    if renderer:
        renderer()

if __name__ == "__main__":
    main()
