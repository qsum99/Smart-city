# 13 — BACKEND IMPLEMENTATION PLAN (PHASED)
### Python/FastAPI backend, phase by phase: tasks → deliverables → outcomes

**Scope:** backend only (frontend = React apps in 12 §3, tasks in 03 work-stream E). Phases **BP0–BP4** map 1:1 to product phases **P0–P4** (11). Hardening IDs (H1–H11) refer to doc 10 §13. All code in monorepo `backend/` (02 §9).

**Team shape:** 3 backend devs (BE1 pipeline, BE2 decisions, BE3 ticketing/platform) + 1 shared ML dev from BP1.

---

## BP0 — Foundation & Walking Skeleton (weeks 1–4)
**Goal:** empty repo → running system where one mock event becomes one ticket.
**STATUS: DONE** ✅ (2026-11-07) — ruff clean · 20/20 pytest green · live `run_all.py` + `demo.py` verified exit 0. Steps S1–S5 all gates met. Implementation in `backend/`.

### Tasks
| # | Task | Detail |
|---|---|---|
| 0.1 | Monorepo scaffold | `backend/services/*` cookiecutter template: `app/{api,core,domain,infra}`, `/healthz`+`/readyz`, uv+ruff+mypy+pytest preconfigured (no Dockerfile — LOCAL profile) |
| 0.2 | Local stack (**no Docker**) | `make init` → `pip install -r requirements.txt` + `alembic upgrade head` + seed; SQLite WAL `cityos.db`; `./data/` (media, events.jsonl, graph.json); `run_all.py` supervisor spawns every service via uvicorn on localhost ports (12 §0 LOCAL profile) |
| 0.3 | Event envelope | Pydantic models for 02 §2 envelope (`event_id, type, source, occurred_at, zone_id, geo, payload, pii_level, trace_id`); JSONL append; serde round-trip tests |
| 0.4 | In-proc bus (4 topics) | `bus.py` asyncio queues: `sensor.readings, citizen.reports, dept.alerts, incident.commands` — idempotent consumers (10 §5), DLQ table, replay CLI from `events.jsonl` |
| 0.5 | Auth (local) | PyJWT HS256 + users/roles in SQLite (09 §1 matrix); FastAPI dependency `require_role(...)`; token endpoint issues/refreshes |
| 0.6 | First 3 services | `ingest-svc` (HTTP+poll → bus), `correlation-svc` (5-min windows, stub chain), `ticketing-svc` (create/route via 1 rule) |
| 0.7 | Store baseline | Alembic init on SQLite (WAL); tables: tickets, timeline, audit_log (08 §3) |
| 0.8 | CI | GitHub Actions (plain Python job): ruff → mypy → pytest → `run_all.py` smoke test |
| 0.9 | Golden replay harness v0 | reads JSON fixture → replays to bus → asserts output events |

### Steps (execute in order)
| Step | Covers | Done when |
|---|---|---|
| **S1 — Scaffold** | 0.1 | `pytest` runs, `/healthz` answers, CI green on empty app |
| **S2 — Store + envelope** | 0.3, 0.7 | `alembic upgrade head` creates tables; envelope serde tests pass |
| **S3 — Bus** | 0.4 | publish → consume → idempotent dedupe → DLQ → `replay` CLI returns same events |
| **S4 — Services + auth** | 0.5, 0.6 | 3 uvicorn services up via `run_all.py`; `require_role` blocks/permits a test endpoint |
| **S5 — Demo + gates** | 0.8, 0.9 | `make demo` end-to-end green; replay harness in CI; **S1→S5 = M0** |

### Outcome (what you can show)
✅ `make demo` runs anywhere: mock flood event → 2-event chain → static rec card → click approve → ticket row → mock citizen notification. CI green in <6 min. **This demo is the M0 exit gate (03).**

---

## BP1 — Core Pipeline: Real Chain & Score (weeks 5–12)  *[P1 MVP depth]*
**Goal:** the flood scenario produces a *real, calibrated* chain and a defensible number.

### Tasks
| # | Task | Detail |
|---|---|---|
| 1.1 | `normalize-svc` | schema+range validation, idempotency key (`source+hash+bucket`), **PII redaction** (09 §2), feed heartbeat tracking (10 §5) |
| 1.2 | `dataquality-svc` (H4) | detectors: stale, range-violation, stuck-value, step-change → quarantine/DLQ + `DEGRADED/SUSPECT` flags on events |
| 1.3 | Knowledge graph loader | OSMnx pull (roads, hospitals) → SQLite nodes/edges + **NetworkX** graph persisted to `data/graph.json`; nightly refresh job; zones from shapefiles (PostGIS-equivalent: GeoJSON zone files locally) |
| 1.4 | `graph-sync` (H2) | ephemeral edges (closures/outages) from `dept.alerts` ≤5s, `valid_from/valid_to` + TTL ≤72h, hourly reconciliation job + drift alert |
| 1.5 | Causal templates | versioned config store (SQLite) for `(cause_type, effect_type, window, mechanism)` tuples; admin CRUD API; **template registry in rules-engine** (H1) |
| 1.6 | `chain-svc` v1 | BFS depth ≤4 / 50-node cap; per-link score = temporal × template × mechanism; confidence = product (10 §1); `chain.correlation` vs `chain.causal-grade` label; freshness discount for stale edges |
| 1.7 | `scoring-svc` (H3) | formula 10 §3: raw = GBM + criticality + population + spread + urgency → **Platt/Isotonic calibrator** trained on labeled incidents; ECE gate: ≥0.05 → banded output; evidence + version always attached |
| 1.8 | M-FLOOD, M-CLASS | training scripts + `make retrain` (APScheduler); Pydantic model IO; serving in-process (<150ms), rules fallback |
| 1.9 | M-CHAIN | LightGBM ranker; labels: operator judgments + synthetic outcomes; nDCG + ECE report per retrain |
| 1.10 | `xai-svc` | SHAP + chain narrative + lineage → XAI package (07 §3 shape); packages immutable under `./data/xai/` |
| 1.11 | Replay backtest v1 | golden set ≥20 incidents from fixtures → report: **chain precision/recall (≥0.85/0.80 gate), detect→recommend p95 (<4s), ECE** — CI job (H11 partial) |
| 1.12 | Load test (local) | locust/k6 against local uvicorn + in-proc bus; record **baseline report**; targets re-based on measured local capacity — failing the H11 budget is the documented trigger to escalate to Kafka (12 §5) |

### Steps (execute in order)
| Step | Covers | Done when |
|---|---|---|
| **S1 — Ingest quality** | 1.1, 1.2 | a poisoned event (bad range / duplicate / stale) is quarantined with `DEGRADED` flag, never reaches scoring |
| **S2 — Graph base** | 1.3, 1.4 | OSM seed loads; a `road.closure` event creates a graph edge ≤5s and it expires by TTL |
| **S3 — Chain engine** | 1.5, 1.6 | flood scenario yields `gauge→R7→traffic→ambulance→hospital` with per-link scores + correlation/causal-grade labels |
| **S4 — Score + models** | 1.7, 1.8, 1.9 | calibrated score with evidence attached; ECE report passes or output bands; M-CLASS routes ≥90% on test set |
| **S5 — Evidence pack** | 1.10, 1.11, 1.12 | XAI package renders; ≥20-incident replay report green (precision/recall/latency/ECE); load baseline recorded |

### Outcome
✅ Chain: `gauge spike → R7 closure → congestion → ambulance delay` in <4s p95 **measured**.
✅ Score shown = calibrated with evidence (auditable); band fallback proven.
✅ 20-incident replay report = Time Machine **evidence pack** (IMPACT M1).
✅ Any feed can fail without corrupting chains (quarantine demo).
**Exit: 11 §2 P1 gate fully green.**

---

## BP2 — Decision & Coordination Engines (weeks 9–14, overlaps BP1)
**Goal:** recommendations become executable workflows; pilot-grade controls.

### Tasks
| # | Task | Detail |
|---|---|---|
| 2.1 | `rules-engine` | decision tables (zone×severity×hour → playbook, priority); versioned, dry-run API, publish flow (05 F1) |
| 2.2 | `workflow-engine` | playbook DSL (states, timers, per-step handler, compensation) — Pydantic-defined; persists instances (08 §3); saga support (10 §9) |
| 2.3 | `notification-svc` | templates + channels (in-app/push mock/SMS-mock), delivery receipts, `notification.delivery` events (08 §4) |
| 2.4 | Admin Console APIs | PUT/GET SLA rules, routing rules, templates, publish draft→test→live (07 §4) |
| 2.5 | `search-svc` | **SQLite FTS5** indices + indexer (tickets/incidents/assets) + `/search` proxy (07 §7) |
| 2.6 | Twin T1 (H10) | NumPy analytic surrogates: queueing approx, travel-time, flood spread; response API `POST /twin/scenarios/run` <2s |
| 2.7 | `optimizer-svc` | OR-Tools VRP/reroute with **30s hard time-box**; job API per 07 §5; `solver_used`, `gap_pct` in response |
| 2.8 | Fatigue layer (H5) | suppression rules, severity gating (<0.5 → digest), attach≠alert, per-type token bucket, FP-rate auto-demote (10 §6) |
| 2.9 | Approval ladder (H6) | AWAITING_APPROVAL timers 5/15/30/60m → reminders → auto-playbook list → UNMANAGED banner (10 §7); role-based duty approver |
| 2.10 | Degraded modes (H7) | mode registry + capability flags per failure (10 §8); API returns `degraded:[...]`; chaos kill-scripts assert behavior |
| 2.11 | Product metrics | `GET /metrics/product` — OKR numbers (06 §4) from SQLite rollups |

### Steps (execute in order)
| Step | Covers | Done when |
|---|---|---|
| **S1 — Rules + workflow** | 2.1, 2.2 | playbook instance runs states/timers; a failing step triggers compensation |
| **S2 — Comms + admin** | 2.3, 2.4 | admin publishes new SLA/routing → next ticket follows new rule, no deploy |
| **S3 — Decision services** | 2.5, 2.6, 2.7 | `/search` returns hits; twin T1 answers <2s; optimizer job returns solution + gap within 30s |
| **S4 — Operator controls** | 2.8, 2.9 | synthetic storm test shows ≤12 alerts/hr; approval timer ladder fires 5→15→30→60m |
| **S5 — Resilience proof** | 2.10, 2.11 | chaos kill-script rows of 10 §8 all assert green; `/metrics/product` returns OKR numbers |

### Outcome
✅ Admin edits SLA at 14:00, tickets reroute at 14:01 — **no code deploy** (06-MVP differentiator).
✅ Approve → workflow runs → citizen gets status notifications, end-to-end.
✅ Chaos drill: kill bus / corrupt graph file / kill a service process one at a time → system degrades *visibly* (10 §8 matrix), never silently.
✅ Fatigue budget: operator sees ≤12 alerts/hr under synthetic storm test.
**Exit: 11 §2 P2 gate green (minus load/DPDP items done in BP3).**

---

## BP3 — Pilot Hardening & Citizen Loop (weeks 13–20)  *[P2 exit]*
**Goal:** production-shaped backend the city can actually pilot.

### Tasks
| # | Task | Detail |
|---|---|---|
| 3.1 | Full citizen API | 07 §1: create report (multipart media), track timeline, feedback, **data-rights** (`GET/DELETE /me/data`, 30d erasure job — DPDP) |
| 3.2 | Media pipeline | upload → virus scan → resize/strip metadata → WORM store + hash chain (09 §2); OCR for text-in-image (mock) |
| 3.3 | Mass broadcast | zone-targeted send with ack counting, dedupe across channels (05 F7); throttle + audit |
| 3.4 | Multizone coordinator | Incident Coordinator for events spanning ≥2 zones (10 §10): leader-elected parent incident |
| 3.5 | Partition hardening (H9) | sub-shard hot zones, fast-lane partition for severity>0.8, lag alarms + KEDA scaling rules |
| 3.6 | DPDP/GDPR pack | consent records, purpose flags in pipelines, export bundle, breach playbook runbook (09 §4) |
| 3.7 | SLOs + on-call | SLO definitions per service in SQLite metrics rollups + log-based alert checks, `docs/runbooks/` |
| 3.8 | Load gates in CI (H11) | budget report fails PR if detect→recommend p95 >4s on the CI runner |
| 3.9 | Chaos suite | scripted drills: kill service process / bus overload / corrupt DB file → assertions = 10 §8 matrix rows |
| 3.10 | Observability completion | trace_id propagation middleware → logs; per-service `/metrics` + JSON log dashboards |

### Steps (execute in order)
| Step | Covers | Done when |
|---|---|---|
| **S1 — Citizen loop** | 3.1, 3.2 | report-with-photo → track → rate; export + erasure verified on seeded citizen |
| **S2 — Coordination** | 3.3, 3.4 | broadcast acks counted; a 2-zone event chain creates one parent incident (no duplicates) |
| **S3 — Hot-zone hardening** | 3.5 | 1-zone event storm passes: scoring never starves (fast-lane asserted in test) |
| **S4 — Privacy pack** | 3.6 | consent records + export bundle + breach runbook pass the self-audit checklist |
| **S5 — Ops gates** | 3.7–3.10 | CI load gate red on regression; chaos suite green; runbook drill executed by someone other than its author |

### Outcome
✅ Load budgets green **in CI** (regressions block merges; measured baseline vs 10 §11 targets).
✅ Privacy audit pass: export + erasure demonstrated on seeded citizen data.
✅ Multi-zone disaster replay passes; hot-zone storm test doesn't starve scoring.
✅ Ops-ready: SLOs defined, on-call paged once in drill, runbooks followed by non-author.
**Exit: 11 §2 P2 gate 100% green → pilot go/no-go.**

---

## BP4 — Safe Actuation & Scale (months 7–12)  *[P3–P4]*
**Goal:** first real actuators behind the full safety pipeline; then platform scale.

### Tasks
| # | Task | Detail |
|---|---|---|
| 4.1 | Actuation framework (H8) | executor interface: `authorize(policy) → dryrun(twin T1/T2) → execute → verify(telelemetry) → rollback(pre-snapshot)`; every adapter MUST implement all 5 |
| 4.2 | Authorization service | per-actuator scopes, blast-radius policy, quorum triggers (10 §9); stored decisions in audit_log |
| 4.3 | Interlocks | hard invariants in executor (last-ambulance, final-access-road, min-green/all-red checks) — unit-tested to failure |
| 4.4 | Saga orchestrator | multi-dept actions with compensation (workflow-engine v2: compensating transitions) |
| 4.5 | Adapter #1: signals | signal-plan mock → SUMO shadow → certified; dry-run delta vs recommendation > tolerance → halt |
| 4.6 | Adapter #2: dispatch | mock unit-dispatch; interlocks first, capabilities second |
| 4.7 | Verification loop | post-exec telemetry check → VERIFY pass/fail → `outcome.captured` (feeds F4 flywheel) |
| 4.8 | Twin T2/T3 (H10) | SUMO meso + precomputed per-zone response surfaces; async T3 job runner |
| 4.9 | LLM ops copilot | retrieval-grounded read-only API over runbooks + incident history; no action rights |
| 4.10 | Federated retrain (P4) | FedAvg across zone nodes on outcome labels; privacy check |
| 4.11 | Quantum benchmark (P4, R&D) | Qiskit/Ocean vs OR-Tools harness on real VRP instances; **verdict doc, not a feature** (ADR-03) |
| 4.12 | Cell-per-district (P4) | partition strategy docs + second-cell bootstrap script (new city = config, not fork) |

### Steps (execute in order — safety-critical, no skipping)
| Step | Covers | Done when |
|---|---|---|
| **S1 — Safety core** | 4.1, 4.2, 4.3 | executor interface complete; interlock tests **fail-safe** (each invariant tested with a dangerous input that must be rejected) |
| **S2 — Saga** | 4.4 | multi-dept action drill: step 2 of 3 fails → step 1 compensated, state consistent |
| **S3 — First adapters** | 4.5, 4.6, 4.7 | mock signals+dispatch run the full 5-gate pipeline; deliberately-bad plan **halted at dry-run**; audit trail complete |
| **S4 — Twin tiers + copilot** | 4.8, 4.9 | T2 what-if <15s; T3 async job completes; copilot answers runbook question read-only |
| **S5 — Scale verdict** | 4.10–4.12 | federated model ≥ local baseline; quantum benchmark verdict written; second-cell bootstrap script run once end-to-end |

### Outcome
✅ Dry-run gate demo: a bad signal plan is **caught and halted before execution** (the safety story).
✅ One real actuator certified with full audit trail: approve→authorize→dry-run→execute→verify→(rollback drill).
✅ Twin T2 what-if answers in <15s; T3 runs overnight for planning.
✅ Quantum: honest verdict report — advantage *or* archived (no overclaim).
✅ Second cell bootstraps from script <1 week.
**Exit: 11 §3–4 gates green.**

---

## Summary: Outcomes per Phase

| Phase | Weeks | Steps | One-sentence outcome | Proof artifact |
|---|---|---|---|---|
| **BP0** | 1–4 | 5 (scaffold→demo) | Repo → running demo: event becomes ticket | `make demo` + CI badge |
| **BP1** | 5–12 | 5 (quality→graph→chain→score→evidence) | Real calibrated chain + score under 4s, measured | replay report (precision/ECE/latency) |
| **BP2** | 9–14 | 5 (rules→comms→decision→controls→resilience) | Configurable rules/workflows + fatigue + degraded modes | admin self-serve demo + chaos drill |
| **BP3** | 13–20 | 5 (citizen→coord→hot-zone→privacy→ops) | Pilot-grade: privacy, load, multizone, on-call | load gate in CI + DPDP audit |
| **BP4** | m7–12 | 5 (safety→saga→adapters→twin→scale) | Safe real actuation + scale/quantum verdict | dry-run-halt demo + certification checklist |

**Rule:** within a phase, steps are ordered — a step's "Done when" is the next step's precondition. Parallel work across *people* is allowed only after that step's gate is green.

**Dependencies:** BP0→BP1→BP2→BP3→BP4 strictly; BP1 (ML) and BP2 (engines) partially parallel after week 9; **H8 (actuation safety) cannot start before BP2's saga exists** — it is the P3 critical path (11).
