# Whole Software Build Plan (WBS)

**Purpose:** Inventory and structure the **entire software** to build, independent of release cuts.  
**Next step (later):** Map this WBS onto releases (R0/R1/R2…).  
**Authority:** PRD v4.1 + this WBS.  
**Date:** 07 November 2026 (Asia/Karachi)

---

## How to read this plan

| Level | Meaning |
|---|---|
| **Step** | Major software area of the whole product |
| **Task** | A buildable work item inside a step |
| **Phase** | Same 5 phases for **every** task (includes testing) |

### Standard phases inside every task (5)

| Phase | Name | Includes |
|---|---|---|
| **P1** | Analysis & design | Requirements trace, UX/API/data design, fixtures, threats |
| **P2** | Implementation | Code, DocTypes, UI, mobile screens, scripts |
| **P3** | Integration | Wire to ERP/API/events/files/other modules |
| **P4** | Testing | Unit, integration, permission negatives, UAT/fixtures, device/regression as applicable |
| **P5** | Fix, document & accept | Defects, runbooks/help, owner sign-off, evidence register |

**Rule:** A task is not complete until **P5 acceptance** is recorded. Testing is never a separate afterthought step—it is **Phase 4 of every task**, plus cross-step system test in Step 18.

---

## Totals (whole software)

| Item | Count |
|---|---|
| **Steps** | **18** |
| **Tasks** | **96** |
| **Phases per task** | **5** |
| **Total task-phases** | **96 × 5 = 480** |
| **Plus program-level system test campaigns** | **6** (listed under Step 18) |

This is the **full product vision** (core + AI + ecosystem + GTM + ops). It is **not** “done after 6 release steps.” Releases will later select subsets of these tasks.

---

## STEP 1 — Program setup & engineering foundation  
**Tasks: 5**

| ID | Task |
|---|---|
| 1.1 | Repos, monorepo/app layout, branching, code owners |
| 1.2 | Dev / staging environments, secrets, CI pipelines |
| 1.3 | Pinned ERPNext/Frappe versions + construction app skeleton |
| 1.4 | Coding standards, SBOM, dependency/license scanning |
| 1.5 | Evidence register + requirements-to-test traceability template |

Each task → P1–P5.

---

## STEP 2 — Platform Admin plane (vendor / installation)  
**Tasks: 5**

| ID | Task |
|---|---|
| 2.1 | Platform Admin console shell & navigation |
| 2.2 | Organization / deployment provisioning jobs |
| 2.3 | Entitlements, modules, capacity meters |
| 2.4 | Support break-glass grants + customer-visible audit |
| 2.5 | Health, metering metadata, control-plane isolation from project ledger |

---

## STEP 3 — Company Admin plane  
**Tasks: 6**

| ID | Task |
|---|---|
| 3.1 | Company profile & country/jurisdiction settings |
| 3.2 | User invite, roles, project entitlements |
| 3.3 | Approval policies & delegation |
| 3.4 | Module configuration & feature flags |
| 3.5 | Integration settings console (credentials, mappings) |
| 3.6 | Company audit / export admin tools |

---

## STEP 4 — Identity, security & permissions core  
**Tasks: 6**

| ID | Task |
|---|---|
| 4.1 | Auth (SSO/password), MFA for privileged roles, sessions |
| 4.2 | Permission engine (tenant ∩ company ∩ role ∩ project ∩ doc ∩ state) |
| 4.3 | Field-level restrictions (gov ID, bank, payroll) |
| 4.4 | Append-only audit events + tamper-aware export |
| 4.5 | File authorization / short-lived scoped links |
| 4.6 | Security test pack (ASVS-oriented negatives, IDOR, export denial) |

---

## STEP 5 — Masters: project, sites, cost codes, country packs  
**Tasks: 5**

| ID | Task |
|---|---|
| 5.1 | Project / site / location / work package masters |
| 5.2 | Cost codes & budget versions |
| 5.3 | Units, conversions, currencies, FX policy hooks |
| 5.4 | Country pack content model (tax/retention templates, ID types, locale) |
| 5.5 | Master-data import validation & history |

---

## STEP 6 — BOQ, contract baseline & estimating import  
**Tasks: 5**

| ID | Task |
|---|---|
| 6.1 | BOQ version/line DocTypes + immutable identities |
| 6.2 | Contract baseline (signed value, retention rules, variations link) |
| 6.3 | Approved estimate import & revision diffs |
| 6.4 | BOQ web UI (ops) + Desk admin paths |
| 6.5 | BOQ exception tests (duplicates, units, concurrency, billed-line removal) |

---

## STEP 7 — Site execution & document control  
**Tasks: 7**

| ID | Task |
|---|---|
| 7.1 | Daily diary / site report workflow |
| 7.2 | Photos & evidence pipeline (hash, retain original) |
| 7.3 | Drawings & revision/supersede |
| 7.4 | RFI workflow + change-candidate link |
| 7.5 | Submittals & technical release gates |
| 7.6 | Inspections / NCR / quality gates |
| 7.7 | Lookahead (basic), handover checklist, transmittals/outputs |

---

## STEP 8 — Measurement, certificates, billing & collection  
**Tasks: 7**

| ID | Task |
|---|---|
| 8.1 | Measurement draft→verify workflow |
| 8.2 | Certificates & cumulative qty rules |
| 8.3 | Billing allocations (reserve/consume/release) + idempotency |
| 8.4 | Remeasurement invoice draft → ERP sales invoice link |
| 8.5 | Retention, advances, deductions display & balances |
| 8.6 | Receipts allocation & collection worklists |
| 8.7 | Billing concurrency / correction / period-lock tests (UAT spine) |

---

## STEP 9 — Change events & commercial recovery  
**Tasks: 4**

| ID | Task |
|---|---|
| 9.1 | Change event model (execution vs commercial states) |
| 9.2 | Assessment, at-risk spend caps, variation baseline update |
| 9.3 | Notice/follow-up & exposure dashboard |
| 9.4 | Change acceptance tests (partial approve, replay, disputed remainder) |

---

## STEP 10 — Procurement, inventory, labour & subcontracts  
**Tasks: 7**

| ID | Task |
|---|---|
| 10.1 | Requisition → approval |
| 10.2 | Supplier quotes comparison (manual/recorded) |
| 10.3 | PO, commitments, amendments, cancel remaining |
| 10.4 | Receiving, tolerances, three-way / service certification rules |
| 10.5 | Stock transfer vs consumption (no double cost) |
| 10.6 | Worker registry + attendance (non-payroll) + external payroll import controls |
| 10.7 | Subcontract work orders, certification, retention |

---

## STEP 11 — Cost engine, forecasts & executive reporting  
**Tasks: 5**

| ID | Task |
|---|---|
| 11.1 | Metric dictionary (A, C, U, ETC, EAC, margin, certified, billed, revenue) |
| 11.2 | Forecast snapshots (immutable) + incompleteness labelling |
| 11.3 | Owner / project dashboards with drill-down |
| 11.4 | Commercial workbench & approval inbox UX |
| 11.5 | Reporting reconciliation tests (fixture totals = drill-down) |

---

## STEP 12 — Domain API, events & web operations UI shell  
**Tasks: 5**

| ID | Task |
|---|---|
| 12.1 | Versioned OpenAPI for domain routes |
| 12.2 | Transactional outbox + domain event consumers |
| 12.3 | Ops web app shell (nav, states: loading/empty/denied/conflict) |
| 12.4 | Accessibility baseline (WCAG-oriented custom screens) |
| 12.5 | API contract tests & schema compatibility checks |

---

## STEP 13 — Native mobile apps & offline sync  
**Tasks: 8**

| ID | Task |
|---|---|
| 13.1 | App shell (Today/Projects/Capture/Inbox/More) iOS+Android |
| 13.2 | Auth, device registration, org/server switch isolation |
| 13.3 | Offline lease + encrypted local DB/outbox |
| 13.4 | Bootstrap / changes pull / operations push |
| 13.5 | Diary, camera/evidence, drawings, inspection drafts |
| 13.6 | Sync centre + conflict UX (no silent qty LWW) |
| 13.7 | Push notifications (or inbox fallback) |
| 13.8 | Device-matrix mobile test campaign (airplane, conflict, revoke, storage) |

---

## STEP 14 — SaaS commercial lifecycle  
**Tasks: 5**

| ID | Task |
|---|---|
| 14.1 | Trial/lead → provision → activate subscription |
| 14.2 | Billing records, webhooks, upgrades/downgrades |
| 14.3 | Grace/restrict/export-only/close lifecycle |
| 14.4 | Multi-tenant isolation & noisy-neighbor load tests |
| 14.5 | Customer offboarding export + deletion/retention evidence |

---

## STEP 15 — Standalone packaging, licensing & portability  
**Tasks: 5**

| ID | Task |
|---|---|
| 15.1 | Installer/package, manifests, health checks |
| 15.2 | Online + offline license activation |
| 15.3 | Backup/restore/upgrade/rehost tooling |
| 15.4 | SaaS↔standalone portability transfer |
| 15.5 | OSS notice/source fulfillment & license compliance review support |

---

## STEP 16 — AI services (optional modules)  
**Tasks: 6**

| ID | Task |
|---|---|
| 16.1 | Isolated AI worker infra (quotas, timeouts, audit, tenant cache) |
| 16.2 | Invoice extraction → human review → draft bill |
| 16.3 | Voice/diary transcription (locale pairs) |
| 16.4 | Read-only owner/PM assistant |
| 16.5 | BOQ compare / contract review assist |
| 16.6 | AI evaluation harness + safety tests (injection, revoke, no auto-post) |

---

## STEP 17 — Later product depth & ecosystem  
**Tasks: 6**

| ID | Task |
|---|---|
| 17.1 | CRM lead/follow-up/quotation |
| 17.2 | Lump-sum & milestone billing strategies |
| 17.3 | Native payroll generation (beyond import) |
| 17.4 | Advanced planning/productivity/quality analytics |
| 17.5 | Client/subcontractor portals |
| 17.6 | BIM/telemetry/external adapters |

---

## STEP 18 — Cross-cutting QA, migration, GTM site & enablement  
**Tasks: 6** (+ 6 system-test campaigns)

### Tasks
| ID | Task |
|---|---|
| 18.1 | Data migration tooling & cutover runbooks |
| 18.2 | Performance/load & chaos/recovery drills |
| 18.3 | Knowledge base + in-product help + training packs |
| 18.4 | Marketing website (Home, Product, Deployments, Trust, Demo, later SEO pages) |
| 18.5 | Store release packs (iOS/Android) + privacy disclosures |
| 18.6 | Production readiness checklist & dual-mode GA evidence pack |

### Program-level system test campaigns (after groups of steps)
| Campaign | Covers |
|---|---|
| ST-A | Foundations + admin + permissions |
| ST-B | Commercial spine (BOQ→bill→cost) |
| ST-C | Procurement + change + site/docs |
| ST-D | Mobile offline production matrix |
| ST-E | SaaS + standalone + portability |
| ST-F | AI + later depth + full regression |

Each campaign also uses design → execute → defect → retest → accept (same 5-phase discipline).

---

## Count summary by step

| Step | Name | Tasks |
|---|---|---|
| 1 | Program setup & foundation | 5 |
| 2 | Platform Admin | 5 |
| 3 | Company Admin | 6 |
| 4 | Identity & security | 6 |
| 5 | Masters & country packs | 5 |
| 6 | BOQ & contract | 5 |
| 7 | Site & documents | 7 |
| 8 | Measurement & billing | 7 |
| 9 | Change events | 4 |
| 10 | Procurement / labour / subcontract | 7 |
| 11 | Cost & reporting | 5 |
| 12 | API, events & web shell | 5 |
| 13 | Native mobile & sync | 8 |
| 14 | SaaS lifecycle | 5 |
| 15 | Standalone & portability | 5 |
| 16 | AI modules | 6 |
| 17 | Later depth & ecosystem | 6 |
| 18 | QA/migration/GTM/enablement | 6 |
| **Total** | | **96** |

**Phases:** 96 tasks × 5 phases = **480 task-phases**  
**+** 6 system-test campaigns × 5 = **30** campaign-phases  
**Grand total planning units:** **510**

---

## What is intentionally not “extra steps”

These are **phases inside tasks**, not separate steps:
- Unit testing  
- Integration testing  
- UAT / fixtures  
- Security negatives  
- Device/matrix testing  
- Performance testing  
- Documentation & acceptance  

---

## Next planning action (your request order)

1. **Now (done in this file):** whole software WBS = 18 steps / 96 tasks / 5 phases each  
2. **Next (when you say so):** release plan that **selects and sequences** these tasks into R0 / R1 / R2 / R3 / R4 / GTM without inventing a second scope  

---

## Document control

| Doc | Role |
|---|---|
| `Construction_AI_ERP_Focused_Scope_PRD_v4.1.docx` | Requirements authority |
| `WHOLE_SOFTWARE_BUILD_PLAN.md` | Full software WBS (this file) |
| `DEVELOPMENT_PLAN.md` | Earlier release-oriented program notes (to be reconciled after release mapping) |
