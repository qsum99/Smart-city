# 12 — TECH STACK
### One file: every technology in Urban Intelligence City OS, with why

**Rule:** Python for backend/ML, React for frontend — everything else justified below. Every choice has a reason and an escape hatch (alternative if it fails).

---

## 0. Profiles — LOCAL (default, NO DOCKER) vs PILOT (optional containers)

**Decision: local-first.** The system runs as plain Python processes on the dev machine — `pip install` + `uvicorn` — **no Docker anywhere in BP0–BP2**. Containers are an *optional* upgrade at pilot (BP3+), never a requirement.

| Subsystem | **LOCAL profile (default)** | PILOT profile (later, optional) | Same contract? |
|---|---|---|---|
| API server | **FastAPI + uvicorn** (one process or several `uvicorn app.main:app` on different ports) | containerized | ✅ OpenAPI |
| DB | **SQLite (WAL mode)** via SQLAlchemy | PostgreSQL 16 + PostGIS | ✅ SQL subset |
| Time series | SQLite tables + rollup views | TimescaleDB | ✅ |
| Graph (chains) | **NetworkX in-process**, persisted to `graph.json` + event-sourced rebuild | Neo4j | ✅ repository layer |
| Event bus | **In-proc asyncio bus** (`bus.py`, queue + fan-out) + SQLite outbox table; **fake Redis via fakeredis** if needed | Apache Kafka | ✅ same envelope/topics |
| Cache | Python `cachetools` LRU | Redis 7 | ✅ |
| Search | **SQLite FTS5** | OpenSearch | ✅ query API |
| Media/object store | **local `./data/media/` folder** (+ hash file for WORM) | MinIO | ✅ S3-like facade later |
| Auth | **PyJWT (HS256)** — self-issued tokens, users in SQLite, roles from 09 §1 | Keycloak OIDC | ✅ same claims/roles |
| Gateway | FastAPI middleware (rate-limit + auth dependency) | Kong | ✅ |
| Background jobs | **APScheduler / asyncio tasks** | Celery/Argo | ✅ |
| Observability | **structlog JSON logs + `prometheus_client` `/metrics`** | Prometheus/Grafana/Loki/OTel | ✅ metrics names |
| CI | plain Python job: ruff → mypy → pytest | + image build (optional) | ✅ |

**Swappability rule:** all data access goes through repository interfaces (`TicketRepo`, `GraphRepo`, `Bus`) so the PILOT profile is a config swap, not a rewrite. Every service keeps `/healthz` so either profile behaves identically.

**Why:** one `python -m uvicorn` loop is the fastest path to a working demo, zero install friction (Windows-friendly), and CI without containers. The heavyweight stack returns only when scale demands it (H11 load gates tell you when).

---

## 1. Languages

| Layer | Language | Why |
|---|---|---|
| Backend (all services) | **Python 3.12** | team skill, ML/AI ecosystem (bundled with model serving — no context-switch), fastest to hackathon-to-production |
| Frontend | **TypeScript + React 18** | mandated; TS = types across the API boundary (OpenAPI generates client) |
| ML/training | **Python 3.12** (PyTorch, scikit-learn) | same language as serving → no serialization gaps |
| Glue/scripts | **Python** + **Bash** | one toolchain, one CI |
| SQL | Postgres dialect | everywhere, plain |

*Go/Rust only if a proven bottleneck appears (e.g., CEP hot path) — measured, not preemptive (10 §11: current budgets fit Python fine).*

---

## 2. Backend (Python)

| Component | Choice | Why / used in |
|---|---|---|
| Web framework | **FastAPI + uvicorn** | async-native, Pydantic validation = free request schemas, **OpenAPI auto-gen** feeds 07 spec + TS client; runs as a plain local process — no container |
| Validation/config | **Pydantic v2** | event envelopes (02 §2), env config, model IO |
| ORM/migrations | **SQLAlchemy 2.0 + Alembic** (SQLite file `cityos.db`, WAL) | 08 §3 tables; same SQL works on Postgres later |
| Auth | **PyJWT (HS256)** local tokens + role dependency (09 §1 roles) | no Keycloak/OIDC in LOCAL profile — claims identical so upgrade path is free |
| Background jobs | **APScheduler + asyncio tasks** | retries, approval timers (10 §7); no Celery/Redis needed locally |
| API docs | FastAPI `/docs` (Swagger) | dev + partner portal (05 F-portal) |
| HTTP client | httpx (async) | feed pollers, adapters |
| Testing | **pytest** + httpx TestClient | 02 §10 |

**Service template (all services):** `app/{api,core,domain,infra}` · structured logs (JSON) · `/healthz`+`/readyz` · OpenTelemetry SDK · graceful shutdown · idempotency middleware (10 §5).

---

## 3. Frontend (React)

| Component | Choice | Why |
|---|---|---|
| Framework | **React 18 + Vite + TypeScript** | mandated; Vite = instant dev/build |
| State | **Zustand** + TanStack Query (React Query) | server state handled by Query (retries, cache, WS invalidation); Zustand for UI state — minimal boilerplate |
| Data fetching | OpenAPI-generated client from FastAPI spec | never hand-write API calls |
| Realtime | **native WebSocket** client with resume (`Last-Event-ID`, 07 §8) | channels → stores |
| Maps | **MapLibre GL JS** + deck.gl (layers/heatmaps) | open-source, no Google lock-in; deck.gl for incident heat + traffic layers |
| 3D/twin viewer | **CesiumJS** (3D Tiles) | matches 01 layer ⑥; 2D fallback = MapLibre |
| UI kit | **MUI (Material UI)** + Tailwind | gov-friendly forms/tables fast; Tailwind for custom layouts |
| Charts | **ECharts** | dashboards (KPI, trends), good large-N performance |
| Forms/reactivity | React Hook Form + Zod | validation mirrors Pydantic schemas |
| i18n | react-i18next | multi-language citizen app (incl. local languages) |
| a11y | axe-core in CI | gov accessibility requirement |

**Three apps, one monorepo package:** `apps/occ-console` (operator) · `apps/citizen-app` (PWA) · `apps/admin-portal` (dept config + public dashboards) — shared `packages/ui`, `packages/api-client`.

---

## 4. Data & Storage

| Need | LOCAL profile (default) | PILOT profile (later) |
|---|---|---|
| Primary OLTP | **SQLite (WAL)** — `cityos.db` | PostgreSQL 16 (+PostGIS) |
| Time series | SQLite rollup tables | TimescaleDB |
| Graph (chains) | **NetworkX + event-sourced rebuild** (`data/graph.json`) | Neo4j 5 |
| Cache / locks | `cachetools` LRU (+ fakeredis if a test needs it) | Redis 7 |
| Event bus | **In-proc asyncio bus + SQLite outbox** (4 topic names kept, envelope unchanged) | Apache Kafka (KRaft) |
| Lakehouse / replay | **Append-only `events.parquet`/JSONL in `./data/`** — Time Machine reads these | Iceberg + Parquet on MinIO |
| Search | **SQLite FTS5** | OpenSearch |
| Object store | **`./data/media/`** (files + SHA-256 manifest for evidence chain) | MinIO (S3) |
| Migrations | Alembic (works both profiles) | Alembic |

**Rule:** source of truth = the DB file; the bus is transport only; every event also appended to `./data/events.jsonl` so replay (Time Machine) works in both profiles.

---

## 5. Event Streaming & Processing

| Stage | LOCAL profile (default) | PILOT profile (escalation) |
|---|---|---|
| Transport | **In-proc asyncio bus** — 4 named queues, envelope (02 §2), at-least-once + idempotent consumers, DLQ table + replay CLI (10 §5) | Apache Kafka; partitioning per 10 §10 |
| Windows (5-min zone correlation) | Python window operator over the in-proc bus (asyncio tasks + timers) | Faust / ksqlDB if capacity requires |
| Consistency | SQLite **outbox table** + retry → graph rebuild | Outbox + Debezium CDC |
| Escalation trigger | H11 load gate: when local bus can't hit the required msg/s in CI **and** pilot is funded | → Kafka (envelope/topic names unchanged) |

*Same code against a `Bus` interface: swapping asyncio→Kafka is one adapter class.*

---

## 6. AI/ML Stack

| Component | LOCAL profile (default) | PILOT profile (later) |
|---|---|---|
| Training | **scikit-learn + XGBoost/LightGBM**; PyTorch only if STGNN needed (pip install) | same + GPU nodes |
| Serving | **in-process** (joblib load in FastAPI — <150ms for GBM/Class) | TorchServe for heavy models |
| Experiment tracking | **`mlruns/` local MLflow server (`mlflow ui`)** | remote tracking server |
| Feature/serving | precomputed feature table in SQLite | Feast feature store |
| Explainability | **SHAP** (unchanged — pure Python) | same |
| Labeling | SQLite `labels` table + simple FastAPI admin endpoint | Label Studio |
| Orchestration | **APScheduler / shell scripts** (`make retrain`) | Argo Workflows |
| Data validation | **Pydantic + custom checks in dataquality-svc** | Great Expectations |
| Drift monitor | **calibration/ECE report in `make backtest`** (10 §3) | Evidently dashboards |

---

## 7. Twin & Optimization

| Component | Choice | Why |
|---|---|---|
| Twin T1 (surrogate, <2s) | pure Python (NumPy/SciPy queueing + closed-form) | 10 §11 tier — must be fast, no engine |
| Twin T2 (meso, <15s) | **SUMO** (traffic) + custom grid flood spread | open, calibrated; precomputed surfaces |
| Twin T3 (full, async) | SUMO micro / high-res flood batch | planning + post-incident only |
| 3D viz | CesiumJS + 3D Tiles | §3 |
| Classical optimizer | **OR-Tools** | VRP/scheduling <30s hard time-box (10 §11) |
| Quantum (R&D only) | **Qiskit** (QAOA) + **D-Wave Ocean** (annealing) | benchmark-vs-OR-Tools harness (ADR-03; resrch/github-repos-quantum) |
| Quant-ML research | PennyLane | QNN experiments (P4 verdict only) |
| **Rule** | quantum **never** in demo critical path | 10 §13 P4 verdict |

---

## 8. Security & Identity

| Component | LOCAL profile (default) | PILOT profile (later) |
|---|---|---|
| Gateway | FastAPI middleware: rate limiting + auth dependency | Kong (WAF rules, 09 §6) |
| Auth/identity | **PyJWT HS256, users+roles in SQLite** (09 §1 matrix unchanged) | Keycloak OIDC (SSO, MFA, duty roles) |
| Secrets | env file (git-ignored) + python-dotenv | HashiCorp Vault |
| Scanning | **pip-audit + Bandit + Gitleaks** in CI (no images to scan) | + Trivy |
| Audit | append-only table + hash chain (08 §3) — same both profiles | same |
| Data rights | FastAPI endpoints + APScheduler erasure jobs | Celery erasure jobs |

---

## 9. Infrastructure & DevOps

**No Docker in the default profile.** Dev & demo run as local Python processes; CI is a plain Python runner.

| Component | LOCAL profile (default) | PILOT profile (later, optional) |
|---|---|---|
| Run | `python -m uvicorn` per service (or a single `run_all.py` supervisor spawning all services + bus) | containers |
| Packaged setup | `make init` = `pip install -r requirements.txt` + `alembic upgrade head` + seed | — |
| Containers | **not used** | Docker + compose when/if BP3 needs it |
| Orchestration | none (uvicorn processes) | k3s → managed K8s |
| CI/CD | **GitHub Actions (plain python job):** ruff → mypy → pytest → build | + optional image build |
| IaC | — | Terraform + Helm (only PILOT) |
| Multi-region | — (single machine) | warm standby (P4) |

*Revisit containers only when H11 load gates or multi-node ops demand it — that's a config decision, not a rewrite (§0 swappability rule).*

---

## 10. Observability & Reliability

| Component | LOCAL profile (default) | PILOT profile (later) |
|---|---|---|
| Metrics | **`prometheus_client` `/metrics` per service** | Prometheus + Grafana |
| Logs | **structlog → JSON files** (`./logs/`, rotated) | Loki / ELK |
| Traces | `trace_id` in Pydantic envelope + log correlation | OpenTelemetry → Tempo |
| Alerts | email/log warnings | Alertmanager → PagerDuty/ops channel |
| Chaos | kill a process / corrupt a feed → assert degraded-mode matrix (10 §8) in tests | Litmus/Chaos Mesh |
| Uptime | `/healthz` polled by smoke script | Blackbox exporter |

---

## 11. Testing & Quality

| Type | LOCAL tool |
|---|---|
| Unit/integration | **pytest** (≥70% services, 02 §10), httpx TestClient, fakeredis-free (bus is in-proc) |
| Frontend | **Vitest** + React Testing Library; Playwright E2E |
| Contract | OpenAPI schema diff (FastAPI → TS client) |
| Load | **locust or k6** against local uvicorn (H11 budget report — numbers cited in demos must come from here) |
| Replay/backtest | golden harness on `./data/events.jsonl` (Time Machine) |
| Static | **ruff + mypy** (Python), **ESLint + tsc** (React) |
| Security | Bandit + pip-audit + Gitleaks (no image scanning needed) |

---

## 12. Delivery Apps & Collaboration

- **GitHub** (monorepo, Actions CI) — team `qsum99/Smart-city`
- **Storybook** — OCC UI component docs
- **Postman/Newman** — API smoke in CI
- **Draw.io/Mermaid** — diagrams live in docs (01/02)

---

## 13. Stack-at-a-Glance

```
CITIZEN (React PWA · MapLibre)      OCC (React · deck.gl · ECharts)      ADMIN (React · forms)
        └───────────────┬───────────────────────────┬──────────────────────────┘
                        ▼  FastAPI middleware (auth PyJWT · rate-limit)
   ┌──────────────────────────────────────────────────────────────────────┐
   │  LOCAL PROFILE (default — no Docker):                                │
   │  uvicorn processes, Python 3.12 + FastAPI: ingest → normalize →      │
   │  correlation → chain → scoring → xai → rules/workflow → ticketing →  │
   │  notification → twin → optimizer → search                            │
   └───────┬─────────────┬──────────────┬──────────────────┬──────────────┘
           ▼             ▼              ▼                  ▼
      SQLite WAL     asyncio bus    NetworkX graph     SQLite FTS5
      + outbox       + events.jsonl  (graph.json)     ./data/media/
           ▲             ▲
   ML: XGBoost/LightGBM · SHAP · MLflow · scikit-learn (Torch optional)
   Twin: NumPy(T1) · SUMO(T2/T3, optional)   Opt: OR-Tools · [Qiskit R&D]
   Obs: structlog + prometheus_client      CI: GitHub Actions (plain Python)
   ── optional PILOT upgrade (config swap, §0) ──
   Postgres · Kafka · Neo4j · Redis · OpenSearch · MinIO · Keycloak · Kong
```

---

## 14. Decision Log (one-liners)

| Decision | Rationale |
|---|---|
| **No Docker — local FastAPI profile** | zero install friction (Windows), `pip install` + uvicorn = demo-ready in minutes; repository/bus interfaces keep the containerized upgrade a config swap (§0) |
| SQLite/NetworkX/asyncio-bus first | same contracts as Postgres/Neo4j/Kafka; correctness before scale — H11 load gates decide when to escalate |
| Python backend, not Go | team speed + ML colocated; budgets fit (10 §11) — revisit only on measured CPU wall |
| React, not Next.js | client-rendered apps behind auth; SSR adds little for dashboards |
| Kafka (when escalated) over RabbitMQ | partitioning (10 §10) + replay from offsets = Time Machine requirement |
| Neo4j (when escalated) over Neptune | ops-light for a 5-person team; swap-able behind repository layer |
| MapLibre/deck.gl over Google Maps | no vendor lock-in (05 F-portal), offline-capable, hackathon-friendly |
| Quantum parked in R&D | de Valk 2026 + ADR-03 — benchmark first, ship only proven advantage |
