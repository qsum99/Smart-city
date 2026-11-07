# 02 — SYSTEM DESIGN
### Component-level design: interfaces, flows, engines, NFRs

Companion to [01-master-architecture](01-master-architecture.md). Defines *how* each component works internally.

> **Runtime note:** default runtime = **LOCAL profile, no Docker** (12 §0). Store/bus/infra names in this doc (Postgres, Kafka, Neo4j, OpenSearch, Keycloak) map to local substitutes (SQLite, asyncio bus + outbox, NetworkX, SQLite FTS5, PyJWT) through the repository/bus interfaces. Component designs, flows, and NFRs apply unchanged to both profiles.

---

## 1. Service Inventory & Responsibilities

| Service | Type | Responsibility | Scaling unit |
|---|---|---|---|
| `ingest-iot` | stateless | MQTT bridge → validated events | replica |
| `ingest-media` | stateless + object store | Photo/video upload, scan, meta extract | replica |
| `ingest-citizen` | stateless | Report intake, rate limit, abuse guard | replica |
| `connector-svc` | stateless (1 pod per source) | Dept API pull/push, CDC, retry/backoff | per-source |
| `normalize-svc` | stateless | Avro validation, dedupe, geo-tag, PII redact | replica |
| `correlation-svc` | stateful-ish (window store) | CEP windowed joins by geo-zone | partition |
| `chain-svc` | stateless + graph cache | Incident chain construction via KG traversal | replica |
| `scoring-svc` | stateless | Risk score = model + rules | replica |
| `inference-svc` | GPU/CPU pool | Serves all prediction/detection models (versioned) | replica/HPA |
| `ticketing-svc` | stateful (DB) | Ticket lifecycle, auto-routing, SLA timers | shard by dept |
| `workflow-engine` | stateful | Playbooks, state machines, escalations, timers | workflow sharding |
| `rules-engine` | stateless + config store | Business rules evaluated as data | replica |
| `notification-svc` | stateful (queues) | Push/SMS/email/IVR fan-out, templates, dedup | per-channel workers |
| `optimizer-svc` | async workers | Classical (OR-Tools) first, quantum jobs second | job queue workers |
| `twin-svc` | compute pool | Scenario simulation, what-if runs | per-scenario job |
| `xai-svc` | stateless | SHAP, chain narrative, lineage assembly | replica |
| `search-svc` | cluster | OpenSearch index over tickets/incidents/assets | shard |
| `admin-svc` | stateless | Dept self-service config (SLA, routes, templates) | replica |
| `citizen-svc` | stateless + DB | Accounts, my-data, preferences | replica |
| `api-gateway` | edge | Routing, rate limits, versioning, WS | replica |
| `iam` | stateful | OIDC, RBAC, audit log | HA pair |

---

## 2. Event Design (backbone contract)

### Envelope (every event)
```json
{
  "event_id": "uuid-v7",
  "event_type": "flood.threshold_exceeded",
  "source": "sensor.gauge-17",
  "zone_id": "Z3",
  "geo": {"lat": 12.97, "lon": 77.59},
  "occurred_at": "2026-11-07T10:32:11Z",
  "ingested_at": "2026-11-07T10:32:11.412Z",
  "schema_ver": "1.2.0",
  "pii_level": "none|redacted|pseudonymous",
  "correlation_hint": "zone:Z3",
  "payload": { }
}
```

### Topic map
| Topic | Producers | Consumers | Partition key |
|---|---|---|---|
| `raw.telemetry` | ingest-iot, connectors | normalize, tsdb-writer | zone_id |
| `vision.events` | ingest-iot (video gw) | normalize, chain | camera_zone |
| `citizen.reports` | ingest-citizen | nlp, ticketing | zone_id |
| `dept.alerts` | connectors | normalize, correlation | zone_id |
| `incident.commands` | workflow-engine | executors (signal/dispatch APIs) | incident_id |
| `model.predictions` | inference-svc | correlation, twin | zone_id |
| `xai.packages` | xai-svc | console, audit store | recommendation_id |

**Retention:** hot 7d → warm 90d (object storage, Parquet) → archive (1y+). Exactly-once for `incident.commands`; at-least-once elsewhere + idempotent consumers.

---

## 3. The Three Missing Engines (from GAP_ANALYSIS A1–A3) — detailed design

### 3.1 Workflow Engine
- **Model:** each playbook = versioned state machine (states: `TRIGGERED → ASSESSED → AWAITING_APPROVAL → EXECUTING → VERIFYING → CLOSED`, plus `ESCALATED`, `FAILED`)
- **Features:** timers (SLA per state), human-task assignment, compensation actions, version pinning (running instances keep their version)
- **Tech:** Temporal (or Camunda if BPMN preferred); workflows as code with retries
- **Escalation:** no-ack in T → escalate per on-call directory; max depth → OCC duty officer

### 3.2 Rules Engine
- **Model:** decision tables (IF zone==Z3 AND severity>0.8 AND hour∈night THEN playbook=PB-014 priority=CRITICAL)
- **Versioning:** rules are data — draft → test (against replay) → publish → audit
- **Tech:** OPA/Rego or Drools-style engine; evaluated pre-scoring and pre-routing
- **Who edits:** department admins via Admin Console (no deploys)

### 3.3 Notification Engine
- **Channels:** push, SMS, email, IVR, webhook, siren (mass)
- **Core logic:** template rendering → channel preference lookup → rate/dedup (same incident+user+type within 15min = merge) → quiet hours (except CRITICAL) → delivery tracking → retry with backoff → receipt events
- **Mass broadcast (F7):** zone-targeted fan-out with ack counting and progress bar for OCC

---

## 4. Key Flows (design level)

### 4.1 Report → Ticket (citizen path)
```
citizen-svc POST /reports → media upload (signed URL) → ingest-citizen
  → normalize (classify via NLP model, geo-tag, redact)
  → topic citizen.reports
  → ticketing: create ticket, rules-engine routes to dept (or chain-svc
    attaches to existing incident), SLA clock starts
  → notification: ack to citizen with ETA
  → status events stream to citizen app (WebSocket) until CLOSED
```

### 4.2 Incident chain construction
```
correlation-svc maintains sliding windows (5 min) per zone
  → on ≥2 related events (type compatibility matrix + spatial join)
  → chain-svc: BFS on Knowledge Graph from epicenter
    (edges: CONNECTED_TO, BLOCKS, SERVES, FEEDS, DEPENDS_ON)
    depth ≤ 4, max 50 nodes
  → scoring-svc: severity = calibrated_P(material_harm ≤6h | evidence)
    = Platt/Isotonic-calibrated(GBM + criticality + population + spread)
    display with CI + evidence + model version; band fallback if ECE ≥0.05
  → chain snapshot persisted (immutable) + pushed to OCC
```
*Semantics (10 §1–3): traversal = correlation; causal-grade only via temporal + template + mechanism + counterfactual gates. Ephemeral edges (closures/outages) sync ≤5s via graph-sync with TTL (10 §2); chains discount stale edges.*

### 4.3 Recommendation with XAI
```
twin-svc runs N candidate playbooks (rules-filtered)
  → optimizer-svc scores feasible options (cost, time, risk)
  → xai-svc builds package: top SHAP features + chain narrative +
    data lineage refs + confidence + known limitations
  → recommendation stored → console card → human approval
  → on approve: workflow-engine executes playbook version
  → outcome captured later (F4) → labeled dataset → retrain
```

### 4.4 Optimizer (hybrid quantum)
```
POST /opt/jobs {type: vrp|tsc|allocation, constraints, budget_ms}
  → QUBO/model builder (per type)
  → run classical solver (OR-Tools) within budget
  → if type ∈ quantum_enabled && queue empty → run QAOA/annealer async
  → compare: best feasible solution + gap vs classical (logged to benchmark store)
  → result webhook → incident.commands
```
*Design rule: classical result always available within latency budget; quantum is additive and measured (ADR-03).*

---

## 5. Data Layer Design

| Store | Write pattern | Read pattern | Design choice |
|---|---|---|---|
| Lakehouse | append (stream sinks) | batch/BI | Iceberg tables per topic; compaction nightly |
| TimescaleDB | high-rate inserts | dashboards (downsampled) | continuous aggregates: 1m/15m/1h |
| Neo4j | transactional updates on incident/asset | chain BFS, asset queries | district sharding; cache hot subgraphs in Redis |
| PostGIS | slow-changing (zones, assets) | spatial joins, map tiles | read replicas; tile server cache |
| Feast | feature materialization | low-latency inference | Redis online store, Parquet offline |
| OpenSearch | index tickets/incidents/assets | operator search, filters | 3 indices + nightly reindex |
| Redis | cache + sessions + pubsub | dashboards, dedup | TTL policies per key class |
| Object store | media + archives | evidence, replay | WORM bucket for evidence chain-of-custody |

---

## 6. Non-Functional Requirements

| NFR | Target |
|---|---|
| Availability (core services) | 99.9% (pilot), 99.95% (city-scale) |
| Ingest throughput (design) | 5,000 msg/s sustained, 20k msg/s peak |
| API latency (p95) | read <300ms, write <500ms |
| Pipeline latency | see 01 §6 budget |
| RPO / RTO | RPO 15min, RTO 1h (critical incident data) |
| Concurrency | 500 OCC operators, 100k citizen sessions |
| Data retention | telemetry 1y, incidents 5y, media 90d (configurable), audit 7y |
| Accessibility | WCAG 2.1 AA; i18n: all UI strings externalized |
| Degraded mode | models unavailable → rules-only scoring + manual queue (explicit fallback flag on every recommendation) |

---

## 7. Repository Structure (monorepo → services)

```
smart-city/
├── README.md  ARCHITECTURE.md  docs/
├── libs/                    # shared: event schemas (Avro), auth, geo utils, logging
├── services/
│   ├── ingest-iot/  ingest-media/  ingest-citizen/  connector-svc/  normalize-svc/
│   ├── correlation-svc/  chain-svc/  scoring-svc/
│   ├── ticketing-svc/  workflow-engine/  rules-engine/  notification-svc/
│   ├── optimizer-svc/  twin-svc/  xai-svc/  search-svc/
│   ├── admin-svc/  citizen-svc/
├── ml/
│   ├── models/               # per-model dirs: data, train, eval, serve
│   ├── pipelines/            # Airflow/Prefect DAGs
│   └── registry/             # MLflow config
├── web/
│   ├── console-occ/  citizen-app/  admin-portal/  public-dashboard/
├── scripts/
│   ├── run_all.py  loadtest/  replay/
└── .github/workflows/        # CI: ruff → mypy → pytest → smoke (plain Python)
```

---

## 8. Testing Strategy (design-level)

| Layer | Approach |
|---|---|
| Unit | ≥70% on services; pure logic (chain builder, rules, SLA math) highest coverage |
| Contract | Pydantic envelope compatibility checks in CI (JSONL samples) |
| Integration | in-proc: real bus + SQLite + NetworkX spun up per PR (no containers) |
| **Replay/backtest (A8)** | golden set of 50 historical incidents → chain accuracy, recommendation hit-rate |
| Load | locust/k6 against local uvicorn — H11 budget report (numbers cited in demos) |
| Chaos | kill bus/service process or corrupt graph file; verify degraded matrix (10 §8) holds (P2) |
| Model | holdout + drift gate in CI; shadow deploy before promotion |
| UAT | scripted 90-second demo journey (see IMPACT_PLAYBOOK §5) |
