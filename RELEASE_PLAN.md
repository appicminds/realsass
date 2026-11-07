# Release Plan — Mapping Whole Software → Releases

**Status:** Active release map (derived from `WHOLE_SOFTWARE_BUILD_PLAN.md`)  
**Date:** 07 November 2026 (Asia/Karachi)  
**Rule:** Releases **select** WBS tasks; they do not invent new product scope.

---

## 1. Release overview

| Release | Goal | WBS tasks (approx) | System tests |
|---|---|---|---|
| **R0** | Discovery + feasibility evidence; fund decision | **12** (spikes/design subset) | none (experiments SP-01…06) |
| **R1** | Design-partner pilot (1 company, 2 projects) | **48** | ST-A, ST-B, ST-C (pilot depth) |
| **R2** | Commercial core + production mobile | **+22** (shared) then **R2S +8** / **R2L +7** | ST-D, ST-E |
| **R3** | AI + depth modules | **+14** | ST-F (partial) |
| **R4** | Ecosystem | **+6** | ST-F (full) |
| **GTM** | Marketing site (optional parallel) | **subset of 18.4** | content QA only |

Task IDs below refer to `WHOLE_SOFTWARE_BUILD_PLAN.md`.  
Every included task still runs **P1→P5** (testing inside P4).

---

## 2. R0 — Discovery & feasibility

**Exit:** Sponsor go/no-go to fund R1. Failed experiment ⇒ remediate that area only.

### R0 included work (12 items)

| WBS | Work in R0 | Notes |
|---|---|---|
| 1.1–1.5 | Foundation skeleton | Repo, CI, sandbox, evidence template |
| 4.2 / 4.6 | Permission model design + negative test *design* | Full build in R1 |
| 5.4 | Country profile schema decision | Content packs later |
| 8.7 | Billing concurrency *spike* (SP-01) | Full billing in R1 |
| 11.1 | Metric dictionary draft | Implementation R1 |
| 12.1 | OpenAPI draft | Implement R1 |
| 13.3 / 13.8 | Offline spike (SP-02) + matrix draft | Full mobile R1 beta / R2 GA |
| 14.4 | Isolation *spike* (SP-03) | Full SaaS R2S |
| 15.1 / 15.3 | Install/restore *spike* (SP-04) | Full standalone R2L |
| 3.1 + 11.4 | Clickable admin/ops UX (SP-05) | Production UI R1 |
| 18.1 | Migration approach rehearsal design | Tooling R1 |
| GTM 18.4 | Optional 1-page demo ask only | Not required |

### R0 experiments (must evidence)
SP-01 Cost/billing · SP-02 Offline · SP-03 Isolation · SP-04 Deploy/recovery · SP-05 Usability · SP-06 Commercial

### R0 not started as product build
Steps 6–11 full modules, production mobile, SaaS billing, AI, portals.

---

## 3. R1 — Design-partner pilot

**Exit:** Two live projects, reconciled money, beta mobile, 4-week observation thresholds met.

### 3.1 R1 task list (48)

#### Foundation & access
| ID | Task | Priority |
|---|---|---|
| 1.1–1.5 | Program foundation (complete if not done in R0) | P0 |
| 2.1 | Platform Admin shell (minimal provision for pilot) | P0 |
| 2.2 | Provision pilot site (manual/assisted OK) | P0 |
| 3.1–3.3 | Company profile/country, users/roles, approvals | P0 |
| 3.4 | Module flags (hide unreleased) | P0 |
| 4.1–4.6 | Auth, permissions, field restrict, audit, files, security pack | P0 |
| 5.1–5.5 | Masters, cost codes, units/FX hooks, country model, imports | P0 |

#### Commercial spine (vertical slice — build in this order)
| Order | ID | Task |
|---|---|---|
| 1 | 6.1–6.5 | BOQ & contract |
| 2 | 7.1–7.2 | Daily report + evidence |
| 3 | 8.1–8.5 | Measurement → certificate → allocation → invoice link → retention/advance display |
| 4 | 11.1–11.5 | Cost metrics, snapshots, dashboards, workbench, reconcile tests |
| 5 | 9.1–9.4 | Change events |
| 6 | 10.1–10.5 | Procurement & stock (core) |
| 7 | 10.6–10.7 | Attendance + subcontract (minimal) |
| 8 | 7.3–7.7 | Drawings, RFI, submittal/inspection gates, lookahead/handover basics |

#### Platform wiring & mobile beta
| ID | Task | Priority |
|---|---|---|
| 12.1–12.5 | OpenAPI, outbox/events, ops web shell, a11y, contract tests | P0 |
| 13.1–13.6 | Mobile shell, auth/switch, lease/outbox, sync, capture, conflicts | P0 beta |
| 13.8 | Mobile test campaign (beta depth) | P0 |
| 18.1 | Migration tooling for pilot cutover | P0 |
| 18.3 | Thin training pack (EN) for pilot roles | P1 |
| ST-A, ST-B, ST-C | System test campaigns | P0 |

### 3.2 Explicitly out of R1
| ID | Deferred to |
|---|---|
| 2.3–2.5 full control-plane polish | R2S |
| 3.5–3.6 advanced integration/export admin | R2 |
| 8.6 collection worklists depth | R2 |
| 13.7 push | R2 |
| 14.* SaaS commercial lifecycle | R2S |
| 15.* standalone packaging GA | R2L |
| 16.* AI | R3 |
| 17.* CRM, lump-sum/milestone, payroll gen, portals, BIM | R3/R4 |
| 18.4 large marketing site | GTM |
| 18.5 store GA packs | R2 |

### 3.3 R1 definition of done
- Vertical path works: report → measure → certify → invoice allocation → cost A/C/U  
- Finance/QS signed opening balances + reconciliation  
- Beta iOS/Android: no silent draft loss in executed tests  
- Applicable UAT/exceptions evidence attached  
- Unreleased modules hidden in UI/offers  

---

## 4. R2 — Commercial core

Split into **shared core**, then **R2S** and/or **R2L**.

### 4.1 Shared R2 tasks (+22)

| ID | Task |
|---|---|
| 2.3–2.5 | Entitlements, support grants, control-plane isolation |
| 3.5–3.6 | Integrations console + company export admin |
| 8.6 | Collection worklists / receipt allocation depth |
| 13.7 | Push (or documented inbox-only mode) |
| 13.1–13.8 | Mobile production hardening (complete remaining P4/P5 to GA bar) |
| 18.2 | Load/chaos/restore drills at GA depth |
| 18.3 | KB + help expansion |
| 18.5 | App Store / Play release packs |
| 18.6 | Production readiness checklist (shared parts) |
| ST-D | Mobile production system test |

### 4.2 R2S — SaaS (+8)

| ID | Task |
|---|---|
| 14.1–14.5 | Trial/provision/subscribe, billing webhooks, lifecycle, isolation load, offboarding |
| 18.6 | SaaS-specific readiness evidence |
| ST-E | Portability prep side (export) |

### 4.3 R2L — Standalone (+7)

| ID | Task |
|---|---|
| 15.1–15.5 | Package, license online/offline, backup/upgrade/rehost, portability, OSS fulfillment |
| 18.6 | Standalone-specific readiness evidence |
| ST-E | Full portability both ways before dual-mode claim |

### 4.4 R2 rules
- Either mode may launch when **shared + that mode** pass  
- **Dual-mode GA** only after ST-E both directions  
- Do not advertise unqualified “SaaS + standalone” before that  

---

## 5. R3 — Intelligence & depth (+14)

| ID | Task | Gate |
|---|---|---|
| 16.1–16.6 | AI infra + invoice + voice + assistant + BOQ/contract assist + eval harness | EVAL-01…06 |
| 17.1 | CRM | UAT CRM |
| 17.2 | Lump-sum & milestone billing | V3-03 / BILL-09 R3 |
| 17.3 | Native payroll generation | LABOUR-05 |
| 17.4 | Advanced ops analytics | separate acceptance |
| ST-F | Partial regression including AI safety | required |

**Rule:** Core ERP remains usable with AI fully down.

---

## 6. R4 — Ecosystem (+6)

| ID | Task |
|---|---|
| 17.5 | Client/subcontractor portals |
| 17.6 | BIM / telemetry / advanced adapters |
| Remaining 17.4 depth if deferred | as funded |
| Air-gapped / local AI options | separately qualified |
| ST-F | Full program regression |

---

## 7. GTM — Marketing website (optional parallel)

| Phase | Scope | When |
|---|---|---|
| GTM-0 | Home, Product, Deployments, Trust, Request demo | With R0/R1 recruiting |
| GTM-1 | Features deep-dives, pricing/contact, legal | With R2 launch |
| GTM-2 | Case studies, blog/SEO, locales | Post-R2 |

Maps to WBS **18.4** only. Does not gate R1 engineering.

---

## 8. Dependency graph (critical path)

```text
R0 evidence
  └─► R1 foundations (1,2min,3,4,5,12)
        └─► R1 spine (6 → 7.1-2 → 8 → 11 → 9 → 10 → 7.3-7)
              └─► R1 mobile beta (13) + migration (18.1)
                    └─► R1 live pilot
                          └─► R2 shared mobile/ops hardening
                                ├─► R2S (14)
                                └─► R2L (15)
                                      └─► dual-mode if both + portability
                                            └─► R3 (16,17.1-4)
                                                  └─► R4 (17.5-6)
```

---

## 9. What we start now (execution kickoff)

### This week — R0 start checklist
1. Appoint owners: sponsor, finance/QS, tech lead, mobile lead, QA  
2. Create evidence register (sheet or issues) with VAL/SP/UAT IDs  
3. Execute WBS **1.1–1.5** (repo, CI, pinned ERP sandbox, app skeleton)  
4. Schedule VAL-01 interviews; collect sanitized BOQ/cost/billing samples  
5. Queue SP-01 and SP-05 first; SP-02 when devices ready  
6. Decide GTM-0 yes/no for partner recruiting  

### First engineering build order after R0 pass
1. Tasks **4 + 5 + 3** (security, masters, company admin)  
2. Tasks **6 → 8 → 11** (BOQ → bill → cost)  
3. Tasks **7.1–7.2 + 13** (site report + mobile beta)  
4. Tasks **9 + 10** (change + procurement)  
5. ST-B then pilot cutover (**18.1**)

---

## 10. Counts at a glance

| Release | Tasks targeted | Phases (×5) |
|---|---|---|
| R0 | 12 (spike/design-weighted) | ~60 |
| R1 | 48 | 240 |
| R2 shared | 22 | 110 |
| R2S | 8 | 40 |
| R2L | 7 | 35 |
| R3 | 14 | 70 |
| R4 | 6 | 30 |
| GTM | 1 task, 3 content phases | — |

Some R0 items are partial precursors of the same WBS IDs fully accepted in R1/R2—do not double-count effort blindly; use the WBS task once for “done,” R0 for evidence only where noted.

---

## 11. Document control

| Doc | Role |
|---|---|
| `WHOLE_SOFTWARE_BUILD_PLAN.md` | Full software inventory (18/96/5) |
| `RELEASE_PLAN.md` | This file — which tasks ship when |
| `DEVELOPMENT_PLAN.md` | Narrative program notes (reconciled by this map) |
| PRD v4.1 | Requirements & acceptance authority |

**Next after kickoff:** open tracker issues/epics for R0 checklist items 1–6 and start Step 1 foundation tasks.
