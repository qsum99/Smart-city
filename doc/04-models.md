# 04 — MODELS
### AI/ML model inventory: tasks, data, training, evaluation, deployment

**Principle:** every model is a versioned product in MLflow — shadow → canary → production, with drift gates and retraining triggers (P4, ADR-08). Research grounding: `../resrch/ai-ml-*.dossier.md`, `../resrch/quantum-computing-smart-city-dossier.md`, `../resrch/rl-*.dossier.md`.

---

## 1. Model Inventory Overview

| ID | Model | Task | Family | Milestone | Priority |
|---|---|---|---|---|---|
| M-FLOOD | FloodNOW | Time-series forecast (threshold) | LSTM/Transformer ensemble | M1 | **P0** |
| M-CLASS | TicketClassifier | Multi-class text classification | Transformer (fine-tuned) | M1 | **P0** |
| M-CHAIN | ChainScorer | Incident severity ranking | GBM + rules hybrid | M1 | **P0** |
| M-TRAFFIC | TrafficNet | Spatio-temporal speed/flow forecast | STGNN (Graph WaveNet-class) | M3 | P1 |
| M-AIR | AirQNet | PM2.5 forecast | CNN-LSTM | M3 | P1 |
| M-VISION | VisionGuard | Vision event classification | YOLO-class detector | M3 | P1 |
| M-DEMAND | DemandNet | Ride/waste demand forecast | LightGBM/STGNN | M4 | P2 |
| M-LLM | CityCopilot | NL Q&A over city knowledge | LLM + RAG | M4 | P1 |
| M-OUTCOME | OutcomeNet | Playbook success probability | GBM | M4 | P1 |
| *M-QUANT* | *QuantOpt* | *Combinatorial optimization* | *QAOA/annealing (hybrid)* | *M5* | *P2 (R&D)* |

---

## 2. P0 Models (detail)

### M-FLOOD — FloodNOW
- **Task:** predict zone-level flood threshold breach 1–6h ahead; binary + severity regression
- **Inputs:** river gauge, rainfall (recent 72h windows), soil/moisture proxy, historical incidents per zone, calendar features → per-zone time series
- **Architecture (v1):** LSTM encoder + gradient-boosted residual (start simple); v2: temporal fusion transformer (NeuralForecast class)
- **Data:** open river/rain gauges + city historical incident logs; synthetic augmentation for rare events (see §7)
- **Training:** walk-forward CV (no shuffle); class imbalance: focal loss / oversampling
- **Metrics:** recall@0.95 precision (never miss a flood), lead-time distribution (median target ≥60 min), AUC-PR
- **Baseline:** persistence + threshold-rule (must beat)
- **Serving:** `inference-svc`, batched per-zone every 5 min → `model.predictions` topic
- **Retrain:** monthly + drift alert (feature PSI > 0.2)

### M-CLASS — TicketClassifier
- **Task:** classify citizen report → {dept, category, subcategory, urgency}
- **Inputs:** text (+ OCR'd image text later), zone, channel
- **Architecture:** multilingual sentence-transformer fine-tune (or distilled BERT); hierarchical: dept first, then category
- **Data:** labeled tickets (start: 2k synthetic + public 311 datasets e.g. NYC 311)
- **Metrics:** dept accuracy ≥90%, category accuracy ≥85%, urgency F1 ≥0.80
- **Serving:** sync in `normalize-svc` path (<150ms p95); fallback = keyword rules
- **Active learning:** low-confidence samples → human labeling queue

### M-CHAIN — ChainScorer
- **Task:** rank candidate incident chains + severity 0–1
- **Inputs:** chain features (event types, window gaps, spatial spread, asset criticality, population-in-zone, model outputs)
- **Architecture:** gradient-boosted trees (interpretable, data-efficient) on labeled chains; **not** a black-box LLM
- **Labels:** operator severity judgments + historical outcomes (M-OUTCOME joins later)
- **Metrics:** nDCG@5 for ranking; calibration (reliability diagram — score 0.9 happens 90% of time)
- **Score formula (10 §3):** `severity = calibrated(w1·GBM + w2·asset_criticality + w3·population + w4·spread_rate + w5·lead_time_urgency)` → Platt/Isotonic mapping on labeled incidents; **binding gate: ECE <0.05, else display banded (LOW/MED/HIGH), never a false-precise decimal**; every shown score carries CI + top-3 evidence + calibration version; operator "score too high/low" button feeds refit
- **Fallback:** pure rules (weights in rules-engine) when model unavailable → degraded mode (10 §8), flagged in UI

---

## 3. P1 Models (summary)

### M-TRAFFIC — TrafficNet
- **Task:** 15/30/60-min speed & flow per road segment
- **Family:** Graph WaveNet-class (adaptive adjacency) — implement via **LibCity / pytorch_geometric_temporal** (see resrch)
- **Data:** open sensor datasets (METR-LA, PEMS-BAY, LargeST subset) + city feed when available
- **Metrics:** MAE/RMSE/MAPE at 15/30/60 horizons vs HA/persistence/LSTM
- **Serving:** every 5 min, zone-partitioned batches

### M-AIR — AirQNet
- **Task:** PM2.5 forecast 24h per station/zone
- **Family:** CNN-LSTM (APNet-class per resrch dossier) + meteorology features
- **Data:** OpenAQ + met feeds
- **Metrics:** MAE, RMSE, R²; beat LSTM-only baseline

### M-VISION — VisionGuard
- **Task:** classify incoming vision *events* (flood-like water on road, crowd density flag, waste pileup, fire smoke)
- **Design:** upstream systems send *events*; optional in-house YOLO-class model for raw frames (privacy: frames stay at source; only events enter OS — ADR-04)
- **Metrics:** mAP per class at agreed operating point; false-alarm budget < X/hour (operator-defined)

### M-LLM — CityCopilot
- **Task:** NL answers for officials ("which wards got most incidents last week?") + draft notes
- **Architecture:** RAG — retrieve from curated city KB (incidents, playbooks, KPIs, assets) + tool-calling to read APIs; **never** free-text actions on city systems
- **Evaluation:** Golden-QA set (100 questions) + hallucination spot-checks; grounded-answer rate target ≥90%
- **Guardrails:** no PII in prompts, redact-then-retrieve, output filters

### M-OUTCOME — OutcomeNet
- **Task:** P(success | incident, playbook, context) for playbook recommendation + post-hoc scoring
- **Data:** outcome labels captured by F4 (did it work? time-to-resolve, recurrence within 7d)
- **Impact:** closes the learning flywheel (IMPACT_PLAYBOOK M9)

---

## 4. M5 / R&D — Quantum Optimization (M-QUANT)

| Aspect | Design |
|---|---|
| Problem classes | VRP (ambulance/collection routing), signal-plan search, resource allocation |
| Formulation | QUBO/Ising with penalty constraints (feasibility-first — see resrch quantum dossier) |
| Runtime path | classical OR-Tools first (always) → quantum (QAOA on Qiskit / D-Wave) async when eligible |
| **Mandatory:** benchmark harness | every quantum result logged with classical gap, runtime, feasibility rate → report (ADR-03) |
| Honest claim | "R&D capability, benchmarked" — no advantage claims until measured (resrch: de Valk 2026) |

---

## 5. Training & MLOps Pipeline

```
data sources → ingest/synthesize → labeled sets (versioned in lakehouse)
  → ml/pipelines DAGs (Prefect/Airflow): validate → train → evaluate (gate) → register (MLflow)
  → shadow deploy (score, compare to live) → canary (5% traffic) → prod
  → drift monitor (feature PSI, performance decay) → alert → retrain queue
  → outcome labels (F4) join training data quarterly
```

| Gate | Threshold |
|---|---|
| Eval vs baseline | must beat baseline on primary metric |
| Calibration | ECE < 0.05 for scoring models |
| Fairness | performance gap across wards < 10% (equity — IMPACT M7) |
| Latency | p95 inference within budget (02 §6) |
| Drift | PSI > 0.2 → warn; > 0.5 → block traffic |

---

## 6. Evaluation Framework (how we prove it works)

1. **Replay/golden set (C5):** ≥20 historical incidents replayed → chain recall, recommendation hit-rate, lead-time — *the Time Machine (IMPACT M1)*
2. **Offline model reports:** per-model cards (data, metrics, limits) in `ml/models/*/MODEL_CARD.md`
3. **Fairness report:** per-ward metrics quarterly
4. **Quantum benchmark report:** quarterly (M5)
5. **Public numbers:** aggregate, anonymized results feed the impact slide (IMPACT M3)

---

## 7. Data Strategy (when city data doesn't exist yet)

| Need | Source |
|---|---|
| Traffic | METR-LA / PEMS-BAY / LargeST (open) |
| Air quality | OpenAQ + EPA |
| Flood/rain | Open-Meteo, gauge APIs, historical event catalogs |
| Tickets | NYC/other open 311 datasets (format-compatible) |
| Vision events | synthetic generator + public anomaly datasets |
| Knowledge graph | OSM (via Osmnx) + hand-seeded city asset list |
| Rare disaster events | scenario synthesis in twin (documented as synthetic) |

*Rule: every metric reported with a data-provenance tag — open / synthetic / city-provided.*

---

## 8. Model Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Imbalanced rare events | focal loss, synthetic scenarios, recall-first thresholds |
| Cold start (no city labels) | transfer from open datasets; rules-first until 500 labels |
| Hallucination (LLM) | RAG-only, golden-QA gate, no autonomous actions |
| Drift in new zones | per-zone calibration; shadow mode per zone |
| Overfitting to replay set | hold-out incidents never used in tuning |
