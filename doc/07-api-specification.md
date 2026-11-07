# 07 — API SPECIFICATION
### Core REST + WebSocket contracts (v1)

Base: `https://api.cityos.example/v1` · Auth: Bearer (OIDC) · All mutations audited · Idempotency-Key header on writes.

---

## 1. Citizen API

### POST /reports — create a report
```json
// request
{
  "type": "infrastructure.pothole",
  "description": "Deep pothole near bus stop",
  "geo": {"lat": 12.9716, "lon": 77.5946},
  "media_refs": ["media://up/8f3a..."],
  "channel": "mobile",
  "anonymous": false
}
// 201 response
{
  "ticket_id": "TCK-2026-004821",
  "status": "RECEIVED",
  "assigned_department": "PWD",
  "sla_due_at": "2026-11-07T16:32:00Z",
  "confidence": 0.91
}
```

### GET /tickets/{id} — status timeline
```json
{
  "ticket_id": "TCK-2026-004821",
  "status": "IN_PROGRESS",
  "timeline": [
    {"at": "...", "state": "RECEIVED", "actor": "system"},
    {"at": "...", "state": "ASSIGNED", "actor": "rules-engine", "dept": "PWD"},
    {"at": "...", "state": "IN_PROGRESS", "actor": "PWD-Ravi"}
  ],
  "eta": "2026-11-07T16:32:00Z",
  "sla_breach": false
}
```

### GET /tickets?mine=true — list mine · POST /tickets/{id}/feedback — rating
### GET /me/data — export my data (zip) · DELETE /me/data — erase (DPDP)

---

## 2. Incident & Chain API

### GET /incidents?status=open&zone=Z3 — OCC list (priority-sorted)
```json
{
  "items": [{
    "incident_id": "INC-000912",
    "severity": 0.93,
    "type": "flood",
    "zone_id": "Z3",
    "chain": {
      "nodes": [
        {"id": "evt:1", "kind": "flood.threshold", "at": "..."},
        {"id": "rd:R7", "kind": "road.closure", "at": "..."},
        {"id": "tr:R7", "kind": "traffic.congestion", "delta_pct": 40},
        {"id": "amb:12", "kind": "ambulance.delay", "minutes": 11},
        {"id": "hsp:H2", "kind": "hospital.access_risk", "level": "HIGH"}
      ],
      "confidence": 0.89
    }
  }]
}
```

### GET /incidents/{id}/recommendations — XAI packages
```json
{
  "recommendations": [{
    "rec_id": "REC-441",
    "playbook": "PB-014",
    "title": "Activate flood response + reroute ambulances",
    "expected_impact": {"ambulance_delay_avoided_min": 14, "citizens_alerted": 312},
    "xai": {
      "why": ["R7 closure blocks primary route to H2", "ambulance 12 en route on R7", "flood peak in 40 min"],
      "top_features": [{"feature": "chain_depth", "value": 4, "shap": 0.31}, {"feature": "hospital_closeness", "shap": 0.22}],
      "confidence": 0.87,
      "limitations": ["forecast uncertainty ±20 min"]
    },
    "options": ["A", "B", "C"]
  }]
}
```

### POST /incidents/{id}/recommendations/{rec}/approve — human approval (X-Approver role)
### POST /incidents/{id}/recommendations/{rec}/reject — with reason

---

## 3. Ticketing & Workflow (dept)

- `GET /depts/{dept}/tickets?sla_at_risk=true`
- `POST /tickets/{id}/claim` · `POST /tickets/{id}/transition {state, note}`
- `GET /workflows/instances/{id}` — playbook state, timers, history
- `POST /workflows/{playbook}/trigger {incident_id}`

---

## 4. Admin (self-service)

- `GET/PUT /admin/depts/{dept}/sla-rules` — decision-table JSON
- `GET/PUT /admin/depts/{dept}/routing-rules`
- `GET/PUT /admin/depts/{dept}/templates` — notification templates
- `POST /admin/depts/{dept}/publish` — versioned publish (draft→test→live)

---

## 5. Optimizer (async jobs)

### POST /opt/jobs
```json
{"type": "vrp", "incident_id": "INC-000912",
 "constraints": {"vehicles": 3, "depots": ["D1"], "budget_ms": 30000},
 "solver": "auto"}   // auto | classical | quantum
// 202
{"job_id": "OPT-771", "status": "QUEUED", "poll": "/opt/jobs/OPT-771"}
```
### GET /opt/jobs/{id} → `{status, solution, solver_used, classical_gap_pct, feasibility, benchmark_ref}`

---

## 6. Twin (what-if)

- `POST /twin/scenarios {name, changes:[{op:"close_road", id:"R7", duration_h:72}]}`
- `GET /twin/scenarios/{id}/results` → metrics: congestion %, delay min, CO₂, affected population
- `POST /twin/scenarios/{id}/compare` — saved comparison (F8)
- `POST /twin/nl-query {"question": "What if we close MG Road for 3 days?"}` → {answer, scenario_ref, charts}

---

## 7. Search & Notifications

- `GET /search?q=...&type=ticket|incident|asset|dept` — OpenSearch proxy
- `GET /notifications/preferences` · `PUT ...` — channel prefs, quiet hours
- `POST /notifications/mass-broadcast {zone_id, template, require_ack}` (OCC role) → progress stream

---

## 8. WebSocket: `wss://api.cityos.example/v1/stream`

| Channel | Payload |
|---|---|
| `occ.incidents` | new/updated incidents + chain deltas |
| `occ.recommendations` | new XAI packages |
| `tickets.{id}` | status transitions (citizen & dept) |
| `broadcast.progress` | mass-notification ack counts |
| `metrics.live` | dashboard KPI ticks |

Envelope: `{channel, seq, at, data}` — client resumes with `Last-Event-ID`.

---

## 9. Model & Ops (internal)

- `POST /ml/infer {model, version, inputs}` — inference-svc
- `GET /ml/models` · `GET /ml/models/{id}/card`
- `POST /backtest/run {incident_set}` → report_id; `GET /backtest/reports/{id}` — Time Machine
- `GET /metrics/product` — OKR metrics (06 §4)

---

## 10. Conventions

| Rule | Value |
|---|---|
| Errors | RFC 7807 problem+json `{type, title, status, detail, trace_id}` |
| Pagination | cursor-based (`?cursor=&limit=`) |
| Time | RFC 3339 UTC |
| IDs | Prefixed ULIDs (TCK-, INC-, REC-, OPT-) |
| Versioning | URI major version; additive changes only within major |
| Rate limits | per-client tiers; 429 + Retry-After |
