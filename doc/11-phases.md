# 11 — PHASES
### What ships, when, and the exit gate for each phase

**Relationship to other docs:** 03 = *how* (tasks/work streams), 06 §3 = *roadmap themes/OKRs*, **11 = phase contract** (scope + exit gates). M1–M5 milestones (03) map into these phases. Hardening items = 10 §13.

---

## Phase 0 — Walking Skeleton (weeks 1–4)
**Goal:** one thin path works end-to-end before anything is wide.

| | |
|---|---|
| **Ships** | Compose/k3s stack: API gateway + 3 core services (ingest→correlation→ticketing) + bus + Postgres; scripted demo: mock flood event → 2-event chain → static recommendation card → approval click → ticket created → citizen notified (mock); seeded flood incident data |
| **Team focus** | Everyone: CI/CD, repo structure (02 §9), golden replay harness stub |
| **Out of scope** | ML models (use rules), real feeds, twin, XAI depth, citizen app polish |
| **Exit gate** | ✅ demo runs twice from clean checkout · ✅ CI green (lint/test/build) · ✅ event envelope + 4 topics live · ✅ one golden replay in CI |
| **Hardening due** | — |

---

## Phase 1 — MVP Depth (weeks 5–12)  *[06: R1]*
**Goal:** the flood scenario, done deep — the story judges/citizens can feel.

| | |
|---|---|
| **Ships** | Full citizen loop (report text+photo → classify → route → track → notify → rate) · rule/causal-template chain (M-FLOOD + M-CLASS deployed) · calibrated severity score with evidence · XAI recommendation cards · human approval + playbook execution on **mock executors** · OCC console (live map, chain view, priority queue) · public KPI dashboard · Time Machine replay of **1** historical event |
| **Team focus** | C-track: graph-sync, calibration pipeline, dataquality-svc; D-track: M-FLOOD/M-CLASS/M-CHAIN v1; B-track: XAI + approval flow |
| **Out of scope** | Quantum, LLM copilot, real actuation, all-but-2 departments, mobile native |
| **Exit gate** | ✅ flood chain detect→recommend p95 **<4s** measured (H11) · ✅ chain precision ≥0.85 on golden set · ✅ score ECE <0.05 or banded (H3) · ✅ ticket auto-route accuracy ≥90% · ✅ data-quality detectors + DLQ live (H4) · ✅ ephemeral graph sync ≤5s (H2) · ✅ demo-day script + backup video |
| **Hardening due** | H2, H3, H4, H10 (T1 twin surrogate) |

---

## Phase 2 — Pilot (months 4–6)  *[06: R2]*
**Goal:** real departments, real operators, real SLAs — without the dangerous parts.

| | |
|---|---|
| **Ships** | 3 departments live (water, traffic, police) with self-service Admin Console (SLA/routing/templates) · 20-incident backtest report (Time Machine evidence pack) · search + media service · mass broadcast (text-only, pilot zones) · **fatigue controls** (suppression/digests) · approval timer ladder + auto-playbook list · degraded-mode matrix with UI badges · load test to **local-profile budget** (H11; escalate to Kafka only if measured baseline fails the required throughput) |
| **Team focus** | E-track: console + citizen app GA; A-track: partitioning work (hot-shard prep); ops: SLOs, on-call runbooks |
| **Out of scope** | Real signal/dispatch actuation, quantum in path, 4th+ departments |
| **Exit gate** | ✅ operator acceptance: XAI approval rate ≥70%, alerts/op/hr ≤12 (H5) · ✅ approval escalations tested (H6) · ✅ all degraded modes demonstrated in chaos drill (H7) · ✅ load test green · ✅ DPDP data-rights API verified (09 §4) · ✅ multi-zone golden incident passes |
| **Hardening due** | H5, H6, H7 + H10 (T2 meso twin) |

---

## Phase 3 — City Deployment (months 7–12)  *[06: R3]*
**Goal:** full domain coverage with **safe real actuation** — the phase where safety controls ship *with* the capability, never after it.

| | |
|---|---|
| **Ships** | All 10 departments onboarded · first **certified actuator adapters** (signal plans, dispatch) behind the full safety pipeline · Incident Coordinator for cross-zone incidents + fast-lane partitions (H9) · twin what-if (T3 async) + NL query · equity (City Health Score) + carbon KPIs · LLM ops copilot (retrieval-grounded, read-only) · outcome flywheel live (labels→retrain loop) · external ethics review completed |
| **Team focus** | H8 actuation safety (authorize→dry-run→interlock→saga→rollback) is the **critical path**; adapter certification checklists per city sign-off |
| **Out of scope** | Multi-city, federated learning, quantum production |
| **Exit gate** | ✅ actuation: every real-executed action passed dry-run + interlock + rollback drill (10 §9) · ✅ hot-partition failover test + cross-zone incident replay (H9) · ✅ equity gap (best/worst ward response) trending and visible · ✅ audit completeness 100% · ✅ external AI review sign-off (06-R5) |
| **Hardening due** | H8, H9, H11 (latency gates in release pipeline) |

---

## Phase 4 — Scale-Out Network (months 12–24)  *[06: R4]*
**Goal:** from one city to a repeatable platform.

| | |
|---|---|
| **Ships** | Cell-per-district architecture · federated learning across zones (privacy-preserving retrain) · **quantum track verdict** (honest benchmark report per ADR-03 — ship Q-integration only if classical gap proven) · white-label onboarding kit · ISO 27001 prep · multi-city pilot |
| **Exit gate** | ✅ quantum: either benchmarked advantage on a real problem or explicitly archived as research · ✅ second city onboarded with <4 weeks effort · ✅ federated model beats or matches local-only baseline |
| **Hardening due** | Full 10 §13 re-audit; per-city threat model (09 §6) |

---

## Cross-Phase Rules

1. **DoD discipline (03 §7):** a phase cannot close with its hardening items open — gates above are binding.
2. **Nothing demos without measurement:** any latency/accuracy number shown (PPT, demo, judges) cites the last CI/measured run (10 §11), not design targets.
3. **Actuation ladder:** mock (P1) → shadow/simulate-only (P2) → certified adapters behind dry-run gates (P3). Never skip a rung.
4. **Causal language ladder:** "correlation chains" until replay precision ≥0.85, then "validated causal links" with evidence (10 §1) — marketing follows validation.
5. **Scope swaps, not adds:** cutting a phase feature requires moving it to the next phase explicitly — updates here, 05 §E, and 03 together in one PR.

---

## One-Page Timeline

```
P0 weeks 1-4    █████░░░░░░░░░░░░░░  skeleton: report→chain→approve→notify (mock)
P1 weeks 5-12   ░░░████████░░░░░░░░  MVP depth: flood chain, XAI, score, replay×1
P2 months 4-6   ░░░░░░░░░████░░░░░░  pilot: 3 depts, admin, fatigue, chaos, 5k msg/s
P3 months 7-12  ░░░░░░░░░░░░████████  city: all depts, SAFE actuation, cross-zone, equity
P4 months 12-24 ░░░░░░░░░░░░░░░░░████  network: federated, quantum verdict, white-label
```

**Critical path:** P0 stack → P1 chain+score (C/D) → P2 fatigue+degraded (E) → **P3 H8 actuation safety** → P4 scale. Everything else is parallelizable within its phase.
