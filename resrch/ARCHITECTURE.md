# URBAN INTELLIGENCE — AI-POWERED CITY OPERATING SYSTEM
## Complete Software Architecture (HLD) — Pure Software, Fully Scalable

**Project:** Cortisol Override — HIMOVATION 2026 Solve-a-Thon
**Theme:** AI for Smart Cities
**Scope:** 100% software system (no hardware/deployment content) — greenfield repo `qsum99/Smart-city`

---

# 1. Software Architecture Principles

| # | Principle | Meaning |
|---|---|---|
| P1 | **Event-driven** | Every city signal becomes an event on a backbone; services react asynchronously |
| P2 | **Loose coupling, high cohesion** | Each domain is an independent service — a police outage never stops traffic |
| P3 | **Scale horizontally, fail gracefully** | No single point of failure; stateless services + partitioned data |
| P4 | **Intelligence as a platform** | ML models are versioned products (MLOps), not embedded scripts |
| P5 | **Explainable by default** | Every AI action carries provenance + rationale (XAI) before human approval |
| P6 | **Secure & privacy-first** | RBAC, encryption, audit trails, PII redaction at ingestion |
| P7 | **API-first & modular** | Every capability is a versioned service; departments plug in via standard APIs |

---

# 2. System Context (Level 1)

```mermaid
graph TB
    subgraph Citizens["Citizens & Front Ends"]
        CA["Citizen Mobile/Web App<br/>(report · track · alerts)"]
        CC["Contact Center / 311"]
        SS["Social & Call-center NLP feed"]
    end

    subgraph Sources["External Data Feeds (software sources)"]
        IoT["IoT Data Streams<br/>(MQTT/CoAP feeds)"]
        VID["Video Analytics Events<br/>(vision service events)"]
        TRF["Traffic Data Feeds<br/>(loops·GPS·transit APIs)"]
        GIS["GIS / Map Services<br/>(geospatial APIs)"]
        DEPT["Department System APIs<br/>(water·police·health·disaster)"]
        WX["Weather & River Gauge Feeds"]
    end

    OS[["URBAN INTELLIGENCE OS<br/>AI-Powered City Operating System"]]

    subgraph Consumers["City Consumers"]
        OCC["Integrated Command &<br/>Control Center (OCC)"]
        DC["Department Consoles"]
        DASH["Executive / Public Dashboards"]
    end

    CA --> OS
    CC --> OS
    SS --> OS
    IoT --> OS
    VID --> OS
    TRF --> OS
    GIS --> OS
    DEPT --> OS
    WX --> OS
    OS --> OCC
    OS --> DC
    OS --> DASH
```

**One-line contract:** *Ingest everything → understand connections → predict consequences → recommend action (with reasons) → humans approve → execute & learn.*

---

# 3. Container Architecture (Level 2) — The 8 Software Layers

```mermaid
graph TB
    subgraph L1["① INTEGRATION / INGESTION LAYER (software)"]
        GW_IOT["IoT Protocol Service<br/>(MQTT/CoAP broker integration)"]
        GW_STREAM["Stream Ingest Services<br/>(video-events · telemetry · tickets)"]
        GW_API["API Connectors<br/>(dept systems · 3rd-party feeds)"]
        GW_CIT["Citizen Ingest API<br/>(reports · NLP intake)"]
        NORM["Normalization & Validation<br/>(schema check · dedupe · PII redact · geo-tag)"]
    end

    subgraph L2["② EVENT BACKBONE"]
        KAFKA["Event Streaming Platform<br/>(Kafka / Redpanda)"]
        BUS["Schema Registry +<br/>Event Catalog (Avro)"]
    end

    subgraph L3["③ DATA PLATFORM"]
        LAKE["Lakehouse<br/>(raw · cleaned · curated zones)"]
        TSDB["Time-Series Store<br/>(TimescaleDB / InfluxDB)"]
        KG["City Knowledge Graph<br/>(Neo4j — entities & relations)"]
        GEO["Geo Store<br/>(PostGIS + 3D Tiles)"]
        FEAT["Feature Store<br/>(Feast)"]
    end

    subgraph L4["④ INTELLIGENCE LAYER (AI/ML)"]
        MLOPS["MLOps Registry<br/>(MLflow · model versioning)"]
        DET["Detection Services<br/>(vision event classifiers)"]
        PRD["Prediction Services<br/>(traffic · air quality · flood · demand)"]
        NLP["NLP Services<br/>(ticket classification · sentiment)"]
        LLM["LLM City Copilot<br/>(RAG over city knowledge)"]
    end

    subgraph L5["⑤ CORRELATION & REASONING"]
        CEP["Complex Event Processing<br/>(link events in time + space)"]
        CHAIN["Incident Chain Engine<br/>(flood→road→traffic→ambulance→hospital)"]
        Prio["Risk / Priority Scoring"]
    end

    subgraph L6["⑥ DECISION INTELLIGENCE"]
        DT["Digital Twin Service<br/>(what-if simulation)"]
        QOPT["Quantum Optimization Service<br/>(QAOA/annealing · routing·signals·resources)"]
        POL["Policy & Playbook Engine<br/>(rules + human approvals)"]
        XAI["Explainability Service<br/>(SHAP · rationale · audit)"]
    end

    subgraph L7["⑦ APPLICATION LAYER"]
        OCC2["Command Center Console"]
        TICKET["Smart Ticketing &<br/>Cross-Dept Workflow"]
        CITAPP["Citizen App Backend<br/>(report→track→resolved)"]
        PUB["Public Dashboards"]
    end

    subgraph L8["⑧ API, IDENTITY & PLATFORM SERVICES"]
        APIG["API Gateway + BFF<br/>(REST/GraphQL · WebSocket live)"]
        IAM["Identity / IAM<br/>(OIDC · RBAC · dept roles)"]
        OBS["Observability<br/>(OpenTelemetry · Prometheus · Grafana)"]
        SEC["Security Services<br/>(encryption · secrets · audit log)"]
    end

    L1 --> KAFKA
    KAFKA --> L3
    L3 --> L4
    L4 --> L5
    L5 --> L6
    L6 --> L7
    L7 --> L8
    L8 --> L7
    L8 -.governs.-> L1 & L2 & L3 & L4 & L5 & L6
```

---

# 4. Layer Specifications (Software Only)

## ① Integration / Ingestion Layer — *unified entry point for all data*
| Service | Responsibility |
|---|---|
| **IoT Protocol Service** | MQTT/CoAP broker integration (EMQX/Mosquitto), device-session management, topic→event mapping |
| **Stream Ingest Services** | Consume video-analytics events, telemetry, external feeds → validate → publish |
| **API Connectors** | Push/push connectors for each department system (REST, webhook, CDC-based where available) |
| **Citizen Ingest API** | Report submission (text/image/location), rate limiting, abuse protection |
| **Normalization & Validation** | Schema enforcement (Avro), deduplication, geo-tagging, **PII redaction** before storage |

*All components are stateless microservices — scale by adding replicas.*

## ② Event Backbone — *the nervous system*
- **Kafka / Redpanda** topics: `raw.telemetry`, `vision.events`, `citizen.reports`, `dept.alerts`, `incident.commands`, `model.predictions`
- **Schema Registry (Avro)** — contract-first evolution; every event versioned
- Exactly-once for commands; at-least-once for telemetry
- **Scale: partition by city zone (geo-hash)** → ordered per zone, parallel across zones
- Retention tiers: hot (7d) → warm (90d, object storage) → archive (Parquet)

## ③ Data Platform — *the memory*
| Store | Data | Purpose |
|---|---|---|
| **Lakehouse** (raw/cleaned/curated) | All events, historical archives | One copy, many engines (batch + streaming) |
| **Time-series DB** | Sensor readings, KPIs | Fast downsampling & dashboards |
| **City Knowledge Graph (Neo4j)** | Roads, zones, hospitals, assets + relations | **Heart of cross-department correlation** |
| **Geo Store (PostGIS + 3D Tiles)** | Maps, zones, CityGML | Spatial queries & twin rendering |
| **Feature Store (Feast)** | Online/offline ML features | Training/serving consistency |

## ④ Intelligence Layer — *reflexes & predictions*
| Service | Input → Output |
|---|---|
| **Detection Services** | Vision events → classified incidents (waste, parking, crowd, anomaly classes) |
| **Prediction Services** | Time series + graph → forecasts (traffic STGNN-class, air-quality CNN-LSTM-class, flood LSTM-class, demand) |
| **NLP Services** | Text/voice → structured tickets, classification, sentiment |
| **LLM City Copilot** | Natural-language queries → insights/recommended actions (RAG over curated city knowledge) |
| **MLOps (MLflow)** | Model registry, versioning, canary/AB rollout, drift monitoring, retraining pipelines |

*Every model served behind a versioned inference API; shadow → canary → production.*

## ⑤ Correlation & Reasoning — *"connected intelligence" (Slide 2 gap)*
```mermaid
sequenceDiagram
    participant S as Feeds
    participant K as Kafka
    participant C as CEP / Chain Engine
    participant G as Knowledge Graph
    participant R as Risk Scorer
    participant D as Decision Layer

    S->>K: flood threshold HIGH (zone Z3)
    K->>C: event #1
    C->>G: query assets in Z3
    G-->>C: roads R7, hospital H2, route A
    S->>K: road.closure R7
    S->>K: traffic.congestion +40%
    C->>C: temporal + spatial join → INCIDENT CHAIN
    C->>R: chain = [flood→closure→congestion→ambulance-delay→hospital-risk]
    R->>D: severity=CRITICAL, score=0.93, chain explanation
    D->>D: recommend playbook PB-014 + optimized reroute
```
- **Complex Event Processing** (Flink/ksqlDB): windowed joins across topics by geo-zone
- **Incident Chain Engine**: graph traversal over Knowledge Graph → produces the exact chain from Slide 2
- **Risk scoring**: model output + business rules → one prioritized queue for OCC

## ⑥ Decision Intelligence — *the brain*
| Service | Role |
|---|---|
| **Digital Twin Service** | What-if simulation ("close this road — what happens?"); renders via 3D Tiles/Cesium; runs per-domain simulation models (traffic, flood plume) |
| **Quantum Optimization Service** | Async job API: `POST /opt/jobs {type: vrp|tsc|allocation}` → QUBO → **QAOA (Qiskit) / D-Wave** with **classical OR-Tools fallback**; use cases: ambulance routing, signal plans, resource deployment; automatic benchmarking of quantum vs classical |
| **Policy & Playbook Engine** | Maps incident → action with guardrails; human-in-the-loop approval for critical actions |
| **Explainability (XAI)** | SHAP attributions + incident-chain narrative + data lineage attached to every recommendation |

## ⑦ Application Layer — *the experience*
- **Command Center Console:** live map, incident chains, recommendations + XAI panel, approval actions (WebSocket push)
- **Smart Ticketing:** auto-routing to the responsible department, SLA timers, cross-dept workflows (solves "citizens don't know who is responsible")
- **Citizen App Backend:** report → auto-classify → track → resolution notification
- **Public Dashboards:** open KPIs (ISO 37120-aligned indicators)

## ⑧ API, Identity & Platform Services
- **API Gateway + BFF** (Kong/Envoy): rate limiting, versioning, WebSocket for live views
- **IAM (Keycloak):** OIDC, RBAC by department/role, citizen pseudonymous IDs, audit log on every read/write
- **Observability:** OpenTelemetry traces (follow an incident end-to-end), Prometheus metrics, Grafana
- **Security:** TLS in transit, encryption at rest, secrets vault, tamper-evident audit log

---

# 5. End-to-End Data Flow (the demo scenario)

```mermaid
flowchart LR
    A[Threshold event:<br/>heavy rain / river spike] --> B[Ingest: validate +<br/>geo-tag + PII redact]
    B --> C[Kafka<br/>raw.telemetry]
    C --> D[Flood prediction model]
    D --> E{Threshold<br/>exceeded?}
    E -- yes --> F[CEP: create incident<br/>+ graph correlation]
    F --> G[Knowledge Graph:<br/>assets & people in zone]
    G --> H[Impact chain +<br/>risk score 0.93]
    H --> I[Digital Twin:<br/>simulate 3 options]
    I --> J[Quantum/classical optimizer:<br/>best reroute + signal plan]
    J --> K[XAI recommendation +<br/>playbook PB-014]
    K --> L{Human approval<br/>in OCC}
    L -- approve --> M[Execute: commands, alerts,<br/>dispatch, citizen push]
    M --> N[Smart tickets to<br/>water/traffic/police/health]
    N --> O[Outcome logged →<br/>model retraining loop]
```

**Latency budget (p95, software pipeline):**
| Stage | Target |
|---|---|
| Ingest → event on bus | < 500 ms |
| Prediction inference | < 2 s |
| Correlation + chain | < 3 s |
| Twin simulation (3 options) | < 30 s |
| Optimization job (quantum/classical) | < 60 s (async) |
| **Human decision** | **variable (by policy)** |
| Command execution ack | < 5 s |

---

# 6. Software Scalability — How It Grows 10×

```mermaid
graph TB
    subgraph S1["SCALE STATE 1 — Single instance"]
        A1["All services ×2 (HA)<br/>Streaming platform 3 nodes<br/>Single data cluster"]
    end
    subgraph S2["SCALE STATE 2 — Horizontal"]
        B1["Zone-partitioned streams<br/>HPA per service (CPU/queue-lag)<br/>Read replicas + caches<br/>Inference pools autoscaled"]
    end
    subgraph S3["SCALE STATE 3 — Multi-instance / cell-based"]
        C1["One 'city cell' per district<br/>Global control plane (IAM, model<br/>registry, dashboards)<br/>Federated learning across cells"]
    end
    S1 --> S2 --> S3
```

### Scaling levers (per dimension)
| Dimension | Mechanism |
|---|---|
| **Ingest** | Broker clustering + zone-partitioned topics; validation/dedupe spread across stateless replicas |
| **Compute** | Stateless microservices → K8s HPA on CPU/queue-lag; KEDA autoscale on stream lag |
| **Data** | Time-series downsampling; lakehouse compaction; Redis caches for dashboard reads |
| **Graph** | District-sharded knowledge graph; read replicas for dashboards |
| **ML** | Pooled GPU training jobs; autoscaled CPU/GPU inference pods; model caching |
| **Optimization** | Job queue + worker pools; classical-first with quantum burst capacity |
| **Multi-tenancy** | Namespace-per-department; cell-per-district isolates noisy neighbors |
| **Geography** | Active-active regions; data residency; CDN for public dashboards |

---

# 7. Technology Stack (software)

| Layer | Primary choice | Alternatives | Research reference (in this folder) |
|---|---|---|---|
| IoT messaging | **EMQX** | Mosquitto | `github-repos-smart-city-frameworks.md` |
| Stream bus | **Kafka / Redpanda** | — | — |
| CEP | **Flink / ksqlDB** | — | — |
| Lakehouse | **Iceberg + MinIO/S3** | — | — |
| Time series | **TimescaleDB** | InfluxDB | — |
| Knowledge graph | **Neo4j** | — | — |
| Geo/3D | **PostGIS + Cesium + 3D Tiles** | 3DCityDB | `github-repos-smart-city-frameworks.md` |
| Traffic ML | **LibCity / pytorch_geometric_temporal / tsl** | — | `github-repos-aiml-traffic-energy.md` |
| Forecasting | **NeuralForecast / TimesFM** | OpenSTEF | same |
| Vision events | **YOLO-class classifiers + DeepSORT** | SAMgeo | `github-repos-vision-llm-datasets.md` |
| NLP/LLM | **CityGPT/UrbanGPT-class RAG** | — | same |
| Federated training (later) | **Flower** | FedML | same |
| RL control (later) | **RESCO / sumo-rl / CityLearn** | CityFlow | `github-repos-rl.md` |
| Quantum optimization | **Qiskit Optimization + D-Wave Ocean + OR-Tools** | QOptLib benchmarks | `github-repos-quantum.md` |
| MLOps | **MLflow + Feast** | — | — |
| APIs / IAM | **Kong + Keycloak** | — | — |
| Orchestration | **Kubernetes + Istio** | — | — |
| Observability | **OpenTelemetry + Prometheus + Grafana** | — | — |

---

# 8. Security & Governance (architecture-level)

1. **Network zones:** public / DMZ / platform / department namespaces with enforced policies
2. **Identity:** OIDC SSO for city staff; citizen pseudonymous IDs; credentials for data feeds
3. **RBAC matrix:** traffic operator sees traffic + incident chains; cannot execute health playbooks
4. **Data protection:** PII redaction at ingestion; column-level masking; encryption in transit/at rest; tamper-evident audit trail on every recommendation & approval
5. **AI governance:** model registry with approval gates, drift alerts, human-in-the-loop for critical actions, XAI packet stored with each decision (**the "AI must be trusted" challenge from Slide 2**)
6. **Resilience:** graceful degraded modes (rules-only when models unavailable), dead-letter queues, circuit breakers between services

---

# 9. Architecture Decision Records

| ADR | Decision | Rationale |
|---|---|---|
| ADR-01 | Event-driven backbone (Kafka) over sync APIs | Decouples siloed departments — the core Slide-2 problem |
| ADR-02 | Knowledge graph as correlation backbone | Cross-department "connected intelligence" needs relations, not rows |
| ADR-03 | Hybrid classical+quantum optimizer with benchmarks | Quantum is early-maturity for city problems (research dossier) — classical-first keeps production honest |
| ADR-04 | Ingest events only, not raw payloads | Bandwidth + privacy (PII redaction at the boundary) |
| ADR-05 | Human-in-the-loop for critical actions | Trust + accountability (Slide 2: "AI needs to be trusted") |
| ADR-06 | Modular monorepo → microservices when scaled | Hackathon speed now, scale boundaries later |

---

# 10. Diagram Pack (for slides / documentation)

1. **System context** (§2) — who interacts with the OS
2. **8-layer container view** (§3) — the core architecture slide
3. **Incident chain sequence** (§4⑤) — how connected intelligence works
4. **End-to-end flood flow** (§5) — the demo narrative
5. **Software scale-out states** (§6) — scalability story for judges

---

*Companion research: `SMART_CITY_RESEARCH_REPORT.md` + 7 technical dossiers + 6 GitHub-repo dossiers in this folder.*
