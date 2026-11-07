# DOC — Urban Intelligence City OS (Cortisol Override)

Canonical product documentation set. **Files 01–05 are the core five**; 06–09 cover gaps identified in review; **10–11 are the hardening/phase contracts; 12 = tech stack; 13 = backend implementation plan**.

| # | File | What it answers |
|---|---|---|
| **01** | [Master Architecture](01-master-architecture.md) | What are the system's layers/containers? How does it scale? |
| **02** | [System Design](02-system-design.md) | How is each component designed — interfaces, flows, NFRs? |
| **03** | [Implementation Plan](03-implementation-plan.md) | How do we build it — milestones, work breakdown, repo structure? |
| **04** | [Models](04-models.md) | Which AI/ML models, trained how, evaluated how, deployed where? |
| **05** | [Features](05-features.md) | Full feature inventory (citizen + government) |
| 06 | [Product Plan](06-product-plan.md) | Roadmap, OKRs, personas, MVP scope, risk register |
| 07 | [API Specification](07-api-specification.md) | REST/WebSocket contracts for all services |
| 08 | [Data Model](08-data-model.md) | Core entities + event schemas (JSON) |
| 09 | [Security & Compliance](09-security-compliance.md) | RBAC, encryption, audit, DPDP/GDPR, AI governance |
| **10** | [Reliability & Safety Hardening](10-reliability-safety-hardening.md) | Corrections + hardening: correlation-vs-causality, live graph sync, score calibration, failure modes, alert fatigue, approval escalation, degraded modes, **actuation safety (authorize→dry-run→rollback)**, hot partitions, justified latency/twin tiers |
| **11** | [Phases](11-phases.md) | Phase contracts P0–P4: what ships, exit gates, hardening due per phase, actuation/causal-language ladders, timeline |
| **12** | [Tech Stack](12-tech-stack.md) | Every technology with justification — **backend: Python/FastAPI · frontend: React/TS** — plus data, ML, twin, security, infra, testing, stack diagram, decision log |
| **13** | [Backend Implementation Plan](13-backend-implementation-plan.md) | Backend phased delivery BP0–BP4: per-phase numbered tasks, deliverables, **outcome + proof artifact**, dependencies (Python/FastAPI) |

> **Precedence:** where 10 conflicts with 01/02/04/06 (causality wording, latency numbers, score semantics), **10 wins** — see 10 §12.

**Related folders:**
- `../resrch/` — 14 research dossiers (smart city, quantum, AI/ML, RL, GitHub repos, master research report)
- `../ARCHITECTURE.md`, `../FEATURES.md`, `../GAP_ANALYSIS.md`, `../IMPACT_PLAYBOOK.md` — root-level working docs (01/05 supersede the first two)
- `../Cortisol Override.pptx` — competition deck
