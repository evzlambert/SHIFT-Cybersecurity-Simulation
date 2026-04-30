"""
SHIFT Cybersecurity Breach Simulation — Student Response App
Saint-Etienne, France

Lightweight response-capture app with decision trees. Students watch the
instructor projection, discuss on their feet, then return here to log
decisions and see consequences unique to their choices.

Launch:  python3 -m streamlit run student_app.py --server.port 8502
"""

import streamlit as st
import json
import os
from datetime import datetime

try:
    import gspread
    from google.oauth2.service_account import Credentials as GCreds
    _GSHEETS_AVAILABLE = True
except ImportError:
    _GSHEETS_AVAILABLE = False

_GSHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def _get_sheet():
    """Return the first sheet of the configured Google Sheet, or None."""
    if not _GSHEETS_AVAILABLE:
        return None
    try:
        creds_info = st.secrets.get("gcp_service_account")
        sheet_url = st.secrets.get("google_sheet_url", "")
        if not creds_info or not sheet_url:
            return None
        creds = GCreds.from_service_account_info(dict(creds_info), scopes=_GSHEETS_SCOPES)
        client = gspread.authorize(creds)
        return client.open_by_url(sheet_url).sheet1
    except Exception:
        return None

def _save_to_gsheet(team_name: str, report_text: str) -> bool:
    """Append one row (team, timestamp, full report) to the Google Sheet."""
    sheet = _get_sheet()
    if sheet is None:
        return False
    try:
        sheet.append_row(
            [team_name, datetime.now().strftime("%Y-%m-%d %H:%M"), report_text],
            value_input_option="RAW",
        )
        return True
    except Exception:
        return False

# ---------------------------------------------------------------------------
# Submissions directory — local fallback when running outside Streamlit Cloud
# ---------------------------------------------------------------------------
SUBMISSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions")
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

st.set_page_config(
    page_title="SHIFT Cyber Sim — Team Response",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .consequence-good {
        background-color: #1b5e20; color: #c8e6c9; padding: 18px;
        border-radius: 10px; margin: 12px 0; border-left: 5px solid #4caf50;
        font-size: 1.05em; line-height: 1.5;
    }
    .consequence-mixed {
        background-color: #e65100; color: #ffe0b2; padding: 18px;
        border-radius: 10px; margin: 12px 0; border-left: 5px solid #ff9800;
        font-size: 1.05em; line-height: 1.5;
    }
    .consequence-bad {
        background-color: #b71c1c; color: #ffcdd2; padding: 18px;
        border-radius: 10px; margin: 12px 0; border-left: 5px solid #f44336;
        font-size: 1.05em; line-height: 1.5;
    }
    .consequence-neutral {
        background-color: #1a237e; color: #c5cae9; padding: 18px;
        border-radius: 10px; margin: 12px 0; border-left: 5px solid #5c6bc0;
        font-size: 1.05em; line-height: 1.5;
    }
    .metric-delta-bad { color: #ff4b4b; font-weight: bold; }
    .metric-delta-good { color: #4caf50; font-weight: bold; }
    .ripple-box {
        background-color: #212121; color: #bdbdbd; padding: 14px;
        border-radius: 8px; margin: 8px 0; border-left: 4px solid #9e9e9e;
        font-size: 0.95em;
    }
    .phase-header {
        border-bottom: 3px solid #ff4b4b;
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .station-banner {
        background: linear-gradient(135deg, #e65100 0%, #ff8f00 100%);
        border: 3px solid #ffb74d;
        border-radius: 12px;
        padding: 25px 30px;
        margin: 20px 0 15px 0;
        color: white;
        font-size: 1.1em;
        line-height: 1.6;
    }
    .station-banner h3 {
        margin: 0 0 10px 0; font-size: 1.3em; letter-spacing: 1px;
    }
    .station-banner .station-time {
        background-color: rgba(0,0,0,0.25); border-radius: 6px;
        padding: 4px 12px; display: inline-block; font-weight: bold;
        margin-bottom: 10px;
    }
    .station-materials {
        background-color: #fff3e0; color: #4e342e; padding: 14px 18px;
        border-radius: 8px; margin: 10px 0; border-left: 4px solid #ff8f00;
        font-size: 0.95em;
    }
    .station-task {
        background-color: #1a1a2e; color: #ffe0b2; padding: 18px;
        border-radius: 10px; margin: 12px 0; border-left: 5px solid #ff8f00;
        font-size: 1.05em; line-height: 1.5;
    }
    .quality-check {
        background-color: #263238; color: #b0bec5; padding: 14px 18px;
        border-radius: 8px; margin: 10px 0; border-left: 4px solid #4caf50;
    }
    .station-complete {
        background-color: #1b5e20; color: #c8e6c9; padding: 15px;
        border-radius: 10px; margin: 12px 0; border-left: 5px solid #4caf50;
        font-size: 1.05em;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------
ROLES = [
    "Not Selected",
    "Incident Commander (Hospital Administrator)",
    "Health Information Manager (HIM Director)",
    "Clinical Operations Lead (Chief Nursing Officer)",
    "IT Security & Informatics Lead",
    "Communications & Compliance Officer",
]

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
DEFAULTS = {
    "team_name": "",
    "team_role": "Not Selected",
    "current_phase": 0,
    "decisions": {},       # key: decision_id, value: chosen option index
    "justifications": {},  # key: decision_id, value: text
    "log": [],             # list of {phase, context, choice, justification, time}
    "comms": [],           # communication log
    "stations_complete": {},   # key: station_id, value: True
    "station_data": {},        # key: station_id, value: dict of field values
    "station_checks": {},      # key: station_id, value: list of checked items
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v if not isinstance(v, (list, dict)) else type(v)(v)

# ---------------------------------------------------------------------------
# Decision tree data
# ---------------------------------------------------------------------------
# Each decision has: id, phase, title, question, options (list of dicts with
# text, consequence_text, consequence_class, metric_effects, ripple)
# consequence_class: good, mixed, bad, neutral
# metric_effects: dict of label: (value, delta_str)
# ripple: text shown later as a downstream effect

DECISIONS = {
    # ===== PHASE 1 =====
    "p1_priority": {
        "phase": "Phase 1: The Breach",
        "title": "First Priority Action",
        "question": "What is your FIRST priority action?",
        "options": [
            {
                "text": "Activate downtime procedures immediately while IT contains the breach in parallel",
                "consequence_text": (
                    "Downtime forms reach nursing stations within 20 minutes. Medication "
                    "administration resumes on paper by 07:30. However, IT reports that the "
                    "ransomware spread to 2 additional servers during the 20-minute window "
                    "before network isolation was complete."
                ),
                "consequence_class": "mixed",
                "ripple": "Your early downtime activation means staff are more prepared for paper processes, but the breach scope is slightly larger.",
            },
            {
                "text": "Focus on network isolation first — prevent further spread (accept 30-60 min clinical delay)",
                "consequence_text": (
                    "IT successfully isolates the network within 15 minutes, preventing spread "
                    "to the backup servers. However, medication administration is delayed by "
                    "45 minutes while paper forms are located and distributed. Two ICU patients "
                    "experience a brief interruption in their IV drip monitoring. Both are "
                    "stabilized quickly by attentive nursing staff."
                ),
                "consequence_class": "mixed",
                "ripple": "Your backup servers are confirmed clean — this will give you better restoration options later. But clinical staff are frustrated by the initial delay.",
            },
            {
                "text": "Split the team: IT isolates while clinical leadership activates downtime simultaneously",
                "consequence_text": (
                    "Both tracks proceed simultaneously. Downtime procedures activate within "
                    "25 minutes and network isolation is complete in 20 minutes. However, "
                    "coordination suffers — the ICU activates a different downtime protocol "
                    "than the medical-surgical floors, creating confusion during the first "
                    "hour. By 08:00, protocols are aligned."
                ),
                "consequence_class": "good",
                "ripple": "You moved fast on both fronts but the coordination gap means some units have inconsistent paper forms for the first hour. This affects data quality later.",
            },
            {
                "text": "Convene a 10-minute emergency leadership huddle before any action",
                "consequence_text": (
                    "The huddle produces a clear, unified action plan. All departments receive "
                    "identical instructions. However, the 10-minute delay meant the ransomware "
                    "spread to 3 more servers, and a pharmacy technician independently attempted "
                    "a cabinet override that triggered a lockout alert. Medication administration "
                    "doesn't resume on paper until 07:50."
                ),
                "consequence_class": "bad",
                "ripple": "Your unified plan is solid, but the delay cost you server containment and clinical time. Staff are asking why leadership didn't act faster.",
            },
        ],
    },

    "p1_communication": {
        "phase": "Phase 1: The Breach",
        "title": "Staff Communication Method",
        "question": "How do you communicate the situation to 1,200 staff?",
        "options": [
            {
                "text": "Overhead PA announcement with instructions to report to charge nurses",
                "consequence_text": (
                    "The PA reaches everyone simultaneously. However, the announcement causes "
                    "visible alarm among patients and families in hallways and waiting areas. "
                    "Several family members begin calling local media to ask what's happening. "
                    "Staff receive consistent information, which reduces rumor spread."
                ),
                "consequence_class": "mixed",
                "ripple": "Patients and families heard the PA. Some are alarmed. A family member contacts a local journalist within the hour.",
            },
            {
                "text": "Runners with printed bulletins to every unit (takes 20-30 min)",
                "consequence_text": (
                    "Staff receive detailed, accurate information in writing. However, it takes "
                    "28 minutes to reach all units. During that time, day-shift staff arriving "
                    "for the 07:00 change hear rumors in the parking lot and hallways. "
                    "By the time bulletins arrive, some staff have already posted on social media."
                ),
                "consequence_class": "mixed",
                "ripple": "Two staff members posted on WhatsApp groups before the bulletin reached them. The posts are vague but mention 'a hack.' No media pickup yet.",
            },
            {
                "text": "Mass text via personal phones (WhatsApp/SMS)",
                "consequence_text": (
                    "Fastest method — staff receive information within 3 minutes. However, "
                    "a screenshot of the WhatsApp message is shared outside the hospital within "
                    "15 minutes. A local journalist now has a direct quote from an internal "
                    "hospital communication confirming a 'cyberattack.' Your Communications "
                    "Officer loses control of the external narrative."
                ),
                "consequence_class": "bad",
                "ripple": "A journalist has a screenshot of your internal communication. They will use it in their story. You've lost the ability to control initial framing.",
            },
            {
                "text": "Hold arriving day-shift at entrances for a 5-minute verbal briefing",
                "consequence_text": (
                    "Staff receive consistent, face-to-face information with the opportunity to "
                    "ask questions. Morale is slightly better — staff feel respected. However, "
                    "the 5-minute delay in reaching patient floors means night-shift nurses are "
                    "alone for longer during the most chaotic period. Night-shift charge nurses "
                    "report feeling abandoned."
                ),
                "consequence_class": "mixed",
                "ripple": "Night-shift staff are resentful that day-shift was briefed while they were still alone on the floors. This affects cross-shift trust.",
            },
        ],
    },

    "p1_safety": {
        "phase": "Phase 1: The Breach",
        "title": "Patient Safety Strategy",
        "question": "What is your patient safety strategy for surgeries, ICU, and maternity?",
        "options": [
            {
                "text": "Cancel elective surgeries; continue only emergency/life-saving procedures with manual verification; maternity continues with midwife-led manual protocols",
                "consequence_text": (
                    "Elective surgeries are canceled, affecting 8 patients. Two patients with "
                    "time-sensitive conditions (a bowel obstruction and a hip fracture) are "
                    "operated on successfully using manual checklists. Maternity delivers "
                    "3 babies safely using midwife-led protocols. One elective patient's family "
                    "is angry about the cancellation — they had traveled from another city."
                ),
                "consequence_class": "good",
                "ripple": "Your surgical cancellations created a backlog. When you decide whether to resume elective surgery later, you'll have 8+ patients waiting.",
            },
            {
                "text": "Cancel ALL surgeries and halt new admissions until systems are assessed",
                "consequence_text": (
                    "Maximum safety posture. No surgical incidents occur. However, the bowel "
                    "obstruction patient must be transferred to a hospital 45 minutes away — "
                    "the transfer is successful but delays their surgery by 4 hours. Staff "
                    "perception: some view this as overly cautious; others are relieved."
                ),
                "consequence_class": "mixed",
                "ripple": "You transferred a surgical patient. The receiving hospital bills you for the procedure. The patient's family is filing a formal complaint about being 'sent away.'",
            },
            {
                "text": "Case-by-case assessment by surgical team and anesthesia; maternity continues; ICU on manual pump management",
                "consequence_text": (
                    "The surgical team assesses each case individually. 9 of 12 scheduled "
                    "surgeries proceed with enhanced manual protocols. All complete successfully, "
                    "though one takes 30 minutes longer due to manual specimen labeling. "
                    "ICU drips are managed manually without incident. This approach required "
                    "significant senior surgeon time for assessment, delaying other clinical work."
                ),
                "consequence_class": "good",
                "ripple": "Your case-by-case approach worked, but the Chief of Surgery spent 90 minutes on assessments instead of operating. He's frustrated and will push hard to resume normal operations.",
            },
            {
                "text": "Continue all procedures — clinical staff can work without computers",
                "consequence_text": (
                    "All 12 surgeries proceed. 11 complete without issues. In the 12th case, "
                    "a surgical specimen is labeled by hand with only the patient's last name — "
                    "no MRN, no DOB. Pathology flags it as incomplete and requests "
                    "re-identification, causing a 48-hour delay in biopsy results for a "
                    "patient awaiting a potential cancer diagnosis. The error is caught and "
                    "corrected, but it shakes staff confidence in paper processes."
                ),
                "consequence_class": "bad",
                "ripple": "A specimen labeling error occurred. It was caught, but the near-miss is now on record. The HIM Director will reference this when the surgery debate arises later.",
            },
        ],
    },

    # ===== PHASE 2 =====
    "p2_medication": {
        "phase": "Phase 2: Downtime",
        "title": "Medication Safety Response",
        "question": "After the near-miss medication event — how do you prevent actual errors?",
        "options": [
            {
                "text": "Buddy-system double-checks for all medication administration",
                "consequence_text": (
                    "The buddy system catches 3 additional potential errors over the next 12 "
                    "hours. No actual medication errors occur. However, medication administration "
                    "now takes twice as long. Patients report longer wait times for pain "
                    "medication. Two nurses request to go home early, citing exhaustion from "
                    "the doubled workload."
                ),
                "consequence_class": "good",
                "ripple": "The buddy system is effective but unsustainable at current staffing levels. When staff morale becomes an issue, this is part of the reason.",
            },
            {
                "text": "Restrict medication dispensing to charge nurses only",
                "consequence_text": (
                    "Charge nurses become the bottleneck. Medication rounds that normally take "
                    "1 hour now take 3 hours. A patient with poorly controlled diabetes misses "
                    "their scheduled insulin by 90 minutes — their blood sugar spikes to 320 "
                    "mg/dL but is corrected without lasting harm. Charge nurses are overwhelmed "
                    "and cannot perform other leadership duties."
                ),
                "consequence_class": "bad",
                "ripple": "Charge nurses are now doing medication rounds instead of leading their units. When the shift handoff comes, they have less situational awareness to pass on.",
            },
            {
                "text": "Deploy printed patient wristbands with photos and add a third identifier",
                "consequence_text": (
                    "IT recovers the patient photo database from a backup drive (separate from "
                    "the encrypted servers). Printed wristbands are produced within 2 hours. "
                    "The three-identifier system (name + DOB + photo) significantly reduces "
                    "identification confusion. The 14 patients named Martin are now clearly "
                    "distinguishable. Staff confidence improves."
                ),
                "consequence_class": "good",
                "ripple": "The wristband solution demonstrated that some data can be recovered independently. IT will reference this when discussing restoration options.",
            },
            {
                "text": "Halt all non-emergency medication until a safety protocol is confirmed",
                "consequence_text": (
                    "Non-emergency medications are paused for 45 minutes while a safety protocol "
                    "is developed. During this time, 6 patients miss scheduled doses of "
                    "antibiotics, 4 miss blood pressure medications, and 2 miss anti-seizure "
                    "drugs. All are restarted without clinical incident, but medical staff are "
                    "angry: 'We paused medications to write a protocol? That IS a patient "
                    "safety event.'"
                ),
                "consequence_class": "bad",
                "ripple": "Several physicians documented formal objections to the medication pause. This will appear in the after-action report and may have legal implications.",
            },
        ],
    },

    "p2_diversion": {
        "phase": "Phase 2: Downtime",
        "title": "Ambulance Diversion Decision",
        "question": "Do you approve ambulance diversion? A pregnant woman at 36 weeks is en route.",
        "options": [
            {
                "text": "Full diversion — redirect all ambulances to nearby facilities",
                "consequence_text": (
                    "Ambulances are redirected. The pregnant woman is diverted to a hospital "
                    "50 minutes away — she delivers safely but without neonatal ICU backup. "
                    "Her OB/GYN files a formal complaint about the diversion, calling it "
                    "'medically reckless.' A 68-year-old chest pain patient is diverted to a "
                    "hospital 35 minutes away; they arrive stable. Over 8 hours, 14 patients "
                    "total are diverted. Your ED empties to manageable levels."
                ),
                "consequence_class": "mixed",
                "ripple": "The OB/GYN's complaint will surface during the media cycle. A reporter will ask: 'Is it true you diverted a pregnant woman from the only neonatal ICU in the region?'",
            },
            {
                "text": "Partial diversion — accept only life-threatening, trauma, cardiac, stroke, and obstetric emergencies",
                "consequence_text": (
                    "The pregnant woman is accepted and delivers safely in your maternity unit. "
                    "Lower-acuity patients are diverted. Your ED volume drops by about 40%, "
                    "making manual triage manageable. Two diverted patients with moderate "
                    "injuries arrive at the partner hospital without complication."
                ),
                "consequence_class": "good",
                "ripple": "Your partial diversion is seen as a reasonable, proportionate response. The ARS approves retroactively.",
            },
            {
                "text": "Deny diversion — implement manual triage and request additional staffing from ARS",
                "consequence_text": (
                    "The ED continues receiving all patients. ARS sends 4 additional nurses "
                    "within 3 hours, but the first 3 hours are extremely difficult. Wait times "
                    "reach 4 hours for non-emergency patients. A patient with a broken wrist "
                    "leaves without being seen and posts an angry review online. No critical "
                    "patient safety events occur, but staff are pushed to their limit."
                ),
                "consequence_class": "mixed",
                "ripple": "Your ED staff are exhausted from managing full volume on paper. When the staff morale crisis hits, ED nurses will be the most affected.",
            },
            {
                "text": "Approve temporary diversion (4 hours) while establishing manual tracking",
                "consequence_text": (
                    "The pregnant woman arrives during the 4-hour diversion window and is "
                    "accepted as an exception (obstetric emergency). She delivers safely. "
                    "During the 4 hours, your team sets up a manual whiteboard tracking system "
                    "in the ED. When diversion lifts, the ED functions at reduced but "
                    "acceptable capacity. A total of 6 patients are diverted during the window."
                ),
                "consequence_class": "good",
                "ripple": "The temporary diversion gave your ED time to adapt. Manual tracking is functional but slow. This buys goodwill with the ARS.",
            },
        ],
    },

    "p2_handoff": {
        "phase": "Phase 2: Downtime",
        "title": "Shift Handoff Strategy",
        "question": "How do you structure the 19:00 shift handoff without electronic tools?",
        "options": [
            {
                "text": "Unit-by-unit bedside handoff with centralized charge nurse briefing",
                "consequence_text": (
                    "The most thorough approach. Each patient gets a face-to-face handoff. "
                    "The process takes 75 minutes — longer than the usual 30. Evening staff "
                    "report feeling well-informed but the extended handoff delays their first "
                    "medication round. Night-shift patients wait an extra 30 minutes for "
                    "evening medications."
                ),
                "consequence_class": "good",
                "ripple": "Evening staff are well-prepared but late starting their rounds. Documentation quality for the evening shift is notably better than during the chaotic day shift.",
            },
            {
                "text": "Centralized cafeteria briefing (15 min) followed by unit handoffs",
                "consequence_text": (
                    "The all-hands briefing gives everyone the big picture. Evening staff ask "
                    "good questions. However, pulling all charge nurses to the cafeteria "
                    "simultaneously leaves units unstaffed for 20 minutes during a vulnerable "
                    "transition. A patient on Unit 2A falls while trying to reach the bathroom "
                    "unassisted — they are bruised but not seriously injured."
                ),
                "consequence_class": "mixed",
                "ripple": "The patient fall is a reportable event. It occurred because units were unstaffed during the centralized briefing. This will appear in the incident log.",
            },
            {
                "text": "Written handoff packets from charge nurses + phone availability",
                "consequence_text": (
                    "Charge nurses spend 45 minutes writing handoff packets — time they don't "
                    "have. The packets vary wildly in quality: Unit 3A's is detailed and clear; "
                    "Unit 5B's is a half-page of barely legible notes. Evening staff on 5B "
                    "struggle for the first 2 hours, making 3 calls to the day-shift charge "
                    "nurse who is trying to sleep."
                ),
                "consequence_class": "mixed",
                "ripple": "Handoff quality was inconsistent. The poorly documented units will generate lower-quality paper records during the evening, compounding the data integrity problem.",
            },
            {
                "text": "Staggered handoff: keep day-shift charge nurses 2 extra hours to overlap and mentor",
                "consequence_text": (
                    "The overlap is highly effective. Evening staff learn paper processes in "
                    "real-time with experienced mentors. Quality of care remains high. However, "
                    "the charge nurses have now worked 16-hour shifts. Two of them become "
                    "emotional during the overlap period. The overtime cost is €2,800 for the "
                    "2-hour extension across all units."
                ),
                "consequence_class": "good",
                "ripple": "The overlap worked beautifully for quality, but your charge nurses are now at 16 hours. When the staff morale crisis hits, they will be mentioned specifically.",
            },
        ],
    },

    "p2_paper": {
        "phase": "Phase 2: Downtime",
        "title": "Paper Records Management",
        "question": "3,200 pages of paper records, 11% unmatched. What is your strategy?",
        "options": [
            {
                "text": "Centralized staging area with HIM staff organizing and auditing in real-time",
                "consequence_text": (
                    "The staging area brings order to chaos. HIM staff catch missing identifiers "
                    "and send forms back to units for completion within hours, not days. Record "
                    "matchability improves to 96%. However, this requires 4 HIM staff working "
                    "continuously — staff who would normally be doing other work. Coding and "
                    "billing functions are completely halted."
                ),
                "consequence_class": "good",
                "ripple": "Your centralized approach means data quality is high. Back-entry will be smoother, but your revenue cycle team has been idle for 2 days — the billing backlog is growing.",
            },
            {
                "text": "Prioritize critical documentation only — defer progress notes",
                "consequence_text": (
                    "Medication records and allergy documentation are prioritized and well-maintained. "
                    "Progress notes are deferred, creating clinical continuity gaps. When a "
                    "consulting physician sees a patient on Day 2, they have no written record "
                    "of the primary team's assessment from Day 1. They must rely entirely on "
                    "verbal updates, increasing the chance of miscommunication."
                ),
                "consequence_class": "mixed",
                "ripple": "Deferred progress notes mean clinical reasoning is not documented. If any adverse event is later reviewed, there will be gaps in the medical record.",
            },
            {
                "text": "Deploy HIM staff as embedded scribes on each unit",
                "consequence_text": (
                    "Embedded scribes dramatically improve documentation quality. Nurses are "
                    "relieved of much of the paper burden. Record completeness reaches 92%. "
                    "However, HIM staff are not clinical — they sometimes record information "
                    "incorrectly because they don't understand the clinical context. Three "
                    "records have medication doses documented incorrectly (caught during "
                    "pharmacy review)."
                ),
                "consequence_class": "mixed",
                "ripple": "The scribe model worked well for completeness but introduced transcription errors. Pharmacy caught them, but it raises questions about using non-clinical staff for clinical documentation.",
            },
            {
                "text": "Photograph paper records with a dedicated hospital camera for digital backup",
                "consequence_text": (
                    "Photos provide a backup, reducing the risk of lost records. However, your "
                    "Communications & Compliance Officer raises an urgent concern: the photos "
                    "create a secondary data store of patient health information on an "
                    "unsecured device. Under GDPR, this requires the same protections as the "
                    "EHR. The camera's SD card is now a data protection liability."
                ),
                "consequence_class": "bad",
                "ripple": "You now have patient data on an SD card. If the CNIL asks about data handling during the breach, this will need to be disclosed. It may complicate your GDPR notification.",
            },
        ],
    },

    # ===== PHASE 4 =====
    "p4_media": {
        "phase": "Phase 4: Escalation",
        "title": "Media Response Strategy",
        "question": "The story is on TV. Phones are ringing. How do you respond?",
        "options": [
            {
                "text": "Hold a press conference within 2 hours — control the narrative",
                "consequence_text": (
                    "The Incident Commander delivers a composed, empathetic press conference. "
                    "Key message: patient safety is the priority, systems are being restored, "
                    "authorities are involved. Media coverage shifts from 'hospital in chaos' "
                    "to 'hospital managing crisis transparently.' However, a journalist asks "
                    "about the ransom demand — which you haven't publicly confirmed. Your "
                    "non-answer is interpreted as confirmation."
                ),
                "consequence_class": "good",
                "ripple": "The press conference was effective but the ransom question is now public. When the ransom decision comes, it will be under public scrutiny.",
            },
            {
                "text": "Written press release only — no live questions",
                "consequence_text": (
                    "The press release provides controlled, vetted information. However, "
                    "journalists interpret the refusal to take questions as evasive. The evening "
                    "news runs the story with the framing: 'Hospital refuses to answer questions "
                    "about cyberattack.' A patient advocacy group issues a statement calling "
                    "for 'full transparency, not press releases.'"
                ),
                "consequence_class": "bad",
                "ripple": "The perception of evasiveness lingers. When you eventually need public trust (for patient data notification), you'll be starting from a deficit.",
            },
            {
                "text": "Updated holding statement now; schedule full press conference for tomorrow",
                "consequence_text": (
                    "The holding statement buys time. Tomorrow's press conference allows you "
                    "to prepare thoroughly and have more complete information. Media coverage "
                    "today is neutral — 'hospital promises update tomorrow.' Patient advocacy "
                    "groups are impatient but willing to wait one more day."
                ),
                "consequence_class": "mixed",
                "ripple": "You've bought 24 hours. If tomorrow's press conference goes well, you'll be in good shape. If not, the delay will be seen as foot-dragging.",
            },
            {
                "text": "Full transparency: detailed update on website and social media",
                "consequence_text": (
                    "The detailed public update is praised by patient advocates and transparency "
                    "organizations. Media coverage is broadly positive. However, your legal "
                    "counsel is alarmed: several statements in the post could be interpreted "
                    "as admissions of negligence. The attackers also see the post and now know "
                    "exactly how far your recovery has progressed."
                ),
                "consequence_class": "mixed",
                "ripple": "Your transparency built public trust but gave the attackers intelligence about your recovery status. Legal counsel is documenting concerns for potential litigation.",
            },
        ],
    },

    "p4_family": {
        "phase": "Phase 4: Escalation",
        "title": "Family Confrontation Response",
        "question": "An angry family member is in the lobby threatening lawyers and press. Who responds?",
        "options": [
            {
                "text": "Incident Commander meets him personally with a factual but limited briefing",
                "consequence_text": (
                    "The family member is impressed that the hospital's top administrator made "
                    "time for him. The Incident Commander provides honest, empathetic information "
                    "without revealing sensitive operational details. The man calms down and "
                    "accepts a direct phone number for daily updates. He does not contact the "
                    "press. However, the Incident Commander spent 30 minutes on one family — "
                    "there are 287 families."
                ),
                "consequence_class": "good",
                "ripple": "The personal touch worked, but it's not scalable. Other families are noticing that this man got special attention. A family information line needs to be established.",
            },
            {
                "text": "Communications Officer with a prepared family info sheet and direct update number",
                "consequence_text": (
                    "The Communications Officer is professional and prepared. The family info "
                    "sheet answers most questions. The man appreciates having a number to call "
                    "but is still frustrated that 'no one in charge' came to see him. He "
                    "takes the info sheet but posts a photo of it on social media with the "
                    "caption: 'This is all the hospital will tell me about my mother.'"
                ),
                "consequence_class": "mixed",
                "ripple": "The info sheet is now on social media. It's factual and professional, so the content is fine — but it means your internal document is now public.",
            },
            {
                "text": "CNO walks him to his mother's bedside, introduces the care team",
                "consequence_text": (
                    "This is the most effective de-escalation. The man sees his mother receiving "
                    "attentive care. The bedside nurse explains what they're doing and why paper "
                    "processes are in place. He leaves satisfied and later posts a positive "
                    "update: 'My mother is being well cared for despite the circumstances. "
                    "The nurses are incredible.' The positive post generates goodwill."
                ),
                "consequence_class": "good",
                "ripple": "His positive social media post helps counter negative coverage. The bedside approach becomes a model for handling other family inquiries.",
            },
            {
                "text": "Patient advocate escorts him to a private room with a written FAQ and follow-up call",
                "consequence_text": (
                    "The patient advocate is calm and professional. The FAQ answers basic "
                    "questions. The man is partially satisfied but feels 'handled' rather "
                    "than heard. He does not contact the press today but remains dissatisfied. "
                    "He files a formal complaint with the hospital patient relations department."
                ),
                "consequence_class": "mixed",
                "ripple": "A formal complaint is now on file. It's not a crisis, but it adds to the growing pile of documentation about patient and family dissatisfaction.",
            },
        ],
    },

    "p4_staff": {
        "phase": "Phase 4: Escalation",
        "title": "Staff Morale Response",
        "question": "Marie-Claire's voicemail. Nurses calling in sick. Near-misses increasing. What do you do?",
        "options": [
            {
                "text": "Request temporary staff from neighbouring hospitals through ARS emergency protocol",
                "consequence_text": (
                    "ARS authorizes mutual aid. 8 nurses arrive from partner hospitals within "
                    "6 hours. However, they are unfamiliar with the facility, the paper forms, "
                    "and the patients. They require orientation, which takes time from your "
                    "already-stretched charge nurses. By hour 40, they are productive. "
                    "The immediate staffing crisis is averted."
                ),
                "consequence_class": "good",
                "ripple": "You have reinforcements, but onboarding temporary staff during a crisis is challenging. Documentation quality from temporary staff is lower than from regular staff.",
            },
            {
                "text": "Reduce patient census: transfer stable patients to partner facilities",
                "consequence_text": (
                    "12 stable patients are transferred over 8 hours. Each transfer requires "
                    "extensive paper documentation, a phone handoff to the receiving facility, "
                    "and ambulance coordination. The workload reduction is real — but the "
                    "transfers consume significant nursing and administrative time. Two patients "
                    "refuse transfer: 'I trust my doctor here.'"
                ),
                "consequence_class": "mixed",
                "ripple": "Your census is lower, easing staff burden. But each transfer generated additional paper records and coordination overhead. The receiving hospitals are now asking questions about your security.",
            },
            {
                "text": "Deploy CISM team and mental health resources for staff",
                "consequence_text": (
                    "The hospital's Employee Assistance Program deploys a 2-person critical "
                    "incident stress team within 4 hours. They set up a rest area with food "
                    "and quiet space. Several nurses take 20-minute breaks. Marie-Claire "
                    "speaks with a counselor and returns to her unit more composed. Staff "
                    "morale doesn't improve dramatically, but the emotional bleeding stops."
                ),
                "consequence_class": "mixed",
                "ripple": "The CISM team addresses emotional needs but doesn't solve the workload problem. Staff appreciate being seen and heard, which matters for retention after the crisis.",
            },
            {
                "text": "All of the above + shorten to 8-hour shifts + provide meals and rest areas",
                "consequence_text": (
                    "The comprehensive response is expensive (estimated €15,000/day in "
                    "additional costs) but effective. Staff feel supported. The 8-hour shifts "
                    "require a third shift cycle, complicating handoffs but reducing fatigue. "
                    "Meals in the break room become an unexpected morale boost — staff gather "
                    "and share experiences. No additional near-misses occur for the rest "
                    "of Day 2."
                ),
                "consequence_class": "good",
                "ripple": "The comprehensive response is the most effective but the most expensive. Your financial impact is growing. The board will ask about these costs.",
            },
        ],
    },

    "p4_social": {
        "phase": "Phase 4: Escalation",
        "title": "Social Media Response",
        "question": "A nurse's relative posted. Advocacy groups are demanding GDPR answers. A doctor predicts deaths. What do you do?",
        "options": [
            {
                "text": "Post an official hospital statement on social media: factual, empathetic, transparent",
                "consequence_text": (
                    "The official statement is well-received. It acknowledges the situation, "
                    "emphasizes patient safety, and provides a contact number. Engagement is "
                    "high — the post is shared 200+ times. Several commenters express support. "
                    "The nurse's relative's post is now overshadowed by the official response. "
                    "However, the comments section becomes a forum for patient complaints."
                ),
                "consequence_class": "good",
                "ripple": "Your social media presence is now active. You'll need to monitor and respond to comments — this is a sustained effort, not a one-time post.",
            },
            {
                "text": "Do not engage on social media — official channels only",
                "consequence_text": (
                    "Without an official presence, the narrative is controlled entirely by "
                    "others. The nurse's relative thread reaches 50,000 views. The advocacy "
                    "group's GDPR post is shared by 3 national media outlets. The verified "
                    "doctor's post is quoted in a Le Monde article. By evening, the dominant "
                    "narrative is 'hospital silent while patients at risk.'"
                ),
                "consequence_class": "bad",
                "ripple": "You've lost the social media narrative. When the ransom decision becomes public, you'll face a hostile information environment.",
            },
            {
                "text": "Ask the employee (through HR) to remove the relative's post",
                "consequence_text": (
                    "HR contacts the nurse. She is offended and upset — she didn't post it, "
                    "her niece did. She feels surveilled and targeted during the worst week of "
                    "her career. She tells her colleagues, and within hours, the unit views "
                    "leadership as 'more concerned about PR than about us.' Two additional "
                    "nurses request sick leave."
                ),
                "consequence_class": "bad",
                "ripple": "Attempting to suppress the post backfired. Staff trust in leadership has taken a significant hit. This will make the recovery period harder.",
            },
            {
                "text": "Engage a professional crisis communications firm (insurance may cover)",
                "consequence_text": (
                    "Your cyber insurance policy includes crisis communications coverage. A "
                    "firm is engaged within 4 hours. They draft a social media strategy, "
                    "manage responses, and begin positive narrative building. The professional "
                    "tone is noted by media as 'polished.' Some commenters view it as "
                    "'corporate crisis management' rather than genuine hospital communication."
                ),
                "consequence_class": "good",
                "ripple": "The crisis firm is effective but their presence is visible. Some media will note that the hospital hired a PR firm, which can be framed positively or negatively.",
            },
        ],
    },

    "p4_conflict": {
        "phase": "Phase 4: Escalation",
        "title": "Surgery vs. HIM Conflict",
        "question": "Resume elective surgery on paper or wait? The Chief of Surgery and HIM Director disagree.",
        "options": [
            {
                "text": "Resume elective cases with enhanced manual safety protocols and a surgical safety officer in each OR",
                "consequence_text": (
                    "Surgery resumes with dedicated safety officers. Over 2 days, 15 elective "
                    "cases are completed without incident. The surgical safety officer catches "
                    "2 potential specimen labeling errors before they happen. The HIM Director "
                    "is not happy but acknowledges the safety officer model works. The cost: "
                    "4 HIM staff redeployed to the OR, reducing paper records management capacity."
                ),
                "consequence_class": "good",
                "ripple": "Elective surgery is back, reducing patient backlog and revenue loss. But your HIM team is now split between OR safety and records management.",
            },
            {
                "text": "Delay elective surgery until basic electronic safety systems are restored",
                "consequence_text": (
                    "The Chief of Surgery is furious. Two patients with conditions worsening "
                    "from delay must be transferred to partner hospitals for their procedures. "
                    "The surgical team feels overruled and morale drops. However, no surgical "
                    "safety events occur. The wait for system restoration adds pressure to the "
                    "IT recovery timeline — 'We need the surgical module first.'"
                ),
                "consequence_class": "mixed",
                "ripple": "The surgical backlog is growing. Revenue from surgical services (a major income stream) is halted. The board will ask about this decision.",
            },
            {
                "text": "Compromise: low-risk, short-duration cases only with HIM staff in OR; defer complex cases",
                "consequence_text": (
                    "The compromise satisfies neither party fully but both accept it. 8 "
                    "low-risk cases proceed over 2 days. Complex cases (including the bowel "
                    "obstruction follow-up) are deferred. The Chief of Surgery grumbles but "
                    "cooperates. The HIM Director accepts the limited scope. Staff see "
                    "leadership finding middle ground, which helps morale."
                ),
                "consequence_class": "good",
                "ripple": "The compromise is seen as reasonable by most staff. The governance precedent — clinical and HIM voices both heard — will serve you well in recovery planning.",
            },
            {
                "text": "Emergency clinical governance meeting with surgery, HIM, nursing, and anesthesia",
                "consequence_text": (
                    "The governance meeting takes 90 minutes — time that could have been spent "
                    "on patient care. However, the collaborative process produces a detailed "
                    "protocol that all parties endorse. Surgery resumes for cases meeting "
                    "specific criteria. The protocol is documented and could serve as a model "
                    "for future downtime situations. Leadership is perceived as inclusive."
                ),
                "consequence_class": "good",
                "ripple": "The governance meeting produced a strong protocol but consumed leadership time. The protocol document will be valuable for the hospital's future preparedness planning.",
            },
        ],
    },

    # ===== PHASE 5 =====
    "p5_ransom": {
        "phase": "Phase 5: Critical Decisions",
        "title": "Ransom Demand",
        "question": "€2.5M demanded. €1M insurance limit. 180,000 records including mental health and HIV data. ANSSI says don't pay.",
        "options": [
            {
                "text": "Do not pay — follow ANSSI guidance, restore from backups, accept data exposure risk",
                "consequence_text": (
                    "You refuse to pay. Over the following weeks, the attackers publish 40,000 "
                    "patient records on the dark web, including 1,200 mental health records "
                    "and 340 HIV status records. Patient notification becomes a massive "
                    "undertaking. Several patients contact the hospital in distress. A class "
                    "action lawsuit is filed. However, ANSSI commends your decision and "
                    "provides enhanced recovery support."
                ),
                "consequence_class": "mixed",
                "ripple": "The data publication causes real harm to patients. But paying would not have guaranteed deletion — and you avoided funding the criminal enterprise.",
            },
            {
                "text": "Negotiate through a professional ransomware negotiator",
                "consequence_text": (
                    "The negotiator (covered by insurance) engages the attackers. Over 5 days, "
                    "the demand is reduced to €800,000 — within your insurance coverage. The "
                    "attackers provide a decryption key and claim to delete the exfiltrated "
                    "data. The key works. However, you have no way to verify data deletion. "
                    "ANSSI is disappointed but acknowledges the decision."
                ),
                "consequence_class": "mixed",
                "ripple": "You paid less than demanded, systems are decrypted, but you can never confirm the data was deleted. You must still proceed with GDPR notification as if data was exposed.",
            },
            {
                "text": "Pay the reduced €1.8M immediately",
                "consequence_text": (
                    "Payment is made within 12 hours. The attackers provide a decryption key "
                    "— it works for 80% of systems. The remaining 20% require manual recovery. "
                    "The attackers claim to delete the data but provide no proof. Your insurance "
                    "covers €1M; the hospital absorbs €800,000. The police report is filed as "
                    "required by Loi LOPMI. ANSSI publicly criticizes hospitals that pay ransoms."
                ),
                "consequence_class": "bad",
                "ripple": "The partial decryption means you still need backup restoration for 20% of systems. The €800K out-of-pocket cost reduces your recovery budget. And you still can't confirm data deletion.",
            },
            {
                "text": "Escalate to Ministry of Health — request emergency government intervention",
                "consequence_text": (
                    "The Ministry acknowledges the request but responds: 'Ransom decisions are "
                    "the hospital's responsibility.' They do send an additional ANSSI team and "
                    "offer to expedite backup restoration resources. The 48-hour ransom deadline "
                    "passes while you wait for a response. The attackers publish a second sample "
                    "of 2,000 records to demonstrate seriousness. The situation intensifies."
                ),
                "consequence_class": "bad",
                "ripple": "The government didn't bail you out. The published 2,000 records increase public pressure. You still need to make the underlying decision — pay or don't pay.",
            },
        ],
    },

    "p5_gdpr": {
        "phase": "Phase 5: Critical Decisions",
        "title": "GDPR Notification",
        "question": "14 hours left on the 72-hour clock. Incomplete information. What do you file?",
        "options": [
            {
                "text": "File preliminary notification NOW and supplement as forensics progresses",
                "consequence_text": (
                    "The CNIL receives your preliminary notification with 14 hours to spare. "
                    "They acknowledge receipt and assign a case officer. They appreciate the "
                    "proactive approach and the clarity about what is known vs. unknown. You "
                    "commit to supplementary filings every 48 hours as forensics progresses. "
                    "The CNIL's public response is measured: 'The hospital is cooperating.'"
                ),
                "consequence_class": "good",
                "ripple": "Your proactive filing builds regulatory goodwill. If fines are assessed, your cooperation will be a mitigating factor.",
            },
            {
                "text": "Wait for the 72-hour deadline, file the most complete report possible",
                "consequence_text": (
                    "You file at hour 71. The report is more detailed than a preliminary filing "
                    "would have been, but the CNIL notes that you used nearly the entire "
                    "window. They ask pointed questions about what you knew at hour 24 vs. "
                    "hour 71. If the filing had been even slightly late, penalties would apply."
                ),
                "consequence_class": "mixed",
                "ripple": "You're technically compliant but the CNIL is watching closely. Any future delays or omissions will be viewed unfavorably.",
            },
            {
                "text": "File CNIL notification AND begin notifying all 180,000 patients simultaneously",
                "consequence_text": (
                    "The CNIL notification is timely and thorough. However, mass patient "
                    "notification before you have complete information creates confusion. "
                    "180,000 letters go out. The hospital switchboard is overwhelmed with "
                    "calls from terrified patients. Several elderly patients call in distress. "
                    "A domestic violence survivor whose address was in the system contacts "
                    "you in panic. The notification letter didn't anticipate these scenarios."
                ),
                "consequence_class": "bad",
                "ripple": "Mass notification without careful planning caused real distress. The DV survivor situation is particularly serious — their safety may be compromised.",
            },
            {
                "text": "File CNIL notification and notify only the 500 patients whose records appeared in the proof sample",
                "consequence_text": (
                    "The CNIL notification is timely. Notifying only the confirmed 500 is "
                    "legally defensible at this stage — you've notified those you KNOW are "
                    "affected. However, if the full 180,000 records are later confirmed "
                    "exposed, those patients will ask: 'Why wasn't I told sooner?' The "
                    "approach is pragmatic but carries future risk."
                ),
                "consequence_class": "mixed",
                "ripple": "The 500 patients are notified. The remaining 179,500 are not — yet. If data is published, you'll face criticism for delayed notification. But you acted on confirmed information.",
            },
        ],
    },

    "p5_restore": {
        "phase": "Phase 5: Critical Decisions",
        "title": "System Restoration Strategy",
        "question": "Backup restore (fast, data loss), decrypt (slow, risky), new instance (clean, massive entry), or hybrid?",
        "options": [
            {
                "text": "Option A: 48-hour backup — fastest return, accept the data gap",
                "consequence_text": (
                    "EHR is restored from backup within 16 hours. Clinical staff are relieved "
                    "to have electronic systems back. However, 48 hours of pre-breach data "
                    "and 3 days of downtime data (on paper) must be entered. The back-entry "
                    "effort will take 4 weeks and cost an estimated €75,000 in temporary staff. "
                    "Some clinical decisions on Day 1 of restoration are made without complete "
                    "historical data."
                ),
                "consequence_class": "good",
                "ripple": "You're back online fastest, but the data gap creates clinical risk for the first week. The back-entry cost is significant but manageable.",
            },
            {
                "text": "Option B: Decrypt and clean — preserve data, accept extended downtime",
                "consequence_text": (
                    "Decryption begins. On Day 5, a decrypted server shows signs of a secondary "
                    "backdoor — the attackers left persistent access. IT must re-isolate and "
                    "re-clean. The process extends to Day 12 before systems are trusted. "
                    "Meanwhile, paper operations continue. Staff morale reaches its lowest "
                    "point. Two senior nurses resign. Total paper records: 14,000+ pages."
                ),
                "consequence_class": "bad",
                "ripple": "The reinfection risk materialized. 12 days of downtime created massive operational, financial, and staff retention damage. But when systems come back, all pre-breach data is preserved.",
            },
            {
                "text": "Option C: New clean instance — most secure, accept massive entry",
                "consequence_text": (
                    "A clean EHR instance is operational within 28 hours. Zero reinfection risk. "
                    "However, the system has no historical patient data — every active patient's "
                    "information must be entered from paper. For the first 48 hours, clinicians "
                    "are working in an EHR with almost no data, which feels nearly as difficult "
                    "as paper. Full data population takes 6 weeks."
                ),
                "consequence_class": "mixed",
                "ripple": "You're on the most secure platform, but the empty EHR frustrates clinicians. 'We have the system back but it knows nothing about our patients.'",
            },
            {
                "text": "Option D: Hybrid — clean instance now for active patients, backup in parallel, merge later",
                "consequence_text": (
                    "Phase 1 succeeds: active inpatients are in a clean EHR within 30 hours. "
                    "Phase 2: the backup is restored in a parallel environment within 1 week. "
                    "Phase 3 (merging) is technically challenging — the IT team discovers 340 "
                    "data conflicts between paper records, backup data, and new entries. "
                    "Full reconciliation takes 5 weeks. Total cost: €120,000. But clinical "
                    "operations return to near-normal fastest."
                ),
                "consequence_class": "good",
                "ripple": "The hybrid approach is the most expensive and complex but provides the best balance of speed, security, and data preservation. It sets a strong precedent for future incident planning.",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Action Stations — hands-on, physical activities interleaved with decisions
# ---------------------------------------------------------------------------
STATIONS = {
    # ===== PHASE 1 =====
    "s1_mar": {
        "phase": "Phase 1: The Breach",
        "title": "ACTION STATION: Design an Emergency Downtime MAR",
        "time_minutes": 8,
        "scenario": (
            "Your EHR is down. Nurses need to administer medications using paper. "
            "The pre-printed downtime forms? Stored on a server that is now encrypted. "
            "Your team must design a Medication Administration Record from scratch — "
            "right now, on blank paper. This form will be photocopied and used by every "
            "nurse in the hospital for the next 72+ hours."
        ),
        "physical_task": (
            "Stand up. Grab blank paper and markers from the supply table. "
            "Your team has 8 minutes to hand-design a paper MAR form. Think about: "
            "What fields are absolutely essential? How do you prevent the MARTIN/MARTIN "
            "confusion? Where does the double-check signature go? How do you flag allergies "
            "on paper? When you're done, bring your form back and log it below."
        ),
        "materials": ["Blank A4 paper", "Pens / markers (multiple colors)", "Ruler (optional)"],
        "capture_prompts": [
            {"key": "safety_features", "label": "What safety features did you build in?",
             "type": "text_area", "height": 100,
             "placeholder": "e.g., Red allergy alert box, two-signature line, patient photo space, second identifier requirement..."},
        ],
        "quality_checks": [
            "Full patient name (first AND last)",
            "Date of birth",
            "At least 2 unique patient identifiers",
            "Allergy field (prominently placed)",
            "Medication name, dose, route, frequency",
            "Scheduled time AND actual administration time",
            "Administering nurse signature line",
            "Second verifier signature line",
            "Date on every page",
            "Room/bed number",
        ],
    },

    "s1_bulletin": {
        "phase": "Phase 1: The Breach",
        "title": "ACTION STATION: Draft the Staff Communication Bulletin",
        "time_minutes": 6,
        "scenario": (
            "You chose a communication method — now create the actual content. "
            "1,200 staff need clear, calm, actionable instructions. Whether this is "
            "a PA script, a printed bulletin, or a verbal briefing — write the words."
        ),
        "physical_task": (
            "At your table, draft the actual communication that 1,200 staff will receive. "
            "Write it on paper first. Read it aloud to your team — does it sound calm? Clear? "
            "Does it tell people what to DO, not just what happened? Then enter your final "
            "version below."
        ),
        "materials": ["Paper", "Pen"],
        "capture_prompts": [
            {"key": "bulletin_text", "label": "Your staff communication (write the actual text):",
             "type": "text_area", "height": 180,
             "placeholder": "ATTENTION ALL STAFF: [Write the full text of your communication here. Include what happened, what to do immediately, where to find supplies, who to contact, and any patient safety reminders...]"},
            {"key": "tone_check", "label": "Read it aloud. How did it sound? What did your team change after hearing it?",
             "type": "text_area", "height": 80, "placeholder": ""},
        ],
        "quality_checks": [
            "Clear description of the situation (no jargon)",
            "Specific immediate actions for staff",
            "Location of downtime supplies/forms",
            "Emergency contact numbers",
            "Patient safety reminders",
            "Calm, authoritative tone (not alarming)",
            "Readable by ALL staff (housekeeping to surgeons)",
            "Instruction on what NOT to do (e.g., don't restart systems)",
        ],
    },

    # ===== PHASE 2 =====
    "s2_wristband": {
        "phase": "Phase 2: Downtime",
        "title": "ACTION STATION: Create Emergency Patient ID Wristband",
        "time_minutes": 6,
        "scenario": (
            "The near-miss happened because two patients named Martin were almost confused. "
            "The electronic wristband printers are down. Your team must design an emergency "
            "handwritten wristband template that prevents misidentification — especially "
            "for the 14 patients named Martin."
        ),
        "physical_task": (
            "Take a strip of paper or card stock from the supply table. Design a handwritten "
            "patient ID wristband template. What information MUST be on it? How do you make "
            "it readable, durable, and unmistakable — even at 3 AM by an exhausted nurse? "
            "Create one sample wristband for a fictional patient, then log your design below."
        ),
        "materials": ["Card stock strips (or paper cut to wristband size)", "Fine-tip markers", "Clear tape (to protect writing)"],
        "capture_prompts": [
            {"key": "martin_solution", "label": "How does your wristband solve the 14-Martins problem?",
             "type": "text_area", "height": 80,
             "placeholder": "e.g., We added a unique color-coded dot system, we require DOB + room number verbal confirmation..."},
            {"key": "durability", "label": "How did you address durability? (Water, sweat, rubbing)",
             "type": "text_area", "height": 60, "placeholder": ""},
        ],
        "quality_checks": [
            "Full legal name (first AND last)",
            "Date of birth",
            "Unique temporary identifier (not just name)",
            "Allergy indicator (visible, color-coded)",
            "Room and bed number",
            "Readable in low light",
            "Won't smudge or wash off",
            "Can be verified with a second identifier",
        ],
    },

    "s2_handoff": {
        "phase": "Phase 2: Downtime",
        "title": "ACTION STATION: Build Your Shift Handoff Tool",
        "time_minutes": 8,
        "scenario": (
            "It's 18:30. The evening shift arrives in 30 minutes. Your day shift has been "
            "running on paper for 12+ hours. Evening staff have never used paper processes. "
            "You need a standardized handoff tool — right now — that works for every unit."
        ),
        "physical_task": (
            "On paper, design a one-page shift handoff template. It must capture everything "
            "the evening shift needs to know — about patients, about paper processes, about "
            "outstanding issues, about where things are physically located. Consider using "
            "SBAR, I-PASS, or your own structure. When done, log your design below."
        ),
        "materials": ["Blank A4 paper", "Pens"],
        "capture_prompts": [],
        "quality_checks": [
            "Patient safety items (allergies, fall risks, isolation)",
            "Medication status (last doses, pending doses)",
            "Location of paper records (where are they physically?)",
            "Downtime procedure reminders",
            "Outstanding orders or pending results",
            "Staff fatigue/emotional status flags",
            "Contact info for off-going charge nurse",
            "Known issues from the day (near-misses, complaints)",
        ],
    },

    "s2_paper_record": {
        "phase": "Phase 2: Downtime",
        "title": "ACTION STATION: Complete a Paper Patient Record",
        "time_minutes": 12,
        "scenario": (
            "Your team has been making decisions about paper processes. Now experience it. "
            "A new patient is arriving: Marie DUPONT, age 74, admitted for chest pain. "
            "Allergic to penicillin. Currently takes metoprolol 50mg twice daily, "
            "lisinopril 10mg daily, and aspirin 81mg daily. She arrived by ambulance. "
            "Vitals: BP 158/92, HR 88, Temp 37.1°C, SpO2 96% on room air. "
            "She has a history of hypertension, type 2 diabetes, and a previous MI in 2019."
        ),
        "physical_task": (
            "Using ONLY blank paper (no templates, no computers), write out a complete "
            "intake record for this patient. Include everything a nurse and physician would "
            "need. Time yourselves. When finished, swap records with a teammate — can they "
            "read it? Is anything missing? Then log your experience below."
        ),
        "materials": ["Blank paper", "Pen (one color only — simulating reality)"],
        "capture_prompts": [
            {"key": "peer_review", "label": "After the swap: What did your teammate say was missing or hard to read?",
             "type": "text_area", "height": 80, "placeholder": ""},
        ],
        "quality_checks": [
            "Patient full name (spelled correctly)",
            "Date of birth",
            "Allergy (with reaction type if known)",
            "Complete medication list with doses",
            "All vitals documented with time",
            "Chief complaint",
            "Relevant medical history",
            "Arrival mode / timestamp",
            "Legible handwriting",
            "Author identification (who wrote this?)",
        ],
    },

    # ===== PHASE 4 =====
    "s4_press": {
        "phase": "Phase 4: Escalation",
        "title": "ACTION STATION: Write the Press Statement",
        "time_minutes": 8,
        "scenario": (
            "The story is on TV. Your phone is ringing. You've decided on a media strategy — "
            "now write the actual words. This statement will be quoted in news articles, "
            "posted on your website, and read aloud if you hold a press conference. "
            "Every word matters."
        ),
        "physical_task": (
            "Draft your press statement on paper first. Read it aloud to your team — does it "
            "sound like a hospital you'd trust? Is it honest without being reckless? "
            "Have one team member pretend to be a journalist and ask one tough question. "
            "Then enter your final statement below."
        ),
        "materials": ["Paper", "Pen"],
        "capture_prompts": [
            {"key": "not_saying", "label": "What are you deliberately NOT saying in this statement, and why?",
             "type": "text_area", "height": 80, "placeholder": "e.g., We are not confirming the ransom because... We are not disclosing the attack vector because..."},
        ],
        "quality_checks": [
            "Acknowledges the situation (doesn't deny)",
            "Leads with patient safety",
            "Provides specific actions being taken",
            "Includes contact information for updates",
            "Professional but empathetic tone",
            "Avoids technical jargon",
            "Does not speculate on scope or blame",
            "Does not make promises you can't keep",
        ],
    },

    "s4_family_letter": {
        "phase": "Phase 4: Escalation",
        "title": "ACTION STATION: Create the Family Information Sheet",
        "time_minutes": 7,
        "scenario": (
            "The angry family member was the first. He will not be the last. You need a "
            "printed information sheet that can be handed to every family member who arrives "
            "at the hospital asking questions. It needs to be honest, empathetic, and complete "
            "— without revealing sensitive operational or security details."
        ),
        "physical_task": (
            "Write a one-page family information sheet. Include FAQs with answers. "
            "Remember: these families are scared. Some are elderly. Some don't speak French "
            "as a first language. Keep it simple, warm, and truthful. Hand it to a teammate "
            "and ask: 'If your parent were in this hospital, would this sheet reassure you?' "
            "Then log your work below."
        ),
        "materials": ["Paper", "Pen"],
        "capture_prompts": [],
        "quality_checks": [
            "Empathetic opening (not corporate/legal)",
            "Honest about the situation",
            "Clear about what IS being done for patient safety",
            "Includes how to get updates (phone, website, in-person)",
            "Addresses data privacy concerns",
            "Does NOT over-promise on timeline",
            "Readable by non-medical audience",
            "Available in multiple languages (noted if not provided)",
        ],
    },

    # ===== PHASE 5 =====
    "s5_board_memo": {
        "phase": "Phase 5: Critical Decisions",
        "title": "ACTION STATION: Draft the Board Recommendation Memo",
        "time_minutes": 8,
        "scenario": (
            "The hospital board meets in 2 hours to decide on the ransom. Your team has made "
            "its recommendation — now write the formal memo that will be presented. "
            "Board members include: the hospital CEO, CFO, Chief Medical Officer, "
            "General Counsel, patient representative, and two community members. "
            "Not all of them understand cybersecurity. All of them understand money and risk."
        ),
        "physical_task": (
            "Write a one-page executive memo. Structure it clearly: situation, options, "
            "your recommendation, rationale, risks, and financial implications. "
            "This is a formal document that may become a legal record. Choose your words "
            "carefully. Then enter it below."
        ),
        "materials": ["Paper", "Pen"],
        "capture_prompts": [],
        "quality_checks": [
            "Clear situation summary (accessible to non-technical readers)",
            "All options presented (not just the recommended one)",
            "Recommendation is explicit and unambiguous",
            "Ethical considerations addressed",
            "Financial impact quantified",
            "Legal implications noted",
            "Patient impact described",
            "Risk of each option acknowledged",
        ],
    },

    "s5_cnil": {
        "phase": "Phase 5: Critical Decisions",
        "title": "ACTION STATION: Complete the CNIL Breach Notification",
        "time_minutes": 10,
        "scenario": (
            "GDPR Article 33 requires notification to the CNIL within 72 hours. "
            "You have 14 hours left. This is a regulatory filing with legal consequences. "
            "Incomplete or inaccurate information can result in fines. But you don't have "
            "complete information yet. You must clearly distinguish what you KNOW from "
            "what you DON'T KNOW."
        ),
        "physical_task": (
            "Complete the CNIL breach notification form below. This simulates the actual "
            "French regulatory filing. For each field, enter what you know — and explicitly "
            "note what is still unknown. In the real world, this document is a legal record."
        ),
        "materials": ["(This station is completed in the app — it simulates a regulatory form)"],
        "capture_prompts": [
            {"key": "org_details", "label": "Organization Details (name, address, DPO contact):",
             "type": "text_area", "height": 60,
             "placeholder": "Centre Hospitalier Sainte-Claire, [address], DPO: [name, contact]"},
            {"key": "breach_nature", "label": "Nature of the Breach (what happened, how, when discovered):",
             "type": "text_area", "height": 100,
             "placeholder": "Ransomware attack (LockBit variant) discovered Monday 06:12. Initial access via phishing email to radiology technician approximately 11 days prior..."},
            {"key": "data_categories", "label": "Categories of Personal Data Affected:",
             "type": "text_area", "height": 100,
             "placeholder": "Confirmed: demographics, diagnoses, medications, lab results, national ID numbers\nSuspected: mental health records, HIV status, imaging reports\nUnknown: [list what you don't yet know]"},
            {"key": "affected_count", "label": "Estimated Number of Affected Data Subjects:",
             "type": "text_area", "height": 60,
             "placeholder": "Estimated: ... Confirmed from sample: ... Basis for estimate: ..."},
            {"key": "measures_taken", "label": "Measures Taken So Far to Address the Breach:",
             "type": "text_area", "height": 100,
             "placeholder": "1. Network isolation at 06:45\n2. ANSSI notified at 07:05\n3. Forensic investigation initiated...\n4. Downtime procedures activated..."},
            {"key": "measures_planned", "label": "Measures Planned (what you will do next):",
             "type": "text_area", "height": 80,
             "placeholder": "1. Complete forensic scope assessment\n2. Individual patient notification (pending scope confirmation)..."},
            {"key": "unknown_items", "label": "CRITICAL: What Is Still Unknown (be honest — this protects you legally):",
             "type": "text_area", "height": 100,
             "placeholder": "1. Full scope of exfiltrated data\n2. Whether attackers still have network access\n3. Complete list of affected data categories..."},
        ],
        "quality_checks": [
            "Organization and DPO clearly identified",
            "Breach timeline accurate (discovery, containment, notification)",
            "Data categories specifically named (not vague)",
            "Estimated scope with basis for estimate",
            "Concrete containment measures listed",
            "Forward-looking measures planned",
            "UNKNOWN items explicitly listed (this is critical)",
            "Supplementary filing timeline committed to",
        ],
    },

    # ===== PHASE 6 =====
    "s6_backentry": {
        "phase": "Phase 6: Recovery",
        "title": "ACTION STATION: Design the Back-Entry Workflow",
        "time_minutes": 8,
        "scenario": (
            "Systems are coming back online. You now face 6,400+ pages of paper records "
            "that must be entered into the EHR. 11% can't be matched to a patient. "
            "34% are missing date of birth. 18% are partially illegible. "
            "This will take weeks and cost tens of thousands of euros. "
            "Design the process."
        ),
        "physical_task": (
            "On paper, map out the back-entry workflow from start to finish. "
            "Who does the entry? How do you prioritize? What quality checks exist? "
            "How do you handle the 11% unmatched records? Draw a flowchart or write "
            "numbered steps. Then log your design below."
        ),
        "materials": ["Large paper or whiteboard", "Markers"],
        "capture_prompts": [
            {"key": "priority_order", "label": "Priority order for back-entry (what gets entered first and why):",
             "type": "text_area", "height": 120,
             "placeholder": "1. Active inpatient medications (patient safety)\n2. Lab results pending action\n3. Surgical/procedure notes\n4. ..."},
            {"key": "workflow_steps", "label": "Back-entry workflow steps (from paper to EHR):",
             "type": "text_area", "height": 150,
             "placeholder": "Step 1: Sort paper records by unit and date\nStep 2: Match to patient using [identifiers]\nStep 3: ...\nStep 4: QA check by...\nStep 5: ..."},
            {"key": "qa_process", "label": "Quality assurance: How do you verify accuracy of back-entered data?",
             "type": "text_area", "height": 80,
             "placeholder": "e.g., Second-person verification, spot audits of 10%, pharmacist review of medication entries..."},
            {"key": "unmatched_plan", "label": "The 11% problem: How do you handle records that can't be matched to a patient?",
             "type": "text_area", "height": 80,
             "placeholder": ""},
            {"key": "staffing", "label": "Staffing plan: Who does this work? How long will it take?",
             "type": "text_area", "height": 80, "placeholder": ""},
        ],
        "quality_checks": [
            "Priority based on patient safety (not convenience)",
            "Clear workflow with defined steps",
            "QA/verification process at each stage",
            "Plan for unmatched records (not just 'discard')",
            "Staffing plan (who, how many, how long)",
            "Error handling (what if back-entry creates a conflict?)",
            "Timeline estimate",
            "Cost estimate considered",
        ],
    },
}

# ---------------------------------------------------------------------------
# Phase flow — interleaves decisions and stations
# ---------------------------------------------------------------------------
PHASE_FLOW = {
    1: [
        ("decision", "p1_priority"),
        ("station", "s1_mar"),
        ("decision", "p1_communication"),
        ("station", "s1_bulletin"),
        ("decision", "p1_safety"),
    ],
    2: [
        ("decision", "p2_medication"),
        ("station", "s2_wristband"),
        ("decision", "p2_diversion"),
        ("decision", "p2_handoff"),
        ("station", "s2_handoff"),
        ("decision", "p2_paper"),
        ("station", "s2_paper_record"),
    ],
    4: [
        ("decision", "p4_media"),
        ("station", "s4_press"),
        ("decision", "p4_family"),
        ("station", "s4_family_letter"),
        ("decision", "p4_staff"),
        ("decision", "p4_social"),
        ("decision", "p4_conflict"),
    ],
    5: [
        ("decision", "p5_ransom"),
        ("station", "s5_board_memo"),
        ("decision", "p5_gdpr"),
        ("station", "s5_cnil"),
        ("decision", "p5_restore"),
    ],
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def get_decision(decision_id):
    return DECISIONS[decision_id]

def save_choice(decision_id, option_index, justification):
    st.session_state.decisions[decision_id] = option_index
    st.session_state.justifications[decision_id] = justification
    d = DECISIONS[decision_id]
    st.session_state.log.append({
        "phase": d["phase"],
        "context": d["title"],
        "choice": d["options"][option_index]["text"],
        "justification": justification,
        "time": datetime.now().strftime("%H:%M:%S"),
    })

def has_decided(decision_id):
    return decision_id in st.session_state.decisions

def get_consequence(decision_id):
    if not has_decided(decision_id):
        return None
    idx = st.session_state.decisions[decision_id]
    return DECISIONS[decision_id]["options"][idx]

def render_consequence(decision_id):
    """Show the consequence of a previous decision."""
    c = get_consequence(decision_id)
    if c is None:
        return
    cls = c["consequence_class"]
    d = DECISIONS[decision_id]
    st.markdown(f"**Result of your decision: {d['title']}**")
    st.markdown(
        f'<div class="consequence-{cls}">{c["consequence_text"]}</div>',
        unsafe_allow_html=True,
    )
    if c.get("ripple"):
        st.markdown(
            f'<div class="ripple-box"><strong>Ripple Effect:</strong> {c["ripple"]}</div>',
            unsafe_allow_html=True,
        )

def render_decision(decision_id):
    """Render a decision form or its locked-in result."""
    d = DECISIONS[decision_id]

    if has_decided(decision_id):
        idx = st.session_state.decisions[decision_id]
        chosen = d["options"][idx]
        st.success(f"**{d['title']}** — Locked in: {chosen['text'][:80]}...")
        render_consequence(decision_id)
        return True

    st.markdown(f"### {d['title']}")
    st.markdown(f"**{d['question']}**")

    option_texts = [o["text"] for o in d["options"]]
    choice = st.radio("Select your team's decision:", option_texts,
                      key=f"radio_{decision_id}", index=None)

    justification = st.text_area("Team justification:",
                                  key=f"just_{decision_id}", height=80)

    if st.button(f"Lock in: {d['title']}", key=f"btn_{decision_id}", type="primary"):
        if choice is not None:
            idx = option_texts.index(choice)
            save_choice(decision_id, idx, justification)
            st.rerun()
        else:
            st.warning("Select an option before locking in.")
    return False


def has_station_complete(station_id):
    return st.session_state.stations_complete.get(station_id, False)


def render_station(station_id):
    """Render an action station activity or its completed state."""
    s = STATIONS[station_id]

    if has_station_complete(station_id):
        st.markdown(
            f'<div class="station-complete"><strong>{s["title"]}</strong> — Completed</div>',
            unsafe_allow_html=True,
        )
        with st.expander("View your station deliverable", expanded=False):
            data = st.session_state.station_data.get(station_id, {})
            for prompt in s["capture_prompts"]:
                val = data.get(prompt["key"], "")
                if val:
                    st.markdown(f"**{prompt['label']}**")
                    st.markdown(val)
        return True

    # --- Active station ---
    st.markdown(
        f'<div class="station-banner">'
        f'<h3>{s["title"]}</h3>'
        f'<div class="station-time">{s["time_minutes"]} MINUTES</div>'
        f'<p>{s["scenario"]}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="station-task"><strong>Your task:</strong><br>{s["physical_task"]}</div>',
        unsafe_allow_html=True,
    )

    materials_html = " &bull; ".join(s["materials"])
    st.markdown(
        f'<div class="station-materials"><strong>Materials needed:</strong> {materials_html}</div>',
        unsafe_allow_html=True,
    )

    field_values = {}
    if s["capture_prompts"]:
        st.markdown("---")
        st.markdown("#### Log Your Work")
        for prompt in s["capture_prompts"]:
            val = st.text_area(
                prompt["label"],
                key=f"station_{station_id}_{prompt['key']}",
                height=prompt.get("height", 100),
                placeholder=prompt.get("placeholder", ""),
            )
            field_values[prompt["key"]] = val

    # Has at least one capture field filled (or no fields required)?
    any_filled = not s["capture_prompts"] or any(v.strip() for v in field_values.values())

    st.markdown("---")
    if st.button(f"Complete Station: {s['title'].replace('ACTION STATION: ', '')}",
                 key=f"btn_station_{station_id}", type="primary"):
        if any_filled:
            st.session_state.stations_complete[station_id] = True
            st.session_state.station_data[station_id] = field_values
            st.session_state.station_checks[station_id] = []
            st.session_state.log.append({
                "phase": s["phase"],
                "context": f"Station: {s['title']}",
                "choice": "Completed",
                "justification": "",
                "time": datetime.now().strftime("%H:%M:%S"),
            })
            st.rerun()
        else:
            st.warning("Enter at least one response before completing the station.")
    return False


# ---------------------------------------------------------------------------
# Phase renderers
# ---------------------------------------------------------------------------
PHASE_DECISIONS = {
    1: ["p1_priority", "p1_communication", "p1_safety"],
    2: ["p2_medication", "p2_diversion", "p2_handoff", "p2_paper"],
    4: ["p4_media", "p4_family", "p4_staff", "p4_social", "p4_conflict"],
    5: ["p5_ransom", "p5_gdpr", "p5_restore"],
}


def render_setup():
    st.markdown("## Team Setup")
    team = st.text_input("Team Name", value=st.session_state.team_name, key="tn")
    if team:
        st.session_state.team_name = team

    if team:
        st.success(f"Team **{team}**")
        if st.button("Ready — Waiting for instructor to begin", type="primary", use_container_width=True):
            st.session_state.current_phase = 1
            st.rerun()
    else:
        st.info("Enter your team name.")


def render_decision_phase(phase_num, title, subtitle):
    st.markdown(f'<h2 class="phase-header">{title}</h2>', unsafe_allow_html=True)
    st.caption(subtitle)

    # Show consequences from earlier phases first
    if phase_num == 2 and any(has_decided(d) for d in PHASE_DECISIONS.get(1, [])):
        with st.expander("Consequences from Phase 1", expanded=False):
            for did in PHASE_DECISIONS[1]:
                render_consequence(did)
                st.markdown("---")

    if phase_num == 4 and any(has_decided(d) for d in PHASE_DECISIONS.get(2, [])):
        with st.expander("Consequences from Phase 2 (Downtime)", expanded=False):
            for did in PHASE_DECISIONS[2]:
                render_consequence(did)
                st.markdown("---")

    if phase_num == 5 and any(has_decided(d) for d in PHASE_DECISIONS.get(4, [])):
        with st.expander("Consequences from Phase 4 (Escalation)", expanded=False):
            for did in PHASE_DECISIONS[4]:
                render_consequence(did)
                st.markdown("---")

    # Show ripple effects from earlier decisions relevant to current phase
    if phase_num >= 4:
        earlier_ripples = []
        for earlier_phase in [1, 2]:
            for did in PHASE_DECISIONS.get(earlier_phase, []):
                c = get_consequence(did)
                if c and c.get("ripple"):
                    earlier_ripples.append((DECISIONS[did]["title"], c["ripple"]))
        if earlier_ripples:
            st.markdown("### Active Ripple Effects from Your Earlier Decisions")
            for title_text, ripple in earlier_ripples:
                st.markdown(
                    f'<div class="ripple-box"><strong>{title_text}:</strong> {ripple}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("---")

    if phase_num == 5:
        earlier_ripples = []
        for did in PHASE_DECISIONS.get(4, []):
            c = get_consequence(did)
            if c and c.get("ripple"):
                earlier_ripples.append((DECISIONS[did]["title"], c["ripple"]))
        if earlier_ripples:
            st.markdown("### Active Ripple Effects from Escalation Phase")
            for title_text, ripple in earlier_ripples:
                st.markdown(
                    f'<div class="ripple-box"><strong>{title_text}:</strong> {ripple}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("---")

    # Render decisions AND stations in flow order
    flow = PHASE_FLOW.get(phase_num, [])
    all_done = True
    for item_type, item_id in flow:
        st.markdown("---")
        if item_type == "decision":
            done = render_decision(item_id)
        else:  # station
            done = render_station(item_id)
        if not done:
            all_done = False
            break  # Show one uncompleted item at a time

    if all_done:
        st.markdown("---")
        st.success("All decisions and stations for this phase are complete. Wait for the instructor to advance.")
        next_phase = {1: 2, 2: 3, 4: 5, 5: 6}
        if phase_num in next_phase:
            if st.button("Proceed to next phase", type="primary", use_container_width=True):
                st.session_state.current_phase = next_phase[phase_num]
                st.rerun()


def render_break():
    st.markdown("## Break Time")
    st.markdown("Review your decisions and consequences so far.")

    for phase_num in [1, 2]:
        st.markdown(f"### Phase {phase_num} Decisions")
        for did in PHASE_DECISIONS.get(phase_num, []):
            if has_decided(did):
                d = DECISIONS[did]
                idx = st.session_state.decisions[did]
                with st.expander(f"{d['title']}: {d['options'][idx]['text'][:60]}..."):
                    render_consequence(did)
        st.markdown("---")

    st.markdown(f"**Decisions logged:** {len(st.session_state.log)}")

    if st.button("Resume", type="primary", use_container_width=True):
        st.session_state.current_phase = 4
        st.rerun()


def render_recovery():
    st.markdown('<h2 class="phase-header">Recovery Planning</h2>', unsafe_allow_html=True)
    st.caption("Hour 72+ — Complete your after-action summary")

    # Back-entry workflow station
    st.markdown("---")
    render_station("s6_backentry")

    # Show all consequences
    with st.expander("Full Decision & Consequence Timeline", expanded=False):
        for phase_num in [1, 2, 4, 5]:
            st.markdown(f"### Phase {phase_num}")
            for did in PHASE_DECISIONS.get(phase_num, []):
                render_consequence(did)
                st.markdown("---")

    # Show all station deliverables
    completed_stations = [sid for sid in STATIONS if has_station_complete(sid)]
    if completed_stations:
        with st.expander("All Station Deliverables", expanded=False):
            for sid in completed_stations:
                s = STATIONS[sid]
                st.markdown(f"#### {s['title']}")
                data = st.session_state.station_data.get(sid, {})
                for prompt in s["capture_prompts"]:
                    val = data.get(prompt["key"], "")
                    if val:
                        st.markdown(f"**{prompt['label']}**")
                        st.markdown(val)
                st.markdown("---")

    # Collect all ripple effects
    all_ripples = []
    for phase_num in [1, 2, 4, 5]:
        for did in PHASE_DECISIONS.get(phase_num, []):
            c = get_consequence(did)
            if c and c.get("ripple"):
                all_ripples.append((DECISIONS[did]["title"], c["ripple"]))

    if all_ripples:
        st.markdown("### All Ripple Effects from Your Decisions")
        for title_text, ripple in all_ripples:
            st.markdown(
                f'<div class="ripple-box"><strong>{title_text}:</strong> {ripple}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### After-Action Summary")

    st.text_area("1. What was the single most important decision your team made? Why?",
                  key="aa1", height=100)
    st.text_area("2. Which decision would you change? What would you do differently?",
                  key="aa2", height=100)
    st.text_area("3. Which role had the most difficult job? Why?",
                  key="aa3", height=100)
    st.text_area("4. What is one thing about cybersecurity in healthcare you didn't appreciate before?",
                  key="aa4", height=100)
    st.text_area("5. Your top 3 recommendations for hospital cybersecurity preparedness:",
                  key="aa5", height=100)

    st.markdown("---")
    if st.button("Export Team Report", type="primary"):
        now = datetime.now()
        after_action = {f"q{i}": st.session_state.get(f"aa{i}", "") for i in range(1, 6)}

        # Build structured data
        decisions_data = []
        for did, idx in st.session_state.decisions.items():
            d = DECISIONS[did]
            opt = d["options"][idx]
            decisions_data.append({
                "phase": d["phase"],
                "title": d["title"],
                "question": d["question"],
                "choice": opt["text"],
                "consequence": opt["consequence_text"],
                "ripple": opt.get("ripple", ""),
                "justification": st.session_state.justifications.get(did, ""),
            })
        stations_data = []
        for sid in STATIONS:
            if has_station_complete(sid):
                s = STATIONS[sid]
                data = st.session_state.station_data.get(sid, {})
                stations_data.append({
                    "station_id": sid,
                    "phase": s["phase"],
                    "title": s["title"],
                    "deliverables": data,
                    "prompts": s["capture_prompts"],
                })

        # --- JSON report ---
        report_json = json.dumps({
            "team_name": st.session_state.team_name,
            "exported_at": now.isoformat(),
            "decisions": decisions_data,
            "stations": [
                {"station_id": s["station_id"], "phase": s["phase"],
                 "title": s["title"], "deliverables": s["deliverables"]}
                for s in stations_data
            ],
            "after_action": after_action,
        }, indent=2, ensure_ascii=False)

        # --- Readable text report ---
        sep = "=" * 60
        thin = "-" * 40
        aa_questions = [
            "What was the single most important decision your team made? Why?",
            "Which decision would you change? What would you do differently?",
            "Which role had the most difficult job? Why?",
            "What is one thing about cybersecurity in healthcare you didn't appreciate before?",
            "Your top 3 recommendations for hospital cybersecurity preparedness:",
        ]
        lines = [
            "SHIFT CYBERSECURITY SIMULATION — TEAM RESPONSE REPORT",
            sep,
            f"Team:      {st.session_state.team_name}",
            f"Exported:  {now.strftime('%Y-%m-%d %H:%M')}",
            "",
        ]

        lines += [sep, "DECISIONS & JUSTIFICATIONS", sep, ""]
        current_phase = None
        for entry in decisions_data:
            if entry["phase"] != current_phase:
                current_phase = entry["phase"]
                lines += [f"[ {current_phase} ]", ""]
            lines += [
                f"DECISION: {entry['title']}",
                f"Question: {entry['question']}",
                thin,
                f"Team chose: {entry['choice']}",
                "",
                f"Justification:",
                entry["justification"] if entry["justification"].strip() else "(none provided)",
                "",
                f"Consequence: {entry['consequence']}",
                f"Ripple effect: {entry['ripple']}" if entry["ripple"] else "",
                "",
            ]

        lines += [sep, "ACTION STATION DELIVERABLES", sep, ""]
        for s in stations_data:
            lines += [f"STATION: {s['title']}", f"Phase: {s['phase']}", thin]
            prompts_by_key = {p["key"]: p["label"] for p in s["prompts"]}
            if s["deliverables"]:
                for key, label in prompts_by_key.items():
                    val = s["deliverables"].get(key, "").strip()
                    lines += [
                        f"{label}",
                        val if val else "(no response)",
                        "",
                    ]
            else:
                lines.append("(no capture fields for this station)")
            lines.append("")

        lines += [sep, "AFTER-ACTION REFLECTION", sep, ""]
        for i, question in enumerate(aa_questions, 1):
            answer = after_action.get(f"q{i}", "").strip()
            lines += [
                f"Q{i}. {question}",
                answer if answer else "(no response)",
                "",
            ]

        report_text = "\n".join(lines)

        # Save to Google Sheets (primary — works on Streamlit Community Cloud)
        sheet_saved = _save_to_gsheet(st.session_state.team_name, report_text)

        # Local filesystem fallback (useful when running the app locally)
        safe_name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in st.session_state.team_name).strip()
        save_path = os.path.join(SUBMISSIONS_DIR, f"{safe_name}.json")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(report_json)

        if sheet_saved:
            st.success("✅ Report submitted to instructor. Your responses have been recorded.")
        else:
            st.warning(
                "⚠️ Could not submit automatically. "
                "Please download the report below and email it to your instructor."
            )

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📄 Download Readable Report (.txt)",
                data=report_text.encode("utf-8"),
                file_name=f"SHIFT_Cyber_{st.session_state.team_name}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col2:
            st.download_button(
                "⬇ Download Raw Data (JSON)",
                data=report_json,
                file_name=f"SHIFT_Cyber_{st.session_state.team_name}.json",
                mime="application/json",
                use_container_width=True,
            )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown("## Team Response App")
        if st.session_state.team_name:
            st.markdown(f"**Team:** {st.session_state.team_name}")
        if st.session_state.team_role != "Not Selected":
            st.markdown(f"**Role:** {st.session_state.team_role}")

        st.markdown("---")
        st.markdown("### Phases")
        phase_labels = {
            0: "Setup", 1: "The Breach", 2: "Downtime",
            3: "Break", 4: "Escalation", 5: "Critical Decisions", 6: "Recovery",
        }
        for i, label in phase_labels.items():
            if i == st.session_state.current_phase:
                st.markdown(f"**>> {label}**")
            elif i <= st.session_state.current_phase:
                if st.button(label, key=f"nav_{i}"):
                    st.session_state.current_phase = i
                    st.rerun()
            else:
                st.markdown(f"*{label}*")

        st.markdown("---")
        st.markdown(f"**Decisions made:** {len(st.session_state.decisions)} / {len(DECISIONS)}")
        stations_done = sum(1 for s in STATIONS if has_station_complete(s))
        st.markdown(f"**Stations completed:** {stations_done} / {len(STATIONS)}")

        # Consequence summary
        good = sum(1 for did in st.session_state.decisions
                    if DECISIONS[did]["options"][st.session_state.decisions[did]]["consequence_class"] == "good")
        mixed = sum(1 for did in st.session_state.decisions
                     if DECISIONS[did]["options"][st.session_state.decisions[did]]["consequence_class"] == "mixed")
        bad = sum(1 for did in st.session_state.decisions
                   if DECISIONS[did]["options"][st.session_state.decisions[did]]["consequence_class"] == "bad")
        if st.session_state.decisions:
            st.markdown("### Outcome Summary")
            st.markdown(f"- Favorable: **{good}**")
            st.markdown(f"- Mixed: **{mixed}**")
            st.markdown(f"- Unfavorable: **{bad}**")

        st.markdown("---")
        if st.button("Reset All", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    render_sidebar()

    phase = st.session_state.current_phase

    if phase == 0:
        render_setup()
    elif phase == 1:
        render_decision_phase(1, "Phase 1: The Breach (Hour 0–2)",
                              "Watch the instructor projection, then log your decisions here.")
    elif phase == 2:
        render_decision_phase(2, "Phase 2: Downtime Operations (Hour 2–24)",
                              "Respond to inject events as the instructor presents them.")
    elif phase == 3:
        render_break()
    elif phase == 4:
        render_decision_phase(4, "Phase 4: Escalation & Pressure (Hour 24–48)",
                              "The pressure mounts. Media, families, staff, departments in conflict.")
    elif phase == 5:
        render_decision_phase(5, "Phase 5: Critical Decisions (Hour 48–72)",
                              "Ransom. GDPR. Restoration. The hardest choices.")
    elif phase == 6:
        render_recovery()


if __name__ == "__main__":
    main()
