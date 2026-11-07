# 10 — RELIABILITY & SAFETY HARDENING
### Answers to the technical critique: causality, sync, scoring, failure modes, actuation safety, partitioning, latency

**Status:** this document corrects overclaims in 01/06 and specifies the missing designs. Where 01 conflicts with 10, **10 wins**.

---

## 1. Chain Semantics: correlation vs causality

**Admission:** v1 chains are *temporal-spatial correlation by graph proximity* (BFS + edge whitelist). Calling them "causal" was an overclaim. Fix in three steps:

**Step 1 — honest naming.** Ships as **"Correlation Chains"**; the positioning claim becomes *"connected context, not just isolated alerts."*

**Step 2 — causal criteria (v1.5).** A chain is promoted to **causal-grade** only if it passes all four gates:

| Gate | Test | Example (flood→R7) |
|---|---|---|
| C1 Temporal precedence | cause strictly precedes effect within domain window | gauge spike 12 min before closure ✓ |
| C2 Domain causal template | edge type is in an authored *causal template* (not any graph edge) | `flood --BLOCKS--> road` is causal; `road --near--> hospital` is NOT |
| C3 Mechanism plausibility | physical/operational mechanism score ≥ threshold | water depth > curb height → road passable=false |
| C4 Counterfactual check | removing candidate cause removes effect in twin/simulator | no flood → closure event wouldn't exist |

- **Authored causal templates:** domain experts write them as `(cause_event_type, effect_event_type, window, mechanism, direction)` tuples — stored as versioned config in `rules-engine` (they *are* authored, not mined, in v1)
- **Chain confidence = product of per-link scores** (each link: temporal × template × mechanism), not a single opaque number
- **Validation:** replay goldens measure **chain precision** (fraction of links humans agree are real) and **recall** — targets: precision ≥0.85, recall ≥0.80 before "causal" language is used anywhere publicly

**What we do NOT claim:** automated causal discovery from data (research-grade, out of scope); unvalidated links stay labeled `correlation` in the UI.

---

## 2. Knowledge Graph Live-State Sync

Problem: graph must reflect *ephemeral* city state (closures, works, incidents), not just static assets.

**Design: split the graph into two lifecycles**

| Layer | Content | Sync mechanism | Freshness SLO |
|---|---|---|---|
| **Static** (slow) | roads, pipes, hospitals, zones | nightly bulk + CDC on GIS system of record | ≤24h |
| **Ephemeral** (fast) | closures, diversions, asset outages, active incidents | **event-sourced edges with TTL** — every state event creates/retires an edge with `valid_from/valid_to` | ≤5s via bus |

**Mechanics:**
1. Every ephemeral change arrives as an event on `dept.alerts` (already in topic map) → `graph-sync` consumer applies within seconds
2. **TTL + heartbeat:** ephemeral edges auto-expire (e.g., closure edges valid ≤72h unless re-asserted) — stale state self-heals
3. **Outbox/CDC** for dual-writes (Postgres↔Neo4j) — already noted in 08, now mandatory for asset edits
4. **Reconciliation job:** hourly diff between event log and graph; drift → alert + auto-repair queue
5. **Chain reads carry a freshness stamp:** if any traversed edge is older than its SLO, chain confidence is discounted and the UI shows "state possibly stale"

---

## 3. Risk Score: formula, meaning, calibration

**0.93 must mean something.** Definition:

```
severity = calibrated_P(material_harm within 6h | evidence)
```

**Computation (v1, deliberately simple & auditable):**
```
raw = w1·M-CHAIN_score + w2·asset_criticality + w3·population_in_zone
      + w4·spread_rate + w5·lead_time_urgency        (weights: rules, versioned)
calibrated = Platt/Isotonic mapping fitted on labeled incidents → [0,1]
display    = calibrated (rounded), ALWAYS with: confidence interval,
             evidence list, model version, fallback flag
```

**Calibration pipeline:**
1. Reliability diagram monthly on hold-out (target **ECE < 0.05**, already in 04 — now binding for display)
2. If ECE ≥ 0.05 → score shown as **band** (LOW/MED/HIGH) instead of a decimal — *no false precision*
3. Every displayed score stores: raw value, calibration version, top-3 evidence refs → auditable via XAI package
4. **Operator feedback loop:** "score too high/low" button → labels for refit

**Rule:** a score never appears without its evidence and version. 0.93 in a demo is always traceable to a calibration report.

---

## 4. Chain Authoring, Learning, Validation

| Phase | Mechanism |
|---|---|
| **Author** | Causal templates + type-compatibility matrix as **versioned config** (editable by domain experts in Admin Console — not code) |
| **Validate** | Before publish: template must pass replay set (new links can't reduce precision below 0.85) — *rule testing in CI* |
| **Learn (v2)** | Outcome labels (F4) → mine candidate links (association-rule style) → **propose** to expert for approval (human-in-loop; never auto-publish) |
| **Audit** | Every chain stores `template_version`; historical chains remain reproducible |

Chain "grammar" (v1): `event_type pairs × max_window × edge_whitelist × max_depth(4) × max_nodes(50)` — all config, all testable.

---

## 5. Data Quality, Faults, Duplicates, Idempotency

**Sensor trust layer (`normalize-svc` + `dataquality-svc`):**

| Fault | Detection | Response |
|---|---|---|
| Stale feed | heartbeat gap > 3× interval | mark feed `DEGRADED`; chains using it discount confidence; UI badge |
| Plausible-range violation | value outside physical bounds | quarantine event → DLQ, feed alert |
| Stuck value | identical reading N times | flag `SUSPECT`, require 2nd source confirmation |
| Drift/calibration jump | step-change detector | annotate, exclude from model features until cleared |
| Duplicate events | idempotency key = `source + content_hash + time_bucket(5s)` | drop at normalize (already designed — now specified) |
| Cross-source conflict | two feeds disagree on same fact | keep both, mark `CONTESTED`, scoring uses lower-confidence path |

**Idempotency contract (all consumers):** event_id as key; writes upsert-by-id; `incident.commands` exactly-once *effect* via outbox + dedup store (7d window). DLQ with replay tooling for every consumer.

**Confidence rule:** chains/scores built on `DEGRADED/SUSPECT` data are labeled in the XAI packet — never silently averaged away.

---

## 6. Alert Fatigue & False Positives

**Fatigue budget (product rule):** no operator receives >**N=12 actionable alerts/hour** (configurable per role); system must merge, demote, or digest the rest.

| Mechanism | Design |
|---|---|
| Suppression rules | same zone+type within window → merge into existing incident (not new alert) |
| Severity gating | score < 0.5 → **digest only** (hourly summary), no pop-up |
| Correlation dedup | chain engine attaches new events to open incidents instead of alerting (attach ≠ alert) |
| Rate shaping | per-type token bucket at correlation output |
| False-positive feedback | every dismissed alert is labeled; per-type FP rate tracked; **type auto-demoted to digest when FP-rate > 40% over 7d** |
| Fatigue metric in OKR | alerts/operator/hour + dismissal rate as product KPI (06 §6) |

**Policy:** false positives are *measured, budgeted, and auto-tuned* — not just "monitored."

---

## 7. Approval Timeout, Absence, Escalation

**Approval is a workflow state with its own SLO:**

```
AWAITING_APPROVAL
  ├─ t+0     : sent to primary approver (OCC duty role, not a person-name)
  ├─ t+5m    : reminder + notify backup approver
  ├─ t+15m   : escalate to supervisor role (on-call directory)
  ├─ t+30m   : auto-actions from pre-approved AUTO-PLAYBOOK list execute
  │            (pre-authorized low-risk actions: alerts, notifications, info requests)
  └─ t+60m   : commissioner on-call + incident flagged UNMANAGED
               (visible on OCC banner — absence itself becomes an event)
```

- **Role-based, not person-based** — approver = duty role with rotation
- **Quorum option:** high-blast-radius actions require 2 distinct roles
- **Break-glass:** any supervisor can seize approval duty (logged, reviewed)
- **Auto-playbook list:** explicitly pre-authorized actions that need *no* human after timeout (defined per playbook, commissioner-signed) — so the system degrades to *safe automation*, not to *nothing*
- Demo/production: approval timer visible on the card ("auto-escalates in 4:32")

---

## 8. Degraded Modes (failure-mode matrix)

| What fails | Mode | System still does | System stops doing |
|---|---|---|---|
| Prediction models down | RULES-ONLY | chain via templates, rules scoring, manual queue | numeric forecasts (UI shows badge) |
| Kafka down | BUFFERED | edge buffers (disk, 1h), citizen/ticket writes to local store, drain on recovery | live map updates (frozen + banner) |
| Neo4j down | SHALLOW-CHAIN | flat event correlation (no traversal), zone-only grouping | deep chains, asset impact |
| Twin down | RECOMMEND-ONLY | rules-based recommendations without simulation options | option comparison, NL what-if |
| Optimizer down | QUEUE-LATE | tickets/dispatch continue; opt jobs queued with ETA | new route/signal solutions |
| IAM/Keycloak down | TOKEN-CACHE | existing sessions (≤30min JWT), read-only | logins, approvals (unless break-glass) |
| Notification channels down | DEGRADED-DELIVERY | in-app + retry queue, channel failover, OCC sees delivery board | push/SMS until recovery |
| Full region loss | FAILOVER | warm standby region (RPO 15m/RTO 1h) | live processing during failover window |

**Every mode:** banner in UI (`DEGRADED: forecasts unavailable — rules-only`), incident auto-created for the outage itself, automatic recovery checks. **Principle: the system never fails silently and never claims confidence it doesn't have.**

---

## 9. Safety-Critical Actuation (the most important section)

**Principle: approval ≠ authorization ≠ execution.** Three separate gates:

```
RECOMMEND → APPROVE (human) → AUTHORIZE (policy check) → DRY-RUN (simulate) → EXECUTE → VERIFY → ROLLBACK-READY
```

| Control | Design |
|---|---|
| **Authorization** | per-actuator scopes in IAM: *who approved × what actuator × blast radius*. E.g., operator can approve signals in zone Z3 but NOT hospital dispatch; actuator policy = allowlist of playbook steps per role |
| **Blast radius limits** | every executable action declares scope (zones affected, # of signals, # of ambulances). Actions exceeding policy threshold → auto-require quorum (§7) |
| **Simulation-before-execute (mandatory)** | executable side effects run through twin dry-run first: expected state delta computed; if dry-run result deviates > tolerance from recommendation's claimed impact → **halt + re-ask**. Signal plans: verify no all-red/all-green, min-green compliance, no starvation (interlock checks) |
| **Interlocks (hard rules)** | safety invariants enforced in executor regardless of approval: e.g., never dispatch last ambulance from a station; never close final access road to a hospital; max concurrent closures per zone |
| **Two-phase for multi-dept** | cross-dept actions (signal plan + dispatch + closure) execute as saga: each step acked, failure → compensate (revert signals, stand down units) |
| **Rollback** | every actuator exposes `revert` with pre-action snapshot stored at execute time (signals: previous plan; dispatch: cancel codes). Rollback itself is one-click in OCC, pre-authorized |
| **Verify** | post-execution telemetry check within T (e.g., signal plan: did queues move as predicted?) → VERIFY pass/fail feeds OutcomeNet (F4) |
| **Executor sandbox** | v1 demo: executors are *mock adapters* — real actuation lands only with adapter certification checklist (per city sign-off) |
| **Audit** | full chain: who approved, XAI version, dry-run output, exec result, verify — hash-chained (09) |

*Non-negotiable for pilot: dry-run gate + interlocks + rollback ship together with the first real actuator.*

---

## 10. Partitioning: hot zones & cross-zone incidents

**Problem A — hot partition** (disaster zone floods its partition with events):

| Mitigation | Design |
|---|---|
| Sub-shard hot zones | partition key = `zone + sub_shard(0..k)` chosen by load; k grows with rate (auto-split at >2k msg/s per partition) |
| Prioritized drain | critical events (`severity>0.8`) get a **fast-lane partition** with dedicated consumer capacity — disaster traffic can't starve scoring |
| Backpressure policy | shed `raw.telemetry` first (lossy OK), never shed `incident.commands` / approvals |
| Hot-zone alert | partition lag > 5s → scale consumers (KEDA) + OCC banner |

**Problem B — incidents cross zones:**

| Mitigation | Design |
|---|---|
| Boundary events | zone-edge graph edges exist (roads connect zones) — chains *may* cross ≤2 zone hops |
| **Incident Coordinator** | when events in ≥2 zones share time window + compatible types → coordinator process creates a **parent incident** spanning zones; child zone-incidents link to it; scoring computed once at parent |
| Global index | `incidents` table is global (partitioning is for *event streams*, not for incident identity) — OCC always sees one list |
| Election | coordinator is leader-elected (single active per spanning incident) to avoid double-creation |
| Validation | golden set includes multi-zone incidents (e.g., river crossing 3 wards) as required test cases |

---

## 11. Latency Budget: justification & the Twin

**Revised, component-justified budget (p95):**

| Stage | Budget | Basis |
|---|---|---|
| Ingest → bus | <500 ms | single async hop + validation; measured in load test (A-k6) |
| Correlation window emit | <2 s | window advance interval = 1s + processing headroom |
| Chain (≤50 nodes) | **<1 s** | Neo4j BFS at 50 nodes is ms-class; budget includes fetch+assemble; *if* >1s → shallow mode |
| Scoring | <300 ms | GBM inference + calibration lookup |
| **Subtotal detect→recommend** | **<4 s** | this is the number we claim (was "3s chain" asserted) |
| Twin — **fidelity tiers** (see below) | T1 <2s · T2 <15s · T3 async | tier selected by decision urgency |
| Optimization (classical) | <30 s (async ok) | OR-Tools with hard time-box |
| Command ack | <5 s | executor round-trip |

**The Twin — defined at last (three fidelity tiers):**

| Tier | What it is | Latency | Used for |
|---|---|---|---|
| **T1 Analytic surrogate** | closed-form/parametric models (queueing approximations, travel-time functions, flood spread formula) | <2 s | instant option comparison, dry-run gate (§9) |
| **T2 Calibrated meso-simulation** | reduced-order simulation (mesoscopic traffic, 2D flood grid at coarse res), precomputed response surfaces per zone | <15 s | recommendation generation, saved scenarios |
| **T3 Full simulation** | microscopic traffic (SUMO-class) / high-res models, batched | async (minutes) | night-time planning, post-incident review, offline what-ifs |

- **Rule:** the demo claims only T1/T2 latency; T3 never sits on the critical path
- **Precomputation:** per-zone response surfaces built nightly (common closures/scenarios pre-simulated) → T2 becomes table lookup + interpolation in the common case
- **Twin honesty:** twin confidence shown alongside; if surrogate error on calibration set > tolerance → fall back to rules-only recommendation (§8)

**Process fix:** all latency numbers are **targets gated by load-test evidence** (03 testing strategy); claims in PPT/demos cite the measured value from the last run, not the design target.

---

## 12. Corrections to Other Docs

| Doc | Correction |
|---|---|
| 01 §4 / chain sequence | rename "causal chains" → "correlation chains (causal-grade per §1 gates)" |
| 06 positioning | same wording fix; differentiator = *connected context + explained action*, not causality |
| 02 §6 latency | replace with §11 justified budget + twin tiers |
| 04 M-CHAIN | adopt §3 formula + calibration fallback to bands |
| 05 B1.2 | feature text: add "with causal-grade validation" |
| GAP_ANALYSIS cross-cutting | items 1–4 (data quality, false positives, degraded mode, feedback) are now **specified here** — mark resolved |

---

## 13. Hardening Backlog (new work items)

| ID | Item | Milestone |
|---|---|---|
| H1 | Causal templates + confidence decomposition (§1) | M2 |
| H2 | graph-sync ephemeral layer + TTL + reconciliation (§2) | M1 |
| H3 | Score calibration pipeline + band fallback (§3) | M1 |
| H4 | Dataquality-svc: fault detectors + quarantine + DLQ tooling (§5) | M1 |
| H5 | Fatigue budget: suppression, digests, FP auto-demote (§6) | M2 |
| H6 | Approval timer ladder + auto-playbook list (§7) | M2 |
| H7 | Degraded-mode matrix + UI badges (§8) | M2 |
| H8 | Actuation: authorize→dry-run→interlock→saga→rollback (§9) | M3 (with first real adapter) |
| H9 | Hot-shard + fast-lane + Incident Coordinator (§10) | M3 |
| H10 | Twin T1/T2 implementation + precomputed surfaces (§11) | M2 |
| H11 | Latency evidence in CI (load tests as release gate) | M3 |
