# 05 — FEATURES
### Complete feature inventory: Citizens + Government + MVP cut

Superseded root copy: `../FEATURES.md` (same content, canonical here).

---

# A. CITIZEN (CONSUMER) — 20 features

## A1. Report & Request
| # | Feature | Description |
|---|---|---|
| 1 | Multi-channel reporting | Mobile app / web / 311 / messaging channels |
| 2 | Smart report form | Photo + auto geo-tag + AI auto-classification |
| 3 | Report anything | Pothole, leak, waste, light, encroachment, fire, flood, crowd hazard |
| 4 | Voice & multilingual | Speech → structured ticket, local-language support |
| 5 | Anonymous option | Pseudonymous reporting |

## A2. Track & Follow-up
| # | Feature | Description |
|---|---|---|
| 6 | Live ticket tracking | Received → Assigned → In Progress → Resolved timeline |
| 7 | "Who is responsible?" | Auto-routed to correct department |
| 8 | ETA / SLA visibility | Promised time + countdown + auto-escalation |
| 9 | Auto-updates | Push/SMS/in-app at every status change |
| 10 | Grievance escalation | SLA breach → auto-escalate |

## A3. Alerts & Safety
| # | Feature | Description |
|---|---|---|
| 11 | Zone-based alerts | Personalized "my area" warnings |
| 12 | Emergency SOS | Panic → priority incident + dispatch |
| 13 | Safe-route advisory | "Flood on R7 — use alternate" (chain + optimizer) |
| 14 | Preventive advisories | Ahead-of-time warnings (pre-position story — IMPACT M2) |

## A4. Assist & Engage
| # | Feature | Description |
|---|---|---|
| 15 | Citizen AI Assistant (LLM) | "When is water supply?" — RAG over city knowledge |
| 16 | Service finder | Nearest hospital/police/clinic + live accessibility |
| 17 | Participatory sensing | Citizens confirm events → better AI accuracy |
| 18 | Feedback & rating | Rate resolution → department KPIs |
| 19 | Public dashboards | Open KPIs (ISO 37120), incl. City Health Score (IMPACT M5) |
| 20 | Claims tracking | Damage/benefit claims linked to incidents |
| 20b | **My Data dashboard** | View/download/delete own data (GAP F6) |

---

# B. GOVERNMENT — 44+ features

## B1. Command & Control Center (core 9)
| # | Feature |
|---|---|
| 1 | Unified live map (one pane of glass) |
| 2 | **Incident Chain Engine** — flood→road→traffic→ambulance→hospital |
| 3 | Risk-prioritized work queue (AI score 0–1) |
| 4 | AI recommendations **with XAI "why" cards** |
| 5 | Human approval workflow for critical actions |
| 6 | Playbook execution (SOPs, one click) |
| 7 | Cross-department parallel tickets + shared status |
| 8 | Resource/team dispatch with live status |
| 9 | Real-time operations feed (WebSocket) |
| 9b | **In-incident collaboration** (chat/notes) — GAP F2 |
| 9c | **On-call/escalation directory** — GAP F3 |

## B2. Department Features

**🚦 Traffic (10–15):** flow prediction (STGNN) · congestion/incident detection · **quantum/hybrid signal-plan optimization** · reroute computation · ambulance priority corridors · transit bunching alerts

**🚰 Water & Sanitation (16–19):** leak/burst prediction · waste overflow + route optimization · quality alarms · supply-schedule + auto citizen notification

**🚔 Police (20–23):** crime hotspot prediction · video event alerts · patrol optimization · missing person/vehicle dissemination

**🏥 Health (24–27):** hospital load/accessibility risk · ambulance fastest-route · outbreak early signals · elderly/fall response tickets

**🌊 Disaster (28–31):** flood/weather prediction · **Digital Twin what-if** · impact chain + evacuation planning · multi-agency response board

**🏛️ Planning & Assets (32–35):** City Knowledge Graph asset registry · 3D twin planning view · permit/work-order lifecycle · **infrastructure decay prediction**

## B3. Cross-cutting (36–44 + gap additions)
| # | Feature |
|---|---|
| 36 | Executive KPI dashboards (ISO 37120) + City Health Score |
| 37 | Smart Ticketing & SLA engine (auto-route, timers, escalation) |
| 38 | LLM Copilot for staff (draft notes, query incidents) |
| 39 | Model governance (MLOps registry, drift, canary) |
| 40 | Quantum Optimization Service (async jobs + classical fallback) |
| 41 | RBAC + tamper-evident audit |
| 42 | Data-sharing APIs + developer portal (GAP A10) |
| 43 | Auto post-incident reports (timeline + XAI) |
| 44 | Open data portal (anonymized KPIs) |
| 45 | **Department Admin Console** (self-service SLA/routing/templates) — GAP F1 |
| 46 | **Outcome capture** ("did it work?") — GAP F4 |
| 47 | **Custom report builder** — GAP F5 |
| 48 | **Mass emergency broadcast** with ack tracking — GAP F7 |
| 49 | **Saved what-if scenarios** (compare/share) — GAP F8 |
| 50 | **Playbook outcome scoring** — GAP F9 |
| 51 | **Department onboarding sandbox** — GAP F10 |
| 52 | **Equity filter** (service fairness by ward) — IMPACT M7 |
| 53 | **Carbon/CO₂ impact per recommendation** — IMPACT M8 |
| 54 | **Learning flywheel counter** (public) — IMPACT M9 |
| 55 | **Preventive pre-position actions** — IMPACT M2 |
| 56 | **Backtest/Time Machine console** — IMPACT M1 |

---

# C. FEATURE → PROBLEM MAP (Slide 2 challenges)

| Challenge | Solving features |
|---|---|
| Citizens forced to follow up | A2 (6–10) |
| Departments in silos | B1.7, 37, 42 |
| Cities remain reactive | predictions + 55 preventive + A3.14 |
| Connected incidents separate | **B1.2 chain engine** (correlation v1, causal-grade validation per 10 §1 — precision ≥0.85 gate before any "causal" claim) |
| Data ≠ decisions | B1.3–1.6 scoring→recommend→approve→playbook |
| AI must be trusted | B1.4 XAI, B1.5 approval, 39 governance |

---

# D. MVP DEMO CUT (hackathon — show only these 6)

1. Citizen reports issue (auto-classify + geo-tag)
2. Smart ticket auto-routed with SLA
3. Live map + **incident chain** (flood→road→traffic→ambulance→hospital)
4. AI recommendation with **XAI "why" card**
5. Human approval → playbook fires → citizen gets status update
6. Public dashboard with KPIs + impact numbers

**Demo script (90s):** see `../IMPACT_PLAYBOOK.md` §5 — end with numbers slide: *6h→4min · −60% follow-ups · 14 min saved*.

---

# E. PRIORITIZATION BACKLOG

| Tier | Features | When |
|---|---|---|
| **Must (MVP)** | B1.1–9, A1–A2, 37, 45–46, M-FLOOD/M-CLASS/M-CHAIN | M0–M2 |
| **Should** | B2 full depts, search, mass broadcast, equity, health score, LLM copilot | M3–M4 |
| **Could** | carbon, FL, RL signal control, white-label, training mode | M4–M5 |
| **Won't (now)** | blockchain, crime QML, multi-city white-label GA | parked |
