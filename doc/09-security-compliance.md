# 09 — SECURITY & COMPLIANCE
### Identity, access, data protection, audit, AI governance, DPDP/GDPR

---

## 1. Identity & Access (IAM)

### Federation
- **Staff:** OIDC via Keycloak (city SSO or national e-ID where available); MFA mandatory for OCC/approver roles
- **Citizens:** pseudonymous IDs (no PAN/SSN stored); phone/email verified; anonymous reports allowed (no account)
- **Services:** mTLS identities (service mesh); short-lived tokens; no shared secrets

### RBAC matrix (v1)
| Role | View map/incidents | Approve recommendations | Execute playbooks | Edit rules/SLA | Manage models | Citizen PII |
|---|---|---|---|---|---|---|
| Citizen | own tickets only | — | — | — | — | own data only |
| Dept Operator | own dept + chains | propose | execute dept steps | — | — | masked |
| OCC Operator | city-wide | **✓** | all | — | — | masked |
| Dept Admin | own dept | — | — | **✓** | — | masked |
| Commissioner | city-wide + KPIs | ✓ (policy) | ✓ | policy | — | masked |
| Data Scientist | aggregated | — | — | — | ✓ (models) | **no** |
| Auditor | read-all incl. audit | — | — | — | — | per case |
| Platform Admin | infra | — | — | — | — | **no** (break-glass logged) |

*Attribute-based extras: zone scoping (operators see their zone unless OCC), time-boxed elevation for incidents.*

---

## 2. Data Protection

| Control | Design |
|---|---|
| In transit | TLS 1.3 everywhere; mTLS service-to-service |
| At rest | AES-256; per-tenant keys where required |
| PII redaction | at `normalize-svc` — pattern detection (phone, ID numbers) → redact before lake; `pii_level` in envelope (02 §2) |
| Data minimization | collect only what an incident needs; retention per 08 §6 |
| Media/evidence | WORM bucket, SHA-256 hash chain, access logged, faces/plates redacted unless case-authorized |
| Secrets | LOCAL: git-ignored env file (never committed) · PILOT: Vault; rotation + CI scanning both profiles |
| Backup | encrypted snapshots; RPO 15min / RTO 1h for critical stores |

---

## 3. Audit & Accountability

- **Every** recommendation, approval, rejection, rule change, data export, admin action → `audit_log` (hash-chained: `prev_hash` integrity)
- Approvals record: *who, when, XAI package version shown, action taken, outcome*
- Immutable export for investigators/auditors (signed bundles)
- Break-glass access: dual-control + post-hoc review within 48h

---

## 4. Privacy Rights (DPDP Act / GDPR aligned)

| Right | Implementation | SLO |
|---|---|---|
| Access | `GET /me/data` — full export (reports, tickets, notifications) | instant |
| Erasure | `DELETE /me/data` — PII tombstone; incident facts retained anonymized | 30 days |
| Consent | granular: alerts, analytics, research reuse; revocable | — |
| Purpose limitation | ticket data never reused for unrelated ML without consent/pseudonymization | enforced in pipelines |
| Breach process | detect→contain→notify (DSAI + affected users) | per statute |

*Data-sharing agreements between departments documented before pilot (06-P6 companion).*

---

## 5. AI Governance (the trust layer)

| Gate | Requirement |
|---|---|
| Registry | every model versioned in MLflow with MODEL_CARD (data, metrics, limits) |
| Pre-deploy | baseline + calibration + **fairness (ward gap <10%)** + latency gates (04 §5) |
| Shadow → canary → prod | with automatic rollback on drift/perf alarms |
| Explainability | XAI package mandatory on every recommendation (XAI feature coverage = 100%) |
| Human-in-the-loop | critical actions require named approver (never auto-execute in v1) |
| Fallback | degraded rules-only mode visible to operators (confidence + fallback flag) |
| Post-hoc | monthly false-positive review; outcome labels feed retraining; incident reports include model versions |
| External review | ethics review of citizen-impacting models before R3 (06-risk R5) |

---

## 6. Application & Infrastructure Security

- Gateway: rate limiting, WAF rules, schema validation, geo/abuse guards on citizen API
- Input hardening: file type/size limits, virus scan on media, OCR sandbox
- Dependencies: SCA in CI, image scanning (Trivy), pin + SBOM
- Network: zones (public/DMZ/platform/dept) with default-deny policies; no direct DB exposure
- Tenancy: namespace-per-department; resource quotas (noisy-neighbor isolation)
- Testing: threat model per core flow (report, approve, broadcast); annual pen-test before GA

---

## 7. Compliance Map

| Framework | How addressed |
|---|---|
| DPDP Act (India) | consent, purpose limit, erasure, breach process (§4) |
| GDPR (if applicable) | same controls + DPO export tooling |
| ISO 27001 (target R4) | ISMS: this doc + runbooks + access reviews + SOC dashboards |
| ISO 37120 / city KPIs | public dashboard indicators |
| Procurement rules | API-first, no lock-in, exportable data (differentiator vs vendors) |

---

## 8. Security Ownership

| Area | Owner |
|---|---|
| IAM/config/policies | Platform admin |
| Rules & SLA content | Dept admins |
| Model gates | ML lead + product |
| Approvals | OCC duty officers |
| Audit review | Auditor role (monthly) |
| Incident response | On-call runbook `SEC-IR-01` |
