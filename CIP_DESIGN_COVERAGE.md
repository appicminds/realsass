# CIP Design Coverage

**Status:** Review draft for sponsor. This is an inventory of what must be designed. It is not a claim that any of it is designed.
**Governing source:** PRD v4.0. v4.1 additions are proposals (`PA-01…PA-11`, see `CIP_PLAN_RECONCILIATION.md` §2).
**Companion documents:** `CIP_PLAN_RECONCILIATION.md`, `CIP_DESIGN_SEQUENCE.md`.

A menu label, a summary card or an unconnected button is **not** a completed workflow. Every row below is a workflow with an entry point, an outcome, the screens it needs and the checks that prove it. Where the PRD gives no rule, the row says **UNRESOLVED**. No rule is invented.

---

## 1. How to read this file

### 1.1 Status values (honest scale)

| Status | Meaning |
|---|---|
| **missing** | No screen exists for this workflow. |
| **partial** | One or more existing Figma frames touch it, but the workflow is incomplete or defective. A single frame is never "designed". |
| **designed** | All required screens and alternate states exist, with correct vocabulary, and have passed design review. |
| **prototype-verified** | A clickable prototype of the full path passed the stated acceptance checks with an observer. |

Current result: **0 workflows are designed and 0 are prototype-verified.** The 13 existing frames make some workflows **partial**.

### 1.2 Legends

**Implementation class:** `DESK` = reuse ERPNext Desk. `CFG` = native workflow configured, thin UI. `CUS` = custom operations screen on the web. `MOB` = native mobile. `NON` = no UI.
**Mode:** `B` = SaaS and standalone. `S` = SaaS only. `L` = standalone only.
**Device:** `D` desktop, `T` tablet, `P` phone. The first letter is primary. A device not listed is not planned for that workflow. Browser-responsive layouts are a fallback for light capture only (v4.1 §3.0, consistent with `MOB-01`).
**Personas (PRD §5 and `COM-05`):**
`OWN` owner, `FIN` finance manager, `ACC` accountant, `OPS` operations manager, `PM` project manager, `QS` quantity surveyor, `PRO` procurement, `SUP` site supervisor, `ERPA` ERP administrator, `ORGA` customer organization administrator, `BILA` customer billing administrator, `VOPS` vendor platform operations, `VBIL` vendor billing staff, `INST` standalone installation administrator *(proposed term)*.
Safety owner, document controller and QA inspector are **not named roles in the PRD** (§5). They are **UNRESOLVED** (`DEC-06`).
**Release and priority:** taken from the PRD tag. "R1 P0 (§6)" means a core functional requirement. §6 says core functions are R1 P0 within the §2 package.
**Evidence tests:** only `UAT-01…16`, `V3-01…24`, `SP-01…06` and `DEC-01…09` that exist in the PRD are cited.

### 1.3 States every screen must specify (`UX-09`, `MOB`)

Loading, empty, filtered-empty, validation, denied, stale/conflict, offline, partial upload, expired session and success. Each row lists the **notable** states. A row never excuses the full set. Mobile targets are 44px. WCAG 2.2 AA applies to custom screens.

### 1.4 Global constraints that apply to every row

1. **No offline financial approval, certification, posting or safety release.** Offline mobile creates drafts and observations only (§10.2, `MOB-S08`, `SAFE-02`).
2. **No approval through administrator access.** Admin roles configure. They do not approve money (`APR-04`, `COM-05`).
3. **Every approval binds a document revision and a policy version.** A stale action returns a conflict with a refresh path (`UX-08`, `APR-02`).
4. **No invented tax defaults, approval thresholds or accounting policy.** Fields stay empty or labelled sample until finance supplies and approves them (`DEC-02`, `APR-01`).
5. **Draft is visibly a draft.** Claimed amounts are never labelled certified (`OUT-01`, §4.2).
6. **Release and entitlement are visible.** Modules not yet released do not appear as available (§17.2). A disabled capability shows its reason and a manual alternative (`PAR-02`).

---

## 2. ERPNext Desk reuse, configured native workflow, or custom operations screen

PRD §12.1 proposes: "ERPNext Desk for back-office administration and finance where suitable, with a focused Vue operations interface for site and commercial tasks. Validate representative screens". PRD §13.1 says ERPNext/Frappe owns masters, authoritative transactions, ledgers and standard workflows, and the construction app owns custom linked records. **This is a proposal to validate in R0, not a settled decision** (reconciliation decision 13). The default is **do not rebuild native ERP screens.**

| Area | Default | Why | Design consequence |
|---|---|---|---|
| General ledger, tax, journals, bank reconciliation | **DESK** | `FIN-01`: use ERPNext for GL, tax, sales/purchase invoices and bank reconciliation | Design only entry links, control totals and reconciliation status inside the ops UI. |
| Sales invoice posting, receipts, credit notes, payment entries | **DESK** | `FIN-01`, `FIN-03` | Ops UI creates the draft and links to Desk. Desk posts. |
| Customer, supplier, item masters, stock entries, warehouses | **DESK** | §13.1: native masters, finance, stock | Link only. |
| Purchase order, receipt, purchase invoice | **DESK or CFG** with custom links | §13.1, `PROC-03/04` | Custom screen for the approval step, matching view and commitments register. Desk keeps the document itself. |
| Approval workflows | **CFG** plus a custom approval inbox | `APR-02`, `UX-08` | Inbox and review pane are custom. Rules are configured. |
| BOQ, contract baseline, change event, measurement, certificate, billing allocation | **CUS** | §13.1: construction app linked DocTypes | Fully designed here. |
| Daily report, drawings, RFI, submittal, inspection, NCR, lookahead, safety record | **CUS** (web) and **MOB** | §13.1, `MOB-S04…S07` | Fully designed here. |
| Forecast snapshot, owner dashboard, alerts, commercial workbench | **CUS** | §13.1: deterministic service, `UX-01/07` | Fully designed here. |
| User and role administration | **CUS** over native permissions | `COM-05`, `ENG-02` | Custom admin shell. Enforcement stays backend. |
| Tenant provisioning, entitlement, licence tooling | **CUS** (control plane) | §18 | Separate from the ledger (`TEN-03`). |
| Native mobile apps | **MOB** | `MOB-01` | Designed as a separate surface, not responsive web. |

---

## 3. Workflow inventory

Columns: **ID · workflow · class** | **PRD · release/priority · depends on** | **Persona · scope · mode · device** | **Entry → outcome** | **Required screens, drawers, dialogs, output previews** | **Actions, state transitions, evidence · financial/authorization constraints** | **Figma nodes · status · acceptance checks**.

### 3.A Vendor control plane (SaaS only)

Vendor operations and vendor billing staff work on **metadata only**. They see no project ledger or payroll by default (`TEN-03`). Entitlement mutations are web-only. Standalone customers have no vendor control plane. Their equivalent is the installation console (3.D).

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-PLT-01** Provision organization or deployment · CUS | `TEN-01/02`, `V3-07` · R2 P0 (R1 assisted, §2.2) · WF-CAD-02, WF-PLT-02 | VOPS · metadata only · S · D | Tenants → New organization → provisioning job → organization ready, first admin invited | Tenants list. New-organization wizard (verification evidence, plan and entitlements, region **UNRESOLVED**). Provisioning job detail (step log, retry, partial-failure recovery). Invitation-sent confirmation. | Idempotent job with operation key. Partial failure leaves a recoverable state. Cleanup only of verified orphans. Never show credentials. All actions audited. · No project or payroll data visible. | `10651:2571` (list only) · **partial** · `V3-07` yields one usable site. Failed step shows recovery action. |
| **WF-PLT-02** Entitlements, modules, capacity · CUS | `COM-03/04`, `BIZ-02` · R2 P0 · WF-PLT-01 | VOPS, VBIL · S · D (web-only, PA-04) | Organization → Entitlements → new revision | Entitlement revision editor (modules, active projects, named back-office users, storage, validity, policy revision). Diff against current. Effective-date dialog. Downgrade-below-usage warning. | Immutable revisions. Show capacity impact. Never delete users or projects automatically. · Field participation is a declared envelope, not seats. | none · **missing** · `V3-09` versioned entitlement. Downgrade shows affected capacity. |
| **WF-PLT-03** Support access grant and break-glass · CUS | `TEN-03` · R2 P0 · WF-CAD-06 | VOPS requests, customer approves · S · D | Organization → Support access → request | Request dialog (purpose, scope, duration). Customer approval state. Active grants with expiry. Break-glass dialog with stronger approval. Customer-visible audit trail. | Time-limited, purpose-bound, logged. No standing access. · Customer sees every access event. | `10651:2571` shows a KPI tile only · **missing** · Expired grant denies access. Trail visible to customer. |
| **WF-PLT-04** Fleet health, metering metadata, incidents · CUS | `TEN-03`, `COM-04`, `NFR-03` · R2 P0 | VOPS · S · D | Platform health → tenant → metric | Fleet overview. Tenant health detail. Usage/metering reconciliation. Incident list. Stale-data banner. | Usage events reference organization, meter, quantity, period, reconciliation state. Duplicates cannot double-bill. · Metadata only. | `10651:2571` KPI summary · **partial** · Every figure shows as-of time. No project data. |
| **WF-PLT-05** Release channel and version policy · CUS | `DEP-05`, `MAPI-02` · R2 P0 | VOPS · S, and publishes packages for L · D | Releases | Release list with supported-version dates. Staged-rollout state. App/server compatibility matrix. | Staged deployment. Routine end-of-support notice of at least 90 days (proposed). | none · **missing** · Unsupported version blocks unsafe writes. |
| **WF-PLT-06** Vendor billing operations · CUS | `BIZ-01/02`, `COM-04`, `V3-09` · R2 P0 | VBIL · S · D | Billing → subscription → payment verification | Subscription record. Invoice and payment reference. Webhook exception queue. Manual payment confirmation. Credits and amendments. | Webhooks authenticated and deduplicated. Verify payment state before activation. Manual confirmation needs authorized finance review. | none · **missing** · `V3-09` replay gives one effect. |
| **WF-PLT-07** Restrict, export-only, close and delete a tenant · CUS | `BIZ-03`, `TEN-04`, `V3-10`, `V3-15` · R2 P0 | VOPS, VBIL · S · D | Organization → Lifecycle | Lifecycle timeline (active, grace, restricted, export-only, closed). Export-window dialog. Retention and legal-hold check. Deletion plan. Completion record. | 30-day grace is **proposed**. Read, export and correction routes stay. A control-plane outage must not disable an active tenant. Completion record states backup limits. | none · **missing** · `V3-10`, `V3-15`. |

### 3.B Customer organization administration

`ORGA` and `ERPA` configure. They do not approve finance (`COM-05`, `APR-04`). Mutations to country profile, entitlements and licensing are **web-only** (PA-04, proposed).

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-CAD-00** Company admin landing · CUS | none (navigation) | ORGA · B · D | Sign in → admin home | Home with admin items only (pending invites, module setup, audit alerts). | Not a workflow. Must not host approvals or operational health. | `10623:841` · **partial** · No financial approval item appears (E-05). |
| **WF-CAD-01** Company profile and country/jurisdiction profile · CFG, CUS | `PA-02` (proposed), §4.1, `SEC-03` · R1 (model decision R0) | ORGA, ERPA, finance review · B · D (web-only) | Settings → Company and country | Company profile form. Country profile editor (currency, tax and retention templates, fiscal calendar, timezone, locale, ID types). Availability badge (Architecture-ready, Pack available, Validated at launch). Unconfigured state. Review-status panel. | Effective-dated changes, audited. · Templates reviewed by finance before activation. **No default rates.** `DEC-01/02`. | `10651:2351` · **partial** · No unreviewed rate shown as fact (E-08). |
| **WF-CAD-02** Users, invitations, roles, project entitlements · CUS | `COM-05`, §5, `ENG-05` · R1 P0 | ORGA, ERPA · B · D | Users and roles → invite, edit role, assign projects | User table. Invite drawer. Role editor (all §5 roles). Project entitlement matrix. SoD conflict panel. Deactivate dialog (open work, approvals). Pending invites. | Roles never grant finance rights through an admin menu. SoD conflict blocks save. Deactivation reassigns open items. Audited. · No implicit finance authority. | `10651:2129` · **partial** · SoD conflict cannot be saved. Seat rule defined (decision 11). |
| **WF-CAD-03** Approval policy and delegation rules · CFG, CUS | `APR-01/03` · R1 P0 | Author **UNRESOLVED** (decision 8), ERPA configures · B · D | Settings → Approval policy | Policy list. Policy editor (type, value, project, budget exception, effective date). Version diff. Activation dialog. Impact preview. | Effective-dated. Version bound to approvals. · **Thresholds not pre-filled.** Owner approval does not bypass SoD. | none · **missing** · `UAT-07`. |
| **WF-CAD-04** Modules and feature availability · CUS | `COM-03`, `PAR-02`, WBS 3.4 · R1/R2 | ORGA · B · D | Settings → Modules | Module list with entitlement state. Disabled-with-reason and manual alternative. Unreleased modules hidden. | Unreleased modules not offered (§17.2). | none · **missing** · No hidden module reachable by URL. |
| **WF-CAD-05** Integration console · CUS | `INT-01`, `PAR-02` · R2 P0 | ORGA, ERPA · B · D | Settings → Integrations | Integration list (last success, backlog, failure reason, impact, mapping version). Credential dialog (write-only). Mapping editor. Retry. | Secrets never displayed. · A failed integration must not make financial records inaccessible. | none · **missing** |
| **WF-CAD-06** Audit, retention, legal hold · CUS | `SEC-02/03` · R1 P0 | ORGA, auditor view · B · D | Settings → Audit | Event table with filters. Detail drawer (actor, effective role, action, entity and revision, time). Retention schedule editor. Legal-hold dialog. Authorized export. | Append-only. · Government/tax IDs and bank details not shown in lists. | none · **missing** · Unauthorized export denied. |
| **WF-CAD-07** Security, sessions, devices · CUS | `SEC-01`, `MOB-S10`, `V3-19` · R1/R2 | ORGA, ERPA · B · D | Settings → Security and devices | MFA policy for privileged roles. SSO setup (R2 option). Sessions and devices list. Revoke-device dialog. | Revocation applies at lease expiry and on reconnect. | none · **missing** · `V3-19`. |
| **WF-CAD-08** Company data export · CUS | `INT-02`, `TEN-04` · R2 P0 | ORGA · B · D | Settings → Export | Export request (scope). Job status. Manifest preview. Expiring secure download. | Async, expiring, authorization re-checked at download. | none · **missing** · `V3-15` (SaaS exit). |

### 3.C Customer subscription and billing administration (SaaS)

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-BIL-01** Subscription and invoices · CUS | `COM-05`, `BIZ-01` · R2 P0 | BILA · S · D | Subscription → overview | Plan and capacity overview. Invoice list. Contact editor. Payment reference. | · No payroll or project data access. | none · **missing** |
| **WF-BIL-02** Plan change and capacity planning · CUS | `BIZ-02` · R2 P0 | BILA, ORGA · S · D | Subscription → change plan | Change dialog with effective date and affected capacity. Archive or reduction plan. | Never delete history automatically. | none · **missing** |
| **WF-BIL-03** Grace and restriction notices · CUS | `BIZ-03` · R2 P0 | BILA, all users see banner · S · D, P | Banner → details | Grace banner. Restricted-create states in business screens. Read and export remain. | Proposed 30-day grace. Support route stays. | none · **missing** · `V3-10`. |

### 3.D Standalone installation administration (customer-operated)

The **customer** runs this console (`DEP-03`). It is not the vendor control plane.

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-STD-01** Prerequisites, install, health · CUS or CLI | `DEP-01/02` · R2 P0 | INST · L · D | Installation → Health | Prerequisite checklist (DNS, HTTPS, firewall, email, time sync, identity provider, push, backup destination, key custody). Install progress. Health dashboard. | Pinned manifests. Kubernetes not mandated. Egress-restricted mode disables cloud features visibly. | none · **missing** · `SP-04`, `V3-12`. |
| **WF-STD-02** Licence activation and renewal · CUS | `LIC-01…05` · R2 P0 | INST · L · D | Licence → activate | Online activation. Offline challenge/response. Licence detail (term or perpetual, modules, capacity, maintenance). Reminder, grace and restriction states. Clock-tamper support-review state. | Signed payload verified locally. Restrictions only where licensing permits. Read and export stay. | none · **missing** · `V3-11`, `V3-12`. |
| **WF-STD-03** Maintenance and upgrade · CUS | `LIC-02`, `DEP-04/05` · R2 P0 | INST · L · D | Upgrade → preflight | Preflight results. Backup verification. Maintenance mode. Staged migration progress. Reconciliation results. Abort and recovery points. | No blind snapshot rollback after new writes. | none · **missing** · `V3-13`. |
| **WF-STD-04** Backup, restore, rehost, disaster recovery · CUS | `DEP-03`, `LIC-04`, `NFR-04` · R2 P0 | INST · L · D | Backups | Schedule and status. Restore wizard (database, files, keys aligned). Rehost or deactivate dialog. DR activation. RPO/RTO evidence. | Key custody. Licensed DR and non-production. | none · **missing** · `V3-16`. |
| **WF-STD-05** Mobile connectivity and push configuration · CUS | `DEP-02`, `PUSH-02`, `PAR-02` · R2 P0 | INST · L · D | Connectivity | HTTPS and VPN trust setup. QR/config generation for `MOB-S01`. Push transport choice. Disabled-with-reason list. | QR carries no secret. | none · **missing** · `V3-23`. |
| **WF-STD-06** Extensions and diagnostics · CUS | `DEP-06` · R2 P0 | INST · L · D | Extensions | Extension inventory. Compatibility results. Sanitized diagnostics export (voluntary). | Core forks unsupported. | none · **missing** |
| **WF-PORT-01** SaaS and standalone transfer · CUS | `PORT-01/02`, `V3-14` · R2 (dual-mode claim) | ORGA + VOPS (SaaS side) + INST (standalone side) · B · D | Export or import → Transfer | Transfer plan. Write freeze or delta capture. Reconciliation (counts, balances, hashes). Read-only validation on destination. Cutover acceptance. Old-endpoint block notice. | Secrets rotated, not copied. Source stays authority until cutover acceptance. | none · **missing** · `V3-14` in both directions. |
| **WF-LIC-01** OSS notices and source offer · NON, About page | `LIC-06/07` · R2 P0 | all · B · D | About → Licences | Notices page. Source-offer text. | Counsel review. | none · **missing** |

### 3.E Role home, approvals, shared

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-CMN-01** Sign-in, MFA, expired session, denied · CUS, MOB | `SEC-01`, `UX-09` · R1 P0 | all · B · D, T, P | Open app → home | Sign-in. MFA challenge. Expired-session dialog that keeps form state. Denied page. | MFA for privileged roles. No privileged key in clients. | none · **missing** |
| **WF-CMN-02** Shared state patterns · design-system spec | `UX-09` · R1 P0 | none | n/a | State kit for the ten states. Status chips. Number formats. | Not a workflow. A component specification. | none · **missing** |
| **WF-CMN-03** Help, support intake, onboarding · CUS | `GROW-03` · R2 P0 | all · B · D | Help → request | In-product help. Support request with severity and impact. Sandbox examples. | Retain export route. | none · **missing** |
| **WF-ROL-01** Role home and work queue · CUS | `UX-02/03` · R1 P0 · all queues | PM, QS, FIN, PRO, SUP · B · D, P | Sign in → home | Home per role: "needs your action" queue, each item with owner, next action, deadline. Assigned projects. | Items open real workflows with a return path. · Only permitted items. | `10651:1245` · **partial** · Each queue item opens its target (E-04). |
| **WF-APR-01** Approval inbox and decision review · CUS | `UX-08`, `APR-02/03/04` · R1 P0 | Approvers per §5 · B · D, with online-only P (`MOB-S08`) | Inbox → item → decision | Master list (filters: type, project, amount, age). Detail pane: amount, budget impact, changed fields against prior revision, policy version, evidence, prior decisions. Decision dialog. Stale-conflict state with refresh. Self-approval block. Re-authentication for high-risk actions. | Approve, reject, return. Binds revision and policy. Stale action returns conflict. · No self-approval. No admin authority. Nothing queued offline. | `10651:1908` · **partial** · `UAT-07`, `V3-06`. |
| **WF-APR-02** User delegation · CUS | `APR-03` · R1 P0 | any approver · B · D, P | Profile → Delegation | Delegation dialog (scope, period, value limit, delegator). Active delegations. Split-request flag review. | Expiring. No self-approval even with several roles. | none · **missing** |

### 3.F Executive and project

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-OWN-01** Owner dashboard · CUS | `UX-01`, `MET-01` · R1 P0 | OWN · B · D, T | Home → dashboard | Contract value, actual cost, remaining commitments, incomplete forecasts, pending recovery, certification backlog, overdue receivables, retention, actionable approvals. Every number shows definition, period, currency, as-of time, drill-down. | Incomplete forecasts labelled. Missing ETC never zero. · **Cash surplus is never labelled profit.** | none · **missing** · Totals equal drill-down. |
| **WF-OWN-02** Metric drill-down and reconciliation · CUS | `MET-01`, `REP-01`, `FIN-06` · R1 P0 | OWN, FIN, PM · B · D | Metric → definition → source rows | Definition drawer (formula, statuses, tax and FX basis, cutoff, `metric_version`, `as_of`). Drill-down tables. Mixed-scope rejection state. Export preview. | Mixed scopes or periods rejected or separated. | none · **missing** · `UAT-01`. |
| **WF-OWN-03** Alerts and actions · CUS | `ALT-01` · R1 P0 | OWN, PM, FIN · B · D, P | Alerts → alert | Alert list. Detail (rule, entity, source revision, history). Acknowledge, assign, resolve, suppress-with-reason dialogs. | Acknowledgement does not clear a breach. Deduplicated. History kept. | none · **missing** |
| **WF-OWN-04** Forecast (A, C, U, ETC, EAC) and snapshot · CUS | `MET-02`, `UAT-01/15`, `V3-04` · R1 manual, R3 scenarios | PM and QS enter ETC. FIN reviews. OWN reads · B · D | Project → Forecast | A/C/U table with sources. ETC input editor per cost code. Completeness flags. Publish-snapshot dialog. Compare against prior snapshot and actuals. Variance. | **Forecast variance = approved budget − EAC.** Missing ETC never zero. Snapshots immutable. Pending recovery only in a labelled scenario. | `10645:477` · **partial** · `UAT-01`, `UAT-15`, `V3-04` (E-02). |
| **WF-PRJ-01** Project, site, location, work package setup · CUS + DESK | `PROJECT-01/02`, `ARC-03` · R1 P0 (§6) | PM, OPS, ERPA · B · D | Projects → new or edit | Project form (ID, location, manager, cost centre, client, dates, status). Site and location tree. Work-package list. Archive dialog. | Cannot archive with open liabilities without explicit resolution. | none · **missing** · `PROJECT-01` acceptance. |
| **WF-PRJ-02** Cost codes, budget versions, transfers · CUS + DESK | `FIN-02`, §4.2 · R1 P0 (§6) | FIN, PM · B · D | Project → Budget | Cost-code tree. Budget version list. Addition, reduction and transfer requests. Budget against committed and actual. | Transfers are authorized. Project and cost code mandatory on expense. | none · **missing** |
| **WF-PRJ-03** Project hub · CUS | `UX-02` · R1 P0 | PM, QS, FIN, OWN · B · D, T | Projects → project | Tabs: scope and BOQ, work packages, schedule, daily reports, materials, labour, commercial, documents. | Every tab opens a real workflow. | `10645:477` · **partial** · Every tab target exists in the prototype. |
| **WF-PRJ-04** Portfolio list · CUS | `UX-01/02` · R1 P0 | OPS, OWN, FIN · B · D | Projects | Portfolio table. Filters. Status definitions. Base-currency note. | One definition per status. | `10651:1466` · **partial** · Counts reconcile (E-03). |

### 3.G Contract and BOQ

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-BOQ-01** Contract baseline and billing configuration · CUS | `BOQ-03`, `BILL-01`, `BILL-09` · R1 P0 | QS, FIN · B · D | Project → Contract | Contract record: signed value with tax basis, milestones, retention rules, billing strategy, unit precision, certification authority, advance and deduction rules. Signed-document attachment. Lock confirmation. | Only a signed or authorized version affects the baseline. Strategy is immutable after first certification unless approved. | none · **missing** · `BOQ-03` acceptance. |
| **WF-BOQ-02** BOQ and estimate import and validation · CUS | `BOQ-01`, `EST-01`, `MIG-01` · R1 P0 | QS · B · D | BOQ → Import | Upload. Column mapping. Validation report (duplicates, unit conversions, missing cost-code mapping). Preview diff. Commit dialog. | Missing mapping or invalid units rejected. Decimal precision. | none · **missing** |
| **WF-BOQ-03** BOQ revisions, approval, diff, immutability · CUS | `BOQ-02`, Appendix A BOQ family · R1 P0 | QS submits, approver decides · B · D | BOQ → revisions | Revision list (draft, submitted, approved, superseded). Line grid. Baseline-against-current diff. Approval review. Billed-line removal blocked state. | Stable line IDs. Approved baseline cannot be edited in place. | none · **missing** |

### 3.H Site execution

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-SIT-01** Daily report entry and submit · CUS, MOB | `OPS-01`, `PROJECT-03`, `UX-03`, `MOB-S04` · R1 web, R1 beta and R2 mobile | SUP, assigned site · B · P, T, D | Today or Capture → Daily report → submit | Report form (project, site, date, shift, reporting unit, activities, quantities and units, manpower, material observations, blockers, evidence). Save-draft. Submit dialog. Duplicate or returned-report state. Validation. | One approved report per tenant, project, site, local date, shift, unit. Draft against accepted always visible. Client operation ID. Copied values marked. | `10645:1265` is a read-only summary · **partial** · `UAT-08`, `V3-17` (E-09). |
| **WF-SIT-02** Daily report review: accept, return, amend · CUS | `OPS-01` · R1 P0 | PM reviews, SUP amends · B · D, P | Review queue → report | Review pane (quantities against plan, evidence, changes since prior revision). Accept dialog. Return-with-reason dialog. Amendment as new revision. History. | A returned report is editable. Amendments create revisions. · Review is not a financial approval. | none · **missing** |
| **WF-SIT-03** Attendance and delivery observations · CUS, MOB | `LABOUR-02`, `MOB-03`, Appendix A LABOUR family · R1 P0 | SUP records, PM or QS verify · B · P, D | Capture → Attendance or Delivery | Roster draft. Overtime and shift. Delivery observation. Overlap exception state. | Nonbinding. No automatic payroll or stock. A worker cannot bill overlapping shifts without exception. | none · **missing** |
| **WF-SIT-04** Evidence capture, linking, retention · MOB, CUS | `OPS-01`, `SYNC-06`, `MOB-S05` · R1 beta, R2 | SUP, QS · B · P | Capture → Photo | Camera, audio, file capture. Annotation as a separate rendition. Link to BOQ item or work package. Upload progress. Camera-denied alternative. | Original and hash retained. Location metadata stripped unless consented. Partial upload resumes. | `10646:1322` · **partial** · `V3-21` (E-12). |
| **WF-SIT-05** Issues and blockers · CUS, MOB | `OPS-01`, `PLAN-01` · R1 P0. **UNRESOLVED:** no separate issue-register ID | SUP raises, PM resolves · B · P, D | Capture → Issue → raise to PM | Issue form. Assignment. Status. Link to lookahead constraint, RFI or change candidate. | Treated as report blockers. A standalone register is not in the PRD. | none · **missing** |
| **WF-SIT-06** Lookahead · CUS | `LOOK-01/02`, `PLAN-01` · R1 basic, R3 advanced | PM · B · D, T | Project → Lookahead | Two-to-six-week grid by site, location, trade. Constraint tracker (drawings, submittals, materials, labour, permits). Weekly commitments. Non-completion reasons. | Needed-by dates. Baseline and current preserved. | none · **missing** |

### 3.I Measurement to cash

Vocabulary follows `CIP_PLAN_RECONCILIATION.md` §6.2: observed progress, verified measurement, certified work, invoice eligibility, posted invoice, payment.

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-MSR-01** Measurement draft and submit · CUS, MOB draft | `PROJECT-04`, `BILL-02`, `MOB-03` · R1 P0 · WF-BOQ-03, WF-SIT-01 | QS (web), SUP or QS observation draft (mobile) · B · D, P | Measurement → new | Measurement sheet by BOQ or variation line (quantity, evidence, location, cumulative against allowable). Submit dialog. | Cumulative cannot exceed allowable without exception. Mobile is a draft only. | none · **missing** |
| **WF-MSR-02** Measurement verification: verify, return, supersede · CUS | `BILL-02` · R1 P0 | QS verifier · B · D | Review queue → measurement | Verification pane (observed against verified quantity, evidence viewer, variance reason). Verify, return, supersede dialogs. | Verified quantity is distinct from observed. Supersession keeps history. | none · **missing** |
| **WF-CRT-01** Certificate preparation · CUS | `BILL-02/04`, `OUT-01` · R1 P0 · WF-MSR-02 | QS prepares, FIN reviews · B · D | Commercial → Certificates → new | Certificate editor with **claimed, verified and certified columns**: gross work value, eligible variations, retention, advance recovery, other deductions, net. Certificate and running-bill preview. Submit dialog. | Draft shows "Claimed, not certified". Amounts come from verified measurement. **Does not reserve invoice quantity.** · Tax shown only from approved configuration. | `10645:1044` · **partial** · `UAT-04` (E-01). |
| **WF-CRT-02** Certificate approval, rejection, dispute, correction · CUS | `BILL-02`, `APR-02/03` · R1 P0 | Authorized certifier. QS cannot approve own · B · D | Approvals → certificate | Decision review (evidence, changed fields, policy, budget impact). Certify, part-certify, reject, dispute dialogs. Correction state. | Certified is revision-bound. Corrections go through credit and rebill. | none · **missing** · `UAT-05`. |
| **WF-INV-01** Invoice eligibility and reservation · CUS | `BILL-03/10/11`, `UAT-03` · R1 P0 · WF-CRT-02 | QS, FIN · B · D | Commercial → Eligibility | Per certificate line: net entitlement, posted, live reservations, remaining eligible. Reserve dialog with idempotency feedback. Release and cancel reservation. Stale or duplicate request state. | Posted + reserved + remaining = entitlement. A concurrent request cannot exceed it. A reservation is not an invoice. | `10645:1044` · **partial** · `UAT-03` (E-01). |
| **WF-INV-02** Invoice draft and ERP sales-invoice link · DESK + CUS | `BILL-03/04`, `FIN-03` · R1 P0 | FIN drafts and posts, QS verifies · B · D | Eligibility → create draft → Desk | Draft preview (net after retention, advance, deductions). Link to Sales Invoice in Desk. Posted-state return. Failure and retry state. | Idempotent conversion. Finance posts. | none · **missing** · `UAT-04`. |
| **WF-INV-03** Corrections: credit and rebill · CUS + DESK | `BILL-08`, `UAT-05`, `FIN-05` · R1 P0 | QS starts, FIN approves · B · D | Invoice → Correct | Correction request with reason. Effect preview (credit note plus rebill). Approval. Period-lock warning. | Old evidence kept. No silent rewrite. A locked period needs controlled reopen. | none · **missing** · `UAT-05`. |
| **WF-COL-01** Receipts and allocation · DESK + CUS | `BILL-05` · R1 P0 | FIN · B · D | Receipts → allocate | Receipt record (partial, on-account). Allocation to several invoices. Withholding evidence and classification dialog. | Allocations reconcile to payment. No unexplained write-off. | none · **missing** |
| **WF-COL-02** Collection worklists · CUS | `BILL-07` · R1 P0 | FIN, QS, PM · B · D | Collections | Four separate worklists: unpaid invoices, uncertified submissions, disputed amounts, overdue retention. Follow-up dialog. | Each row has owner and next action. Aging uses defined due dates. | none · **missing** |
| **WF-COL-03** Advances and recovery · DESK + CUS | `BILL-04`, `FIN-03` · R1 P0 | FIN · B · D | Advance → apply | Advance record. Recovery schedule on certificate. Balance. | Advance application not counted twice as revenue. | none · **missing** |
| **WF-RET-01** Customer retention schedule and release · CUS | `BILL-06`, `HAND-02` · R1 tracking, R2 defect-liability link | FIN, QS · B · D | Retention | Schedule by contract and certificate (held, eligible, requested, approved, invoiced, received). Release request and approval. Contract evidence. | Partial release cannot exceed eligible balance. Customer and supplier retention separate. Release conditions **UNRESOLVED** (decision 10). | none · **missing** |
| **WF-OUT-01** Output templates and preview · CUS | `OUT-01` R1, `OUT-02` R2 | role-dependent · B · D | Any document → Preview | Templates: PO, change request, measurement sheet, certificate, running bill, retention statement, RFI, submittal, transmittal, daily report, monthly progress report. Preview with draft marking, issuer, project, period, source revisions, approval status, attachment manifest. Issue and email authorization dialog (R2). | Draft is visibly draft. Approval is not a legal digital signature. Generating is not sending. | none · **missing** · `V3-05`. |

### 3.J Change events and commercial recovery

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-CHG-01** Change event intake · CUS | `CHG-01`, `RFI-01` · R1 P0 | PM, QS. SUP raises · B · D, P | Report, RFI or instruction → new change event | Intake form (source type, instruction date, project and location, description, evidence). Link to RFI or drawing. Execution and commercial state indicators. | Execution states are independent of commercial states. | none · **missing** |
| **WF-CHG-02** Assessment and exposure verification · CUS | `CHG-02` · R1 P0 | QS assesses, FIN or PM verifies, manager approves · B · D | Change → Assessment | Assessment editor (cost, time, at-risk spend cap). Verification. Approval. | At-risk spend within the cap. QS cannot approve own variation. | none · **missing** |
| **WF-CHG-03** Notice and follow-up · CUS | `CHG-04` · R1 P0 | QS, PM · B · D | Change → Notices | Notice due dates from contract. Evidence status. Responsible person. Reminders. Follow-up log. | Contract-configured due dates. | none · **missing** |
| **WF-CHG-04** Claim, response, baseline update · CUS | `CHG-03`, `BOQ-04`, `UAT-02` · R1 P0 | QS submits, manager approves · B · D | Change → Claim | Claim by revision (requested, approved, rejected, disputed amounts separate). Response entry. Partial approval. Baseline-update confirmation. | A replay increases the approved contract once. Disputed amount stays separate. Unapproved claim excluded from revised signed contract. | none · **missing** · `UAT-02`. |
| **WF-CHG-05** Closure and recovery view · CUS | `CHG-05`, `UX-07` · R1 P0, scenarios R3 | QS, FIN · B · D | Change → Close | Disposition. Remaining exposure. Rejected recovery keeps actual cost. Labelled recovery scenario. | Pending recovery stays outside A, C and U. | none · **missing** |
| **WF-CHG-06** Commercial workbench register · CUS | `UX-07` · R1 P0 | QS, FIN, PM · B · D | Commercial | Separate sections: change events, submitted claims, certificates, invoice eligibility, disputes, retention. Each row has owner, next action, deadline, evidence. | Register only. Each row opens its workflow. | `10645:1044` · **partial** · No section mixes certificate preparation with reservation (E-01). |

### 3.K Procurement and inventory

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-PRC-01** Requisition · CFG, CUS | `PROC-01`, `APR-02`, `MOB-03` · R1 P0 | SUP, PM request. PM approves within limit · B · P, D | Requisitions → new | Form (quantity, needed-by, inventory check, budget code). Duplicate-open warning. Submit. Returned state. | States: draft, submitted, returned, approved, rejected, cancelled. Revision-bound. | none · **missing** |
| **WF-PRC-02** Supplier quote comparison · CUS | `PROC-02`, `PROC-10` · R1 recorded | PRO · B · D | RFQ → compare | Quote entry. Comparison (equivalent scope, unit conversion, freight, tax basis, exclusions, warranty). Selection rationale. | A quote change cannot overwrite a signed selection. | none · **missing** |
| **WF-PRC-03** PO, commitments, amendments · CUS + DESK | `PROC-03`, `APR-02`, `UAT-07` · R1 P0 | PRO drafts, approver decides · B · D | PO → create, amend, cancel remaining | PO editor. Amendment revision diff. Approval review. Cancel-remaining dialog. Commitments register by cost code. | An approved PO reserves commitment. A change after approval invalidates approval. Cancel removes only unfulfilled quantity. | `10651:1687` · **partial** · `UAT-07` (E-13). |
| **WF-PRC-04** Supplier onboarding and bank verification · DESK + CFG | `PROC-09`, `APR-04` · R1 P0 | PRO requests, independent verifier · B · D | Suppliers → onboarding | Supplier form. Bank-detail change request. Independent verification step. Status. | Independent verification before payment eligibility. | none · **missing** |
| **WF-PRC-05** Receiving and discrepancy · CUS, MOB observation | `PROC-04/06/07` · R1 P0 | PRO, SUP observation · B · D, P | Receiving → PO → receive | Receipt entry (accept, reject, batch, discrepancy photo). Ordered, accepted, rejected, returned, invoiced, outstanding quantities. | No invoice match before accepted goods are recorded. | none · **missing** · `UAT-06`. |
| **WF-PRC-06** Invoice matching and duplicate detection · DESK + CUS | `PROC-06/09`, `UAT-06` · R1 P0 | ACC · B · D | Invoices → match | Matching view (PO, receipt, invoice, tolerance). Service invoice against certification. Duplicate warning with exception reason. | Duplicate key: tenant, company, supplier, normalized number, fiscal context, file fingerprint. | `10651:1687` "invoices to match" tile only · **missing** |
| **WF-PRC-07** Stock transfer, issue, consumption, returns · DESK | `PROC-05/08` · R1 P0 | PRO, storekeeper **UNRESOLVED role** · B · D | Stock → entry | Transfer. Issue and consumption with project and cost code. Return. | Transfers create no duplicate cost. Consumption follows approved policy. | none · **missing** · `UAT-06`. |
| **WF-PRC-08** Payment preparation, verification, authorization · DESK | `APR-04` · R1 P0 | ACC prepares, verifier, FIN authorizes · B · D | Payments | Three separate steps and states. | Separate actions. AI cannot execute. Admin has no implicit authority. | none · **missing** |

### 3.L Labour and subcontract

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-LAB-01** Worker registry · DESK, CUS | `LABOUR-01` · R1 minimal | PM, ACC · B · D | Workers | Worker record. Restricted fields (government ID, bank) hidden by role. Duplicate flag. | Privacy restrictions. Archived workers keep history. | none · **missing** |
| **WF-LAB-02** Attendance verification · CUS | `LABOUR-02` · R1 | PM verifies · B · D | Attendance review | Roster verification. Overlap exception. | No payroll calculation in R1. | none · **missing** |
| **WF-LAB-03** External payroll import · CUS + DESK | `LABOUR-05` R1 import controls | FIN · B · D | Import → batch | Batch upload. Source batch ID. Allocation totals. Duplicate protection. Reconciliation. | One controlled interface. Worker privacy. | none · **missing** |
| **WF-SUB-01** Subcontract work order · CUS | `LABOUR-06`, `LABOUR-04` · R1 P0 | PM, QS create. Approver decides · B · D | Subcontracts → new | Work order (unit-rate or milestone basis, scope ceiling, retention, deductions). Approval. Revision. | Scope ceiling enforced. | none · **missing** |
| **WF-SUB-02** Submission, verified quantity, certificate, payable · CUS | `LABOUR-06` · R1 P0 | QS verifies, certifier approves, ACC pays · B · D | Subcontracts → certification | Four separate states and screens: subcontractor submission, verified quantity, approved certificate, payable. Cumulative against ceiling. | The four are separate. A reversed certificate starts a correction document. | `10651:1687` subcontract tile only · **missing** |
| **WF-SUB-03** Variations, deductions, retention release, closeout · CUS | `LABOUR-06` · R1 P0 | QS, FIN · B · D | Subcontracts → variation or release | Variation and deduction dialogs. Retention release. Closeout summary. | Release cannot exceed eligible. Corrections via documents. | none · **missing** |

### 3.M Documents, quality, safety, closeout

Safety owner, document controller and QA inspector are **UNRESOLVED roles** (`DEC-06`).

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-DOC-01** Drawing register, revisions, supersede · CUS, MOB | `DOC-01/02`, `UAT-16`, `MOB-S06` · R1 P0 | PM. All read · B · D, T, P | Documents → Drawings | Register (discipline, number, revision, effective date, approval state). Revision upload. Supersede dialog. Stale warning on web and mobile. | Old revision marked superseded. A downloaded revision is labelled stale if freshness is unchecked. | none · **missing** · `UAT-16`. |
| **WF-DOC-02** RFI · CUS | `RFI-01`, `UAT-16` · R1 P0 | PM, SUP raise. Response recorded · B · D | RFI → new | Form (question, location, affected drawing, assignee, required-by, response, evidence). Link to change candidate with scope impact. | A response creates a linked change candidate. No automatic contract increase. | none · **missing** |
| **WF-DOC-03** Submittal register and review · CUS | `SUB-01/02/03`, `V3-01` · R1 P0 when contract requires | QS, PM. Reviewer · B · D | Submittals | Register. Review states. Gate indicator that blocks gated procurement or installation release. | Block applies on custom UI, Desk and API. | none · **missing** · `V3-01`. |
| **WF-DOC-04** Transmittals · CUS | `DOC-03`, `V3-05` · R1 build, R2 acceptance | PM · B · D | Transmittals → new | Document and revision selection. Recipients. Purpose. Issue confirmation. Access revocation. | Exact IDs and revisions kept as issued. | none · **missing** · `V3-05`. |
| **WF-QUA-01** Inspection and test plans, requests · CUS | `QUAL-02/03` · R1 P0 | QA authority **UNRESOLVED** · B · D | Plans → new | Versioned plan editor. Request and schedule. | Criteria supplied by authorized professionals. | none · **missing** |
| **WF-QUA-02** Inspection record and result · CUS, MOB | `QUAL-03`, `V3-02`, `MOB-S07` · R1 P0 | Inspector. PM and QS review · B · P, T, D | Capture → inspection | Checklist draft (offline, revision-bound). Evidence. Result. Gate effect on certification. Corrective closure. | A failed portion blocks certification per contract gate. A changed checklist on sync requires review. | none · **missing** · `V3-02`. |
| **WF-QUA-03** NCR and corrective action · CUS | `QUAL-01` · R1 P0 essential | QA, PM · B · D, P | NCR → new | Form (severity, responsible party). Corrective action. Verification. Closure. | Closure after verified correction. | none · **missing** |
| **WF-SAF-01** Safety record: hazard, near miss, incident reference · CUS, MOB | `SAFE-01`, `MOB-S07` · R1 P0 | SUP reports. Safety owner **UNRESOLVED** · B · P, D | Capture → Safety | Report form (severity, owner, corrective action, due date). Restricted injury details. Emergency guidance linking to the site procedure. Native-or-integration mode banner. | This app is not an emergency-response system. Offline reports stay pending. Personal details restricted. | none · **missing** |
| **WF-SAF-02** Corrective actions and verification · CUS | `SAFE-01` · R1 P0 | Safety owner · B · D, P | Safety → actions | Action tracker with verification. | Verification recorded. | none · **missing** |
| **WF-SAF-03** Toolbox talk, RAMS, permit status references · CUS | `SAFE-02` · R2 reference, R3 native permits | Safety authority · B · D, P | Safety → references | Status and reference records. No permit issuance in R2. | Financial or technical approval does not issue a permit. A local app cannot authorize gated work. | none · **missing** |
| **WF-EQP-01** Basic equipment records · CUS | `EQP-01` · R1 P1 | OPS · B · D | Equipment | Rental period, utilization, fuel, downtime with project cost. | Basic only. | none · **missing** |
| **WF-CLO-01** Handover checklist · CUS | `HAND-01` · R1 P0 baseline | PM · B · D, T | Project → Handover | Checklist per location and system. Partial handover scope and date. | Critical unresolved items block acceptance under policy. | none · **missing** |
| **WF-CLO-02** Defect liability and warranty · CUS | `HAND-02`, `PROJECT-05` · R2 P0 basic | PM, QS · B · D | Project → Defects | Defect register. Dates from contract triggers. Rectification. Independent verification. Retention link. | Retention release references handover and defect conditions. | none · **missing** |
| **WF-CLO-03** Project closeout and final bill · CUS | `PROJECT-05`, `PROJECT-01` · R1 P0 | PM, FIN · B · D | Project → Closeout | Closure gate list. Final bill link. Archive blocked by liabilities or critical punch items. | Closure blocked by unresolved critical items. | none · **missing** |

### 3.N Finance operations (mostly Desk)

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-FIN-01** Ledger, project attribution, reconciliation · DESK | `FIN-01/02/06`, `MET-01` · R1 P0 (§6) | FIN, ACC · B · D | Desk, plus a status view in the ops UI | Desk for GL, invoices, bank reconciliation. A reconciliation-status view with control totals. | Subledger matches GL. No AI-maintained balances. | none · **missing** |
| **WF-FIN-02** Site petty cash · DESK, CUS | `FIN-04`, Appendix A petty-cash exception · **UNRESOLVED release** (decision 6) | ACC, SUP · B · D, P | Petty cash → advance | Accountable advance. Receipts. Settlement. Approval. Duplicate-receipt flag. | An open advance stays visible until reconciled. | none · **missing** |
| **WF-FIN-03** Month close, period lock, controlled reopen · DESK | `FIN-05`, `UAT-05` · R1 P0 | FIN · B · D | Close | Close checklist. Exceptions. Lock. Reopen dialog with privileged approval. | Backdated documents need controlled reopen. | none · **missing** · `UAT-05`. |
| **WF-FIN-04** Financial reports: AR, AP, aging, retention, EAC · DESK, CUS | `FIN-06`, `REP-01` · R1 P0 | FIN, OWN · B · D | Reports | Report viewer with explicit filters and date definitions. Drill-down. Export authorization. | Total equals drill-down. | none · **missing** |
| **WF-FIN-05** Opening balances, migration reconciliation, sign-off · CUS | `MIG-01…04`, `UAT-12` · R1 P0 | FIN, QS sign. Implementation staff run · B · D | Migration → reconcile | Migration inventory. Staged-import validation. Reconciliation (trial balance, AP/AR, bank, stock, advances, retention, commitments). Sign-off dialog. Cutover and rollback authority page. | Invoiced work is not billable again. Finance and QS sign off. | none · **missing** · `UAT-12`. |

### 3.O Native mobile (iOS and Android)

Mobile hosts Employee/Operations only (PA-04, proposed). R1 is a beta of capture, drawings, inspection drafts and sync centre (§2.2). R2 expands to the §10 core roles. R1 is assumed to be a single organization (UNRESOLVED, reconciliation D-14).

| ID · workflow · class | PRD · rel · deps | Persona · scope · mode · device | Entry → outcome | Screens, drawers, dialogs, previews | Actions, states, evidence · constraints | Figma · status · acceptance |
|---|---|---|---|---|---|---|
| **WF-MOB-01** Organization connection · MOB | `MOB-S01`, `V3-20/23` · R2 P0 | all · B · P, T | Open app → connect | Choose SaaS organization or scan or enter standalone config. Verified hostname and organization before sign-in. Certificate failure state. | QR carries no secret. A credential is never redirected to a different server. | none · **missing** · `V3-20`, `V3-23`. |
| **WF-MOB-02** Sign-in, MFA, device registration, lease · MOB | `MOB-S02`, `SYNC-02`, `V3-19` · R1 beta | all · B · P, T | Connect → sign in | System-browser sign-in. MFA. Device name and consent. Lease issued, expiring, locked states. | No embedded privileged key. Signed scoped lease (24 hours, 72 maximum). | none · **missing** · `V3-19`. |
| **WF-MOB-03** Project pack and offline expiry · MOB | `MOB-S03`, `SYNC-01` · R1 beta | SUP, PM, QS · B · P, T | Projects → pack | Pack list (size, revision, last sync, expiry, quota). Module availability. | Downloads never imply offline approval authority. | none · **missing** |
| **WF-MOB-04** Today and primary navigation · MOB | `MOB-04` · R2 P0 (R1 beta subset) | all field roles · B · P | Open app → Today | Tabs Today, Projects, Capture, **Inbox**, More. Today shows tasks, overdue actions, sync status. | Labels finalized in usability testing. | `10646:1231` · **partial** · tab label (E-11). |
| **WF-MOB-05** Capture hub and progress capture · MOB | `MOB-04`, `MOB-03`, `MOB-S04` · R1 beta, R2 | SUP, QS · B · P | Capture → type | Role-based list: report, photo, issue, inspection, measurement draft. Record-progress form with three-state save feedback. | **Saved on device, uploading, accepted by server** are separate. | `10646:1322` · **partial** · `UAT-08` (E-12). |
| **WF-MOB-06** Inbox and online approvals · MOB | `MOB-S08`, `MOB-04` · R2 P0 | PM, QS, approvers · B · P, T | Inbox → item | Inbox list. Decision screen. Re-authentication. Offline: cached context readable, decision disabled. | **An approval is never queued for later execution.** | none · **missing** |
| **WF-MOB-07** Sync centre · MOB | `MOB-S09`, `SYNC-05/07/08` · R1 beta | SUP, PM, QS · B · P | More → Sync | Item states: queued, uploading, awaiting server validation, synced, failed, conflict, access revoked, action required. Retry, review, safe cancel. | Saved on device differs from uploaded bytes differs from accepted record. Drafts are not auto-deleted at seven days. A prompt appears. | none · **missing** · `V3-17`, `UAT-08`. |
| **WF-MOB-08** Conflict resolution · MOB | `SYNC-05`, `V3-18` · R1 beta | SUP, QS · B · P | Sync → conflict | Local against current values. Base version. Choose, merge or discard, with explanation. | No silent overwrite of quantities. | none · **missing** · `V3-18`. |
| **WF-MOB-09** Account, settings, organization and server switching · MOB | `MOB-S10`, `V3-20` · R2 P0 | all · B · P, T | More → Account | Sessions. Language. Storage. Download policy. Privacy. Logout. Switch with unsent-draft warning. | Database and cache partitioned by server, tenant, user. Drafts locked to the original identity. | none · **missing** · `V3-20`. |
| **WF-MOB-10** Failure and recovery states · MOB | `SYNC-06`, `MAPI-02`, `MSEC-03`, `V3-21/22` · R1 beta, R2 | all · B · P, T | Any capture | Camera denied with manual alternative. Storage full. Interrupted upload resume. Unsupported version handshake with update path. Access revoked. Lease expired lock. Clock-drift notice. | Never mark a business record as accepted before the server accepts it. | none · **missing** · `V3-21`, `V3-22`. |
| **WF-MOB-11** Push and deep links with inbox fallback · MOB | `PUSH-01/02` · R2 P0 | all · B · P | Notification → item | Opaque notification. Deep link after identity switch. Push-disabled inbox fallback. | Minimal metadata. No cross-identity detail. | none · **missing** · `V3-20`. |
| **WF-MOB-12** Drawings and submittals view · MOB | `MOB-S06`, `MOB-03` · R1 beta | SUP, PM, QS · B · T, P | Projects → drawing | Revision viewer. Stale label. Supersession detection. Permitted markup. Tablet layout. | Cached content is labelled potentially stale when freshness cannot be checked. | none · **missing** · `UAT-16`. |
| **WF-MOB-13** PM and QS online review surfaces · MOB | `MOB-03` · R2 P0 | PM, QS · B · P, T | Inbox → review | Report review. Lookahead constraints. Measurement and certificate read views. | Permitted approvals online only. | none · **missing** |
| **WF-MOB-14** Urdu RTL field navigation and field screens · MOB | PRD v4.0 §10.3, `V3-24` · R2 P0. **v4.1 PA-06 relaxes this and is unapproved** | field roles · B · P, T | Language → Urdu | Mirrored layouts of Today, Projects, Capture, Inbox, More and the field screens `MOB-S01…S10`. Mixed Latin identifiers and numeric units inside RTL text. | Full finance translation is a later pack. | none · **missing** · `V3-24`. |
| **WF-MOB-15** English and Urdu quick-start and recovery guides · NON | `MREL-04` · R2 P0 (v4.0). v4.1 `PA-07` relaxes it | field users · B | Help → guides | Guides with real-device screenshots. Not a screen. | Content deliverable. | none · **missing** |
| **WF-MOB-16** Tablet layouts for drawings and inspection · MOB | `MOB-01` · R2 P0 | SUP, QS · B · T | Projects → drawing or inspection | Tablet-specific layouts. | Usable tablet layout is required for drawings and inspection. | none · **missing** |

### 3.P Later releases (provisional)

Detailed screens for these stay **provisional** until their rules are approved. They must never be shown as available to customers before their gates (§17.2).

| ID · workflow · class | PRD · rel | Persona · scope · mode · device | Notes and unresolved rules | Figma · status |
|---|---|---|---|---|
| **WF-EST-01** Estimate build-up, tender comparison, estimating intelligence · CUS | `EST-01` R3, `PROJECT-02` advanced R3 | QS · B · D | R1 imports an approved estimate only. Build-up rules **UNRESOLVED**. | none · **missing** |
| **WF-CRM-01** Lead intake, follow-ups, quotation · CUS | `CRM-01…03` R3. Gate cites acceptance text (no `UAT-CRM` ID exists) | sales role **UNRESOLVED** · B · D | Won lead creates exactly one linked customer and project draft. | none · **missing** |
| **WF-BIL-R3** Lump-sum and milestone billing strategies · CUS | `BILL-09`, `V3-03` R3 | QS, FIN · B · D | Eligibility uses certified percentage against prior invoiced. | none · **missing** |
| **WF-LAB-04** Payroll generation and advances · CUS + DESK | `LABOUR-03/05` R3 | FIN · B · D | Payroll law is jurisdiction-specific. **UNRESOLVED.** | none · **missing** |
| **WF-AI-01** Invoice extraction review · CUS | `UX-04`, `EVAL-02`, `UAT-10` R3 | ACC · B · D | Source evidence beside editable extracted fields. No auto-post. | none · **missing** |
| **WF-AI-02** Voice and diary transcription · MOB | `EVAL-03`, `UAT-11` R3 | SUP · B · P | Locale pairs per v4.0 (Urdu and English). PA-08 pending. | none · **missing** |
| **WF-AI-03** Read-only assistant · CUS | `UX-05`, `EVAL-04`, `UAT-09` R3 | OWN, PM · B · D, P | Shows evidence, cutoff and interpretation. | none · **missing** |
| **WF-AI-04** BOQ and contract comparison · CUS | `UX-06`, `EVAL-05`, `UAT-14` R3 | QS · B · D | Stable line identities. Reviewer sign-off. | none · **missing** |
| **WF-AI-05** Forecast scenarios and narratives · CUS | `FCT-01`, `EVAL-06` R3 | FIN, OWN · B · D | Base, adverse, favourable. Immutable. | none · **missing** |
| **WF-AI-06** AI administration, quotas, usage · CUS | `AI-OPS-01/02`, `BIZ-02` R3 | ORGA · B · D | Metered add-on. Manual fallback. | none · **missing** |
| **WF-PLN-01** Advanced planning, productivity, quality analytics · CUS | `PLAN-01`, `LOOK-02`, `QUAL-01` R3 | PM · B · D | Separate acceptance. | none · **missing** |
| **WF-ECO-01** Client and subcontractor portals · CUS | R4, `GROW-02` | external roles (R4, §10.3) · B · D | External roles must not reuse employee entitlements. | none · **missing** |
| **WF-ECO-02** BIM, telemetry, advanced adapters · CUS | R4 | **UNRESOLVED** | Needs paying-customer evidence first. | none · **missing** |
| **WF-ECO-03** Air-gapped mobile and local AI · MOB | R4, `PAR-01` | **UNRESOLVED** | Separately qualified. | none · **missing** |
| **WF-GTM-01** Marketing website | **Not a PRD requirement.** Plan-defined (WBS 18.4, `DEVELOPMENT_PLAN.md` §8) | prospects | Optional track. Not a product workflow. | none · **missing** |

---

## 4. Non-UI requirements and validation responsibility

These have no screen. They are validated by tests and evidence, not design. Each needs a named owner and a result in the evidence register.

| Requirement | What it enforces | Validated by | Owner stream |
|---|---|---|---|
| `ARC-01/02` tenant and file isolation | Separate site and database per customer. Namespaced files, caches, queues, jobs. | `SP-03`, `V3-08` | Platform, QA |
| `ARC-03/04/05` entities, decimals, outbox | DocTypes. Decimal money. Transactional events. | `UAT-13`, `ENG-03` | ERP domain |
| `API-01…04`, `MAPI-01` | Authenticated scoped API with idempotency. Mobile contracts. | Contract tests | ERP domain, mobile |
| `ENG-01…05` | Invariants enforced across Desk, REST, import, jobs. | `V3-06` | ERP domain |
| `SYNC-02…08` protocol | Lease, encrypted store, cursors, upload sessions. | `SP-02`, `V3-17…22` | Mobile, QA |
| `TEN-02` provisioning job, `BIZ-01` webhooks, `LIC-03` signature check | Idempotent jobs. Authenticated webhooks. Local verification. | `V3-07`, `V3-09`, `V3-12` | Control plane |
| `STD-01…03`, `NFR-01…06` | Security evidence, performance, availability, restore. | `QA-01`, restore drills | Platform, QA |
| `MET-01` calculation service | Deterministic metrics with `metric_version` and `as_of`. | `UAT-01`, `V3-04` | ERP domain, finance |
| `MIG-01…04` tooling | Staged imports. Reconciliation. Rollback rules. | `UAT-12` | Implementation |

---

## 5. Existing Figma frames mapped to workflows

None of the 13 frames is a completed workflow. Defects are listed in `CIP_PLAN_RECONCILIATION.md` §7 (E-01…E-14).

| Frame | Node | Maps to | Status |
|---|---|---|---|
| Company Admin Home | `10623:841` | WF-CAD-00 | partial |
| Overview | `10651:1245` | WF-ROL-01 | partial |
| Projects | `10651:1466` | WF-PRJ-04 | partial |
| Project Hub | `10645:477` | WF-PRJ-03, WF-OWN-04 | partial |
| Procurement | `10651:1687` | WF-PRC-03 (register only) | partial |
| Commercial Workbench | `10645:1044` | WF-CRT-01, WF-INV-01, WF-CHG-06 | partial, mixes three workflows |
| Approvals | `10651:1908` | WF-APR-01 | partial |
| Users and Roles | `10651:2129` | WF-CAD-02 | partial |
| Country Settings | `10651:2351` | WF-CAD-01 | partial |
| Daily Report | `10645:1265` | WF-SIT-01 (summary only), WF-SIT-02 | partial |
| Platform Admin Tenants | `10651:2571` | WF-PLT-01 (list), WF-PLT-04 (summary) | partial |
| Mobile Today | `10646:1231` | WF-MOB-04 | partial |
| Mobile Capture | `10646:1322` | WF-MOB-05, WF-SIT-04 | partial |

---

## 6. Coverage summary

Counts are generated from the tables above. See `CIP_DESIGN_SEQUENCE.md` for batch assignment.

| Group | Workflows | missing | partial | designed | prototype-verified |
|---|---|---|---|---|---|
| 3.A Vendor control plane (SaaS only) | 7 | 5 | 2 | 0 | 0 |
| 3.B Customer organization administration | 9 | 6 | 3 | 0 | 0 |
| 3.C Customer subscription and billing administration (SaaS) | 3 | 3 | 0 | 0 | 0 |
| 3.D Standalone installation administration (customer-operated) | 8 | 8 | 0 | 0 | 0 |
| 3.E Role home, approvals, shared | 6 | 4 | 2 | 0 | 0 |
| 3.F Executive and project | 8 | 5 | 3 | 0 | 0 |
| 3.G Contract and BOQ | 3 | 3 | 0 | 0 | 0 |
| 3.H Site execution | 6 | 4 | 2 | 0 | 0 |
| 3.I Measurement to cash | 12 | 10 | 2 | 0 | 0 |
| 3.J Change events and commercial recovery | 6 | 5 | 1 | 0 | 0 |
| 3.K Procurement and inventory | 8 | 7 | 1 | 0 | 0 |
| 3.L Labour and subcontract | 6 | 6 | 0 | 0 | 0 |
| 3.M Documents, quality, safety, closeout | 14 | 14 | 0 | 0 | 0 |
| 3.N Finance operations (mostly Desk) | 5 | 5 | 0 | 0 | 0 |
| 3.O Native mobile (iOS and Android) | 16 | 14 | 2 | 0 | 0 |
| 3.P Later releases (provisional) | 15 | 15 | 0 | 0 | 0 |
| **Total** | **132** | **114** | **18** | **0** | **0** |

---

## 7. Limitations

- Release and priority tags are copied from PRD v4.0. Where the PRD gives none, the row says so.
- "Persona" uses PRD §5 and `COM-05`. Roles the PRD does not name are marked **UNRESOLVED**, not invented.
- Surface lists are the **minimum** needed to complete each workflow. They are not final screen counts.
- The Desk-versus-custom split is the PRD §12.1 proposal and needs R0 validation.
- Nothing here is designed or approved. **The software design and implementation are not complete.**
