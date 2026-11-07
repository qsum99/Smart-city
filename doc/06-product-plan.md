# 06 — PRODUCT PLAN
### Roadmap · OKRs · Personas · MVP scope · Risk register

---

## 1. Product Vision & Positioning

**Vision:** Every city decision connected, explained, and provably faster.

**Positioning statement:** For city governments drowning in fragmented data, Urban Intelligence is the **connected-intelligence operating system** that turns isolated signals into connected incident chains, explained recommendations, and coordinated action — unlike dashboards that only *show* data, we show **why it matters and what to do**. *(Wording discipline — 10 §1: "causal" only for links that pass the causal-grade gates; default claim is connected context, not causality.)*

**Differentiation table:**
| Competitor class | What they do | What we do differently |
|---|---|---|
| Existing command centers (ICCC) | Display data & CCTV | **Connected incident chains (causal-grade validated) + XAI recommendations + closed loop to citizens** |
| Point solutions (waste/traffic apps) | Single domain | **Cross-domain correlation** |
| Generic BI/analytics | Reports after the fact | **Predictive → preventive actions with approvals** |

---

## 2. Personas & Journeys

| Persona | Goal | Pain | Success signal |
|---|---|---|---|
| **Citizen Asha** (35, ward resident) | Get a pothole fixed; know who to call | Endless follow-ups, no status | Reports once, gets ETA, sees resolution, rates it |
| **Operator Ravi** (OCC, night shift) | Handle what matters now | Alert storms, phone chaos | Works top-5 of priority queue; approves with XAI card in <30s |
| **Dept Admin Meera** (Water) | Meet SLA, defend performance | No control over routing rules | Edits SLA/routing herself; sees her dept's KPI trending |
| **Commissioner Arun** | City-wide oversight, political risk | Can't answer "why is Ward 9 slow?" | City Health Score + equity view; 6h→4min story for press |
| **Integrator Dev** (IT vendor) | Connect existing systems | Proprietary lock-in | Portal + sandbox + APIs; live in 2 weeks |

**Key journeys:** Asha: report→track→resolved→rate · Ravi: alert→chain→XAI→approve→monitor · Meera: configure→receive→resolve→report.

---

## 3. Roadmap (feature milestones — see also 03-implementation-plan)

| Phase | Horizon | Theme | Key outcomes |
|---|---|---|---|
| **R1 — MVP** | 0–3 mo | One chain, done deep | Flood chain end-to-end, ticketing, XAI, citizen loop, **replay proof of 1 event** |
| **R2 — Pilot** | 3–6 mo | 3 departments, real users | Water/traffic/police live, admin console, search, 20-event backtest, load test passed |
| **R3 — City** | 6–12 mo | Full domain coverage | All departments, twin what-if, mass broadcast, equity + carbon KPIs, LLM copilot, outcome flywheel |
| **R4 — Network** | 12–24 mo | Scale-out | Cell-per-district, federated learning, quantum benchmark report, white-label |

---

## 4. OKRs (first 2 quarters)

**O1: Prove connected intelligence works**
| KR | Metric | Target |
|---|---|---|
| KR1 | Chain recall on golden replay set | ≥85% |
| KR2 | Median detect→recommend time | ≤4 min |
| KR3 | Recommendation acceptance rate (pilot operators) | ≥70% |
| KR4 | Historical disaster replay demo completed | 1 (Time Machine) |

**O2: Deliver trusted citizen loop**
| KR | Metric | Target |
|---|---|---|
| KR1 | Ticket auto-routing accuracy | ≥90% |
| KR2 | Citizen follow-up contacts per ticket | −60% vs baseline |
| KR3 | Median time-to-resolve (pilot categories) | −40% |
| KR4 | Citizen satisfaction (post-resolve rating) | ≥4.2/5 |

**O3: Platform maturity**
| KR | Metric | Target |
|---|---|---|
| KR1 | Services with SLOs + dashboards | 100% of core |
| KR2 | p95 API latency (reads) | <300ms |
| KR3 | Load test sustained | 5,000 msg/s |
| KR4 | Audit coverage on decision actions | 100% |

---

## 5. MVP Scope & Non-Goals

**MVP = flood scenario, full depth:**
✅ citizen report (text+photo) · ✅ classify+route ticket · ✅ 2+ events → chain · ✅ risk score · ✅ recommendation + XAI card · ✅ human approve · ✅ playbook (mock executors) · ✅ citizen status notification · ✅ public KPI dashboard · ✅ replay of 1 historical event

**Explicit NON-goals (v1):** ❌ real SMS/IVR production contracts · ❌ quantum in demo path (R&D track only) · ❌ all 10 departments · ❌ mobile native apps (responsive web) · ❌ multi-city · ❌ real-time video ingestion (events only) · ❌ autonomous actions without approval

---

## 6. Success Metrics (product-level KPIs)

| Category | KPI |
|---|---|
| Impact | detect→decide minutes · cross-dept handoffs/incident · citizens alerted |
| Adoption | DAU operators · % tickets via auto-route · departments onboarded |
| Quality | chain precision/recall · false-alarm rate · SLA compliance % |
| Trust | XAI card open rate · approval rate · override rate · audit completeness |
| Equity | response-time gap between best/worst ward |

---

## 7. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Scope explosion (64 features) | High | High | MVP non-goals (§5); backlog tiers in 05-features §E |
| R2 | Chain false positives → operator distrust | Med | High | Compatibility matrix + replay gate before pilot; show confidence |
| R3 | Data scarcity / garbage-in | High | High | Open+synthetic strategy (04 §7); data-quality monitors |
| R4 | Dept refusal to share data | Med | High | Executive mandate story; sandbox onboarding; APIs not scrapers |
| R5 | Surveillance optics / privacy backlash | Med | High | Events-not-video (ADR-04), PII redaction, equity framing, transparency page |
| R6 | Quantum overclaim backfire | Med | Med | Benchmark-first narrative (ADR-03); never claim unproven advantage |
| R7 | Model drift in new zones | Med | Med | Shadow deploy per zone; rules fallback |
| R8 | Key-person dependency (5-person team) | High | Med | Monorepo docs, runbooks, pair rotation, DoD (03 §7) |
| R9 | Demo day failure | Med | High | Scripted 90s demo + local golden replay + recorded backup video |
| R10 | Legal (DPDP) non-compliance | Low | High | Data-rights API (G4), retention policy, consent flows early |

---

## 8. Operating Model

- **Cadence:** weekly demo · biweekly roadmap review · monthly KPI review with pilot sponsor
- **Decision rights:** tech lead = architecture; product = scope; dept admin = rules/SLA content; commissioner = playbook approvals in prod
- **Support model (post-pilot):** tier-1 (city helpdesk) → tier-2 (our team) → platform on-call; runbooks per service (03)
- **Change management (G6):** operator training mode on replayed incidents; champion per department; 2-week assisted pilot
