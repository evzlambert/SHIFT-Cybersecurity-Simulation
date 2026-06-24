"""
SHIFT Cybersecurity Simulation — ICC Incident Command Center Dashboard
Second Floor Read-Only Display

Reads from team JSON save files produced by student_app.py (or student_app_v2.py).
The student app's "Save Progress" button in the sidebar produces the correct format.
In v2, the student app will auto-save on every decision — no manual file transfer needed.

Shared folder setup:
  - Place this script on the ICC laptop
  - Create (or mount) a shared folder accessible to all team laptops
  - Set SHIFT_SHARED_DIR environment variable to that path, or drop files in ./submissions/
  - Teams copy their SHIFT_[teamname].json save files to that folder

Launch:
    streamlit run icc_dashboard.py --server.port 8504

Config:
    SHIFT_SHARED_DIR  — path to shared folder (default: ./submissions/ next to this script)
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import os
import glob
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
SHARED_DIR = os.environ.get(
    "SHIFT_SHARED_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions"),
)

st.set_page_config(
    page_title="ICC — Regional Intelligence Board",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — dark projection display theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d0d1a; color: #ccccdd; }
    div[data-testid="stSidebar"] { background-color: #0a0a14; }

    .icc-header {
        text-align: center;
        color: #ffffff;
        font-size: 1.5em;
        font-weight: bold;
        letter-spacing: 4px;
        text-transform: uppercase;
        padding: 12px 0 6px;
        border-bottom: 2px solid #ff4b4b;
        margin-bottom: 6px;
    }
    .icc-sub {
        text-align: center;
        color: #666688;
        font-size: 0.8em;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .team-panel {
        background-color: #141428;
        border: 1px solid #2a2a4a;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 8px;
        min-height: 420px;
    }
    .team-name {
        font-size: 1.05em;
        font-weight: bold;
        color: #ffffff;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 1px solid #2a2a4a;
        padding-bottom: 10px;
        margin-bottom: 14px;
    }
    .metric-block {
        background-color: #0d0d1a;
        border-radius: 6px;
        padding: 8px 10px;
        margin-bottom: 7px;
    }
    .metric-lbl {
        color: #555577;
        font-size: 0.68em;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .metric-val {
        font-size: 1.05em;
        font-weight: bold;
        line-height: 1.3;
    }
    .metric-sub {
        font-size: 0.75em;
        color: #888899;
        margin-top: 2px;
    }
    .phase-badge {
        display: inline-block;
        background-color: #1a1a38;
        color: #8888aa;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.72em;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    .burn-footer {
        background-color: #130808;
        border: 1px solid #2a1010;
        border-radius: 8px;
        padding: 12px 20px;
        margin-top: 16px;
        text-align: center;
        color: #bb6600;
        font-size: 0.85em;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .empty-panel {
        background-color: #0d0d1a;
        border: 1px dashed #222244;
        border-radius: 10px;
        padding: 30px 16px;
        text-align: center;
        color: #333355;
        min-height: 200px;
    }
    .no-data-wrap {
        background-color: #0d0d1a;
        border: 1px solid #222244;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Decision → metric tables (keyed by option index 0–3)
# Source decisions: p1_priority and p1_communication from student_app.py
# ─────────────────────────────────────────────────────────────────────────────
# p1_priority: how fast was the initial response
EXPOSURE_MAP = {
    0: ("12,000–40,000", "#FF8F00"),  # downtime + parallel — mixed, some spread
    1: ("8,000–22,000",  "#4CAF50"),  # isolation first — good, contained
    2: ("10,000–30,000", "#FF8F00"),  # split team — fast but coordination gap
    3: ("18,000–55,000", "#F44336"),  # huddle first — bad, spread to 3 more servers
}

# p1_communication: how staff were notified
STAFF_MAP = {
    0: (82, "#FF8F00"),  # PA announcement — mixed, patient alarm
    1: (78, "#FF8F00"),  # runners/bulletins — mixed, slow but accurate
    2: (70, "#F44336"),  # WhatsApp — bad, screenshot leaked
    3: (74, "#FF8F00"),  # entry briefing — mixed, night shift resentment
}

PHASE_LABELS = {
    0: "Setup", 1: "The Breach", 2: "Downtime Operations",
    3: "Break", 4: "Escalation", 5: "Critical Decisions", 6: "Recovery",
}

FINANCIAL_BURN_PER_SIM_HOUR = 28_400  # € per simulated hour (scenario constant)

# ─────────────────────────────────────────────────────────────────────────────
# Data loading — reads all SHIFT_*.json files from the shared directory
# ─────────────────────────────────────────────────────────────────────────────
def load_teams():
    os.makedirs(SHARED_DIR, exist_ok=True)
    teams = []
    for path in sorted(glob.glob(os.path.join(SHARED_DIR, "SHIFT_*.json"))):
        try:
            with open(path) as f:
                data = json.load(f)
            if data.get("team_name"):
                teams.append(data)
        except Exception:
            pass
    return teams


# ─────────────────────────────────────────────────────────────────────────────
# Scenario time calculations
# ─────────────────────────────────────────────────────────────────────────────
def sim_hours_elapsed(sim_start, mins_per_sim_hour):
    """Real elapsed time converted to simulated hours."""
    if sim_start is None:
        return 0.0
    real_mins = (datetime.now() - sim_start).total_seconds() / 60
    return real_mins / max(mins_per_sim_hour, 0.1)


def gdpr_hours_remaining(sim_hours):
    return max(0.0, 72.0 - sim_hours)


def financial_burn(sim_hours):
    return int(sim_hours * FINANCIAL_BURN_PER_SIM_HOUR)


def media_pressure_pct(sim_hours):
    # Escalates from 0% at hour 0 to 100% at hour 48 (Phase 4 onset)
    return min(100, int((sim_hours / 48) * 100))


# ─────────────────────────────────────────────────────────────────────────────
# Metric derivation — combines team decisions with scenario time
# ─────────────────────────────────────────────────────────────────────────────
def derive_team_metrics(team, gdpr_h, media_pct, burn, hie_status):
    decisions = team.get("decisions", {})

    p1p = decisions.get("p1_priority")
    if p1p is not None and p1p in EXPOSURE_MAP:
        exp_label, exp_color = EXPOSURE_MAP[p1p]
    else:
        exp_label, exp_color = "Awaiting Phase 1", "#333355"

    p1c = decisions.get("p1_communication")
    if p1c is not None and p1c in STAFF_MAP:
        staff_pct, staff_color = STAFF_MAP[p1c]
        staff_label = f"{staff_pct}%"
    else:
        staff_label, staff_color = "Awaiting Phase 1", "#333355"

    phase = team.get("current_phase", 0)
    n_dec = len(decisions)

    return {
        "exp_label": exp_label, "exp_color": exp_color,
        "staff_label": staff_label, "staff_color": staff_color,
        "gdpr_h": gdpr_h, "media_pct": media_pct, "burn": burn,
        "hie_status": hie_status,
        "phase_label": PHASE_LABELS.get(phase, f"Phase {phase}"),
        "n_decisions": n_dec,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Panel rendering
# ─────────────────────────────────────────────────────────────────────────────
def metric_block(label, value, color="#ccccdd", sub=None):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="metric-block">
        <div class="metric-lbl">{label}</div>
        <div class="metric-val" style="color:{color};">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_gdpr_block(hours):
    if hours > 36:
        color, label = "#4CAF50", f"{hours:.1f} hrs remaining"
    elif hours > 12:
        color, label = "#FF8F00", f"{hours:.1f} hrs remaining ⚠"
    elif hours > 0:
        color, label = "#F44336", f"URGENT — {hours:.1f} hrs left"
    else:
        color, label = "#F44336", "DEADLINE PASSED"
    metric_block("GDPR / CNIL CLOCK (SIM)", label, color)


def render_media_block(pct):
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    if pct < 30:
        color, level = "#4CAF50", "Low"
    elif pct < 60:
        color, level = "#FF8F00", "Building"
    elif pct < 85:
        color, level = "#F44336", "High"
    else:
        color, level = "#F44336", "CRITICAL"
    metric_block("MEDIA PRESSURE", bar, color, sub=f"{level} ({pct}%)")


def render_hie_block(status):
    STATUS_MAP = {
        "Connected":   ("● Connected",                "#FF8F00"),
        "Compromised": ("● COMPROMISED — ALERT",      "#F44336"),
        "Isolated":    ("● Isolated (decision made)", "#4CAF50"),
    }
    label, color = STATUS_MAP.get(status, ("● Unknown", "#555577"))
    metric_block("HIE NETWORK STATUS", label, color)


def render_team_panel(team, m):
    st.markdown(f"""
    <div class="team-panel">
        <div class="team-name">{team['team_name']}</div>
    </div>
    """, unsafe_allow_html=True)

    metric_block("DATA EXPOSURE ESTIMATE",
                 f"~{m['exp_label']} records", m["exp_color"])
    metric_block("STAFF AVAILABILITY INDEX",
                 m["staff_label"], m["staff_color"])
    render_gdpr_block(m["gdpr_h"])
    render_media_block(m["media_pct"])
    render_hie_block(m["hie_status"])
    metric_block("FINANCIAL BURN (SIM)",
                 f"€{m['burn']:,}", "#BB6600",
                 sub=f"@ €{FINANCIAL_BURN_PER_SIM_HOUR:,}/sim-hr")

    st.markdown(f"""
    <div class="phase-badge">
        {m['phase_label']} &nbsp;·&nbsp; {m['n_decisions']} decisions logged
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — co-facilitator controls (ICC floor laptop only)
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("## ICC Controls")
        st.caption("Co-Facilitator — ICC Floor")
        st.markdown("---")

        # ── Simulation clock ──────────────────────────────────────────────
        st.markdown("### Simulation Clock")
        if "sim_start" not in st.session_state:
            st.session_state.sim_start = None
        if "mins_per_sim_hour" not in st.session_state:
            st.session_state.mins_per_sim_hour = 2.7

        if st.session_state.sim_start is None:
            st.info("Clock not started.")
            if st.button("▶  Start Clock", type="primary", use_container_width=True):
                st.session_state.sim_start = datetime.now()
                st.rerun()
            st.caption(
                "Clock drives GDPR countdown and media escalation.\n"
                "Start when the instructor begins Phase 1."
            )
        else:
            real_elapsed = (datetime.now() - st.session_state.sim_start).total_seconds() / 60
            sim_h = real_elapsed / st.session_state.mins_per_sim_hour
            st.success(
                f"Running\n\n"
                f"Real: {real_elapsed:.0f} min elapsed\n\n"
                f"Sim: Hour {sim_h:.1f}"
            )
            if st.button("■  Reset Clock", use_container_width=True):
                st.session_state.sim_start = None
                st.rerun()

        st.session_state.mins_per_sim_hour = st.slider(
            "Real min per sim hour",
            min_value=1.0, max_value=10.0,
            value=float(st.session_state.mins_per_sim_hour),
            step=0.1,
            help="Default 2.7 min = 72 sim hours across a 3h15 session",
        )

        st.markdown("---")

        # ── HIE status ───────────────────────────────────────────────────
        st.markdown("### HIE Network")
        hie = st.selectbox(
            "HIE status (shown to all teams)",
            ["Connected", "Compromised", "Isolated"],
        )
        st.session_state["hie_status"] = hie
        if hie == "Compromised":
            st.warning("⚠ HIE alert is active — inject has fired")
        elif hie == "Isolated":
            st.success("HIE disconnected — team made the call")

        st.markdown("---")

        # ── File status ──────────────────────────────────────────────────
        st.markdown("### Team Files")
        st.caption(f"Shared folder:\n`{SHARED_DIR}`")
        team_files = glob.glob(os.path.join(SHARED_DIR, "SHIFT_*.json"))
        if team_files:
            st.success(f"{len(team_files)} team file(s) loaded")
            for fp in team_files:
                st.caption(f"· {os.path.basename(fp)}")
        else:
            st.warning("No team files found")

        if st.button("Refresh Now", use_container_width=True):
            st.rerun()

        st.markdown("---")

        # ── Display options ──────────────────────────────────────────────
        st.markdown("### Display")
        auto = st.checkbox("Auto-refresh every 30s", value=True)
        st.session_state["auto_refresh"] = auto
        if auto:
            st.caption("Page reloads automatically.")

        st.markdown("---")
        st.caption(
            "**Usage note:** Teams save their progress using the "
            "'Save Progress' button in the student app sidebar. "
            "The JSON file should be named `SHIFT_[teamname].json` "
            "and placed in the shared folder above.\n\n"
            "In student_app_v2.py this save happens automatically "
            "on every decision."
        )


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    render_sidebar()

    # Auto-refresh via injected JavaScript (zero-height iframe)
    if st.session_state.get("auto_refresh", True):
        components.html(
            "<script>setTimeout(function(){window.location.reload();},30000);</script>",
            height=0,
        )

    # Header
    now = datetime.now()
    st.markdown('<div class="icc-header">SHIFT — Incident Command Center</div>',
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="icc-sub">'
        f'Regional Intelligence Board &nbsp;·&nbsp; '
        f'{now.strftime("%H:%M:%S")} &nbsp;·&nbsp; '
        f'Read-Only Display — Do Not Interact'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Compute scenario time
    sim_start = st.session_state.get("sim_start")
    mph = st.session_state.get("mins_per_sim_hour", 2.7)
    sim_h = sim_hours_elapsed(sim_start, mph)
    gdpr_h = gdpr_hours_remaining(sim_h)
    burn = financial_burn(sim_h)
    media_pct = media_pressure_pct(sim_h)
    hie_status = st.session_state.get("hie_status", "Connected")

    # Load teams
    teams = load_teams()

    if not teams:
        st.markdown("""
        <div class="no-data-wrap">
            <h3 style="color:#444466;">Waiting for team data...</h3>
            <p style="color:#333355; margin-top:12px;">
                No team JSON files found in the shared folder.<br>
                Teams save progress via the student app sidebar.<br>
                Files must be named <code>SHIFT_[teamname].json</code>
                and placed in the folder shown in the sidebar.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Quick setup", expanded=True):
            st.markdown(f"""
**Shared folder:** `{SHARED_DIR}`

**How teams share their data:**
1. Student opens app → enters team name → plays through decisions
2. At any point: sidebar → "💾 Save Progress" → downloads `SHIFT_[teamname].json`
3. File is copied to the shared folder above (USB / AirDrop / network drive)
4. This dashboard detects and displays it within the next auto-refresh (30s)

**In student_app_v2.py:** the app auto-saves on every decision — no manual copy needed.

**For a quick test:** copy any saved `.json` from a student session into `{SHARED_DIR}`.
            """)
        return

    # Team panels — up to 4 columns
    n = min(len(teams), 4)
    cols = st.columns(n)
    for i, team in enumerate(teams[:4]):
        with cols[i]:
            m = derive_team_metrics(team, gdpr_h, media_pct, burn, hie_status)
            render_team_panel(team, m)

    # Footer — scenario constants shared across all teams
    gdpr_label = (
        f"{gdpr_h:.1f} sim hrs remaining" if gdpr_h > 0 else "DEADLINE PASSED"
    )
    st.markdown(f"""
    <div class="burn-footer">
        Financial Burn: €{burn:,} &nbsp;·&nbsp;
        GDPR Clock: {gdpr_label} &nbsp;·&nbsp;
        LockBit 3.0 — FR-2025-HOSP-0847 &nbsp;·&nbsp;
        Sim Hour: {sim_h:.1f}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
