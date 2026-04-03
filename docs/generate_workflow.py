#!/usr/bin/env python3
"""Generates workflow.svg and workflow.bpmn for red·proto framework."""

import math, textwrap

# ── Canvas & Layout ───────────────────────────────────────────────────────────
W, H = 1600, 680
POOL_LBL_W = 38
LANE_LBL_W = 118
PH         = 44          # pool-header height
CX_OFF     = POOL_LBL_W + LANE_LBL_W   # 156 – content start x

# Lane y-ranges  (y from top of SVG)
L1Y, L1H = PH,           140   # Nutzer
L2Y, L2H = PH + 140,     322   # Claude – Commands
L3Y, L3H = PH + 140+322, 174   # Sub-Agents
# total: 44+140+322+174 = 680 ✓

L1_CY = L1Y + L1H // 2  # 114
L2_CY = L2Y + L2H // 2  # 345
L3_CY = L3Y + L3H // 2  # 579

# ── Colour Palette ────────────────────────────────────────────────────────────
BG       = "#f8fafc"
POOL_HDR = "#0f172a"
POOL_FG  = "#f1f5f9"
LANE_HDR = "#1e293b"
LANE_FG  = "#cbd5e1"
L1_BG    = "#f8fafc"
L2_BG    = "#ffffff"
L3_BG    = "#f0f9ff"

SETUP_BG = "#fffbeb";  SETUP_BD = "#f59e0b"
LOOP_BG  = "#f0fdf4";  LOOP_BD  = "#22c55e"

TASK_BG  = "#dbeafe";  TASK_BD  = "#3b82f6";  TASK_FG  = "#1e3a5f"
AGEN_BG  = "#e0e7ff";  AGEN_BD  = "#6366f1";  AGEN_FG  = "#1e1b4b"
GW_BG    = "#fef9c3";  GW_BD    = "#eab308";  GW_FG    = "#713f12"
SE_BG    = "#dcfce7";  SE_BD    = "#16a34a"
EE_BG    = "#fee2e2";  EE_BD    = "#dc2626"

FLOW_CLR = "#64748b"
LOOP_CLR = "#dc2626"
SES_CLR  = "#f97316"
OPT_CLR  = "#94a3b8"

FONT     = "Inter, system-ui, -apple-system, sans-serif"

# ── SVG helpers ───────────────────────────────────────────────────────────────
out = []

def e(s): out.append(s)

def task(cx, cy, label, bg=TASK_BG, bd=TASK_BD, fg=TASK_FG, w=114, h=50):
    x, y = cx - w//2, cy - h//2
    e(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
      f'fill="{bg}" stroke="{bd}" stroke-width="1.5"/>')
    lines = label.split("\n")
    base_y = cy - (len(lines)-1) * 7.5
    for i, ln in enumerate(lines):
        e(f'<text x="{cx}" y="{base_y + i*15 + 4}" text-anchor="middle" '
          f'font-size="10.5" font-weight="600" fill="{fg}" font-family="{FONT}">{ln}</text>')

def small_task(cx, cy, label, bg=AGEN_BG, bd=AGEN_BD, fg=AGEN_FG, w=104, h=42):
    task(cx, cy, label, bg, bd, fg, w, h)

def start_event(cx, cy, label=""):
    e(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{SE_BG}" stroke="{SE_BD}" stroke-width="2.5"/>')
    e(f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{SE_BD}" stroke-width="1"/>')
    if label:
        e(f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-size="9.5" '
          f'fill="#475569" font-family="{FONT}" font-weight="600">{label}</text>')

def end_event(cx, cy, label=""):
    e(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{EE_BG}" stroke="{EE_BD}" stroke-width="3.5"/>')
    if label:
        e(f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-size="9.5" '
          f'fill="#475569" font-family="{FONT}" font-weight="600">{label}</text>')

def gateway(cx, cy, label="", lx=None, ly=None):
    s = 20
    pts = f"{cx},{cy-s} {cx+s},{cy} {cx},{cy+s} {cx-s},{cy}"
    e(f'<polygon points="{pts}" fill="{GW_BG}" stroke="{GW_BD}" stroke-width="1.8"/>')
    e(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="13" '
      f'fill="{GW_FG}" font-family="{FONT}">✕</text>')
    if label:
        tx = lx if lx else cx
        ty = ly if ly else cy + s + 14
        for i, ln in enumerate(label.split("\n")):
            e(f'<text x="{tx}" y="{ty + i*12}" text-anchor="middle" font-size="9" '
              f'fill="#475569" font-family="{FONT}">{ln}</text>')

def arrow(x1, y1, x2, y2, label="", color=FLOW_CLR, dashed=False, loffx=0, loffy=-6):
    dx, dy = x2-x1, y2-y1
    ln = math.hypot(dx, dy)
    if ln == 0: return
    ux, uy = dx/ln, dy/ln
    AHS = 9
    ex, ey = x2 - ux*AHS, y2 - uy*AHS
    px, py = -uy*4.5, ux*4.5
    dash = 'stroke-dasharray="6,4"' if dashed else ''
    e(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
      f'stroke="{color}" stroke-width="1.5" {dash}/>')
    e(f'<polygon points="{x2:.1f},{y2:.1f} {ex+px:.1f},{ey+py:.1f} {ex-px:.1f},{ey-py:.1f}" '
      f'fill="{color}"/>')
    if label:
        mx, my = (x1+x2)/2 + loffx, (y1+y2)/2 + loffy
        e(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-size="9" '
          f'fill="{color}" font-family="{FONT}" font-style="italic">{label}</text>')

def path_arrow(d, color=FLOW_CLR, dashed=False, label="", lx=0, ly=0):
    dash = 'stroke-dasharray="6,4"' if dashed else ''
    e(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" {dash}/>')
    # arrowhead at end – caller handles it manually if needed
    if label:
        e(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="9" '
          f'fill="{color}" font-family="{FONT}" font-style="italic">{label}</text>')

def arrowhead(cx, cy, angle_deg, color=FLOW_CLR):
    """Draw an arrowhead pointing in angle_deg direction."""
    a = math.radians(angle_deg)
    AHS = 9
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy*4.5, ux*4.5
    x2, y2 = cx, cy
    ex, ey = cx - ux*AHS, cy - uy*AHS
    e(f'<polygon points="{x2:.1f},{y2:.1f} {ex+px:.1f},{ey+py:.1f} {ex-px:.1f},{ey-py:.1f}" '
      f'fill="{color}"/>')

def session_line(x, label, color=SES_CLR):
    e(f'<line x1="{x}" y1="{L2Y+6}" x2="{x}" y2="{L3Y+L3H-6}" '
      f'stroke="{color}" stroke-width="1.5" stroke-dasharray="4,3"/>')
    e(f'<text x="{x+4}" y="{L2Y+18}" font-size="8.5" fill="{color}" '
      f'font-family="{FONT}" font-weight="600">{label}</text>')

def label_tag(cx, cy, text, bg="#e2e8f0", fg="#334155"):
    tw = len(text)*5.5 + 12
    e(f'<rect x="{cx - tw/2:.1f}" y="{cy-9}" width="{tw:.1f}" height="18" rx="9" fill="{bg}"/>')
    e(f'<text x="{cx}" y="{cy+4.5}" text-anchor="middle" font-size="9" '
      f'fill="{fg}" font-family="{FONT}" font-weight="700">{text}</text>')

# ── Element positions ─────────────────────────────────────────────────────────
# Setup zone:  x = 156 – 730
# Loop zone:   x = 740 – 1560

SE_X      = 193                  # Start event x
SPAR_X    = 280
SETUP_X   = 393
RES_GW_X  = 506                  # Research gateway
RES_X     = 506                  # Research task (above gw)
REQ_X     = 615
FLOW_X    = 716
UX_X      = 830
ARCH_X    = 965
DEV_X     = 1098
QA_X      = 1238
BUG_GW_X  = 1367
MF_GW_X   = 1480                 # More-features gateway (Nutzer lane)
EE_X      = 1555                 # End event

SETUP_ZONE_X1 = 158;  SETUP_ZONE_X2 = 734
LOOP_ZONE_X1  = 742;  LOOP_ZONE_X2  = 1574

SES1_X = 1035   # session boundary 1 (before dev)
SES2_X = 1173   # session boundary 2 (before qa)

# Sub-agent x positions
FE_DEV_X  = 1060
BE_DEV_X  = 1140
QA_ENG_X  = 1210
UX_REV_X  = 1298

# ── SVG build ─────────────────────────────────────────────────────────────────
e(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
  f'viewBox="0 0 {W} {H}" style="background:{BG};font-family:{FONT};">')

# ── Background regions ───────────────────────────────────────────────────────
e(f'<rect x="{SETUP_ZONE_X1}" y="{L1Y}" width="{SETUP_ZONE_X2-SETUP_ZONE_X1}" '
  f'height="{L2H+L1H+L3H}" rx="0" fill="{SETUP_BG}" opacity="0.5"/>')
e(f'<rect x="{LOOP_ZONE_X1}" y="{L1Y}" width="{LOOP_ZONE_X2-LOOP_ZONE_X1}" '
  f'height="{L2H+L1H+L3H}" rx="0" fill="{LOOP_BG}" opacity="0.4"/>')

# Zone labels
e(f'<text x="{(SETUP_ZONE_X1+SETUP_ZONE_X2)//2}" y="{L1Y+12}" text-anchor="middle" '
  f'font-size="9" fill="{SETUP_BD}" font-family="{FONT}" font-weight="700" '
  f'letter-spacing="0.5">EINMALIG PRO PROJEKT</text>')
e(f'<text x="{(LOOP_ZONE_X1+LOOP_ZONE_X2)//2}" y="{L1Y+12}" text-anchor="middle" '
  f'font-size="9" fill="{LOOP_BD}" font-family="{FONT}" font-weight="700" '
  f'letter-spacing="0.5">PRO FEATURE WIEDERHOLEN</text>')

# Zone borders
e(f'<rect x="{SETUP_ZONE_X1}" y="{L1Y}" width="{SETUP_ZONE_X2-SETUP_ZONE_X1}" '
  f'height="{L2H+L1H+L3H}" fill="none" stroke="{SETUP_BD}" stroke-width="1.2" stroke-dasharray="6,4"/>')
e(f'<rect x="{LOOP_ZONE_X1}" y="{L1Y}" width="{LOOP_ZONE_X2-LOOP_ZONE_X1}" '
  f'height="{L2H+L1H+L3H}" fill="none" stroke="{LOOP_BD}" stroke-width="1.2" stroke-dasharray="6,4"/>')

# ── Pool frame ───────────────────────────────────────────────────────────────
# Lane backgrounds
e(f'<rect x="{POOL_LBL_W}" y="{L1Y}" width="{W-POOL_LBL_W}" height="{L1H}" fill="{L1_BG}"/>')
e(f'<rect x="{POOL_LBL_W}" y="{L2Y}" width="{W-POOL_LBL_W}" height="{L2H}" fill="{L2_BG}"/>')
e(f'<rect x="{POOL_LBL_W}" y="{L3Y}" width="{W-POOL_LBL_W}" height="{L3H}" fill="{L3_BG}"/>')

# Pool outer border
e(f'<rect x="0" y="0" width="{W}" height="{H}" rx="4" fill="none" '
  f'stroke="#94a3b8" stroke-width="1.5"/>')

# Pool header
e(f'<rect x="0" y="0" width="{POOL_LBL_W}" height="{H}" rx="4" fill="{POOL_HDR}"/>')
e(f'<text x="{POOL_LBL_W//2}" y="{H//2}" text-anchor="middle" dominant-baseline="middle" '
  f'font-size="11" font-weight="700" fill="{POOL_FG}" font-family="{FONT}" '
  f'transform="rotate(-90,{POOL_LBL_W//2},{H//2})">red·proto Workflow</text>')

# Pool title bar
e(f'<rect x="{POOL_LBL_W}" y="0" width="{W-POOL_LBL_W}" height="{PH}" fill="{POOL_HDR}" opacity="0.92"/>')
e(f'<text x="{POOL_LBL_W + (W-POOL_LBL_W)//2}" y="{PH//2+1}" text-anchor="middle" dominant-baseline="middle" '
  f'font-size="13" font-weight="700" fill="{POOL_FG}" font-family="{FONT}" letter-spacing="0.3">'
  f'Produktentwicklungs-Pipeline</text>')

# Lane header boxes
lane_meta = [
    (L1Y, L1H, "Nutzer"),
    (L2Y, L2H, "Claude – Commands"),
    (L3Y, L3H, "Sub-Agents"),
]
for ly, lh, ln in lane_meta:
    e(f'<rect x="{POOL_LBL_W}" y="{ly}" width="{LANE_LBL_W}" height="{lh}" fill="{LANE_HDR}"/>')
    e(f'<text x="{POOL_LBL_W + LANE_LBL_W//2}" y="{ly + lh//2}" text-anchor="middle" '
      f'dominant-baseline="middle" font-size="10" font-weight="600" fill="{LANE_FG}" '
      f'font-family="{FONT}" transform="rotate(-90,{POOL_LBL_W + LANE_LBL_W//2},{ly + lh//2})">{ln}</text>')

# Lane separator lines
for ly in [L2Y, L3Y, L1Y+L1H+L2H+L3H]:
    e(f'<line x1="{POOL_LBL_W}" y1="{ly}" x2="{W}" y2="{ly}" stroke="#cbd5e1" stroke-width="1"/>')
e(f'<line x1="{POOL_LBL_W + LANE_LBL_W}" y1="{L1Y}" x2="{POOL_LBL_W + LANE_LBL_W}" '
  f'y2="{H}" stroke="#cbd5e1" stroke-width="1"/>')

# ── Session boundary lines ────────────────────────────────────────────────────
session_line(SES1_X, "Neue Session →")
session_line(SES2_X, "Neue Session →")

# ── Connections (drawn before elements so they appear behind) ─────────────────

# Start → sparring
arrow(SE_X+20, L1_CY, SPAR_X-57, L2_CY)

# sparring → dev-setup
arrow(SPAR_X+57, L2_CY, SETUP_X-57, L2_CY)

# dev-setup → research-gw
arrow(SETUP_X+57, L2_CY, RES_GW_X-20, L2_CY)

# research-gw → research (optional, upward)
arrow(RES_GW_X, L2_CY-20, RES_X, L2Y+62, color=OPT_CLR, dashed=True, label="optional")

# research → requirements (skip down then right)
e(f'<path d="M {RES_X} {L2Y+62+21} L {RES_X} {L2_CY-30} L {REQ_X-57} {L2_CY-30} L {REQ_X-57} {L2_CY}" '
  f'fill="none" stroke="{OPT_CLR}" stroke-width="1.5" stroke-dasharray="6,4"/>')
arrowhead(REQ_X-57, L2_CY, 90, OPT_CLR)

# research-gw → requirements (direct, main path)
arrow(RES_GW_X+20, L2_CY, REQ_X-57, L2_CY, label="überspringen", loffy=+12)

# requirements → flows
arrow(REQ_X+57, L2_CY, FLOW_X-57, L2_CY)

# flows → ux  (crossing zone boundary)
arrow(FLOW_X+57, L2_CY, UX_X-57, L2_CY)

# ux → architect
arrow(UX_X+57, L2_CY, ARCH_X-57, L2_CY)

# architect → dev
arrow(ARCH_X+57, L2_CY, DEV_X-57, L2_CY)

# dev → qa
arrow(DEV_X+57, L2_CY, QA_X-57, L2_CY)

# qa → bug-gw
arrow(QA_X+57, L2_CY, BUG_GW_X-20, L2_CY)

# bug-gw → more-features-gw (upward, cross-lane)
e(f'<path d="M {BUG_GW_X+20} {L2_CY} L {MF_GW_X} {L2_CY} L {MF_GW_X} {L1_CY+20}" '
  f'fill="none" stroke="{FLOW_CLR}" stroke-width="1.5"/>')
arrowhead(MF_GW_X, L1_CY+20, 270)

# more-features-gw → end event
arrow(MF_GW_X+20, L1_CY, EE_X-20, L1_CY, label="nein")

# more-features-gw → ux (loop back, goes above)
LOOP_Y_TOP = L1Y - 22
e(f'<path d="M {MF_GW_X} {L1_CY-20} L {MF_GW_X} {LOOP_Y_TOP} L {UX_X} {LOOP_Y_TOP} L {UX_X} {L2Y}" '
  f'fill="none" stroke="{LOOP_CLR}" stroke-width="1.8" stroke-dasharray="6,4"/>')
arrowhead(UX_X, L2Y, 90, LOOP_CLR)
e(f'<text x="{(MF_GW_X+UX_X)//2}" y="{LOOP_Y_TOP-5}" text-anchor="middle" font-size="9" '
  f'fill="{LOOP_CLR}" font-family="{FONT}" font-style="italic">ja – nächstes Feature</text>')

# bug-gw → dev (loop back, goes below)
LOOP_Y_BOT = L3Y + L3H + 18
e(f'<path d="M {BUG_GW_X} {L2_CY+20} L {BUG_GW_X} {LOOP_Y_BOT} L {DEV_X} {LOOP_Y_BOT} L {DEV_X} {L2_CY+25}" '
  f'fill="none" stroke="{LOOP_CLR}" stroke-width="1.8" stroke-dasharray="6,4"/>')
arrowhead(DEV_X, L2_CY+25, 90, LOOP_CLR)
e(f'<text x="{(BUG_GW_X+DEV_X)//2}" y="{LOOP_Y_BOT+13}" text-anchor="middle" font-size="9" '
  f'fill="{LOOP_CLR}" font-family="{FONT}" font-style="italic">Bugs gefunden – Fix &amp; Retest</text>')

# dev → sub-agents (dashed, spawn)
arrow(DEV_X, L2_CY+25, FE_DEV_X, L3Y, color=AGEN_BD, dashed=True)
arrow(DEV_X, L2_CY+25, BE_DEV_X, L3Y, color=AGEN_BD, dashed=True)

# qa → sub-agents (dashed, spawn)
arrow(QA_X, L2_CY+25, QA_ENG_X, L3Y, color=AGEN_BD, dashed=True)
arrow(QA_X, L2_CY+25, UX_REV_X, L3Y, color=AGEN_BD, dashed=True)

# start → sparring (Nutzer initiates)
e(f'<path d="M {SE_X} {L1_CY+20} L {SE_X} {L2_CY-25}" '
  f'fill="none" stroke="{FLOW_CLR}" stroke-width="1.5"/>')
arrowhead(SE_X, L2_CY-25, 90)

# ── Elements ──────────────────────────────────────────────────────────────────

# Nutzer lane
start_event(SE_X, L1_CY, "Idee")
gateway(MF_GW_X, L1_CY, label="Weitere\nFeatures?", ly=L1_CY+28)
end_event(EE_X, L1_CY, "Release 🎉")

# Commands lane – setup
task(SPAR_X, L2_CY, "/red:proto-\nsparring")
task(SETUP_X, L2_CY, "/red:proto-\ndev-setup")
task(RES_X, L2Y+62, "/red:proto-\nresearch", w=110)
gateway(RES_GW_X, L2_CY, label="Research?", ly=L2_CY+28)
task(REQ_X, L2_CY, "/red:proto-\nrequirements")
task(FLOW_X, L2_CY, "/red:proto-\nflows")

# Commands lane – feature loop
task(UX_X, L2_CY, "/red:proto-\nux")
task(ARCH_X, L2_CY, "/red:proto-\narchitect")
task(DEV_X, L2_CY, "/red:proto-\ndev")
task(QA_X, L2_CY, "/red:proto-\nqa")
gateway(BUG_GW_X, L2_CY, label="Bugs\ngefunden?", lx=BUG_GW_X+2, ly=L2_CY+28)

# Handoff annotation
e(f'<rect x="{DEV_X+58}" y="{L2_CY-14}" width="90" height="28" rx="5" '
  f'fill="#fff7ed" stroke="{SES_CLR}" stroke-width="1"/>')
e(f'<text x="{DEV_X+103}" y="{L2_CY-3}" text-anchor="middle" font-size="8.5" '
  f'fill="{SES_CLR}" font-family="{FONT}" font-weight="600">Handoff</text>')
e(f'<text x="{DEV_X+103}" y="{L2_CY+9}" text-anchor="middle" font-size="8" '
  f'fill="{SES_CLR}" font-family="{FONT}">context/FEAT-x.md</text>')

# Sub-agents lane
small_task(FE_DEV_X, L3_CY, "frontend-\ndeveloper")
small_task(BE_DEV_X, L3_CY, "backend-\ndeveloper")
small_task(QA_ENG_X, L3_CY, "qa-\nengineer")
small_task(UX_REV_X, L3_CY, "ux-\nreviewer")

# Parallel markers on dev/qa tasks
for x in [FE_DEV_X, BE_DEV_X]:
    label_tag(x, L3_CY - 30, "parallel")
for x in [QA_ENG_X, UX_REV_X]:
    label_tag(x, L3_CY - 30, "parallel")

# proto-workflow hint (floating tag bottom right)
e(f'<rect x="{W-210}" y="{H-32}" width="200" height="24" rx="12" '
  f'fill="#1e293b" opacity="0.85"/>')
e(f'<text x="{W-110}" y="{H-16}" text-anchor="middle" font-size="9.5" '
  f'fill="#f1f5f9" font-family="{FONT}" font-weight="600">'
  f'/red:proto-workflow  – Orientierung jederzeit</text>')

# Gateway labels for bug/features
e(f'<text x="{BUG_GW_X-32}" y="{L2_CY+8}" text-anchor="end" font-size="8.5" '
  f'fill="{LOOP_CLR}" font-family="{FONT}" font-style="italic">ja</text>')
e(f'<text x="{BUG_GW_X+2}" y="{L2_CY-26}" text-anchor="middle" font-size="8.5" '
  f'fill="{FLOW_CLR}" font-family="{FONT}" font-style="italic">nein</text>')

e('</svg>')

svg_content = "\n".join(out)

# ── Write SVG ─────────────────────────────────────────────────────────────────
import os
base = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(base, "workflow.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"SVG written: {svg_path}")


# ── BPMN 2.0 XML ─────────────────────────────────────────────────────────────
bpmn = '''<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  targetNamespace="http://red-proto.dev/workflow"
  id="Definitions_RedProto">

  <bpmn:collaboration id="Collab_RedProto">
    <bpmn:participant id="Pool_RedProto" name="red·proto Workflow" processRef="Process_RedProto"/>
  </bpmn:collaboration>

  <bpmn:process id="Process_RedProto" isExecutable="false">
    <bpmn:laneSet id="LaneSet_1">
      <bpmn:lane id="Lane_Nutzer" name="Nutzer">
        <bpmn:flowNodeRef>Start_Idee</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gw_MoreFeatures</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>End_Release</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_Commands" name="Claude – Commands">
        <bpmn:flowNodeRef>Task_Sparring</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_DevSetup</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_Research</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gw_Research</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_Requirements</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_Flows</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_UX</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_Architect</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_Dev</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_QA</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gw_Bugs</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_Agents" name="Sub-Agents">
        <bpmn:flowNodeRef>Task_FrontendDev</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_BackendDev</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_QAEngineer</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Task_UXReviewer</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>

    <!-- Start -->
    <bpmn:startEvent id="Start_Idee" name="Idee"/>

    <!-- Setup Phase -->
    <bpmn:task id="Task_Sparring" name="/red:proto-sparring&#10;Idee → PRD"/>
    <bpmn:task id="Task_DevSetup" name="/red:proto-dev-setup&#10;Tech-Stack + GitHub"/>
    <bpmn:exclusiveGateway id="Gw_Research" name="Research?" gatewayDirection="Diverging"/>
    <bpmn:task id="Task_Research" name="/red:proto-research&#10;Personas + Problem Statement"/>
    <bpmn:task id="Task_Requirements" name="/red:proto-requirements&#10;Feature Specs"/>
    <bpmn:task id="Task_Flows" name="/red:proto-flows&#10;Screen-Inventar + Transitions"/>

    <!-- Feature Loop -->
    <bpmn:task id="Task_UX" name="/red:proto-ux&#10;UX-Entscheidungen"/>
    <bpmn:task id="Task_Architect" name="/red:proto-architect&#10;Tech-Design + Security"/>
    <bpmn:task id="Task_Dev" name="/red:proto-dev&#10;Implementierung&#10;[Neue Session]"/>
    <bpmn:task id="Task_QA" name="/red:proto-qa&#10;Tests + Bug-Loop&#10;[Neue Session]"/>
    <bpmn:exclusiveGateway id="Gw_Bugs" name="Bugs gefunden?" gatewayDirection="Diverging"/>
    <bpmn:exclusiveGateway id="Gw_MoreFeatures" name="Weitere Features?" gatewayDirection="Diverging"/>
    <bpmn:endEvent id="End_Release" name="Release 🎉"/>

    <!-- Sub-Agents -->
    <bpmn:task id="Task_FrontendDev" name="frontend-developer"/>
    <bpmn:task id="Task_BackendDev" name="backend-developer"/>
    <bpmn:task id="Task_QAEngineer" name="qa-engineer"/>
    <bpmn:task id="Task_UXReviewer" name="ux-reviewer"/>

    <!-- Sequence Flows -->
    <bpmn:sequenceFlow id="Sf_Start_Sparring" sourceRef="Start_Idee" targetRef="Task_Sparring"/>
    <bpmn:sequenceFlow id="Sf_Sparring_Setup" sourceRef="Task_Sparring" targetRef="Task_DevSetup"/>
    <bpmn:sequenceFlow id="Sf_Setup_GwRes" sourceRef="Task_DevSetup" targetRef="Gw_Research"/>
    <bpmn:sequenceFlow id="Sf_GwRes_Research" name="optional" sourceRef="Gw_Research" targetRef="Task_Research"/>
    <bpmn:sequenceFlow id="Sf_Research_Req" sourceRef="Task_Research" targetRef="Task_Requirements"/>
    <bpmn:sequenceFlow id="Sf_GwRes_Req" name="überspringen" sourceRef="Gw_Research" targetRef="Task_Requirements"/>
    <bpmn:sequenceFlow id="Sf_Req_Flows" sourceRef="Task_Requirements" targetRef="Task_Flows"/>
    <bpmn:sequenceFlow id="Sf_Flows_UX" sourceRef="Task_Flows" targetRef="Task_UX"/>
    <bpmn:sequenceFlow id="Sf_UX_Arch" sourceRef="Task_UX" targetRef="Task_Architect"/>
    <bpmn:sequenceFlow id="Sf_Arch_Dev" sourceRef="Task_Architect" targetRef="Task_Dev"/>
    <bpmn:sequenceFlow id="Sf_Dev_QA" sourceRef="Task_Dev" targetRef="Task_QA"/>
    <bpmn:sequenceFlow id="Sf_QA_GwBugs" sourceRef="Task_QA" targetRef="Gw_Bugs"/>
    <bpmn:sequenceFlow id="Sf_Bugs_Dev" name="ja – Fix &amp; Retest" sourceRef="Gw_Bugs" targetRef="Task_Dev"/>
    <bpmn:sequenceFlow id="Sf_Bugs_GwMF" name="nein" sourceRef="Gw_Bugs" targetRef="Gw_MoreFeatures"/>
    <bpmn:sequenceFlow id="Sf_MF_UX" name="ja" sourceRef="Gw_MoreFeatures" targetRef="Task_UX"/>
    <bpmn:sequenceFlow id="Sf_MF_End" name="nein" sourceRef="Gw_MoreFeatures" targetRef="End_Release"/>
    <bpmn:sequenceFlow id="Sf_Dev_FE" sourceRef="Task_Dev" targetRef="Task_FrontendDev"/>
    <bpmn:sequenceFlow id="Sf_Dev_BE" sourceRef="Task_Dev" targetRef="Task_BackendDev"/>
    <bpmn:sequenceFlow id="Sf_QA_QAEng" sourceRef="Task_QA" targetRef="Task_QAEngineer"/>
    <bpmn:sequenceFlow id="Sf_QA_UXRev" sourceRef="Task_QA" targetRef="Task_UXReviewer"/>
  </bpmn:process>

  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collab_RedProto">
      <bpmndi:BPMNShape id="Shape_Pool" bpmnElement="Pool_RedProto" isHorizontal="true">
        <dc:Bounds x="0" y="0" width="1600" height="680"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Lane_Nutzer" bpmnElement="Lane_Nutzer" isHorizontal="true">
        <dc:Bounds x="38" y="44" width="1562" height="140"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Lane_Commands" bpmnElement="Lane_Commands" isHorizontal="true">
        <dc:Bounds x="38" y="184" width="1562" height="322"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Lane_Agents" bpmnElement="Lane_Agents" isHorizontal="true">
        <dc:Bounds x="38" y="506" width="1562" height="174"/>
      </bpmndi:BPMNShape>

      <!-- Start Event -->
      <bpmndi:BPMNShape id="Shape_Start" bpmnElement="Start_Idee">
        <dc:Bounds x="173" y="94" width="40" height="40"/>
      </bpmndi:BPMNShape>
      <!-- Tasks -->
      <bpmndi:BPMNShape id="Shape_Sparring" bpmnElement="Task_Sparring">
        <dc:Bounds x="223" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_DevSetup" bpmnElement="Task_DevSetup">
        <dc:Bounds x="336" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_GwRes" bpmnElement="Gw_Research">
        <dc:Bounds x="486" y="325" width="40" height="40"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Research" bpmnElement="Task_Research">
        <dc:Bounds x="451" y="228" width="110" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Req" bpmnElement="Task_Requirements">
        <dc:Bounds x="558" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Flows" bpmnElement="Task_Flows">
        <dc:Bounds x="659" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_UX" bpmnElement="Task_UX">
        <dc:Bounds x="773" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Architect" bpmnElement="Task_Architect">
        <dc:Bounds x="908" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Dev" bpmnElement="Task_Dev">
        <dc:Bounds x="1041" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_QA" bpmnElement="Task_QA">
        <dc:Bounds x="1181" y="320" width="114" height="50"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_GwBugs" bpmnElement="Gw_Bugs">
        <dc:Bounds x="1347" y="325" width="40" height="40"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_GwMF" bpmnElement="Gw_MoreFeatures">
        <dc:Bounds x="1460" y="94" width="40" height="40"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_End" bpmnElement="End_Release">
        <dc:Bounds x="1535" y="94" width="40" height="40"/>
      </bpmndi:BPMNShape>
      <!-- Sub-agents -->
      <bpmndi:BPMNShape id="Shape_FEDev" bpmnElement="Task_FrontendDev">
        <dc:Bounds x="1008" y="557" width="104" height="44"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_BEDev" bpmnElement="Task_BackendDev">
        <dc:Bounds x="1093" y="557" width="104" height="44"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_QAEng" bpmnElement="Task_QAEngineer">
        <dc:Bounds x="1163" y="557" width="104" height="44"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_UXRev" bpmnElement="Task_UXReviewer">
        <dc:Bounds x="1276" y="557" width="104" height="44"/>
      </bpmndi:BPMNShape>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>'''

bpmn_path = os.path.join(base, "workflow.bpmn")
with open(bpmn_path, "w", encoding="utf-8") as f:
    f.write(bpmn)
print(f"BPMN written: {bpmn_path}")
