# 03 — IMPLEMENTATION PLAN
### How we build Urban Intelligence City OS — milestones, work breakdown, sequencing

> **Runtime note:** all build work targets the **LOCAL profile — no Docker** (12 §0): `pip install` + uvicorn + SQLite + in-proc bus. Container/Kafka/Neo4j/Keycloak tasks are optional PILOT-profile escalation, not part of the default path.

---

## 1. Delivery Philosophy

- **Walking skeleton first:** one thin end-to-end path (report → chain → recommendation → approve → notify) before breadth
- **Depth over features:** prove the Incident Chain + XAI on one scenario (flood) before other domains
- **Demo-driven:** every milestone ends with something clickable
- **Monorepo, modular monolith → split when scaled** (ADR-06)

---

## 2. Milestones

| MS | Name | Exit criteria (definition of done) |
|---|---|---|
| **M0** | Walking skeleton | 3 services + in-proc bus + SQLite running via `run_all.py` (no Docker); scripted demo: mock event → chain (2 events) → static recommendation card → approval click → ticket created → citizen notified (mock) |
| **M1** | Intelligence | Flood prediction model + NLP ticket classifier in registry; inference-svc versioned; XAI package on every recommendation; 10-model test suite green |
| **M2** | Depth (flood domain) | Full flood playbook: twin sim (simplified), optimizer (classical), workflow engine, notification engine (mock channels), SLA timers, OCC console v1 |
| **M3** | Breadth + proof | Ticketing for 3 departments (water/traffic/police), search, admin console v1, **backtest engine replaying 20 historical events** with accuracy report |
| **M4** | Pilot-ready | IAM hardening, audit log, observability dashboards, load test (5k msg/s), DPDP data-rights endpoints, training mode, runbooks |
| **M5** | Scale | Zone partitioning enforced, HPA/KEDA tuned, cell design validated, quantum optimizer benchmark report vs classical |

---

## 3. Work Breakdown (by stream)

### Stream A — Platform (bus, data, infra)
| ID | Task | Milestone |
|---|---|---|
| A1 | Monorepo skeleton + CI (lint/test/build/scan) | M0 |
| A2 | In-proc asyncio bus + topic map + Pydantic envelopes + outbox table (Kafka adapter = later escalation) | M0 |
| A3 | Lakehouse zones (raw/curated) + sinks | M1 |
| A4 | TimescaleDB + continuous aggregates | M1 |
| A5 | Graph schema (assets, zones, relations) in SQLite + NetworkX seed data (`data/graph.json`) | M0 |
| A6 | PostGIS + zone/asset CRUD | M1 |
| A7 | Feast feature store wiring | M1 |
| A8 | Observability (OTel traces, Prometheus, Grafana, alerts) | M2 |

### Stream B — Ingestion
| ID | Task | Milestone |
|---|---|---|
| B1 | ingest-citizen (reports + signed media URLs) | M0 |
| B2 | normalize-svc (validation, dedupe, geo-tag, PII redaction) | M0 |
| B3 | ingest-iot (MQTT bridge, device sessions) | M1 |
| B4 | connector-svc framework + 2 mock dept connectors | M1 |
| B5 | ingest-media (scan, thumbnail, meta) | M1 |

### Stream C — Correlation & Chain (the differentiator)
| ID | Task | Milestone |
|---|---|---|
| C1 | correlation-svc windowed joins (zone-based) | M0 |
| C2 | chain-svc BFS traversal + chain snapshot persistence | M0 |
| C3 | scoring-svc (rules v1 → model v2) | M1 |
| C4 | type-compatibility matrix + tuning on replay set | M3 |
| C5 | backtest/replay engine (A8) + golden incidents | M3 |

### Stream D — Decision
| ID | Task | Milestone |
|---|---|---|
| D1 | workflow-engine (playbook state machine v1: flood PB-014) | M2 |
| D2 | rules-engine (decision tables + versioning) | M2 |
| D3 | notification-svc (templates, dedup, mock channels → real SMS later) | M2 |
| D4 | xai-svc (SHAP + chain narrative + lineage) | M1 |
| D5 | optimizer-svc classical (OR-Tools: VRP, signal-plan) | M2 |
| D6 | quantum path (Qiskit QAOA + D-Wave client) + benchmark harness | M5 |
| D7 | twin-svc v1 (scenario CRUD + simplified simulation) | M2 |

### Stream E — Applications
| ID | Task | Milestone |
|---|---|---|
| E1 | OCC console (live map, chain view, XAI card, approve) | M0→M2 |
| E2 | citizen app (report, track, alerts) | M0→M2 |
| E3 | ticketing UI + dept console | M2 |
| E4 | admin console (SLA/routing/template self-service) | M3 |
| E5 | public dashboard (KPIs, City Health Score) | M3 |
| E6 | LLM city copilot (RAG) | M4 |

### Stream F — ML
| ID | Task | Milestone |
|---|---|---|
| F1 | Flood prediction model (train on open data; pipeline in ml/pipelines) | M1 |
| F2 | Ticket classifier (NLP) | M1 |
| F3 | Traffic STGNN (LibCity-based) | M3 |
| F4 | Model registry + drift gates + shadow deploy | M2 |
| F5 | Outcome-label pipeline (analytics flywheel) | M4 |

### Stream G — Product & Governance
| ID | Task | Milestone |
|---|---|---|
| G1 | Personas + journey maps (06-product-plan) | M1 |
| G2 | OKRs + metric instrumentation | M1 |
| G3 | RBAC matrix + PyJWT auth (users/roles in SQLite; Keycloak only in PILOT profile) | M2 |
| G4 | Audit log (tamper-evident) + data-rights API (export/delete) | M4 |
| G5 | Risk register review + mitigations | M2 |
| G6 | Operator training mode (replay sandbox) | M4 |

---

## 4. Sequencing (critical path)

```
M0 (weeks 1-3):  A1,A2,A5,B1,B2,C1,C2,E1(skeleton),E2(skeleton)
M1 (weeks 4-8):  A3-A7,B3-B5,C3,D4,F1,F2,F4,E1v2,G1,G2
M2 (weeks 9-14): A8,D1,D2,D3,D5,D7,E2v2,E3,G3,G5
M3 (weeks 15-20): C4,C5,D?,E4,E5,F3
M4 (weeks 21-26): E6,F5,G4,G6 + hardening/load tests
M5 (weeks 27-32): D6 + scale validation + cell experiment
```

*Parallel tracks: A/B/C run ahead of D/E; F runs from M1; G continuous.*

---

## 5. Team Shape (minimal viable)

| Role | Count | Owns |
|---|---|---|
| Tech lead / architect | 1 | A, cross-service contracts |
| Backend engineers | 2 | B, C, D services |
| Frontend engineers | 2 | E (console + citizen) |
| ML engineer | 1 | F, MLOps |
| Product/UX | 1 | G, journeys, design system |
| QA/automation | 1 (or shared) | test pyramid, replay goldens |
| *Hackathon subset* | *team of 5* | *M0 + flood slice of M1/M2 only* |

---

## 6. Repository & CI/CD

- **Monorepo** `qsum99/Smart-city` (currently empty → M0 fills it)
- CI pipeline: ruff → mypy → pytest → `run_all.py` smoke → replay smoke (plain Python job — no image build/scan)
- CD: staging auto on main; production gated by replay-golden + approval
- Environments: `local` (venv + SQLite) · `staging` · `prod` — same code, config-swap via 12 §0

---

## 7. Definition of Done (per feature)

1. Code + tests (unit + 1 integration)
2. Avro/contract updated if events changed
3. RBAC + audit events covered
4. Metrics + trace emitted
5. Docs (API spec 07 updated)
6. XAI/rule impact assessed (if decision-affecting)
7. Replay goldens still green

---

## 8. Top Risks to Delivery

| Risk | Mitigation |
|---|---|
| Scope explosion (64 features) | MVP cut in 06-product-plan; park rest in backlog |
| Data scarcity | Synthetic + open datasets (OpenAQ, METR-LA, NYC TLC) — see 04-models §7 |
| Chain false positives | Type-compatibility matrix + replay tuning gate (C4) before M3 exit |
| Empty repo at demo time | M0 is non-negotiable first sprint |
| Quantum overclaim | D6 ships only with benchmark report (ADR-03) |

---

## 9. Hardening Backlog (from doc/10 — binding)

Critical-path hardening items H1–H11 in **10-reliability-safety-hardening.md §13**, woven into work streams: H2 graph-sync → C-track (M1) · H3 score calibration, H4 dataquality-svc, H10 twin tiers → C/D-track (M1–M2) · H5 alert fatigue, H6 approval ladder, H7 degraded modes → B/E-track (M2) · H8 actuation safety (authorize→dry-run→interlock→rollback) gates **first real actuator (M3)** · H9 hot-shard/fast-lane/Incident Coordinator → A-track (M3) · H11 latency load-tests as release gate. **Exit criteria: no milestone passes DoD with its assigned H-items open.**
