# WHO Academy Setup Guide
## SHIFT Cybersecurity Simulation v2
### Day-Of Reference — Print and Bring

**Simulation duration:** ~3 hours 15 minutes active  
**Team size:** 2–4 teams of 5 students  
**Apps running:** Student app (port 8502) + ICC Dashboard (port 8504)  
**GitHub repo:** `evzlambert/SHIFT-Cybersecurity-Simulation`

---

## Delegation Overview

| Role | Person | Responsibilities |
|------|--------|-----------------|
| **Primary Facilitator** | Dr. Lambert | Main floor, all phase transitions, narrative |
| **ICC Co-Facilitator** | Assigned co-facilitator | Second floor, Phase 3 Regional Briefing (in character), intelligence card handoffs, ICC screen |
| **Tech Lead** | Tech-savvy co-facilitator | Laptop setup, Streamlit launch, IP sharing, troubleshooting |

*If you only have one co-facilitator, combine Tech Lead + ICC Co-Facilitator. Tech setup completes before the simulation starts.*

---

## SECTION 1 — Night Before (or morning of, at hotel)

- [ ] **YOU** — Confirm GitHub repo is current: `github.com/evzlambert/SHIFT-Cybersecurity-Simulation`
- [ ] **YOU** — Print and cut Intelligence Cards from `v2/Intelligence-Cards.md`
  - Card 1: ANSSI Advisory (1 copy)
  - Card 2: HIE Advisory (1 copy)
  - Cards 3A–3D: Regional Briefing (one per team — select based on how many teams you have)
- [ ] **YOU** — Pack physical simulation supplies:
  - Blank A4 paper (at least 100 sheets)
  - Markers and pens (multiple colors, multiple sets)
  - Card stock or thick paper strips (for wristband station)
  - Clear tape
  - Rulers (optional)
- [ ] **TECH LEAD** — Confirm Python and Streamlit are installed on instructor laptop:
  ```
  python3 --version
  streamlit --version
  ```
  If Streamlit is not installed: `pip install streamlit fpdf2`
- [ ] **TECH LEAD** — Clone or pull the latest code:
  ```
  git clone https://github.com/evzlambert/SHIFT-Cybersecurity-Simulation.git
  ```
  Or if already cloned:
  ```
  cd SHIFT-Cybersecurity-Simulation
  git pull origin main
  ```
- [ ] **TECH LEAD** — Do a dry-run launch of both apps to confirm no errors:
  ```
  cd SHIFT-Cybersecurity-Simulation
  streamlit run v2/student_app_v2.py --server.port 8502
  ```
  Open a second terminal:
  ```
  streamlit run v2/icc_dashboard.py --server.port 8504
  ```
  Visit `http://localhost:8502` and `http://localhost:8504` — both should load cleanly.

---

## SECTION 2 — On Arrival at WHO Academy (45–60 min before students)

### Step 1: Connect to WHO WiFi
- [ ] **ALL LAPTOPS** — Connect instructor laptop, ICC floor laptop, and any facilitator devices to the **same WiFi network**
- [ ] Note the network name — teams will need to connect to the same one

### Step 2: Find the Instructor Laptop's Local IP
- [ ] **TECH LEAD** — On the instructor laptop (Mac):
  - Go to **System Settings → WiFi → Details** next to the connected network
  - Copy the **IP Address** (format: `192.168.x.x` or `10.x.x.x`)
  - Write it here: **IP = ___________________**
- [ ] Alternatively, run in terminal: `ipconfig getifaddr en0`

### Step 3: Launch Both Apps on Instructor Laptop
- [ ] **TECH LEAD** — Open Terminal, navigate to the repo folder, and run:

  **Terminal Window 1 — Student App:**
  ```
  cd SHIFT-Cybersecurity-Simulation
  streamlit run v2/student_app_v2.py --server.port 8502
  ```

  **Terminal Window 2 — ICC Dashboard:**
  ```
  cd SHIFT-Cybersecurity-Simulation
  streamlit run v2/icc_dashboard.py --server.port 8504
  ```

  Keep both terminal windows open for the entire simulation. Do not close them.

### Step 4: Verify Connections
- [ ] **TECH LEAD** — From a DIFFERENT laptop (not the instructor laptop), open a browser and go to:
  ```
  http://[IP ADDRESS]:8502
  ```
  You should see the SHIFT student app. If you don't, see Troubleshooting below.

- [ ] **ICC CO-FACILITATOR** — On the ICC floor laptop, open a browser in full-screen (F11) and go to:
  ```
  http://[IP ADDRESS]:8504
  ```
  You should see the dark ICC dashboard. Connect this laptop to the ICC floor screen via HDMI.

### Step 5: Configure the ICC Dashboard
- [ ] **ICC CO-FACILITATOR** — In the ICC dashboard sidebar:
  - Confirm HIE Network is set to **"Connected"**
  - Do NOT start the simulation clock yet — wait for Dr. Lambert's signal at Phase 1 start
  - Confirm the "Auto-refresh every 30s" checkbox is checked

### Step 6: Test the Auto-Save Loop
- [ ] **TECH LEAD** — On a team laptop, go to `http://[IP]:8502`, enter a test team name (e.g., "TEST"), advance to Phase 1, and lock in one decision
- [ ] **TECH LEAD** — Check that a file named `SHIFT_TEST.json` appeared in the `v2/submissions/` folder on the instructor laptop
- [ ] **ICC CO-FACILITATOR** — Confirm the TEST team panel appears on the ICC dashboard after the next 30-second refresh (or click "Refresh Now" in the sidebar)
- [ ] **TECH LEAD** — Delete the test file: `rm v2/submissions/SHIFT_TEST.json`

---

## SECTION 3 — Room Setup (run in parallel with tech setup)

### Main Floor
- [ ] **CO-FACILITATOR** — Set up team tables (one per team, groups of 5)
- [ ] **CO-FACILITATOR** — Place supply kits at each table: paper, pens, markers, card stock
- [ ] **CO-FACILITATOR** — Place one laptop per team (teams bring their own or use provided)
- [ ] **CO-FACILITATOR** — Write team WiFi URL on the whiteboard or a visible card at each table:
  ```
  http://[IP ADDRESS]:8502
  ```

### ICC Floor (Second Floor)
- [ ] **ICC CO-FACILITATOR** — Connect ICC laptop to the large screen (HDMI)
- [ ] **ICC CO-FACILITATOR** — Open ICC dashboard in full-screen browser: `http://[IP]:8504`
- [ ] **ICC CO-FACILITATOR** — Set browser to full-screen mode (F11 / Cmd+Shift+F on Mac)
- [ ] **ICC CO-FACILITATOR** — Place intelligence cards at the ICC station in a folder:
  - ANSSI Advisory Card (Card 1) — top of pile
  - HIE Advisory Card (Card 2)
  - Regional Briefing Cards 3A–3D — labeled and ready
- [ ] **ICC CO-FACILITATOR** — Familiarize yourself with the Regional Briefing script (see Intelligence Cards doc, Facilitator Notes section)

---

## SECTION 4 — Pre-Simulation Briefing (15 min before students)

- [ ] **YOU** — Confirm all team laptops can reach `http://[IP]:8502` in their browsers
- [ ] **YOU** — Brief ICC co-facilitator on timing for each dispatch (Phases 1, 2, 3)
- [ ] **YOU** — Brief co-facilitator on Phase 3 in-character role (Regional Health Authority Director)
- [ ] **ICC CO-FACILITATOR** — Review which intelligence cards go to which teams:
  - Only use as many Regional Briefing cards as you have teams
  - Default order: 3A → 3B → 3C → 3D
- [ ] **YOU** — Start Phase 0 (student orientation) when ready — do NOT start the simulation clock yet

---

## SECTION 5 — Simulation Start Protocol

**When Phase 1 begins (after orientation):**

- [ ] **YOU** — Announce Phase 1 to the room
- [ ] **ICC CO-FACILITATOR** — In ICC dashboard sidebar, click **"▶ Start Clock"** immediately
- [ ] The GDPR countdown and financial burn will begin automatically

---

## SECTION 6 — During Simulation Quick Reference

### ICC Dispatch Timing

| Dispatch | Phase | Your cue | Who goes up | Card to hand |
|----------|-------|---------|-------------|-------------|
| ANSSI Briefing | Phase 1 — after first decision set | "IT Security and HIM Director: you are being called to the Incident Command Center. Go now." | IT Security + HIM Director (one team at a time) | Card 1: ANSSI Advisory |
| HIE Spread | Phase 2 — ~20 min in (play HIE audio inject) | "IT Security: urgent escalation at the ICC. Go immediately." | IT Security Lead (their team only) | Card 2: HIE Advisory |
| Regional Briefing | Phase 3 — after Phase 2 complete | "Incident Commanders: all of you, ICC, now." | All ICs simultaneously | Cards 3A–3D (one per team) |
| Media Crisis | Phase 4 — when media inject fires | "IC and Communications Officer: ICC, immediately." | IC + Comms Officer (their team) | No card — they view media board on screen |

### ICC Co-Facilitator: HIE Status Toggles
| When | Action |
|------|--------|
| Phase 2 HIE inject fires | Sidebar → HIE Network → **"Compromised"** |
| Team makes HIE disconnection decision | Sidebar → HIE Network → **"Isolated"** |

### Phase 3 — Regional Briefing Script (ICC Co-Facilitator)
Deliver this in character as the Regional Health Authority Director (~3 minutes):

> *"Thank you for coming. I'll be direct — we have a regional situation. Sainte-Claire has been identified as the likely origin of anomalous activity affecting two partner hospitals. ANSSI has issued a national advisory recommending against ransom payment. The GDPR clock is at Hour 20 — you have 52 hours remaining. And Le Monde has contacted our office. National press coverage is imminent."*

Then hand each IC their team-specific card. Give them 2 minutes to read. Announce:

> *"You have two minutes before you return to your teams. In a real incident, Incident Commanders talk to each other. Use this time."*

Step back. Observe what they share. After 2 minutes:

> *"Return to your teams. You have five minutes to brief them before we continue."*

---

## SECTION 7 — Wrap-Up and Export

- [ ] At simulation end, remind all teams to export their PDF report from the student app
- [ ] Reports auto-download to team laptops — teams upload to Canvas assignment
- [ ] After all teams export, you can close the Streamlit terminal windows
- [ ] The `v2/submissions/` folder on your laptop contains all team JSON files — back these up if you want a record

---

## SECTION 8 — Troubleshooting

**Teams can't reach `http://[IP]:8502`**
- Confirm all laptops are on the same WiFi network (same SSID, same subnet)
- Try `http://[IP]:8502` from the instructor laptop itself — if that fails, Streamlit didn't launch correctly
- Rerun: `streamlit run v2/student_app_v2.py --server.port 8502`
- If port 8502 is in use, switch to 8510: `--server.port 8510` (update the URL you give teams)

**ICC dashboard shows "Waiting for team data" even after teams start**
- Confirm teams are connecting to the student app (v2) URL, not the old one
- On instructor laptop, check: `ls v2/submissions/` — you should see `SHIFT_[teamname].json` files
- If no files: the auto-save may have failed silently. Ask one team to use the manual "💾 Save Progress" button in the student app sidebar as a fallback.

**ICC dashboard not updating**
- Click "Refresh Now" in the ICC dashboard sidebar
- Confirm "Auto-refresh every 30s" is checked
- If still stale, reload the browser tab entirely (F5)

**Port already in use error**
```
OSError: [Errno 48] Address already in use
```
Kill the existing process and relaunch:
```
lsof -ti:8502 | xargs kill -9
lsof -ti:8504 | xargs kill -9
```
Then relaunch both apps.

**Streamlit not found**
```
command not found: streamlit
```
Install it: `pip3 install streamlit fpdf2`
Or try: `python3 -m streamlit run v2/student_app_v2.py --server.port 8502`

**Student app crashes mid-simulation**
- Streamlit sessions are browser-based — each team's progress lives in their browser tab
- If a team's browser closes accidentally, their data may be recoverable from the last auto-save in `v2/submissions/`
- Have the team load their saved file: student app sidebar → "📂 Load Saved Progress"

---

## Quick Reference Card (tear off or screenshot for co-facilitator)

```
STUDENT APP:   http://[IP]:8502
ICC DASHBOARD: http://[IP]:8504

PHASE 1: After decision set → IT Security + HIM Director → ICC → Card 1
PHASE 2: ~20 min in, HIE inject → IT Security → ICC → Card 2
         Toggle ICC dashboard: HIE = Compromised
PHASE 3: End of Phase 2 → All ICs → ICC → Cards 3A-3D
         Run 3-min Regional Authority briefing (in character)
         2-min IC exchange → ICs return → 5-min team brief → Break
PHASE 4: Media inject → IC + Comms → ICC → no card, view media board
```
