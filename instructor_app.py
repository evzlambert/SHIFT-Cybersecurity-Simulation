"""
SHIFT Cybersecurity Breach Simulation — Instructor Projection App ("The Broadcast")
Saint-Etienne, France

Cinematic projection app with narrated audio, animated text reveals,
and sound cues. Run on the classroom projector.

Launch:  python3 -m streamlit run instructor_app.py
Audio:   Ensure audio/ directory contains slide_00.mp3 through slide_34.mp3
         (generate with: python3 generate_audio.py)
"""

import streamlit as st
import base64
import csv
import io
import json
import os

SUBMISSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions")

st.set_page_config(
    page_title="SHIFT Cyber Sim — Instructor Broadcast",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

# ---------------------------------------------------------------------------
# CSS — cinematic, projection-optimized, with animations
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #0a0a1a; }
    .block-container { max-width: 1200px; }
    #MainMenu, footer, header { visibility: hidden; }

    /* Fade-in animation for all slide content */
    .slide-content {
        animation: fadeIn 1.2s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Staggered fade-in for events */
    .event-card {
        background-color: #1a1a2e;
        border-left: 5px solid #e94560;
        padding: 18px 24px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        font-size: 1.25em;
        color: #e0e0f0;
        line-height: 1.5;
        animation: slideIn 0.8s ease-out both;
    }
    .event-card:nth-child(1) { animation-delay: 0.3s; }
    .event-card:nth-child(2) { animation-delay: 0.8s; }
    .event-card:nth-child(3) { animation-delay: 1.3s; }
    .event-card:nth-child(4) { animation-delay: 1.8s; }
    .event-card:nth-child(5) { animation-delay: 2.3s; }
    .event-card:nth-child(6) { animation-delay: 2.8s; }
    .event-card:nth-child(7) { animation-delay: 3.3s; }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .event-card.warning { border-left-color: #ffa726; }
    .event-card.info { border-left-color: #29b6f6; }

    .event-time {
        color: #e94560; font-weight: bold;
        font-family: 'Courier New', monospace; font-size: 1.1em;
    }
    .event-time.warning { color: #ffa726; }
    .event-time.info { color: #29b6f6; }

    /* Broadcast header */
    .broadcast-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #e94560;
        border-radius: 12px;
        padding: 20px 30px;
        text-align: center;
        margin-bottom: 20px;
        animation: fadeIn 1.5s ease-in;
    }
    .broadcast-header h1 {
        color: #e94560; font-size: 2.2em; margin: 0; letter-spacing: 2px;
    }
    .broadcast-header p {
        color: #a0a0c0; font-size: 1.1em; margin: 5px 0 0 0;
    }

    /* Crisis banner */
    .crisis-banner {
        background-color: #b71c1c;
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.8em;
        font-weight: bold;
        letter-spacing: 2px;
        animation: pulse 2s infinite;
        margin: 20px 0;
    }
    @keyframes pulse { 0%{opacity:1} 50%{opacity:0.75} 100%{opacity:1} }

    /* Pause screen */
    .pause-screen {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 16px;
        text-align: center;
        margin: 30px 0;
        font-size: 1.5em;
        border: 3px solid #4caf50;
        animation: fadeIn 1s ease-in;
    }
    .pause-screen h2 {
        font-size: 2em; margin-bottom: 20px; letter-spacing: 3px;
        animation: glowGreen 2s ease-in-out infinite;
    }
    @keyframes glowGreen {
        0%, 100% { text-shadow: 0 0 10px rgba(76, 175, 80, 0.5); }
        50% { text-shadow: 0 0 25px rgba(76, 175, 80, 0.8), 0 0 50px rgba(76, 175, 80, 0.3); }
    }
    .pause-screen .prompt {
        font-size: 0.85em; color: #c8e6c9; margin-top: 15px; font-style: italic;
    }

    /* Break screen */
    .break-screen {
        background: linear-gradient(135deg, #4a148c 0%, #7b1fa2 100%);
        color: white; padding: 80px 40px; border-radius: 16px;
        text-align: center; margin: 30px 0; border: 3px solid #ce93d8;
        animation: fadeIn 2s ease-in;
    }
    .break-screen h1 { font-size: 3em; letter-spacing: 4px; }
    .break-screen p { font-size: 1.3em; color: #e1bee7; margin-top: 20px; }

    /* News ticker */
    .news-ticker {
        background-color: #1a1a2e;
        border: 2px solid #e94560;
        border-radius: 10px;
        padding: 25px 30px;
        margin: 15px 0;
        font-size: 1.3em;
        color: #e0e0f0;
        line-height: 1.6;
        animation: fadeIn 1.5s ease-in;
    }
    .news-ticker .source {
        color: #e94560; font-weight: bold; font-size: 0.9em;
        text-transform: uppercase; letter-spacing: 1px;
        animation: tickerFlash 3s ease-in-out infinite;
    }
    @keyframes tickerFlash {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* Voicemail */
    .voicemail {
        background-color: #1a1a2e;
        border: 2px solid #ffa726;
        border-radius: 10px;
        padding: 25px 30px;
        margin: 15px 0;
        font-size: 1.2em;
        color: #ffe0b2;
        font-style: italic;
        line-height: 1.6;
        animation: fadeIn 1.5s ease-in;
    }
    .voicemail .label {
        color: #ffa726; font-weight: bold; font-style: normal;
        font-size: 0.9em; text-transform: uppercase;
    }

    /* Social post */
    .social-post {
        background-color: #1a1a2e;
        border: 2px solid #42a5f5;
        border-radius: 10px;
        padding: 20px 25px;
        margin: 10px 0;
        font-size: 1.15em;
        color: #bbdefb;
        line-height: 1.5;
    }
    .social-post:nth-child(1) { animation: slideIn 0.8s ease-out 0.5s both; }
    .social-post:nth-child(2) { animation: slideIn 0.8s ease-out 1.5s both; }
    .social-post:nth-child(3) { animation: slideIn 0.8s ease-out 2.5s both; }
    .social-post .handle { color: #42a5f5; font-weight: bold; }

    /* Scene */
    .scene {
        background-color: #1a1a2e;
        border: 2px solid #ab47bc;
        border-radius: 10px;
        padding: 25px 30px;
        margin: 15px 0;
        font-size: 1.2em;
        color: #e1bee7;
        line-height: 1.6;
        animation: fadeIn 1.5s ease-in;
    }
    .scene .label {
        color: #ab47bc; font-weight: bold; font-style: normal;
        font-size: 0.9em; text-transform: uppercase;
    }

    /* Phase titles */
    .phase-title {
        color: #e94560;
        font-size: 2.5em;
        text-align: center;
        letter-spacing: 3px;
        margin: 30px 0 10px 0;
        text-transform: uppercase;
        animation: fadeIn 1s ease-in;
    }
    .phase-subtitle {
        color: #a0a0c0; font-size: 1.2em;
        text-align: center; margin-bottom: 30px;
        animation: fadeIn 1.2s ease-in;
    }

    /* Decision prompt */
    .decision-prompt {
        background: linear-gradient(135deg, #1a1a2e 0%, #0d47a1 100%);
        border: 2px solid #42a5f5;
        border-radius: 12px;
        padding: 25px 30px;
        margin: 15px 0;
        font-size: 1.3em;
        color: #bbdefb;
        text-align: center;
        line-height: 1.5;
        animation: fadeIn 1.5s ease-in 0.5s both;
    }

    /* Systems grid */
    .status-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
        margin: 15px 0;
    }
    .sys-down {
        background-color: #c62828; color: white;
        padding: 14px 8px; border-radius: 8px;
        text-align: center; font-size: 1em; font-weight: bold;
        animation: systemDown 0.5s ease-out both;
    }
    @keyframes systemDown {
        0% { background-color: #2e7d32; }
        50% { background-color: #ff6f00; }
        100% { background-color: #c62828; }
    }
    .sys-degraded {
        background-color: #e65100; color: white;
        padding: 14px 8px; border-radius: 8px;
        text-align: center; font-size: 1em;
    }
    .sys-up {
        background-color: #2e7d32; color: white;
        padding: 14px 8px; border-radius: 8px;
        text-align: center; font-size: 1em;
    }

    /* Metrics */
    .metric-row {
        display: flex; justify-content: space-around;
        margin: 20px 0; flex-wrap: wrap;
    }
    .metric-box {
        background-color: #1a1a2e;
        border: 1px solid #e94560;
        border-radius: 10px;
        padding: 15px 25px;
        text-align: center;
        min-width: 140px;
        margin: 5px;
        animation: fadeIn 1s ease-in;
    }
    .metric-box .value {
        color: #e94560; font-size: 2em; font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    .metric-box .label {
        color: #a0a0c0; font-size: 0.85em; margin-top: 5px;
    }

    /* Ransom typewriter effect */
    .ransom-text {
        font-family: 'Courier New', monospace;
        color: #ff6b6b;
        font-size: 1.1em;
        animation: typewriter 3s steps(60) 1s both;
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #ff6b6b;
    }
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }

    /* Audio player - hidden but functional */
    .audio-container audio {
        width: 100%;
        height: 40px;
        margin-top: 10px;
    }

    /* Action station instructor cue */
    .station-cue {
        background: linear-gradient(135deg, #e65100 0%, #ff8f00 100%);
        border: 3px solid #ffb74d;
        border-radius: 12px;
        padding: 15px 25px;
        margin: 15px 0;
        color: white;
        font-size: 1.1em;
        text-align: center;
        line-height: 1.5;
    }
    .station-cue .station-label {
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .station-cue strong {
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "slide" not in st.session_state:
    st.session_state.slide = 0
if "autoplay" not in st.session_state:
    st.session_state.autoplay = True

# ---------------------------------------------------------------------------
# Audio helper
# ---------------------------------------------------------------------------
def get_audio_html(slide_num, autoplay=True):
    """Return HTML audio element for a slide's narration with forced autoplay."""
    filename = os.path.join(AUDIO_DIR, f"slide_{slide_num:02d}.mp3")
    if not os.path.exists(filename):
        return ""
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    # Unique ID per slide so Streamlit treats each as a new element
    audio_id = f"slideAudio_{slide_num}"
    autoplay_attr = "autoplay" if autoplay else ""
    # JavaScript forces play even if browser blocks autoplay attribute
    play_script = f"""
    <script>
    (function() {{
        var audio = document.getElementById('{audio_id}');
        if (audio) {{
            audio.currentTime = 0;
            audio.play().catch(function(e) {{ console.log('Autoplay blocked:', e); }});
        }}
    }})();
    </script>
    """ if autoplay else ""
    return f"""
    <div class="audio-container">
        <audio controls {autoplay_attr} id="{audio_id}"
               src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    </div>
    {play_script}
    """

def sound_cue_js(cue_type="alert"):
    """Generate a browser sound cue using Web Audio API."""
    sounds = {
        "alert": "o.frequency.setValueAtTime(880,c.currentTime);g.gain.setValueAtTime(0.3,c.currentTime);o.start();o.stop(c.currentTime+0.15);setTimeout(()=>{let o2=c.createOscillator();let g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o2.frequency.setValueAtTime(880,c.currentTime);g2.gain.setValueAtTime(0.3,c.currentTime);o2.start();o2.stop(c.currentTime+0.15);},250);",
        "critical": "o.frequency.setValueAtTime(440,c.currentTime);o.frequency.setValueAtTime(880,c.currentTime+0.1);g.gain.setValueAtTime(0.4,c.currentTime);o.start();o.stop(c.currentTime+0.3);setTimeout(()=>{let o2=c.createOscillator();let g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o2.frequency.setValueAtTime(440,c.currentTime);o2.frequency.setValueAtTime(880,c.currentTime+0.1);g2.gain.setValueAtTime(0.4,c.currentTime);o2.start();o2.stop(c.currentTime+0.3);},500);",
        "notification": "o.frequency.setValueAtTime(587,c.currentTime);o.frequency.setValueAtTime(784,c.currentTime+0.1);g.gain.setValueAtTime(0.2,c.currentTime);o.start();o.stop(c.currentTime+0.2);",
        "phone": "o.frequency.setValueAtTime(440,c.currentTime);g.gain.setValueAtTime(0.2,c.currentTime);o.start();o.stop(c.currentTime+0.5);setTimeout(()=>{let o2=c.createOscillator();let g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o2.frequency.setValueAtTime(440,c.currentTime);g2.gain.setValueAtTime(0.2,c.currentTime);o2.start();o2.stop(c.currentTime+0.5);},700);",
    }
    code = sounds.get(cue_type, sounds["notification"])
    return f"""
    <script>
    (function(){{
        try {{
            var c = new (window.AudioContext || window.webkitAudioContext)();
            var o = c.createOscillator();
            var g = c.createGain();
            o.connect(g);
            g.connect(c.destination);
            {code}
        }} catch(e) {{}}
    }})();
    </script>
    """

# ---------------------------------------------------------------------------
# Systems grid helper
# ---------------------------------------------------------------------------
def systems_grid(statuses):
    html = '<div class="status-grid">'
    for name, cls in statuses:
        html += f'<div class="{cls}">{name}</div>'
    html += "</div>"
    return html

ALL_UP = [("EHR (DPI)", "sys-up"), ("Lab (LIS)", "sys-up"), ("PACS", "sys-up"),
          ("Pharmacy", "sys-up"), ("Patient Portal", "sys-up"),
          ("Email", "sys-up"), ("Scheduling", "sys-up"), ("Billing", "sys-up"),
          ("Nurse Call", "sys-up"), ("Badge Access", "sys-up")]

ALL_DOWN = [("EHR (DPI)", "sys-down"), ("Lab (LIS)", "sys-down"), ("PACS", "sys-down"),
            ("Pharmacy", "sys-down"), ("Patient Portal", "sys-down"),
            ("Email", "sys-down"), ("Scheduling", "sys-down"), ("Billing", "sys-down"),
            ("Nurse Call", "sys-degraded"), ("Badge Access", "sys-degraded")]

DAY2 = [("EHR (DPI)", "sys-down"), ("Lab (LIS)", "sys-down"), ("PACS", "sys-down"),
        ("Pharmacy", "sys-down"), ("Patient Portal", "sys-down"),
        ("Email", "sys-down"), ("Scheduling", "sys-down"), ("Billing", "sys-down"),
        ("Nurse Call", "sys-up"), ("Badge Access", "sys-up")]

DAY3 = [("EHR (DPI)", "sys-down"), ("Lab (LIS)", "sys-down"), ("PACS", "sys-down"),
        ("Pharmacy", "sys-down"), ("Patient Portal", "sys-down"),
        ("Email", "sys-degraded"), ("Scheduling", "sys-down"), ("Billing", "sys-down"),
        ("Nurse Call", "sys-up"), ("Badge Access", "sys-up")]

RECOVERY = [("EHR (DPI)", "sys-degraded"), ("Lab (LIS)", "sys-degraded"), ("PACS", "sys-down"),
            ("Pharmacy", "sys-degraded"), ("Patient Portal", "sys-down"),
            ("Email", "sys-up"), ("Scheduling", "sys-degraded"), ("Billing", "sys-down"),
            ("Nurse Call", "sys-up"), ("Badge Access", "sys-up")]

# ---------------------------------------------------------------------------
# Slide content: (type, html, sound_cue)
# type is for categorization; sound_cue is the cue to play
# ---------------------------------------------------------------------------
SLIDES = []

# 0: Title
SLIDES.append(("title", """
<div class="slide-content">
<div class="broadcast-header">
    <h1>SHIFT CYBERSECURITY BREACH SIMULATION</h1>
    <p>Centre Hospitalier Sainte-Claire &nbsp;|&nbsp; Saint-Etienne, France</p>
</div>
<div style="text-align:center; color:#a0a0c0; font-size:1.3em; margin:40px 0;">
    <p>A 350-bed regional hospital. 1,200 staff. 287 inpatients.</p>
    <p>The only Level 1 trauma center and neonatal ICU in the region.</p>
    <p style="margin-top:30px; color:#e94560; font-size:1.2em; letter-spacing:2px;">
        IT IS MONDAY, 06:12 AM.
    </p>
    <p style="color:#666; margin-top:40px;">All systems operational.</p>
</div>
""" + systems_grid(ALL_UP) + "</div>", None))

# 1: First reports
SLIDES.append(("breach", """
<div class="slide-content">
<div class="phase-title">The Breach Begins</div>
<div class="phase-subtitle">Monday — 06:12 to 06:24</div>
<div>
<div class="event-card warning"><span class="event-time warning">06:12</span> — Night-shift nurse reports EHR is "frozen" on 3 workstations in the ICU.</div>
<div class="event-card warning"><span class="event-time warning">06:15</span> — Second nurse reports the same in maternity. Cannot access patient birth plans.</div>
<div class="event-card warning"><span class="event-time warning">06:18</span> — IT help desk receives 12 simultaneous calls. Lab system showing errors.</div>
<div class="event-card warning"><span class="event-time warning">06:22</span> — Pharmacy technician: automated dispensing cabinets unresponsive.</div>
<div class="event-card"><span class="event-time">06:24</span> — Radiology PACS displays a ransom message:<br><span class="ransom-text">"Your files are encrypted. Contact us for the decryption key. You have 72 hours."</span></div>
</div>
</div>""", "alert"))

# 2: Escalation
SLIDES.append(("breach", """
<div class="slide-content">
<div class="phase-title">Systems Falling</div>
<div class="phase-subtitle">Monday — 06:26 to 06:42</div>
<div>
<div class="event-card"><span class="event-time">06:26</span> — Night IT admin restarts servers — same ransom message on 4 of 6 core servers.</div>
<div class="event-card"><span class="event-time">06:30</span> — Pharmacy dispensing confirmed offline. Medication cabinets locked hospital-wide.</div>
<div class="event-card"><span class="event-time">06:33</span> — Patient portal goes dark. 47 telehealth appointments scheduled today.</div>
<div class="event-card"><span class="event-time">06:35</span> — Scheduling unresponsive. 142 outpatient appointments unconfirmable.</div>
<div class="event-card"><span class="event-time">06:38</span> — Billing and revenue cycle encrypted. No claims can be submitted.</div>
<div class="event-card"><span class="event-time">06:40</span> — <strong>IT confirms: LockBit variant' ransomware across EHR, LIS, PACS, pharmacy, billing</strong></div>
<div class="event-card"><span class="event-time">06:42</span> — Forensics: initial access was <strong>11 days ago</strong> via phishing email to radiology tech.</div>
</div>
</div>""", "critical"))

# 3: Full picture
SLIDES.append(("breach", """
<div class="slide-content">
<div class="phase-title">Full-Scale Attack Confirmed</div>
<div class="phase-subtitle">Monday — 06:45 to 07:05</div>
<div>
<div class="event-card"><span class="event-time">06:45</span> — Email servers compromised. Communication limited to phone and in-person.</div>
<div class="event-card warning"><span class="event-time warning">06:48</span> — Nurse call system degraded. Some units report delays.</div>
<div class="event-card warning"><span class="event-time warning">06:50</span> — Badge access intermittent. Pharmacy and server room unsecured.</div>
<div class="event-card info"><span class="event-time info">06:55</span> — 400+ day-shift staff arriving. Most have no information.</div>
<div class="event-card info"><span class="event-time info">07:00</span> — Hospital Incident Command System (HICS) activated.</div>
<div class="event-card info"><span class="event-time info">07:05</span> — ANSSI contacted. Forensics team: 6–8 hours away.</div>
</div>
<div class="crisis-banner">ALL MAJOR CLINICAL SYSTEMS ARE DOWN</div>
""" + systems_grid(ALL_DOWN) + "</div>", "critical"))

# 4: PAUSE — Phase 1
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>You are the hospital's crisis leadership team. It is 07:05 AM.</p>
    <p style="margin-top:20px;">Discuss with your team:</p>
    <div class="prompt">
        1. What is your FIRST action? Downtime procedures or network isolation?<br>
        2. How do you communicate to 1,200 staff with no email?<br>
        3. 15 ICU patients on smart pump drips. 8 women in labor. 12 surgeries scheduled. What is your patient safety strategy?<br>
        4. Who do you call first? Police, insurance, regulator, or the board?
    </div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss on your feet. Then return to your device to log your decisions.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Stations After This Pause</div>
    <strong>Station 1:</strong> Design an Emergency Downtime MAR (8 min) — Grab blank paper, design the form nurses will use<br>
    <strong>Station 2:</strong> Draft the Staff Communication Bulletin (6 min) — Write the actual words staff will receive
</div>
</div>""", "notification"))

# 5: Downtime begins
SLIDES.append(("downtime", """
<div class="slide-content">
<div class="phase-title">Downtime Operations</div>
<div class="phase-subtitle">Monday 08:00 — Tuesday 06:00 | Hour 2 to 24</div>
<div class="crisis-banner" style="background-color:#e65100; animation:none;">ALL CLINICAL SYSTEMS OPERATING MANUALLY</div>
""" + systems_grid(ALL_DOWN) + """
<div style="text-align:center; color:#e0e0f0; font-size:1.3em; margin:30px 0;">
    <p>Every medication. Every patient ID check. Every lab order. Every note.</p>
    <p style="color:#ffa726; font-weight:bold; font-size:1.3em;">On paper.</p>
</div>
<div class="metric-row">
    <div class="metric-box"><div class="value">287</div><div class="label">Inpatients</div></div>
    <div class="metric-box"><div class="value">42</div><div class="label">ICU Patients</div></div>
    <div class="metric-box"><div class="value">8</div><div class="label">Maternity</div></div>
    <div class="metric-box"><div class="value">14</div><div class="label">Patients Named Martin</div></div>
    <div class="metric-box"><div class="value">0</div><div class="label">Systems Online</div></div>
</div>
</div>""", "alert"))

# 6: Near-miss
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Inject: Near-Miss Medication Event</div>
<div class="phase-subtitle">Hour 4</div>
<div class="event-card">A nurse reports a <strong>near-miss</strong>: without barcode scanning, <span style="color:#e94560;">MARTIN, Jean-Pierre</span> vs. <span style="color:#e94560;">MARTIN, Jean-Paul</span> — almost given the wrong medication.</div>
<div class="event-card warning">The manual five-rights check caught it. But staff are shaken and requesting additional safety protocols.</div>
<div class="decision-prompt">How does your team prevent actual medication errors during downtime?</div>
</div>""", "alert"))

# 7: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>A near-miss just occurred. Your staff are scared.</p>
    <div class="prompt">From your role's perspective: What is the immediate response?<br>How do you prevent the next one from being an actual error?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision in the student app.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 3:</strong> Create Emergency Patient ID Wristband (6 min) — Design a handwritten wristband that solves the Martin problem
</div>
</div>""", "notification"))

# 8: Ambulance
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Inject: Ambulance Diversion Request</div>
<div class="phase-subtitle">Hour 8</div>
<div class="event-card">The ED is overwhelmed. Without electronic triage or patient tracking, <strong>wait times have tripled</strong>. The ED Medical Director requests diversion.</div>
<div class="event-card warning">Nearest Level 1 trauma center: <strong>45 minutes away</strong>. Only neonatal ICU in the region: <strong>yours</strong>. A pregnant woman at 36 weeks is in an ambulance <strong>en route to you right now</strong>.</div>
<div class="decision-prompt">Do you approve diversion? What about the woman in the ambulance?</div>
</div>""", "phone"))

# 9: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>An ambulance with a pregnant patient is en route. Your ED is overwhelmed.</p>
    <div class="prompt">Full diversion? Partial? Deny entirely?<br>What do you tell the paramedics right now?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
</div>""", "notification"))

# 10: Shift handoff
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Inject: The 19:00 Shift Handoff</div>
<div class="phase-subtitle">Hour 13</div>
<div class="event-card">Evening shift arriving. Day shift: <strong>13 hours</strong> of crisis management. Evening staff have minimal information.</div>
<div class="event-card warning">You must hand off:<br>• 287 inpatients — <em>all on paper</em><br>• Active downtime procedures<br>• Outstanding issues (near-miss, diversion status)<br>• Location of all paper records<br>• Emotional state of day-shift staff — <em>several nurses in tears</em></div>
<div class="decision-prompt">How do you hand off a paper-based hospital to staff who've never used paper?</div>
</div>""", "notification"))

# 11: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>Evening staff arriving. They know nothing about paper processes.</p>
    <div class="prompt">How do you structure the handoff?<br>Keep exhausted day-shift longer, or let them go?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 4:</strong> Build Your Shift Handoff Tool (8 min) — Design the one-page handoff template that every unit will use tonight
</div>
</div>""", "notification"))

# 12: Paper crisis
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Inject: Paper Records Crisis</div>
<div class="phase-subtitle">Hour 18</div>
<div class="event-card"><strong>3,200 pages</strong> of handwritten records accumulated. Quality audit of 50 records:</div>
<div class="metric-row">
    <div class="metric-box"><div class="value">34%</div><div class="label">Missing DOB</div></div>
    <div class="metric-box"><div class="value">22%</div><div class="label">No Allergies</div></div>
    <div class="metric-box"><div class="value">18%</div><div class="label">Illegible</div></div>
    <div class="metric-box"><div class="value">11%</div><div class="label">Can't Match to Patient</div></div>
    <div class="metric-box"><div class="value">4</div><div class="label">Duplicates</div></div>
</div>
<div class="decision-prompt">How do you manage the backlog while maintaining data integrity?</div>
</div>""", "alert"))

# 13: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>3,200 pages. 11% unmatched. Illegible handwriting. Exhausted staff.</p>
    <div class="prompt">What is your data management strategy?<br>How will you handle back-entry when systems return?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision. After this, we take a break.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 5:</strong> Complete a Paper Patient Record (7 min) — Using ONLY blank paper, document a simulated patient intake. Experience the difficulty.
</div>
</div>""", "notification"))

# 14: BREAK
SLIDES.append(("break", """
<div class="slide-content">
<div class="break-screen">
    <h1>BREAK</h1>
    <p>20 minutes. The crisis does not pause, but you can.</p>
    <p style="margin-top:30px; font-size:0.9em;">When you return, it will be <strong>Hour 24</strong>.<br>The media are calling. Families are arriving. Staff are breaking.<br>The pressure is about to intensify.</p>
</div>
</div>""", None))

# 15: Day 2
SLIDES.append(("escalation", """
<div class="slide-content">
<div class="phase-title">Escalation & Stakeholder Pressure</div>
<div class="phase-subtitle">Tuesday — Hour 24 to 48 | Day 2</div>
<div class="crisis-banner" style="background-color:#e65100; animation:none;">24 HOURS OF DOWNTIME — EXTERNAL PRESSURE MOUNTING</div>
""" + systems_grid(DAY2) + """
<div class="metric-row">
    <div class="metric-box"><div class="value">24h</div><div class="label">Downtime</div></div>
    <div class="metric-box"><div class="value">3,200</div><div class="label">Paper Records</div></div>
    <div class="metric-box"><div class="value">23</div><div class="label">Surgeries Canceled</div></div>
    <div class="metric-box"><div class="value">14</div><div class="label">Diverted</div></div>
    <div class="metric-box"><div class="value">€240K</div><div class="label">Revenue Lost</div></div>
</div>
</div>""", "alert"))

# 16: Media
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">The Story Breaks</div>
<div class="phase-subtitle">Hour 26</div>
<div class="news-ticker">
    <div class="source">BREAKING — France 3 Auvergne-Rhône-Alpes — 12:00 Noon</div><br>
    "Centre Hospitalier Sainte-Claire has been operating without its computer systems for over 24 hours following what sources describe as a 'major cyberattack.' Ambulances have been diverted. A hospital spokesperson confirmed a 'technology disruption' but declined to provide details. Patient advocacy groups demand transparency. The ARS says it is 'monitoring the situation.'"
</div>
<div class="decision-prompt">The phone is ringing. Media, patients, families. How do you respond?</div>
</div>""", "notification"))

# 17: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>The story is on television. Your phone lines are overwhelmed.</p>
    <div class="prompt">Press conference? Written statement? Full transparency?<br>Who is the spokesperson? What is the ONE key message?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 6:</strong> Write the Press Statement (8 min) — Draft the actual words. Read it aloud. Have a teammate play journalist and ask a tough question.
</div>
</div>""", "notification"))

# 18: Family
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">A Family Demands Answers</div>
<div class="phase-subtitle">Hour 28</div>
<div class="scene">
    <div class="label">Scene: Hospital Main Lobby</div><br>
    A man approaches the information desk. Visibly upset. His mother, 82, admitted three days ago for pneumonia. Unable to reach anyone by phone. Portal down. Drove 90 minutes.<br><br>
    <em>"I can't access my mother's records. I don't know what medications she's on. The nurse told me they're using PAPER. Paper! What year is this? I want to know if my mother's personal information has been stolen. I want to speak to whoever is in charge. And if I don't get answers, I'm calling my lawyer and the press."</em>
</div>
<div class="decision-prompt">Who responds? What do you say? What can't you say?</div>
</div>""", "phone"))

# 19: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>This man represents hundreds of families with the same fears.</p>
    <div class="prompt">Who meets with him? What can you share?<br>He's threatening legal action and media. How do you de-escalate?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 7:</strong> Create the Family Information Sheet (7 min) — Write the one-page handout for every worried family member. Have a teammate read it as a scared relative.
</div>
</div>""", "notification"))

# 20: Staff morale
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Staff Morale Crisis</div>
<div class="phase-subtitle">Hour 32</div>
<div class="voicemail">
    <div class="label">Voicemail — Marie-Claire, Charge Nurse, Unit 3B</div><br>
    "This is Marie-Claire on 3B. I need to tell you that my nurses are done. We've been working 14-hour shifts on paper for two days. Three of my nurses called in sick today — I think they're not actually sick, they just can't take it anymore. The ones who are here are making mistakes. Small ones so far. But I'm scared. We had another near-miss — wrong dose calculated by hand because we don't have the EHR doing the math for us. I need more staff, I need someone to acknowledge what we're going through, and I need to know when this is going to end. Please call me back."
</div>
<div class="decision-prompt">Staff burnout is becoming a patient safety issue. What do you do?</div>
</div>""", "phone"))

# 21: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>Marie-Claire is one of your best charge nurses. If she breaks, the unit breaks.</p>
    <div class="prompt">Mutual aid? Reduce census? Crisis counseling? Shorter shifts?<br>What does each cost you?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
</div>""", "notification"))

# 22: Social media
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Social Media Firestorm</div>
<div class="phase-subtitle">Hour 34</div>
<div>
<div class="social-post"><span class="handle">@HealthWatchFR</span> (12,400 followers)<br>"THREAD: My aunt is a nurse at Sainte-Claire. She says they've been writing EVERYTHING by hand for 2 days. No access to patient histories. No medication barcodes. She's terrified of making an error. This is a patient safety EMERGENCY. 1/7"</div>
<div class="social-post"><span class="handle">@PatientRightsFR</span> (34,200 followers)<br>"If Sainte-Claire has had 180,000 patient records stolen, where is the CNIL notification? GDPR requires transparency. Silence is not acceptable. #DataBreach #GDPR"</div>
<div class="social-post"><span class="handle">Dr. Laurent M.</span> (verified physician)<br>"The Sainte-Claire situation is exactly what we've warned about. French hospitals are chronically under-invested in cybersecurity. This will happen again."</div>
</div>
<div class="decision-prompt">Social media is shaping the narrative. Do you engage or stay silent?</div>
</div>""", "notification"))

# 23: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>A nurse's relative posted. Advocacy groups demanding answers.</p>
    <div class="prompt">Official social media response? Ignore it?<br>Ask the employee to remove it? Hire a crisis firm?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
</div>""", "notification"))

# 24: Department conflict
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">Inter-Department Conflict</div>
<div class="phase-subtitle">Hour 36</div>
<div class="scene">
    <div class="label">Scene: Incident Command Center</div><br>
    The Chief of Surgery and the HIM Director are in a heated argument.<br><br>
    <strong>Chief of Surgery:</strong> <em>"We operated for decades before computers. I am not letting a computer problem endanger my patients by delaying their care."</em><br><br>
    <strong>HIM Director:</strong> <em>"And we had higher error rates for decades before computers. We are not going backward. Every mislabeled specimen is a potential catastrophe."</em>
</div>
<div class="decision-prompt">Both are right. Both are wrong. The Incident Commander must decide.</div>
</div>""", "alert"))

# 25: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>Surgery vs. HIM. Patient harm from delay vs. patient harm from error.</p>
    <div class="prompt">Resume elective surgery on paper? Delay? Compromise? Governance meeting?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
</div>""", "notification"))

# 26: Day 3
SLIDES.append(("critical", """
<div class="slide-content">
<div class="phase-title">Critical Decisions</div>
<div class="phase-subtitle">Wednesday — Hour 48 to 72 | Day 3</div>
<div class="crisis-banner">RANSOM DEADLINE APPROACHING — GDPR CLOCK TICKING</div>
""" + systems_grid(DAY3) + """
<div class="metric-row">
    <div class="metric-box"><div class="value">48h</div><div class="label">Downtime</div></div>
    <div class="metric-box"><div class="value">6,400</div><div class="label">Paper Records</div></div>
    <div class="metric-box"><div class="value">38</div><div class="label">Surgeries Canceled</div></div>
    <div class="metric-box"><div class="value">€480K</div><div class="label">Revenue Lost</div></div>
    <div class="metric-box"><div class="value">89</div><div class="label">Complaints</div></div>
</div>
</div>""", "critical"))

# 27: Ransom
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">The Ransom Demand</div>
<div class="phase-subtitle">Hour 50</div>
<div class="event-card">The attackers have made formal contact through an encrypted channel.</div>
<div class="metric-row">
    <div class="metric-box" style="border-color:#e94560;"><div class="value">€2.5M</div><div class="label">Ransom</div></div>
    <div class="metric-box" style="border-color:#ffa726;"><div class="value">€1M</div><div class="label">Insurance Limit</div></div>
    <div class="metric-box" style="border-color:#e94560;"><div class="value">180K</div><div class="label">Records Stolen</div></div>
    <div class="metric-box" style="border-color:#ffa726;"><div class="value">48h</div><div class="label">Deadline</div></div>
</div>
<div class="event-card">500 genuine patient records provided as proof. Includes diagnoses, medications, national IDs, <strong>mental health and HIV status</strong>.</div>
<div class="event-card warning"><strong>ANSSI advises: do not pay.</strong><br><strong>Loi LOPMI (2023):</strong> Police report within 72h of payment required for insurance.</div>
<div class="decision-prompt">€2.5 million. 180,000 patients. Mental health records. HIV status.<br>What do you recommend to the board?</div>
</div>""", "critical"))

# 28: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>This is the hardest decision in the simulation.</p>
    <div class="prompt">Pay? Negotiate? Refuse? Escalate?<br>What are the ethical dimensions?<br>Who bears the harm in each scenario?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss thoroughly, then log your decision and reasoning.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 8:</strong> Draft the Board Recommendation Memo (8 min) — Write the formal one-page memo to the board. Situation, options, recommendation, rationale, risks.
</div>
</div>""", "notification"))

# 29: GDPR
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">GDPR 72-Hour Notification Deadline</div>
<div class="phase-subtitle">Hour 58 — 14 hours remaining</div>
<div class="event-card"><strong>GDPR Article 33:</strong> Notify CNIL within 72 hours. Clock started 06:40 Monday. <strong>14 hours remain.</strong></div>
<div class="event-card warning">Forensics:<br>• Attackers had access <strong>11 days</strong> before encryption<br>• Large data transfers confirmed<br>• Exact scope: <strong>unknown</strong><br>• 500-record sample verified genuine<br>• Likely includes demographics, diagnoses, meds, labs, mental health records</div>
<div class="decision-prompt">File now with incomplete info? Wait for deadline? Notify patients too?</div>
</div>""", "alert"))

# 30: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — TEAM DISCUSSION</h2>
    <p>14 hours. Incomplete information. 180,000 potentially affected patients.</p>
    <div class="prompt">File preliminary now? Wait for the deadline?<br>How do you notify 180,000 patients?<br>Consider: elderly patients, mental health stigma, domestic violence survivors.</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your decision.</p>
</div>
<div class="station-cue">
    <div class="station-label">Action Station</div>
    <strong>Station 9:</strong> Complete the CNIL Breach Notification (10 min) — Fill out the simulated regulatory form in the student app. Mark what you KNOW vs. what you DON'T KNOW.
</div>
</div>""", "notification"))

# 31: Restoration
SLIDES.append(("inject", """
<div class="slide-content">
<div class="phase-title" style="font-size:1.8em;">System Restoration Strategy</div>
<div class="phase-subtitle">Hour 64</div>
<div class="event-card info"><strong>Option A: 48-hour backup.</strong> EHR in 12–18h. Loses pre-breach + downtime data. Clean. Back-entry: 3–4 weeks.</div>
<div class="event-card warning"><strong>Option B: Decrypt & clean.</strong> 5–10 more days. Preserves data. 15–20% reinfection risk. Forensics recommends against.</div>
<div class="event-card info"><strong>Option C: New clean instance.</strong> 24–36h. Zero risk. Requires manual entry of ALL active patient data.</div>
<div class="event-card" style="border-left-color:#ab47bc;"><strong>Option D: Hybrid.</strong> Phase 1 (24h): clean instance for active patients. Phase 2 (1 week): restore backup. Phase 3 (2–4 weeks): merge & reconcile.</div>
<div class="decision-prompt">Speed vs. data preservation vs. security. Who decides?</div>
</div>""", "notification"))

# 32: PAUSE
SLIDES.append(("pause", """
<div class="slide-content">
<div class="pause-screen">
    <h2>PAUSE — FINAL TEAM DISCUSSION</h2>
    <p>Four options. Each has costs. Each has risks.</p>
    <div class="prompt">Which path? Technical decision? Clinical? Financial? Data integrity?<br>Who has the final say?</div>
    <p style="margin-top:30px; font-size:0.8em; color:#a5d6a7;">Discuss, then log your final decision.</p>
</div>
</div>""", "notification"))

# 33: Recovery
SLIDES.append(("recovery", """
<div class="slide-content">
<div class="phase-title">Recovery Planning</div>
<div class="phase-subtitle">Thursday — Hour 72+ | Day 4</div>
<div style="text-align:center; color:#a0a0c0; font-size:1.3em; margin:20px 0;">Partial systems restoration in progress.</div>
""" + systems_grid(RECOVERY) + """
<div style="text-align:center; color:#e0e0f0; font-size:1.4em; margin:40px 0; line-height:2;">
    <p>The systems will come back in <strong>days</strong>.</p>
    <p>The trust takes <strong>months</strong>.</p>
    <p>The lessons last <strong>careers</strong>.</p>
</div>
<div class="decision-prompt">In your student app: complete Recovery Planning.<br>Prioritize back-entry. Plan trust recovery. Assess preparedness. Write your after-action summary.</div>
<div class="station-cue">
    <div class="station-label">Final Action Station</div>
    <strong>Station 10:</strong> Design the Back-Entry Workflow (8 min) — 6,400+ pages of paper. Map the process: priority, staffing, QA, the 11% unmatched records.
</div>
</div>""", None))

# 34: End
SLIDES.append(("end", """
<div class="slide-content">
<div class="broadcast-header" style="border-color:#4caf50;">
    <h1 style="color:#4caf50;">END OF SIMULATION</h1>
    <p>Thank you for your work. The 2-hour debrief will follow.</p>
</div>
<div style="text-align:center; color:#a0a0c0; font-size:1.2em; margin:40px 0; line-height:2;">
    <p>Export your team reports from the student app.</p>
    <p>Prepare to share your most difficult decision and what you learned.</p>
</div>
</div>""", None))


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
total_slides = len(SLIDES)

# Navigation bar
nav1, nav2, nav3, nav4 = st.columns([1, 2, 1, 1])
with nav1:
    if st.button("◀ Previous", disabled=st.session_state.slide <= 0, use_container_width=True):
        st.session_state.slide -= 1
        st.rerun()
with nav2:
    st.markdown(
        f'<div style="text-align:center; color:#666; font-size:0.9em; padding-top:8px;">'
        f'Slide {st.session_state.slide + 1} of {total_slides}</div>',
        unsafe_allow_html=True,
    )
with nav3:
    st.session_state.autoplay = st.checkbox("Autoplay audio", value=st.session_state.autoplay)
with nav4:
    if st.button("Next ▶", disabled=st.session_state.slide >= total_slides - 1,
                 use_container_width=True, type="primary"):
        st.session_state.slide += 1
        st.rerun()

# Slide content
slide_type, slide_html, sound_cue = SLIDES[st.session_state.slide]
st.markdown(slide_html, unsafe_allow_html=True)

# Sound cue
if sound_cue and st.session_state.autoplay:
    st.markdown(sound_cue_js(sound_cue), unsafe_allow_html=True)

# Audio narration
audio_html = get_audio_html(st.session_state.slide, autoplay=st.session_state.autoplay)
if audio_html:
    st.markdown(audio_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar — phase map
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Slide Navigation")
    target = st.number_input("Jump to slide:", 1, total_slides, st.session_state.slide + 1, key="jump")
    if target - 1 != st.session_state.slide:
        st.session_state.slide = target - 1
        st.rerun()

    st.markdown("---")
    st.markdown("### Phase Map")
    phase_map = {
        "Title": 0, "Breach 1: First Reports": 1, "Breach 2: Systems Falling": 2,
        "Breach 3: Full Attack": 3, "⏸ PAUSE: Phase 1 Decisions": 4,
        "Downtime Begins": 5, "💉 Near-Miss Medication": 6, "⏸ PAUSE": 7,
        "🚑 Ambulance Diversion": 8, "⏸ PAUSE": 9,
        "🔄 Shift Handoff": 10, "⏸ PAUSE": 11,
        "📄 Paper Records Crisis": 12, "⏸ PAUSE (then Break)": 13,
        "☕ BREAK": 14, "Day 2: Escalation": 15,
        "📺 Media Story": 16, "⏸ PAUSE": 17,
        "👨‍👩‍👦 Family Confrontation": 18, "⏸ PAUSE": 19,
        "😰 Staff Morale": 20, "⏸ PAUSE": 21,
        "📱 Social Media": 22, "⏸ PAUSE": 23,
        "⚔️ Dept Conflict": 24, "⏸ PAUSE": 25,
        "Day 3: Critical Decisions": 26, "💰 Ransom Demand": 27,
        "⏸ PAUSE (Ransom)": 28, "📋 GDPR Deadline": 29,
        "⏸ PAUSE (GDPR)": 30, "🖥️ Restoration": 31,
        "⏸ PAUSE (Final)": 32, "Recovery Planning": 33, "End": 34,
    }
    for label, idx in phase_map.items():
        prefix = "▶ " if idx == st.session_state.slide else ""
        if st.button(f"{prefix}{label}", key=f"pj_{idx}"):
            st.session_state.slide = idx
            st.rerun()

    # ------------------------------------------------------------------
    # Download all team submissions
    # ------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### Download Team Submissions")

    submission_files = sorted(
        [f for f in os.listdir(SUBMISSIONS_DIR) if f.endswith(".json")]
        if os.path.isdir(SUBMISSIONS_DIR) else []
    )

    if not submission_files:
        st.caption("No submissions yet. Teams must click Export in the student app.")
    else:
        st.caption(f"{len(submission_files)} team(s) submitted")

        # Load all reports
        all_reports = []
        for fname in submission_files:
            fpath = os.path.join(SUBMISSIONS_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    all_reports.append(json.load(f))
            except Exception:
                pass

        # Combined JSON download
        combined_json = json.dumps(all_reports, indent=2, ensure_ascii=False)
        st.download_button(
            "Download All (JSON)",
            data=combined_json,
            file_name="all_team_reports.json",
            mime="application/json",
            use_container_width=True,
        )

        # CSV summary download
        csv_buf = io.StringIO()

        # Collect all decision titles and station IDs across all reports
        all_decision_titles = []
        all_station_ids = []
        for r in all_reports:
            for d in r.get("decisions", []):
                t = d["title"]
                if t not in all_decision_titles:
                    all_decision_titles.append(t)
            for s in r.get("stations", []):
                sid = s.get("station_id", s["title"])
                if sid not in all_station_ids:
                    all_station_ids.append(sid)

        # Collect all deliverable keys per station
        station_deliverable_keys = {}
        for r in all_reports:
            for s in r.get("stations", []):
                sid = s.get("station_id", s["title"])
                for key in s.get("deliverables", {}).keys():
                    station_deliverable_keys.setdefault(sid, [])
                    if key not in station_deliverable_keys[sid]:
                        station_deliverable_keys[sid].append(key)

        # Build header row
        header = ["team_name", "exported_at", "decisions_made", "stations_completed"]
        for title in all_decision_titles:
            header.append(f"decision: {title}")
            header.append(f"justification: {title}")
        for sid in all_station_ids:
            for key in station_deliverable_keys.get(sid, []):
                header.append(f"{sid}: {key}")
        for i in range(1, 6):
            header.append(f"after_action_q{i}")

        writer = csv.DictWriter(csv_buf, fieldnames=header, extrasaction="ignore")
        writer.writeheader()

        for r in all_reports:
            row = {
                "team_name": r.get("team_name", ""),
                "exported_at": r.get("exported_at", ""),
                "decisions_made": len(r.get("decisions", [])),
                "stations_completed": len(r.get("stations", [])),
            }
            for d in r.get("decisions", []):
                row[f"decision: {d['title']}"] = d.get("choice", "")
                row[f"justification: {d['title']}"] = d.get("justification", "")
            for s in r.get("stations", []):
                sid = s.get("station_id", s["title"])
                for key, val in s.get("deliverables", {}).items():
                    row[f"{sid}: {key}"] = val
            aa = r.get("after_action", {})
            for i in range(1, 6):
                row[f"after_action_q{i}"] = aa.get(f"q{i}", "")
            writer.writerow(row)

        st.download_button(
            "Download All (CSV)",
            data=csv_buf.getvalue(),
            file_name="all_team_reports.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # List teams
        st.caption("Teams saved: " + ", ".join(r.get("team_name", "?") for r in all_reports))
