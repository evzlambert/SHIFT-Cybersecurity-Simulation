"""
SHIFT Cybersecurity Breach Simulation — Instructor Projection App v2 ("SENTINEL")
Centre Hospitalier Sainte-Claire | Saint-Etienne, France

Enhanced cinematic command-center edition. Run on the classroom projector.
Original instructor_app.py is preserved; this is a standalone alternative.

Launch:  python3 -m streamlit run instructor_app_v2.py
Audio:   Ensure audio/ directory contains slide_00.mp3 through slide_34.mp3
"""

import streamlit as st
import base64
import csv
import io
import json
import os
import time

SUBMISSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions")
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

st.set_page_config(
    page_title="SENTINEL — Sainte-Claire Incident Command",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# CSS — Security Operations Center command-center aesthetic
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@400;700;900&display=swap');

/* ── Base ── */
:root {
    --red:      #ff1a1a;
    --red-dim:  #8b0000;
    --amber:    #ff8c00;
    --amber-dim:#5c3300;
    --cyan:     #00e5ff;
    --cyan-dim: #004d60;
    --green:    #00ff88;
    --green-dim:#004422;
    --purple:   #b44aff;
    --bg:       #020408;
    --bg2:      #060c14;
    --bg3:      #0a1420;
    --panel:    #0d1b2a;
    --border:   #1a3050;
    --text:     #e0ecf8;
    --text-dim: #8899b8;
    --mono:     'Share Tech Mono', monospace;
    --head:     'Orbitron', monospace;
    --body:     'Rajdhani', sans-serif;
}

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body);
}

/* Scanline overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.07) 2px,
        rgba(0,0,0,0.07) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* Vignette */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at center,
        transparent 60%,
        rgba(0,0,0,0.5) 100%);
    pointer-events: none;
    z-index: 9998;
}

.block-container {
    max-width: 1280px !important;
    padding-top: 0.5rem !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── TOP STATUS BAR ── */
.sentinel-header {
    background: linear-gradient(90deg, #020408 0%, #0d1b2a 40%, #0d1b2a 60%, #020408 100%);
    border-bottom: 1px solid var(--red);
    padding: 8px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.sentinel-header::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    animation: scanSweep 4s linear infinite;
}
@keyframes scanSweep {
    to { left: 200%; }
}
.sentinel-wordmark {
    font-family: var(--head);
    font-size: 1.1em;
    font-weight: 900;
    color: var(--red);
    letter-spacing: 4px;
    text-shadow: 0 0 20px rgba(255,26,26,0.6);
}
.sentinel-sub {
    font-family: var(--mono);
    font-size: 0.75em;
    color: var(--text-dim);
    letter-spacing: 2px;
}
.incident-badge {
    background: var(--red-dim);
    border: 1px solid var(--red);
    border-radius: 3px;
    padding: 4px 16px;
    font-family: var(--head);
    font-size: 0.7em;
    color: var(--red);
    letter-spacing: 3px;
    animation: badgePulse 1.5s ease-in-out infinite;
}
@keyframes badgePulse {
    0%, 100% { box-shadow: 0 0 6px rgba(255,26,26,0.4); }
    50%       { box-shadow: 0 0 18px rgba(255,26,26,0.8); }
}

/* ── TICKER BAR ── */
.ticker-wrap {
    background: rgba(255,26,26,0.08);
    border-top: 1px solid rgba(255,26,26,0.3);
    border-bottom: 1px solid rgba(255,26,26,0.3);
    overflow: hidden;
    height: 28px;
    margin-bottom: 16px;
}
.ticker-content {
    display: inline-block;
    white-space: nowrap;
    font-family: var(--mono);
    font-size: 0.75em;
    color: var(--red);
    letter-spacing: 1px;
    padding: 5px 0;
    animation: tickerScroll 40s linear infinite;
}
@keyframes tickerScroll {
    from { transform: translateX(100vw); }
    to   { transform: translateX(-100%); }
}

/* ── NAV BAR ── */
.nav-container {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

/* ── SLIDE WRAPPER ── */
.slide-wrapper {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 28px 36px;
    min-height: 480px;
    position: relative;
    overflow: hidden;
}
.slide-wrapper::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), var(--amber), transparent);
    opacity: 0.6;
}

/* ── ANIMATIONS ── */
.fade-in {
    animation: fadeUp 0.8s ease-out both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.glitch {
    animation: fadeUp 0.5s ease-out both;
    position: relative;
}
.glitch::before, .glitch::after {
    content: attr(data-text);
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
}
.glitch::before {
    color: var(--cyan);
    animation: glitchTop 3s infinite;
    clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
    transform: translate(-2px, -2px);
}
.glitch::after {
    color: var(--red);
    animation: glitchBot 3s infinite;
    clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
    transform: translate(2px, 2px);
}
@keyframes glitchTop {
    0%, 90%, 100% { transform: translate(-2px, -2px); opacity: 0; }
    92%, 94% { transform: translate(2px, -2px); opacity: 0.8; }
    96%, 98% { transform: translate(-4px, 2px); opacity: 0.6; }
}
@keyframes glitchBot {
    0%, 85%, 100% { transform: translate(2px, 2px); opacity: 0; }
    87%, 89% { transform: translate(-2px, 3px); opacity: 0.8; }
    91%, 93% { transform: translate(3px, -1px); opacity: 0.5; }
}

/* ── PHASE TITLE ── */
.phase-header {
    text-align: center;
    margin-bottom: 8px;
}
.phase-label {
    font-family: var(--mono);
    font-size: 0.7em;
    color: var(--text-dim);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.phase-name {
    font-family: var(--head);
    font-size: 2.2em;
    font-weight: 900;
    color: var(--red);
    letter-spacing: 3px;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(255,26,26,0.4);
    margin: 0;
}
.phase-time {
    font-family: var(--mono);
    font-size: 0.85em;
    color: var(--amber);
    letter-spacing: 2px;
    margin-top: 4px;
}
.phase-divider {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    margin: 12px auto;
}

/* ── EVENT FEED ── */
.event-feed { margin: 16px 0; }
.event-row {
    display: grid;
    grid-template-columns: 90px 1fr;
    gap: 0;
    margin-bottom: 8px;
    animation: feedSlide 0.6s ease-out both;
}
.event-row:nth-child(1) { animation-delay: 0.1s; }
.event-row:nth-child(2) { animation-delay: 0.3s; }
.event-row:nth-child(3) { animation-delay: 0.5s; }
.event-row:nth-child(4) { animation-delay: 0.7s; }
.event-row:nth-child(5) { animation-delay: 0.9s; }
.event-row:nth-child(6) { animation-delay: 1.1s; }
.event-row:nth-child(7) { animation-delay: 1.3s; }
@keyframes feedSlide {
    from { opacity: 0; transform: translateX(-16px); }
    to   { opacity: 1; transform: translateX(0); }
}
.event-ts {
    font-family: var(--mono);
    font-size: 0.78em;
    padding: 10px 10px 10px 0;
    border-right: 2px solid var(--red);
    text-align: right;
    color: var(--red);
    align-self: stretch;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}
.event-ts.amber  { color: var(--amber); border-right-color: var(--amber); }
.event-ts.cyan   { color: var(--cyan);  border-right-color: var(--cyan);  }
.event-ts.green  { color: var(--green); border-right-color: var(--green); }
.event-body {
    background: rgba(255,26,26,0.05);
    border-top: 1px solid rgba(255,26,26,0.15);
    border-right: 1px solid rgba(255,26,26,0.15);
    border-bottom: 1px solid rgba(255,26,26,0.15);
    border-radius: 0 4px 4px 0;
    padding: 10px 16px;
    font-size: 1.05em;
    color: var(--text);
    line-height: 1.5;
    font-family: var(--body);
}
.event-body.amber  { background: rgba(255,140,0,0.05); border-color: rgba(255,140,0,0.2); }
.event-body.cyan   { background: rgba(0,229,255,0.04); border-color: rgba(0,229,255,0.2); }
.event-body.green  { background: rgba(0,255,136,0.04); border-color: rgba(0,255,136,0.2); }
.ransom-line {
    font-family: var(--mono);
    color: var(--red);
    font-size: 0.9em;
    margin-top: 6px;
    border-left: 3px solid var(--red);
    padding-left: 10px;
    opacity: 0;
    animation: typeIn 1s ease-out 1.5s both;
}
@keyframes typeIn {
    from { opacity: 0; max-height: 0; }
    to   { opacity: 1; max-height: 60px; }
}

/* ── CRITICAL ALARM ── */
.alarm-bar {
    background: linear-gradient(135deg, #1a0000 0%, #2d0000 100%);
    border: 1px solid var(--red);
    border-radius: 4px;
    padding: 20px 30px;
    text-align: center;
    font-family: var(--head);
    font-size: 1.4em;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 3px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}
.alarm-bar::before {
    content: '⬛';
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.8em;
    animation: alarmDot 0.8s ease-in-out infinite;
}
.alarm-bar::after {
    content: '⬛';
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.8em;
    animation: alarmDot 0.8s ease-in-out infinite 0.4s;
}
@keyframes alarmDot {
    0%, 100% { opacity: 1; color: var(--red); }
    50%       { opacity: 0.2; }
}
.alarm-bar.amber {
    background: linear-gradient(135deg, #1a0a00 0%, #2d1500 100%);
    border-color: var(--amber);
    color: var(--amber);
}
.alarm-bar.amber::before, .alarm-bar.amber::after {
    animation-name: alarmDotAmber;
}
@keyframes alarmDotAmber {
    0%, 100% { color: var(--amber); opacity: 1; }
    50%       { opacity: 0.2; }
}

/* ── SYSTEM GRID ── */
.sys-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
    margin: 12px 0;
}
.sys-cell {
    border-radius: 3px;
    padding: 10px 4px;
    text-align: center;
    font-family: var(--mono);
    font-size: 0.72em;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
}
.sys-cell::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: rgba(255,255,255,0.2);
}
.sys-up {
    background: linear-gradient(180deg, #003320, #001a10);
    border: 1px solid var(--green);
    color: var(--green);
    text-shadow: 0 0 8px rgba(0,255,136,0.5);
}
.sys-down {
    background: linear-gradient(180deg, #2d0000, #1a0000);
    border: 1px solid var(--red);
    color: var(--red);
    text-shadow: 0 0 8px rgba(255,26,26,0.5);
    animation: sysDownFlicker 2s ease-in-out infinite;
}
@keyframes sysDownFlicker {
    0%, 90%, 100% { opacity: 1; }
    92%           { opacity: 0.6; }
    94%           { opacity: 1; }
    96%           { opacity: 0.4; }
    98%           { opacity: 1; }
}
.sys-degraded {
    background: linear-gradient(180deg, #2d1800, #1a0e00);
    border: 1px solid var(--amber);
    color: var(--amber);
    text-shadow: 0 0 8px rgba(255,140,0,0.5);
}

/* ── METRICS ── */
.metrics-row {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 8px;
    margin: 16px 0;
}
.metric-cell {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 20px;
    text-align: center;
    min-width: 120px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.8s ease-out both;
}
.metric-cell::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: var(--red);
    opacity: 0.4;
}
.metric-cell.amber::after { background: var(--amber); }
.metric-val {
    font-family: var(--head);
    font-size: 2em;
    font-weight: 700;
    color: var(--red);
    text-shadow: 0 0 12px rgba(255,26,26,0.4);
    display: block;
}
.metric-cell.amber .metric-val { color: var(--amber); text-shadow: 0 0 12px rgba(255,140,0,0.4); }
.metric-cell.cyan   .metric-val { color: var(--cyan);  text-shadow: 0 0 12px rgba(0,229,255,0.4); }
.metric-lbl {
    font-family: var(--mono);
    font-size: 0.65em;
    color: var(--text-dim);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
    display: block;
}

/* ── PAUSE SCREEN ── */
.pause-wrap {
    background: linear-gradient(135deg, #001a0d, #003320);
    border: 1px solid var(--green);
    border-radius: 6px;
    padding: 48px 36px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.pause-wrap::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(0,255,136,0.03) 60deg, transparent 120deg);
    animation: radarSpin 8s linear infinite;
}
@keyframes radarSpin { to { transform: rotate(360deg); } }
.pause-title {
    font-family: var(--head);
    font-size: 2em;
    font-weight: 900;
    color: var(--green);
    letter-spacing: 4px;
    text-shadow: 0 0 20px rgba(0,255,136,0.5);
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
}
.pause-body {
    font-family: var(--body);
    font-size: 1.15em;
    color: #cceedd;
    line-height: 1.7;
    position: relative;
    z-index: 1;
}
.pause-questions {
    background: rgba(0,0,0,0.4);
    border-left: 3px solid var(--green);
    border-radius: 0 4px 4px 0;
    padding: 16px 20px;
    text-align: left;
    margin: 16px auto;
    max-width: 680px;
    font-family: var(--mono);
    font-size: 0.9em;
    color: #b8eec8;
    line-height: 1.9;
    position: relative;
    z-index: 1;
}
.pause-footer {
    font-family: var(--mono);
    font-size: 0.72em;
    color: rgba(0,255,136,0.9);
    margin-top: 20px;
    letter-spacing: 1px;
    position: relative;
    z-index: 1;
}

/* ── STATION CUE ── */
.station-cue {
    background: linear-gradient(135deg, #1a0d00, #2d1800);
    border: 1px solid var(--amber);
    border-radius: 4px;
    padding: 14px 20px;
    margin-top: 16px;
    position: relative;
    z-index: 1;
}
.station-label {
    font-family: var(--mono);
    font-size: 0.65em;
    color: var(--amber);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.station-body {
    font-family: var(--body);
    font-size: 1em;
    color: #fff0c8;
    line-height: 1.7;
}

/* ── BREAK SCREEN ── */
.break-wrap {
    background: linear-gradient(135deg, #0a001a, #16003a);
    border: 1px solid var(--purple);
    border-radius: 6px;
    padding: 80px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.break-wrap::before {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(180,74,255,0.06) 0%, transparent 70%);
    transform: translate(-50%, -50%);
    animation: breathe 4s ease-in-out infinite;
}
@keyframes breathe {
    0%, 100% { transform: translate(-50%, -50%) scale(1); }
    50%       { transform: translate(-50%, -50%) scale(1.15); }
}
.break-title {
    font-family: var(--head);
    font-size: 3.5em;
    font-weight: 900;
    color: var(--purple);
    letter-spacing: 8px;
    text-shadow: 0 0 40px rgba(180,74,255,0.6);
    position: relative;
    z-index: 1;
}
.break-body {
    font-family: var(--body);
    font-size: 1.2em;
    color: #ddb8ff;
    margin-top: 24px;
    line-height: 1.8;
    position: relative;
    z-index: 1;
}

/* ── NEWS TICKER CARD ── */
.news-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-left: 4px solid var(--cyan);
    border-radius: 0 4px 4px 0;
    padding: 20px 24px;
    margin: 12px 0;
    animation: fadeUp 0.8s ease-out both;
}
.news-source {
    font-family: var(--mono);
    font-size: 0.7em;
    color: var(--cyan);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    animation: sourceFlash 3s ease-in-out infinite;
}
@keyframes sourceFlash {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}
.news-body {
    font-family: var(--body);
    font-size: 1.15em;
    color: #cce6f8;
    line-height: 1.6;
}

/* ── VOICEMAIL ── */
.voicemail-card {
    background: var(--bg3);
    border: 1px solid rgba(255,140,0,0.4);
    border-radius: 4px;
    padding: 20px 24px;
    margin: 12px 0;
    animation: fadeUp 0.8s ease-out both;
}
.vm-label {
    font-family: var(--mono);
    font-size: 0.7em;
    color: var(--amber);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.vm-label::before {
    content: '●';
    color: var(--red);
    animation: alarmDot 0.8s infinite;
    font-size: 0.9em;
}
.vm-body {
    font-family: var(--body);
    font-size: 1.1em;
    color: #f0cc98;
    font-style: italic;
    line-height: 1.65;
}

/* ── SCENE ── */
.scene-card {
    background: var(--bg3);
    border: 1px solid rgba(180,74,255,0.35);
    border-radius: 4px;
    padding: 20px 24px;
    margin: 12px 0;
    animation: fadeUp 0.8s ease-out both;
}
.scene-label {
    font-family: var(--mono);
    font-size: 0.7em;
    color: var(--purple);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.scene-body {
    font-family: var(--body);
    font-size: 1.1em;
    color: #e0ccf8;
    line-height: 1.65;
}

/* ── SOCIAL POST ── */
.social-card {
    background: var(--bg3);
    border: 1px solid rgba(0,229,255,0.25);
    border-radius: 4px;
    padding: 16px 20px;
    margin: 8px 0;
    animation: feedSlide 0.6s ease-out both;
}
.social-card:nth-child(1) { animation-delay: 0.3s; }
.social-card:nth-child(2) { animation-delay: 0.9s; }
.social-card:nth-child(3) { animation-delay: 1.5s; }
.social-handle {
    font-family: var(--mono);
    font-size: 0.82em;
    color: var(--cyan);
    font-weight: bold;
    margin-bottom: 6px;
}
.social-body {
    font-family: var(--body);
    font-size: 1.05em;
    color: #b8e0f5;
    line-height: 1.5;
}

/* ── DECISION PROMPT ── */
.decision-box {
    background: linear-gradient(135deg, #00080d, #001a2d);
    border: 1px solid rgba(0,229,255,0.4);
    border-radius: 4px;
    padding: 20px 28px;
    text-align: center;
    font-family: var(--body);
    font-size: 1.2em;
    color: #c0eeff;
    line-height: 1.6;
    margin: 16px 0;
    animation: fadeUp 0.8s ease-out 0.4s both;
}

/* ── TITLE SLIDE ── */
.title-logo {
    text-align: center;
    padding: 20px 0 10px;
}
.title-main {
    font-family: var(--head);
    font-size: 2.6em;
    font-weight: 900;
    color: var(--red);
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: 0 0 40px rgba(255,26,26,0.5);
    animation: fadeUp 1s ease-out both;
}
.title-hospital {
    font-family: var(--mono);
    font-size: 0.9em;
    color: #99b8d8;
    letter-spacing: 3px;
    margin-top: 6px;
    animation: fadeUp 1s ease-out 0.3s both;
}
.title-stats {
    text-align: center;
    font-family: var(--body);
    font-size: 1.2em;
    color: #aac4dc;
    line-height: 2;
    margin: 28px 0;
    animation: fadeUp 1s ease-out 0.6s both;
}
.title-timestamp {
    font-family: var(--head);
    font-size: 1.1em;
    color: var(--red);
    letter-spacing: 4px;
    text-align: center;
    margin: 12px 0;
    animation: fadeUp 1s ease-out 0.9s both;
}
.title-allclear {
    font-family: var(--mono);
    font-size: 0.8em;
    color: var(--green);
    text-align: center;
    margin-top: 8px;
    letter-spacing: 2px;
    animation: fadeUp 1s ease-out 1.2s both;
}

/* ── END SLIDE ── */
.end-wrap {
    background: linear-gradient(135deg, #001a0d, #003320);
    border: 1px solid var(--green);
    border-radius: 6px;
    padding: 40px;
    text-align: center;
}
.end-title {
    font-family: var(--head);
    font-size: 2.5em;
    color: var(--green);
    letter-spacing: 4px;
    text-shadow: 0 0 30px rgba(0,255,136,0.4);
}
.end-body {
    font-family: var(--body);
    font-size: 1.15em;
    color: #aaeaaa;
    margin-top: 20px;
    line-height: 1.9;
}

/* ── SLIDE COUNTER ── */
.slide-counter {
    font-family: var(--mono);
    font-size: 0.7em;
    color: var(--text-dim);
    text-align: center;
    letter-spacing: 2px;
    margin-top: 10px;
}
.progress-bar-bg {
    width: 100%;
    height: 2px;
    background: var(--border);
    border-radius: 1px;
    margin-top: 6px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--red), var(--amber));
    border-radius: 1px;
    transition: width 0.4s ease;
}

/* Streamlit button override */
.stButton > button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.75em !important;
    letter-spacing: 1px !important;
    border-radius: 3px !important;
}
.stButton > button:hover {
    border-color: var(--red) !important;
    color: var(--red) !important;
    box-shadow: 0 0 10px rgba(255,26,26,0.2) !important;
}
.stButton > button[kind="primary"] {
    background: rgba(255,26,26,0.1) !important;
    border-color: var(--red) !important;
    color: var(--red) !important;
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
if "auto_advance" not in st.session_state:
    st.session_state.auto_advance = True

# ---------------------------------------------------------------------------
# Audio helpers
# ---------------------------------------------------------------------------
def get_audio_html(slide_num, autoplay=True, auto_advance=False, stop_slide=False):
    filename = os.path.join(AUDIO_DIR, f"slide_{slide_num:02d}.mp3")
    if not os.path.exists(filename):
        return ""
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_id = f"audio_{slide_num}"
    autoplay_attr = "autoplay" if autoplay else ""
    # Build JS: play + optional auto-advance on ended
    advance_js = ""
    if auto_advance and not stop_slide:
        advance_js = f"""
        a.addEventListener('ended', function() {{
            setTimeout(function() {{
                var attempt = 0;
                function tryNext() {{
                    // Streamlit markdown runs inside an iframe — search parent doc first
                    var docs = [];
                    try {{ docs.push(window.parent.document); }} catch(e) {{}}
                    docs.push(document);
                    var btn = null;
                    for (var d = 0; d < docs.length && !btn; d++) {{
                        // Try Streamlit's primary button testid
                        btn = docs[d].querySelector('[data-testid="baseButton-primary"]');
                        if (!btn) {{
                            var all = docs[d].querySelectorAll('button');
                            for (var i = 0; i < all.length; i++) {{
                                var t = (all[i].textContent || '').trim();
                                if (t.indexOf('NEXT') !== -1 && !all[i].disabled) {{
                                    btn = all[i]; break;
                                }}
                            }}
                        }}
                    }}
                    if (btn && !btn.disabled) {{
                        btn.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true}}));
                    }} else if (++attempt < 30) {{
                        setTimeout(tryNext, 400);
                    }}
                }}
                tryNext();
            }}, 800);
        }});"""
    play_script = f"""
    <script>
    (function(){{
        var a = document.getElementById('{audio_id}');
        if (!a) return;
        a.currentTime = 0;
        a.play().catch(function(){{}});
        {advance_js}
    }})();
    </script>
    """ if autoplay else ""
    return f"""
    <audio controls {autoplay_attr} id="{audio_id}"
           src="data:audio/mp3;base64,{b64}" type="audio/mp3"
           style="width:100%;height:36px;margin-top:8px;filter:invert(0.8)sepia(1)hue-rotate(160deg);">
    </audio>{play_script}"""

def sound_cue_js(cue_type="alert"):
    sounds = {
        "alert":    "o.frequency.setValueAtTime(880,c.currentTime);g.gain.setValueAtTime(0.25,c.currentTime);o.start();o.stop(c.currentTime+0.12);setTimeout(()=>{let o2=c.createOscillator();let g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o2.frequency.setValueAtTime(880,c.currentTime);g2.gain.setValueAtTime(0.25,c.currentTime);o2.start();o2.stop(c.currentTime+0.12);},220);",
        "critical": "o.frequency.setValueAtTime(220,c.currentTime);o.frequency.linearRampToValueAtTime(880,c.currentTime+0.15);g.gain.setValueAtTime(0.4,c.currentTime);o.start();o.stop(c.currentTime+0.35);setTimeout(()=>{let o2=c.createOscillator();let g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o2.frequency.setValueAtTime(220,c.currentTime);o2.frequency.linearRampToValueAtTime(880,c.currentTime+0.15);g2.gain.setValueAtTime(0.4,c.currentTime);o2.start();o2.stop(c.currentTime+0.35);},500);",
        "notification": "o.frequency.setValueAtTime(587,c.currentTime);o.frequency.setValueAtTime(784,c.currentTime+0.1);g.gain.setValueAtTime(0.15,c.currentTime);o.start();o.stop(c.currentTime+0.2);",
        "phone":    "o.frequency.setValueAtTime(440,c.currentTime);g.gain.setValueAtTime(0.18,c.currentTime);o.start();o.stop(c.currentTime+0.5);setTimeout(()=>{let o2=c.createOscillator();let g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o2.frequency.setValueAtTime(440,c.currentTime);g2.gain.setValueAtTime(0.18,c.currentTime);o2.start();o2.stop(c.currentTime+0.5);},700);",
    }
    code = sounds.get(cue_type, sounds["notification"])
    return f"""<script>(function(){{try{{var c=new(window.AudioContext||window.webkitAudioContext)();var o=c.createOscillator();var g=c.createGain();o.connect(g);g.connect(c.destination);{code}}}catch(e){{}}}})();</script>"""

# ---------------------------------------------------------------------------
# System grid helper
# ---------------------------------------------------------------------------
def sys_grid(statuses):
    cells = "".join(f'<div class="sys-cell {cls}">{name}</div>' for name, cls in statuses)
    return f'<div class="sys-grid">{cells}</div>'

ALL_UP   = [("EHR / DPI","sys-up"),("Lab / LIS","sys-up"),("PACS","sys-up"),
            ("Pharmacy","sys-up"),("Pt Portal","sys-up"),
            ("Email","sys-up"),("Scheduling","sys-up"),("Billing","sys-up"),
            ("Nurse Call","sys-up"),("Badge","sys-up")]
ALL_DOWN = [("EHR / DPI","sys-down"),("Lab / LIS","sys-down"),("PACS","sys-down"),
            ("Pharmacy","sys-down"),("Pt Portal","sys-down"),
            ("Email","sys-down"),("Scheduling","sys-down"),("Billing","sys-down"),
            ("Nurse Call","sys-degraded"),("Badge","sys-degraded")]
DAY2     = [("EHR / DPI","sys-down"),("Lab / LIS","sys-down"),("PACS","sys-down"),
            ("Pharmacy","sys-down"),("Pt Portal","sys-down"),
            ("Email","sys-down"),("Scheduling","sys-down"),("Billing","sys-down"),
            ("Nurse Call","sys-up"),("Badge","sys-up")]
DAY3     = [("EHR / DPI","sys-down"),("Lab / LIS","sys-down"),("PACS","sys-down"),
            ("Pharmacy","sys-down"),("Pt Portal","sys-down"),
            ("Email","sys-degraded"),("Scheduling","sys-down"),("Billing","sys-down"),
            ("Nurse Call","sys-up"),("Badge","sys-up")]
RECOVERY = [("EHR / DPI","sys-degraded"),("Lab / LIS","sys-degraded"),("PACS","sys-down"),
            ("Pharmacy","sys-degraded"),("Pt Portal","sys-down"),
            ("Email","sys-up"),("Scheduling","sys-degraded"),("Billing","sys-down"),
            ("Nurse Call","sys-up"),("Badge","sys-up")]

def metrics(*items):
    cells = ""
    for val, lbl, cls in items:
        cells += f'<div class="metric-cell {cls}"><span class="metric-val">{val}</span><span class="metric-lbl">{lbl}</span></div>'
    return f'<div class="metrics-row">{cells}</div>'

def phase_header(title, time_range=""):
    return f"""
<div class="phase-header fade-in">
    <div class="phase-label">INCIDENT TIMELINE</div>
    <div class="phase-name">{title}</div>
    {'<div class="phase-time">'+time_range+'</div>' if time_range else ''}
    <div class="phase-divider"></div>
</div>"""

def events(*rows):
    html = '<div class="event-feed">'
    for ts, body, variant in rows:
        html += f'''
<div class="event-row">
    <div class="event-ts {variant}">{ts}</div>
    <div class="event-body {variant}">{body}</div>
</div>'''
    html += "</div>"
    return html

def alarm(text, cls=""):
    return f'<div class="alarm-bar {cls}">{text}</div>'

def decision(text):
    return f'<div class="decision-box">{text}</div>'

def pause_slide(title, lead, questions, footer, station_html=""):
    return f"""
<div class="fade-in">
<div class="pause-wrap">
    <div class="pause-title">{title}</div>
    <div class="pause-body">{lead}</div>
    <div class="pause-questions">{questions}</div>
    <div class="pause-footer">{footer}</div>
</div>
{station_html}
</div>"""

def station(label, body):
    return f"""
<div class="station-cue">
    <div class="station-label">{label}</div>
    <div class="station-body">{body}</div>
</div>"""

# ---------------------------------------------------------------------------
# SLIDES  (type, html, sound_cue)
# ---------------------------------------------------------------------------
SLIDES = []

# 0: Title
SLIDES.append(("title", f"""
<div class="fade-in">
<div class="title-logo">
    <div class="title-main">SHIFT CYBERSECURITY BREACH SIMULATION</div>
    <div class="title-hospital">CENTRE HOSPITALIER SAINTE-CLAIRE &nbsp;·&nbsp; SAINT-ETIENNE, FRANCE</div>
</div>
<div class="title-stats">
    <p>A 350-bed regional hospital &nbsp;·&nbsp; 1,200 staff &nbsp;·&nbsp; 287 inpatients</p>
    <p>The only Level 1 trauma center and neonatal ICU in the region.</p>
</div>
<div class="title-timestamp">IT IS MONDAY — 06:12</div>
<div class="title-allclear">◉ ALL SYSTEMS OPERATIONAL</div>
{sys_grid(ALL_UP)}
</div>""", None))

# 1: First reports
SLIDES.append(("breach", f"""
<div class="fade-in">
{phase_header("THE BREACH BEGINS", "MONDAY — 06:12 TO 06:24")}
{events(
    ("06:12", "Night-shift nurse reports EHR is frozen on 3 ICU workstations.", "amber"),
    ("06:15", "Second report from maternity — cannot access birth plans.", "amber"),
    ("06:18", "IT help desk receives 12 simultaneous calls. Lab system returning errors.", "amber"),
    ("06:22", "Pharmacy technician: automated dispensing cabinets are unresponsive.", "amber"),
    ("06:24", 'Radiology PACS displays a message:<div class="ransom-line">» YOUR FILES ARE ENCRYPTED. CONTACT US FOR THE DECRYPTION KEY. YOU HAVE 72 HOURS. «</div>', ""),
)}
</div>""", "alert"))

# 2: Escalation
SLIDES.append(("breach", f"""
<div class="fade-in">
{phase_header("SYSTEMS FALLING", "MONDAY — 06:26 TO 06:42")}
{events(
    ("06:26", "Night admin restarts servers — ransom message on 4 of 6 core servers.", ""),
    ("06:30", "Pharmacy dispensing confirmed offline. Medication cabinets locked hospital-wide.", ""),
    ("06:33", "Patient portal goes dark. 47 telehealth appointments scheduled today.", ""),
    ("06:35", "Scheduling unresponsive. 142 outpatient appointments unconfirmable.", ""),
    ("06:38", "Billing and revenue cycle encrypted. No claims can be submitted.", ""),
    ("06:40", "<strong>IT confirms: LockBit variant ransomware across EHR, LIS, PACS, pharmacy, billing.</strong>", ""),
    ("06:42", "Forensics: initial access was <strong>11 days ago</strong> via phishing email to radiology tech.", ""),
)}
</div>""", "critical"))

# 3: Full picture
SLIDES.append(("breach", f"""
<div class="fade-in">
{phase_header("FULL-SCALE ATTACK CONFIRMED", "MONDAY — 06:45 TO 07:05")}
{events(
    ("06:45", "Email servers compromised. Communication limited to phone and in-person.", ""),
    ("06:48", "Nurse call system degraded. Some units reporting response delays.", "amber"),
    ("06:50", "Badge access intermittent. Pharmacy and server room potentially unsecured.", "amber"),
    ("06:55", "400+ day-shift staff arriving. Most have received no information.", "cyan"),
    ("07:00", "Hospital Incident Command System (HICS) activated.", "cyan"),
    ("07:05", "ANSSI contacted. Forensics team: 6–8 hours away.", "cyan"),
)}
{alarm("ALL MAJOR CLINICAL SYSTEMS ARE DOWN")}
{sys_grid(ALL_DOWN)}
</div>""", "critical"))

# 4: PAUSE — Phase 1
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "You are the hospital's crisis leadership team. It is 07:05 AM.",
    "1. What is your FIRST action? Downtime procedures or network isolation?\n2. How do you communicate to 1,200 staff with no email?\n3. 15 ICU patients on smart pump drips. 8 women in labor. 12 surgeries scheduled. What is your patient safety strategy?\n4. Who do you call first? Police, insurance, regulator, or the board?",
    "Discuss on your feet. Then return to your device to log your decisions.",
    station("ACTION STATIONS AFTER THIS PAUSE",
            "<strong>Station 1:</strong> Design an Emergency Downtime MAR (8 min) — Grab blank paper, design the form nurses will use<br>"
            "<strong>Station 2:</strong> Draft the Staff Communication Bulletin (6 min) — Write the actual words staff will receive")
), "notification"))

# 5: Downtime
SLIDES.append(("downtime", f"""
<div class="fade-in">
{phase_header("DOWNTIME OPERATIONS", "MONDAY 08:00 — TUESDAY 06:00 · HOUR 2 TO 24")}
{alarm("ALL CLINICAL SYSTEMS OPERATING MANUALLY", "amber")}
{sys_grid(ALL_DOWN)}
<div style="text-align:center; font-size:1.2em; color:var(--text); margin:24px 0; font-family:var(--body); line-height:2;">
<p>Every medication. Every patient ID check. Every lab order. Every note.</p>
<p style="color:var(--amber); font-weight:bold; font-size:1.25em; font-family:var(--head); letter-spacing:2px;">ON PAPER.</p>
</div>
{metrics(
    ("287","Inpatients",""),
    ("42","ICU Patients",""),
    ("8","Maternity",""),
    ("14","Patients Named Martin","amber"),
    ("0","Systems Online",""),
)}
</div>""", "alert"))

# 6: Near-miss
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("INJECT: NEAR-MISS MEDICATION EVENT", "HOUR 4")}
{events(
    ("REPORT", "A nurse flags a <strong>near-miss</strong>: without barcode scanning, <span style='color:var(--red)'>MARTIN, Jean-Pierre</span> vs. <span style='color:var(--red)'>MARTIN, Jean-Paul</span> — almost given the wrong medication.", "amber"),
    ("STATUS", "The manual five-rights check caught it. Staff are shaken and requesting additional safety protocols.", "amber"),
)}
{decision("How does your team prevent actual medication errors during the remainder of downtime?")}
</div>""", "alert"))

# 7: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "A near-miss just occurred. Your staff are scared.",
    "From your role's perspective: What is the immediate response?\nHow do you prevent the next one from being an actual error?",
    "Discuss, then log your decision in the student app.",
    station("ACTION STATION",
            "<strong>Station 3:</strong> Create Emergency Patient ID Wristband (6 min) — Design a handwritten wristband that solves the Martin problem")
), "notification"))

# 8: Ambulance
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("INJECT: AMBULANCE DIVERSION REQUEST", "HOUR 8")}
{events(
    ("STATUS", "The ED is overwhelmed. Without electronic triage or patient tracking, <strong>wait times have tripled</strong>. ED Medical Director requests diversion.", ""),
    ("CRITICAL", "Nearest Level 1 trauma center: <strong>45 minutes away</strong>. Only neonatal ICU in the region: <strong>yours</strong>.", "amber"),
    ("LIVE", "A pregnant woman at 36 weeks is in an ambulance <strong>en route to you right now</strong>.", "amber"),
)}
{decision("Do you approve diversion? What about the woman in the ambulance?")}
</div>""", "phone"))

# 9: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "An ambulance with a pregnant patient is en route. Your ED is overwhelmed.",
    "Full diversion? Partial? Deny entirely?\nWhat do you tell the paramedics right now?",
    "Discuss, then log your decision."
), "notification"))

# 10: Shift handoff
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("INJECT: THE 19:00 SHIFT HANDOFF", "HOUR 13")}
{events(
    ("19:00", "Evening shift arriving. Day shift: <strong>13 hours</strong> of crisis management. Evening staff have minimal information.", "cyan"),
    ("HANDOFF", "You must transfer: 287 inpatients (all on paper) · Active downtime procedures · Outstanding issues (near-miss, diversion status) · Location of all paper records", "amber"),
    ("MORALE", "Several day-shift nurses are in tears. Three refused to leave without knowing who would cover their patients.", "amber"),
)}
{decision("How do you hand off a paper-based hospital to staff who have never used paper?")}
</div>""", "notification"))

# 11: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "Evening staff are arriving. They know nothing about paper processes.",
    "How do you structure the handoff?\nKeep exhausted day-shift longer, or let them go?",
    "Discuss, then log your decision.",
    station("ACTION STATION",
            "<strong>Station 4:</strong> Build Your Shift Handoff Tool (8 min) — Design the one-page handoff template that every unit will use tonight")
), "notification"))

# 12: Paper crisis
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("INJECT: PAPER RECORDS CRISIS", "HOUR 18")}
{events(
    ("AUDIT", "<strong>3,200 pages</strong> of handwritten records accumulated. Quality audit of 50 records reveals:", "amber"),
)}
{metrics(
    ("34%","Missing DOB",""),
    ("22%","No Allergies",""),
    ("18%","Illegible",""),
    ("11%","Cannot Match to Patient",""),
    ("4","Duplicates","amber"),
)}
{decision("How do you manage the backlog while maintaining data integrity?")}
</div>""", "alert"))

# 13: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "3,200 pages. 11% unmatched. Illegible handwriting. Exhausted staff.",
    "What is your data management strategy?\nHow will you handle back-entry when systems return?",
    "Discuss, then log your decision. After this, we take a break.",
    station("ACTION STATION",
            "<strong>Station 5:</strong> Complete a Paper Patient Record (7 min) — Using ONLY blank paper, document a simulated patient intake. Experience the difficulty.")
), "notification"))

# 14: BREAK
SLIDES.append(("break", """
<div class="fade-in">
<div class="break-wrap">
    <div class="break-title">BREAK</div>
    <div class="break-body">
        <p>20 minutes. The crisis does not pause, but you can.</p>
        <p style="margin-top:24px; font-size:0.9em;">When you return, it will be <strong>Hour 24</strong>.<br>
        The media are calling. Families are arriving. Staff are breaking.<br>
        The pressure is about to intensify.</p>
    </div>
</div>
</div>""", None))

# 15: Day 2
SLIDES.append(("escalation", f"""
<div class="fade-in">
{phase_header("ESCALATION & STAKEHOLDER PRESSURE", "TUESDAY — HOUR 24 TO 48 · DAY 2")}
{alarm("24 HOURS OF DOWNTIME — EXTERNAL PRESSURE MOUNTING", "amber")}
{sys_grid(DAY2)}
{metrics(
    ("24h","Downtime",""),
    ("3,200","Paper Records",""),
    ("23","Surgeries Canceled",""),
    ("14","Patients Diverted","amber"),
    ("€240K","Revenue Lost","amber"),
)}
</div>""", "alert"))

# 16: Media
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("THE STORY BREAKS", "HOUR 26")}
<div class="news-card">
    <div class="news-source">BREAKING — France 3 Auvergne-Rhône-Alpes — 12:00 Noon</div>
    <div class="news-body">"Centre Hospitalier Sainte-Claire has been operating without its computer systems for over 24 hours following what sources describe as a 'major cyberattack.' Ambulances have been diverted. A hospital spokesperson confirmed a 'technology disruption' but declined to provide details. Patient advocacy groups demand transparency. The ARS says it is 'monitoring the situation.'"</div>
</div>
{decision("The phone is ringing. Media, patients, families. How do you respond?")}
</div>""", "notification"))

# 17: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "The story is on television. Your phone lines are overwhelmed.",
    "Press conference? Written statement? Full transparency?\nWho is the spokesperson? What is the ONE key message?",
    "Discuss, then log your decision.",
    station("ACTION STATION",
            "<strong>Station 6:</strong> Write the Press Statement (8 min) — Draft the actual words. Read it aloud. Have a teammate play journalist and ask a tough question.")
), "notification"))

# 18: Family
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("A FAMILY DEMANDS ANSWERS", "HOUR 28")}
<div class="scene-card">
    <div class="scene-label">Scene: Hospital Main Lobby</div>
    <div class="scene-body">A man approaches the information desk. Visibly upset. His mother, 82, admitted three days ago for pneumonia. Unable to reach anyone by phone. Portal down. Drove 90 minutes.<br><br>
    <em>"I can't access my mother's records. I don't know what medications she's on. The nurse told me they're using PAPER. Paper! What year is this? I want to know if my mother's personal information has been stolen. I want to speak to whoever is in charge. And if I don't get answers, I'm calling my lawyer and the press."</em></div>
</div>
{decision("Who responds? What do you say? What can't you say?")}
</div>""", "phone"))

# 19: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "This man represents hundreds of families with the same fears.",
    "Who meets with him? What can you share?\nHe's threatening legal action and media. How do you de-escalate?",
    "Discuss, then log your decision.",
    station("ACTION STATION",
            "<strong>Station 7:</strong> Create the Family Information Sheet (7 min) — Write the one-page handout for every worried family member. Have a teammate read it as a scared relative.")
), "notification"))

# 20: Staff morale
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("STAFF MORALE CRISIS", "HOUR 32")}
<div class="voicemail-card">
    <div class="vm-label">Voicemail — Marie-Claire, Charge Nurse, Unit 3B</div>
    <div class="vm-body">"This is Marie-Claire on 3B. I need to tell you that my nurses are done. We've been working 14-hour shifts on paper for two days. Three of my nurses called in sick today — I think they're not actually sick, they just can't take it anymore. The ones who are here are making mistakes. Small ones so far. But I'm scared. We had another near-miss — wrong dose calculated by hand because we don't have the EHR doing the math for us. I need more staff, I need someone to acknowledge what we're going through, and I need to know when this is going to end. Please call me back."</div>
</div>
{decision("Staff burnout is becoming a patient safety issue. What do you do?")}
</div>""", "phone"))

# 21: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "Marie-Claire is one of your best charge nurses. If she breaks, the unit breaks.",
    "Mutual aid? Reduce census? Crisis counseling? Shorter shifts?\nWhat does each option cost you?",
    "Discuss, then log your decision."
), "notification"))

# 22: Social media
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("SOCIAL MEDIA FIRESTORM", "HOUR 34")}
<div class="social-card">
    <div class="social-handle">@HealthWatchFR &nbsp;·&nbsp; 12,400 followers</div>
    <div class="social-body">THREAD: My aunt is a nurse at Sainte-Claire. She says they've been writing EVERYTHING by hand for 2 days. No access to patient histories. No medication barcodes. She's terrified of making an error. This is a patient safety EMERGENCY. 1/7</div>
</div>
<div class="social-card">
    <div class="social-handle">@PatientRightsFR &nbsp;·&nbsp; 34,200 followers</div>
    <div class="social-body">If Sainte-Claire has had 180,000 patient records stolen, where is the CNIL notification? GDPR requires transparency. Silence is not acceptable. #DataBreach #GDPR</div>
</div>
<div class="social-card">
    <div class="social-handle">Dr. Laurent M. &nbsp;·&nbsp; ✓ Verified Physician</div>
    <div class="social-body">The Sainte-Claire situation is exactly what we've warned about. French hospitals are chronically under-invested in cybersecurity. This will happen again.</div>
</div>
{decision("Social media is shaping the narrative. Do you engage or stay silent?")}
</div>""", "notification"))

# 23: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "A nurse's relative posted. Advocacy groups demanding answers.",
    "Official social media response? Ignore it?\nAsk the employee to remove it? Hire a crisis firm?",
    "Discuss, then log your decision."
), "notification"))

# 24: Department conflict
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("INTER-DEPARTMENT CONFLICT", "HOUR 36")}
<div class="scene-card">
    <div class="scene-label">Scene: Incident Command Center</div>
    <div class="scene-body">The Chief of Surgery and the HIM Director are in a heated argument.<br><br>
    <strong>Chief of Surgery:</strong> <em>"We operated for decades before computers. I am not letting a computer problem endanger my patients by delaying their care."</em><br><br>
    <strong>HIM Director:</strong> <em>"And we had higher error rates for decades before computers. We are not going backward. Every mislabeled specimen is a potential catastrophe."</em></div>
</div>
{decision("Both are right. Both are wrong. The Incident Commander must decide.")}
</div>""", "alert"))

# 25: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "Surgery vs. HIM. Patient harm from delay vs. patient harm from error.",
    "Resume elective surgery on paper? Delay? Compromise? Governance meeting?",
    "Discuss, then log your decision."
), "notification"))

# 26: Day 3
SLIDES.append(("critical", f"""
<div class="fade-in">
{phase_header("CRITICAL DECISIONS", "WEDNESDAY — HOUR 48 TO 72 · DAY 3")}
{alarm("RANSOM DEADLINE APPROACHING — GDPR CLOCK TICKING")}
{sys_grid(DAY3)}
{metrics(
    ("48h","Downtime",""),
    ("6,400","Paper Records",""),
    ("38","Surgeries Canceled",""),
    ("€480K","Revenue Lost","amber"),
    ("89","Complaints Filed",""),
)}
</div>""", "critical"))

# 27: Ransom
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("THE RANSOM DEMAND", "HOUR 50")}
{events(
    ("CONTACT", "The attackers have made formal contact through an encrypted channel.", ""),
)}
{metrics(
    ("€2.5M","Ransom Demand",""),
    ("€1M","Insurance Limit","amber"),
    ("180K","Records Stolen",""),
    ("48h","Deadline","amber"),
)}
{events(
    ("PROOF", "500 genuine patient records provided. Includes diagnoses, medications, national IDs, <strong>mental health and HIV status</strong>.", ""),
    ("ANSSI", "Advises: <strong>do not pay.</strong> — Loi LOPMI (2023): Police report within 72h of payment required for insurance coverage.", "amber"),
)}
{decision("€2.5 million. 180,000 patients. Mental health records. HIV status.<br>What do you recommend to the board?")}
</div>""", "critical"))

# 28: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "This is the hardest decision in the simulation.",
    "Pay? Negotiate? Refuse? Escalate?\nWhat are the ethical dimensions?\nWho bears the harm in each scenario?",
    "Discuss thoroughly, then log your decision and reasoning.",
    station("ACTION STATION",
            "<strong>Station 8:</strong> Draft the Board Recommendation Memo (8 min) — Write the formal one-page memo to the board. Situation, options, recommendation, rationale, risks.")
), "notification"))

# 29: GDPR
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("GDPR 72-HOUR NOTIFICATION DEADLINE", "HOUR 58 — 14 HOURS REMAINING")}
{events(
    ("LAW", "<strong>GDPR Article 33:</strong> Notify CNIL within 72 hours. Clock started 06:40 Monday. <strong>14 hours remain.</strong>", ""),
    ("FORENSICS", "Attackers had access <strong>11 days</strong> before encryption · Large data transfers confirmed · Exact scope: <strong>unknown</strong> · 500-record sample verified genuine · Likely includes demographics, diagnoses, meds, labs, mental health records", "amber"),
)}
{decision("File now with incomplete info? Wait for the deadline? Notify patients too?")}
</div>""", "alert"))

# 30: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — TEAM DISCUSSION",
    "14 hours. Incomplete information. 180,000 potentially affected patients.",
    "File preliminary now? Wait for the deadline?\nHow do you notify 180,000 patients?\nConsider: elderly patients, mental health stigma, domestic violence survivors.",
    "Discuss, then log your decision.",
    station("ACTION STATION",
            "<strong>Station 9:</strong> Complete the CNIL Breach Notification (10 min) — Fill out the simulated regulatory form in the student app. Mark what you KNOW vs. what you DON'T KNOW.")
), "notification"))

# 31: Restoration
SLIDES.append(("inject", f"""
<div class="fade-in">
{phase_header("SYSTEM RESTORATION STRATEGY", "HOUR 64")}
{events(
    ("OPT A", "<strong>48-hour backup.</strong> EHR in 12–18h. Loses pre-breach + downtime data. Clean start. Back-entry: 3–4 weeks.", "cyan"),
    ("OPT B", "<strong>Decrypt & clean.</strong> 5–10 more days. Preserves data. 15–20% reinfection risk. Forensics recommends against.", "amber"),
    ("OPT C", "<strong>New clean instance.</strong> 24–36h. Zero risk. Requires manual entry of ALL active patient data.", "cyan"),
    ("OPT D", "<strong>Hybrid.</strong> Phase 1 (24h): clean instance for active patients. Phase 2 (1 week): restore backup. Phase 3 (2–4 weeks): merge & reconcile.", ""),
)}
{decision("Speed vs. data preservation vs. security. Who decides?")}
</div>""", "notification"))

# 32: PAUSE
SLIDES.append(("pause", pause_slide(
    "PAUSE — FINAL TEAM DISCUSSION",
    "Four options. Each has costs. Each has risks.",
    "Which path? Technical decision? Clinical? Financial? Data integrity?\nWho has the final say?",
    "Discuss, then log your final decision."
), "notification"))

# 33: Recovery
SLIDES.append(("recovery", f"""
<div class="fade-in">
{phase_header("RECOVERY PLANNING", "THURSDAY — HOUR 72+ · DAY 4")}
<div style="text-align:center; font-family:var(--mono); font-size:0.8em; color:var(--text-dim); letter-spacing:2px; margin:8px 0;">PARTIAL RESTORATION IN PROGRESS</div>
{sys_grid(RECOVERY)}
<div style="text-align:center; font-family:var(--body); font-size:1.35em; color:var(--text); margin:36px 0; line-height:2.2;">
<p>The systems will come back in <strong>days</strong>.</p>
<p>The trust takes <strong>months</strong>.</p>
<p style="color:var(--amber);">The lessons last <strong>careers</strong>.</p>
</div>
{decision("In your student app: complete Recovery Planning.<br>Prioritize back-entry. Plan trust recovery. Assess preparedness. Write your after-action summary.")}
{station("FINAL ACTION STATION",
          "<strong>Station 10:</strong> Design the Back-Entry Workflow (8 min) — 6,400+ pages of paper. Map the process: priority, staffing, QA, the 11% unmatched records.")}
</div>""", None))

# 34: End
SLIDES.append(("end", """
<div class="fade-in">
<div class="end-wrap">
    <div class="end-title">END OF SIMULATION</div>
    <div class="end-body">
        <p>Thank you for your work. The 2-hour debrief will follow.</p>
        <p style="margin-top:24px;">Export your team reports from the student app.<br>
        Prepare to share your most difficult decision and what you learned.</p>
    </div>
</div>
</div>""", None))


# ---------------------------------------------------------------------------
# HEADER BAR
# ---------------------------------------------------------------------------
total_slides = len(SLIDES)
slide_type, slide_html, sound_cue = SLIDES[st.session_state.slide]

st.markdown(f"""
<div class="sentinel-header">
    <div>
        <div class="sentinel-wordmark">SENTINEL</div>
        <div class="sentinel-sub">INCIDENT COMMAND · SAINTE-CLAIRE</div>
    </div>
    <div class="incident-badge">ACTIVE INCIDENT</div>
    <div style="text-align:right;">
        <div style="font-family:var(--mono, monospace);font-size:0.7em;color:#607080;letter-spacing:2px;">SLIDE {st.session_state.slide + 1} / {total_slides}</div>
        <div style="font-family:var(--mono, monospace);font-size:0.7em;color:#e94560;margin-top:2px;">{slide_type.upper()}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Scrolling ticker
st.markdown("""
<div class="ticker-wrap">
<div class="ticker-content">
⚠ RANSOMWARE INCIDENT ACTIVE &nbsp;·&nbsp; ALL CLINICAL SYSTEMS COMPROMISED &nbsp;·&nbsp; HICS ACTIVATED &nbsp;·&nbsp;
ANSSI FORENSICS EN ROUTE &nbsp;·&nbsp; GDPR 72H CLOCK RUNNING &nbsp;·&nbsp;
MEDIA INQUIRIES LOGGED &nbsp;·&nbsp; DOWNTIME PROCEDURES IN EFFECT &nbsp;·&nbsp;
PAPER FALLBACK OPERATIONAL &nbsp;·&nbsp; RANSOM €2.5M — DO NOT PAY &nbsp;·&nbsp;
CNIL NOTIFICATION PENDING &nbsp;·&nbsp; ⚠ RANSOMWARE INCIDENT ACTIVE &nbsp;·&nbsp;
</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
nav1, nav2, nav3, nav4, nav5, nav6 = st.columns([1, 1, 2, 1, 1, 1])
with nav1:
    if st.button("◀◀ START", disabled=st.session_state.slide <= 0, use_container_width=True):
        st.session_state.slide = 0
        st.rerun()
with nav2:
    if st.button("◀ PREV", disabled=st.session_state.slide <= 0, use_container_width=True):
        st.session_state.slide -= 1
        st.rerun()
with nav3:
    pct = int((st.session_state.slide / (total_slides - 1)) * 100) if total_slides > 1 else 0
    st.markdown(f"""
    <div style="text-align:center; padding-top:4px;">
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%;"></div></div>
        <div class="slide-counter">{st.session_state.slide + 1} of {total_slides}</div>
    </div>""", unsafe_allow_html=True)
with nav4:
    if st.button("NEXT ▶", disabled=st.session_state.slide >= total_slides - 1,
                 use_container_width=True, type="primary"):
        st.session_state.slide += 1
        st.rerun()
with nav5:
    st.session_state.autoplay = st.checkbox("Audio", value=st.session_state.autoplay)
with nav6:
    st.session_state.auto_advance = st.checkbox("Auto-advance", value=st.session_state.auto_advance,
        help="Slides advance automatically when audio ends. Stops at every Pause and Break.")

# ---------------------------------------------------------------------------
# Slide content
# ---------------------------------------------------------------------------
st.markdown(f'<div class="slide-wrapper">{slide_html}</div>', unsafe_allow_html=True)

# Sound + audio
if sound_cue and st.session_state.autoplay:
    st.markdown(sound_cue_js(sound_cue), unsafe_allow_html=True)
audio_html = get_audio_html(
    st.session_state.slide,
    autoplay=st.session_state.autoplay,
    auto_advance=st.session_state.auto_advance,
    stop_slide=slide_type in ("pause", "break"),
)
if audio_html:
    st.markdown(audio_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar — phase map + downloads
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""<div style="font-family:'Share Tech Mono',monospace;color:#ff1a1a;
    font-size:0.8em;letter-spacing:3px;padding:8px 0;border-bottom:1px solid #1a3050;
    margin-bottom:12px;">PHASE MAP</div>""", unsafe_allow_html=True)

    target = st.number_input("Jump to slide:", 1, total_slides, st.session_state.slide + 1, key="jump")
    if target - 1 != st.session_state.slide:
        st.session_state.slide = target - 1
        st.rerun()

    st.markdown("---")
    phase_map = {
        "Title": 0, "Breach 1: First Reports": 1, "Breach 2: Systems Falling": 2,
        "Breach 3: Full Attack": 3, "⏸ PAUSE: Phase 1": 4,
        "Downtime Begins": 5, "💉 Near-Miss": 6, "⏸ PAUSE": 7,
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

    # Downloads
    st.markdown("---")
    st.markdown("""<div style="font-family:'Share Tech Mono',monospace;color:#607080;
    font-size:0.7em;letter-spacing:2px;padding:4px 0;">TEAM SUBMISSIONS</div>""",
    unsafe_allow_html=True)

    submission_files = sorted(
        [f for f in os.listdir(SUBMISSIONS_DIR) if f.endswith(".json")]
        if os.path.isdir(SUBMISSIONS_DIR) else []
    )

    if not submission_files:
        st.caption("No submissions yet.")
    else:
        st.caption(f"{len(submission_files)} team(s) submitted")
        all_reports = []
        for fname in submission_files:
            fpath = os.path.join(SUBMISSIONS_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    all_reports.append(json.load(f))
            except Exception:
                pass

        combined_json = json.dumps(all_reports, indent=2, ensure_ascii=False)
        st.download_button("Download All (JSON)", data=combined_json,
                           file_name="all_team_reports.json", mime="application/json",
                           use_container_width=True)

        csv_buf = io.StringIO()
        all_decision_titles, all_station_ids = [], []
        for r in all_reports:
            for d in r.get("decisions", []):
                if d["title"] not in all_decision_titles:
                    all_decision_titles.append(d["title"])
            for s in r.get("stations", []):
                sid = s.get("station_id", s["title"])
                if sid not in all_station_ids:
                    all_station_ids.append(sid)

        station_deliverable_keys = {}
        for r in all_reports:
            for s in r.get("stations", []):
                sid = s.get("station_id", s["title"])
                for key in s.get("deliverables", {}).keys():
                    station_deliverable_keys.setdefault(sid, [])
                    if key not in station_deliverable_keys[sid]:
                        station_deliverable_keys[sid].append(key)

        header = ["team_name", "exported_at", "decisions_made", "stations_completed"]
        for t in all_decision_titles:
            header += [f"decision: {t}", f"justification: {t}"]
        for sid in all_station_ids:
            for key in station_deliverable_keys.get(sid, []):
                header.append(f"{sid}: {key}")
        for i in range(1, 6):
            header.append(f"after_action_q{i}")

        writer = csv.DictWriter(csv_buf, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for r in all_reports:
            row = {"team_name": r.get("team_name",""), "exported_at": r.get("exported_at",""),
                   "decisions_made": len(r.get("decisions",[])), "stations_completed": len(r.get("stations",[]))}
            for d in r.get("decisions", []):
                row[f"decision: {d['title']}"] = d.get("choice","")
                row[f"justification: {d['title']}"] = d.get("justification","")
            for s in r.get("stations", []):
                sid = s.get("station_id", s["title"])
                for key, val in s.get("deliverables", {}).items():
                    row[f"{sid}: {key}"] = val
            aa = r.get("after_action", {})
            for i in range(1, 6):
                row[f"after_action_q{i}"] = aa.get(f"q{i}","")
            writer.writerow(row)

        st.download_button("Download All (CSV)", data=csv_buf.getvalue(),
                           file_name="all_team_reports.csv", mime="text/csv",
                           use_container_width=True)
        st.caption("Teams: " + ", ".join(r.get("team_name","?") for r in all_reports))
