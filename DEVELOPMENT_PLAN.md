# Construction Intelligence Platform — Full Development Plan

> **Reconciliation notice (see `CIP_PLAN_RECONCILIATION.md`):** PRD v4.0 governs; v4.1 changes are proposed amendments PA-01…PA-11 and are not approved. Open items in this plan: R2 English/Urdu field navigation, RTL and field guides are required by v4.0 (D-06); admin roles are conflated (D-07); `DEC-10` is plan-local (D-11); R1 build order differs from RELEASE_PLAN (D-13). The body of this file is otherwise unchanged.

**Status:** Working plan aligned to PRD v4.1  
**Product:** International construction ERP (SaaS + standalone) with web, iOS, and Android  
**Foundation:** ERPNext / Frappe + version-controlled construction app + optional isolated AI  
**Date:** 07 November 2026 (Asia/Karachi)

This plan turns the PRD into an executable delivery program. It does **not** replace the PRD. Where they differ, update both with a recorded decision.

---

## 1. Outcome and non-negotiables

### 1.1 Primary outcome
Give mid-size building contractors earlier visibility and control of **project margin and cash exposure** through a traceable path:

**Site evidence → change/cost exposure → verified measurement → certification → billing → collection**, with reconciled actual/commitment/ETC cost.

### 1.2 Non-negotiables (every release)
- Deterministic money, quantities, and authorization (AI never posts or invents fiscal policy)
- Human approval + append-only audit for financial effects
- Tenant isolation; no cross-company leakage via files, search, jobs, cache, or mobile
- Idempotent posting; no duplicate invoice allocation or silent quantity overwrite
- Offline mobile = drafts/observations only; no offline financial/safety release authority
- International core + **country/jurisdiction packs** (no single-country hardcoding)
- Three access planes: **Platform Admin**, **Company Admin**, **Company Employee/Operations**

### 1.3 What “done” means for the first commercial product
A customer can run BOQ remeasurement projects on web + production mobile, reconcile cost and billing, and buy either **SaaS (R2S)** or **standalone (R2L)** with tested export/portability. Dual-mode GA requires both.

---

## 2. Product surfaces

| Surface | Purpose | Who |
|---|---|---|
| **Desktop / web — Platform Admin** | Provision orgs/deployments, entitlements, licensing, health, backups, support grants | Vendor (SaaS) or installation admin (standalone) |
| **Desktop / web — Company Admin** | Country profile, users/roles/projects, policies, modules, integrations, audit | Org admin / ERP admin |
| **Desktop / web — Employee/Operations** | Commercial, procurement, finance Desk, dashboards, site/commercial workbench | Owner, Finance, QS, PM, Procurement, Accountant, etc. |
| **Native iOS / Android** | Field capture, evidence, limited review/approvals online, sync centre | Supervisors + entitled ops roles |
| **Optional GTM website** | Public education, pricing narrative, demo request | Prospects (not in PRD core; see §8) |
| **Knowledge base / in-product help** | Post-signup support content | Paying customers / trial users |

**Rule:** One business API and one permission model. Mobile and web never implement divergent financial rules.

---

## 3. Program structure

```text
R0 Discovery & feasibility     → fund only this until evidence passes
R1 Design-partner pilot        → 1 legal entity, 2 projects, beta mobile
R2 Commercial core             → R2S SaaS and/or R2L standalone + production mobile
R3 Intelligence & depth        → AI modules, CRM, payroll gen, extra billing strategies
R4 Ecosystem                   → portals, BIM/telemetry, advanced integrations, air-gap options
GTM (parallel, optional)       → marketing site + content (does not gate R1)
```

**Funding rule:** A calendar timebox ending does **not** prove feasibility. Failed mode-specific experiments limit funding to remediation for that mode.

---

## 4. Workstreams (standing teams)

| ID | Workstream | Owns | Primary artifacts |
|---|---|---|---|
| W1 | Product / BA / QS-finance SME | Scope, fixtures, acceptance, country-pack rules | Requirement IDs, metric dictionary, UAT fixtures |
| W2 | ERP / domain (Frappe app) | DocTypes, hooks, invariants, Desk finance paths | Construction app, migrations, event outbox |
| W3 | Web operations UI | Employee + commercial Vue (or chosen) UI | Screens UX-01…, approval inbox, workbench |
| W4 | Control plane | SaaS tenancy, entitlements, standalone license tooling | Provisioning jobs, admin consoles |
| W5 | Mobile | iOS/Android, offline lease, sync, evidence upload | App trains, MAPI contracts |
| W6 | Platform / DevOps / security | Envs, CI, backups, restore drills, SBOM | Staging/prod, runbooks |
| W7 | QA | SP experiments, UAT, device matrix, regression | Evidence packs |
| W8 | Implementation / support | Migration, training, pilot ops | Cutover checklists, KB |
| W9 | Commercial / GTM | Packaging, quotes, optional marketing site | Offers, demo funnel |

One person may cover multiple streams early; finance approval and security sign-off stay independent.

---

## 5. Phase plans

### 5.1 R0 — Discovery and feasibility (bounded)

**Goal:** Decide whether to fund the full build, with evidence—not optimism.

#### R0 exit gate (all required)
- [ ] VAL-01 / VAL-02 customer discovery recorded in evidence register
- [ ] Section 13.6 ERP fit matrix on **pinned** ERPNext/Frappe versions
- [ ] SP-01…SP-06 executed with pass/fail and remediation notes
- [ ] Finance-approved worked examples (A/C/U, retention, certificate→invoice)
- [ ] OSS/license disposition path for standalone proprietary packaging (DEC-04)
- [ ] Mobile framework spike decision (Flutter candidate vs RN alternative)
- [ ] Bottom-up work-package estimate for R1 (and rough R2 bands)
- [ ] Named owners for sponsor, finance/QS, tech lead, mobile lead, QA

#### R0 work packages

| WP | Deliverable | Owner stream | Depends on |
|---|---|---|---|
| R0-01 | Prospect list + 12 role sessions + evidence register | W1 / W9 | Access to contractors |
| R0-02 | Sanitized BOQ, cost, certificate, invoice samples | W1 | Pilot prospects |
| R0-03 | Pinned sandbox ERP + construction app skeleton | W2 / W6 | Repo, versions |
| R0-04 | SP-01 cost & billing concurrency | W2 / W7 | R0-03, fixtures |
| R0-05 | SP-02 offline durability (iPhone + low-end Android) | W5 / W7 | Framework spike |
| R0-06 | SP-03 tenant isolation attacks | W2 / W6 / W7 | Multi-site setup |
| R0-07 | SP-04 install/restore/portability feasibility | W4 / W6 / W7 | Packaging draft |
| R0-08 | SP-05 usability (5 supervisors, 3 QS/finance) | W3 / W5 / W1 | Clickable flows |
| R0-09 | SP-06 commercial packaging & cost worksheet | W9 | Discovery notes |
| R0-10 | Country profile + access-plane IA decision | W1 / W3 / W4 | PRD §3.0 / §4.1 |
| R0-11 | OpenAPI + mobile sync draft contracts | W2 / W5 | Domain list |
| R0-12 | R1 backlog, staffing, critical path | All leads | Experiments |

#### R0 architecture decisions to lock
1. ERPNext/Frappe versions + extension strategy (no unjustified core forks)
2. Tenant model: site/DB per customer (default)
3. Web UI split: Desk for finance/admin vs focused ops UI
4. Mobile framework + supported device matrix draft
5. Country profile schema (currency, tax templates, fiscal calendar, TZ, ID types, locale)
6. Metric dictionary v1 (`metric_version`, `as_of`, A/C/U/ETC/EAC rules)

**R0 out of scope:** production customers, AI GA, full marketing site, multi-entity consolidation.

---

### 5.2 R1 — Design-partner pilot

**Goal:** Prove the spine on **one legal entity, two projects**, BOQ remeasurement, one approved accounting policy, beta iOS/Android capture. Not a public launch.

#### Vertical slice (build in this order)
1. Identity: tenant → company (country profile) → users/roles → project/site entitlements  
2. Platform Admin minimal + Company Admin (users, roles, country settings)  
3. Project master, cost codes, BOQ import/versioning  
4. Site daily report + evidence (web + beta mobile drafts)  
5. Measurement verification  
6. Change event (execution vs commercial states)  
7. Certificate → billing allocation → draft/posted invoice link  
8. Procurement path: requisition → PO → receipt → invoice/stock consumption (policy-correct)  
9. Cost snapshot A / C / U / ETC / EAC with drill-down  
10. Migration rehearsal + opening balance sign-off  
11. Four operating weeks observation against §1.4 thresholds  

#### R1 module checklist (P0)

| Domain | Must ship | Explicitly defer |
|---|---|---|
| Commercial | BOQ, measurement, certificate, remeasurement billing, retention/advance display | Lump-sum / milestone strategies |
| Cost | Actual, commitment, manual ETC, forecast snapshot | Predictive ML costing |
| Procurement | Req, recorded quote compare, PO, receipt, issue | Automated RFQ campaigns |
| Site/docs | Diary, photos, RFI link, drawings, essential submittal/inspection gates, simple lookahead, handover checklist | Advanced scheduling, permit engine |
| Labour | Worker ref + attendance observation; external payroll import controls | Payroll generation |
| AI | Rules-based budget alerts only | Invoice AI, voice, assistant |
| Mobile | Beta diary/evidence/drawings/inspection drafts + sync centre | Full production offline matrix sign-off |
| CRM / sales | Direct customer/project entry | CRM-01…03 automation |

#### R1 engineering backlog (epics)

**E1 — Platform foundations**
- Auth, MFA for privileged roles, audit event model
- Permission intersection enforcement (API, Desk, jobs, files)
- Idempotency keys + optimistic versions
- Transactional outbox for domain events
- File upload initiate/resume with tenant scope

**E2 — Company & access planes**
- Company Admin: invitations, roles, project assignment, country profile
- Platform Admin (minimal): provision pilot site, entitlement stub, support grant
- Employee role homepages and approval inbox

**E3 — Commercial spine**
- Construction Contract, BOQ Version/Line, Measured Work, Certificate/Line, Billing Allocation
- BILL-09…11 reservation invariants (remeasurement)
- Change Event DocTypes + transitions

**E4 — Procurement & cost**
- Native ERP purchasing/stock configuration + custom links
- Material issue / transfer rules (no double cost)
- Forecast Snapshot service + MET-01 dictionary

**E5 — Site & documents**
- Daily report uniqueness (tenant/project/site/date/shift/unit)
- Drawing revision + stale warnings
- Submittal/inspection gates that block certification/release where configured

**E6 — Mobile beta**
- Capabilities, device registration, offline lease, bootstrap/changes/operations
- Encrypted outbox; conflict UX for quantities (no last-write-wins)
- English UI; locale hook ready

**E7 — Pilot operations**
- Staging rehearsal, migration scripts, training guides (EN)
- Telemetry events from PRD (no money from analytics)
- Defect triage + weekly pilot review

#### R1 acceptance pack
- Applicable UAT-01…08, 12–13, 15 (manual forecast), 16
- Applicable Appendix A exceptions for shipped capabilities
- V3-01, V3-02, V3-04, V3-06, V3-17 (beta)
- Finance/QS sign-off on opening balances and reconciliation
- Zero unexplained control-total differences

#### R1 success thresholds (observe ≥4 weeks)
- Financial integrity: full reconcile; every pilot certificate/invoice allocation verified
- Site adoption: ≥90% scheduled reports accepted next business day
- Field usability: median report ≤3 minutes; users understand draft vs accepted
- Billing readiness: measure eligibility→submission delay vs baseline (25% target is hypothesis)
- Reliability: no unresolved critical/high access defects; no silent draft loss in tests

---

### 5.3 R2 — Commercial release

**Goal:** Sell the validated core with production mobile. Launch **R2S** and **R2L** independently; claim both only after portability both ways.

#### Shared R2 core (before either mode launch)
- Production iOS/Android on published device matrix
- Full SYNC-01…08 / MSEC / MTEST gates
- Hardened permissions, ASVS/MASVS evidence pack (risk-based)
- Export schemas + customer exit path
- Support tiers, runbooks, on-call
- Product schedule stating exact mode differences
- Localization: English GA; additional locale packs as entitlements

#### R2S — SaaS launch extras
- Control plane separate from customer data planes
- Idempotent provisioning; tenant status lifecycle
- Isolation + noisy-neighbor load test (≥10 tenants including heavy importer)
- Invoice-based subscription + entitlement revisions (card checkout optional)
- Grace/restriction policy for nonpayment without data wipe
- Offboarding export window + deletion/retention honesty

#### R2L — Standalone launch extras
- Reproducible installer/package, health checks, backup/restore scripts
- Online + offline signed license activation
- Upgrade preflight + recovery path from supported N-1
- Customer ops guide; shared-responsibility matrix
- OSS notices / corresponding-source fulfillment as required
- VPN/private CA mobile connectivity tested

#### R2 exit gate
- Shared core + mobile acceptance signed
- Mode-specific V3-07…V3-16 / V3-18…V3-24 as applicable
- Measured RPO/RTO published for contracted infra
- Commercial terms, support hours, pricing decision (DEC-07) accepted
- No open P0 on isolation, duplicate money effects, or unowned recovery

---

### 5.4 R3 — Intelligence and depth

Ship only behind evaluation gates; core ERP must work with AI fully down.

| Capability | Gate |
|---|---|
| Invoice extraction → reviewed draft | EVAL-02; no auto-post |
| Voice diary (locale pairs) | EVAL-03; null unknowns |
| Owner/PM assistant | EVAL-04; tool allowlist only |
| BOQ/contract review assist | EVAL-05; reviewer sign-off |
| Forecast narratives / scenarios | EVAL-06; deterministic fixtures first |
| CRM-01…03, LABOUR-03/05 payroll gen | Separate UAT + policy |
| Lump-sum / milestone billing | BILL-09 R3 fixtures (e.g. V3-03) |

---

### 5.5 R4 — Ecosystem
Client/subcontractor portals, BIM/telemetry, advanced integrations, qualified air-gapped mobile/local AI. Each item needs paying-customer evidence and support model before roadmap commitment.

---

## 6. Technical blueprint (implementation shape)

### 6.1 Recommended system map
```text
[Platform Admin / License control plane]
              │ provisions / entitlements
              ▼
[Customer Frappe site / DB] ── native ERPNext (GL, buy/sell, stock, project dims)
              │
              ├── Construction app (custom DocTypes + domain services)
              ├── Ops web UI (commercial/site)
              ├── Mobile API (capabilities, lease, sync, operations)
              ├── Files / search / queues (tenant-tagged)
              └── AI workers (optional, isolated, draft-only outputs)
```

### 6.2 Core custom entities (build early)
Construction Contract, BOQ Version/Line, Budget Cost Code, Site Daily Report, Measured Work, Change Event, Certificate/Line, Billing Allocation, Retention Schedule, Work Package, Location, Drawing Revision, Submittal, Inspection, Forecast Snapshot/Line, Alert Action, Approval & Audit Event, AI Job/Extraction (R3).

### 6.3 API / event discipline
- Authenticated identity; server-side scope; `schemaVersion`, `correlationId`, `Idempotency-Key`
- Money as decimal strings; RFC3339 UTC timestamps; local work dates separate
- Domain events via transactional outbox (`project.created`, `measurement.certified`, `certificate.approved`, …)
- OpenAPI + sync schemas version-controlled **before** broad client work

### 6.4 Environments
| Env | Use |
|---|---|
| Dev | Engineers; synthetic data |
| Staging | Rehearsal, UAT, restore drills; sanitized fixtures |
| Pilot / Prod | Design partner then GA; backups + monitoring |

CI: lint, unit, permission negative tests, migration smoke, mobile contract tests, dependency/SBOM scan.

---

## 7. Delivery sequence (first 90 engineering days after R0 pass)

Illustrative critical path once R0 is funded—adjust to actual capacity; do not treat as a calendar promise.

| Band | Focus | Tangible demo |
|---|---|---|
| Days 1–15 | Foundations, company/project, permissions, BOQ import | Admin creates company + project + BOQ |
| Days 16–30 | Daily report web + evidence + measurement | Supervisor→QS verified qty |
| Days 31–45 | Certificate + invoice allocation + cost snapshot | Eligible bill + A/C/U view |
| Days 46–60 | Procurement/stock path + change events | PO→receipt→cost correct |
| Days 61–75 | Mobile beta sync + conflict/lease tests | Airplane-mode diary survives |
| Days 76–90 | Migration rehearsal, hardening, pilot readiness review | Finance sign-off dry-run |

Then: controlled live pilot → four-week measurement → R2 hardening.

---

## 8. Marketing website (GTM track — optional, not PRD core)

The ERP PRD does **not** require a large multi-page marketing site for R1. Commercially it only requires lead/demo/trial intake and later a knowledge base.

### 8.1 Recommendation
Run GTM in parallel without blocking the pilot.

| Stage | Site scope | Purpose |
|---|---|---|
| **GTM-0** (with R0/R1) | 3–5 pages: Home, Product, Deployments (SaaS/Standalone), Security summary, Request demo | Recruit design partners |
| **GTM-1** (with R2) | + Features deep-dives, Pricing or “Talk to us”, Resources/KB teaser, Legal (privacy/terms) | Support launch |
| **GTM-2** (post-R2) | Case studies, blog/SEO, locale landing pages, partner page, comparison pages | Scale inbound |

### 8.2 GTM-0 page list (minimum viable marketing)
1. Home — problem, outcome, CTA  
2. Product — evidence→billing spine, roles, mobile  
3. Deployments — SaaS vs standalone  
4. Trust — isolation, audit, offline limits (honest)  
5. Request demo — form → CRM/sales pipeline (can be spreadsheet initially)  

### 8.3 Explicit non-goals for GTM-0
Self-serve signup/checkout, localized SEO empire, fake ROI calculators, claiming dual-mode GA before gates pass.

---

## 9. Staffing model (minimum credible)

| Role | R0 | R1 | R2 |
|---|---|---|---|
| Product sponsor | Required | Required | Required |
| Finance/QS SME | Part-time | Part-time | As needed |
| Product/BA | 1 | 1 | 1 |
| ERP/backend engineers | 1–2 | 2–3 | 3+ |
| Web UI | 0.5–1 | 1–2 | 1–2 |
| Mobile | 1 | 1–2 | 2 |
| QA | 0.5–1 | 1–2 | 2 |
| DevOps/security | 0.5 | 1 | 1–2 |
| Implementation/support | 0.5 | 1 | 1–2 |
| Commercial/GTM | 0.5 | 0.5–1 | 1 |

Exact numbers follow the R0 bottom-up estimate. Do not start R1 without named finance/QS acceptance ownership.

---

## 10. Quality, security, and evidence

### 10.1 Evidence register
Every VAL/SP/UAT/V3 item: ID, method, sample, result, contrary evidence, attachments, owner, reviewer, status (`NOT STARTED`…`PASS` / `FAIL` / `ACCEPTED SCOPE DEFERRAL`).

### 10.2 Regression spine (always green before pilot expand / GA)
- Allocation concurrency (BILL-10/11)
- Permission negatives across API, Desk, import, job, file URL
- Mobile airplane-mode + two-device conflict + identity switch
- Backup/restore ledger + files + keys alignment
- Tenant isolation smoke

### 10.3 Security baseline
MFA for privileged roles, TLS, secrets management, encrypted backups, upload controls, field restrictions for government IDs/bank data, customer-visible support access audit.

---

## 11. Commercial packaging (to validate, not invent prices)

| Offer | When sellable | Includes |
|---|---|---|
| SaaS Core | After R2S gates | Hosted org, declared capacity, core workflows, mobile, assisted onboarding priced separately |
| Standalone annual / perpetual version | After R2L + license review | Customer-hosted core; maintenance/support separate; infra customer-funded unless managed |
| Country pack | After jurisdiction content exists | Tax/ID/templates/locale for that country |
| AI add-on | After each EVAL gate | Metered; manual fallback required |
| Operations Plus / Enterprise options | R3/R4 | Advanced planning/analytics, extra entities, SSO, portals, etc. |

Security, audit, export, and correct accounting are **never** premium-only safety features.

---

## 12. Risk register (top)

| Risk | Impact | Mitigation |
|---|---|---|
| ERP cost fields ≠ PRD EAC | Wrong margins | Custom projection + SP-01; never sum native fields blindly |
| Permission bypass paths in Frappe | Data leak | SP-03; review `get_all` / ignore_permissions |
| Offline sync duplicates | Bad billing inputs | Operation IDs + business uniqueness + conflict UX |
| OSS/GPL packaging conflict | Block standalone SKU | DEC-04 before sale; counsel review |
| Scope creep (AI, CRM, multi-entity) | Missed pilot | R3/R4 parking lot; vertical slice rule |
| Marketing overclaim | Trust/legal | Gate dual-mode and AI claims on evidence |
| Single-country assumptions | Rework | Country profile from R0; beachhead ≠ product limit |

---

## 13. Decision checklist (from PRD DEC-*)

| ID | Decision | Needed by |
|---|---|---|
| DEC-01 | Segment / beachhead countries | R0 |
| DEC-02 | Financial policy examples | Before live pilot |
| DEC-03 | ERP versions + infra | R0 design; reconfirm GA |
| DEC-04 | License/OSS distribution | Before standalone sale |
| DEC-05 | Mobile framework + matrix | R0 select; R2 production |
| DEC-06 | Technical/safety ownership | Before R1 |
| DEC-07 | Pricing & support | Before mode launch |
| DEC-08 | Funding beyond R0 | After R0 evidence |
| DEC-09 | Mode rollout order (SaaS vs standalone first) | Before sales promises |
| DEC-10 | GTM website scope (this plan) | Optional; choose GTM-0 before partner recruiting at scale |

---

## 14. Immediate next actions (start here)

1. Appoint sponsor, finance/QS lead, tech lead, mobile lead, QA owner.  
2. Open evidence register (spreadsheet or issue tracker) with VAL/SP IDs.  
3. Stand up pinned ERPNext/Frappe sandbox + empty construction app repo layout.  
4. Schedule discovery interviews; collect sanitized BOQ/cost/billing samples.  
5. Run SP-01 and SP-05 first (money truth + usability); parallelize SP-02 when devices ready.  
6. Confirm whether **GTM-0 marketing site** is in or out for partner recruiting.  
7. After R0 pass, fund R1 vertical slice only—no horizontal module sprawl.

---

## 15. Document control

| Doc | Role |
|---|---|
| `Construction_AI_ERP_Focused_Scope_PRD_v4.1.docx` | Requirements & acceptance authority |
| `DEVELOPMENT_PLAN.md` (this file) | Delivery program, sequencing, workstreams |
| Evidence register (to create) | Proof of VAL/SP/UAT/V3 |
| OpenAPI / sync schemas (to create) | Implementation contracts |
| Product schedule / terms (at R2) | What is sold vs operated |

**Change rule:** Financial definitions, billing allocation, permissions, or release scope changes need a versioned PRD amendment plus impact review on this plan.

---

## 16. One-page summary

We build an **international** construction ERP on **ERPNext/Frappe**, with **web admin/ops** and **native mobile field clients**, sold as **SaaS and/or standalone**.  

We fund **R0 evidence** first; then a **pilot vertical slice** (evidence→cost→bill); then **production mobile + mode launch**; then AI/depth; then ecosystem.  

A **large marketing website is optional GTM**, not required to prove the ERP—start with a thin demo site if needed, expand at R2.  

Success is **reconciled money + adopted field reporting**, not feature count.
