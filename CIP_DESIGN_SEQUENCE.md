# CIP Design Sequence

**Status:** Review draft for sponsor. This orders the design work. It does not start any batch.
**Governing source:** PRD v4.0. v4.1 additions are proposals (`PA-01…PA-11`).
**Companion documents:** `CIP_PLAN_RECONCILIATION.md`, `CIP_DESIGN_COVERAGE.md`. Workflow IDs (`WF-…`) are defined in the coverage file.

**Scope of this pass:** no Figma screens were created or changed and no application code was written. The 13 existing frames are preserved. Corrections to them are scheduled inside the batches below. They are not applied yet.

---

## 1. Principles

1. **One batch is one coherent user journey**, designed, reviewed and prototype-checked before the next starts.
2. **The order follows the PRD, not the menu.** PRD §17.1 says "the first implementation increment must connect one field report through measurement to an eligible invoice and reconciled cost view." Design starts on that spine. `SP-05` (R0) tests it with a clickable flow: save offline, identify an accepted report, resolve a conflict, reject a stale drawing, prepare a correct incremental bill.
3. **Design the full product, and show release and entitlement on every frame.** Each frame carries a release chip (R1, R2, R3, R4) and, where relevant, an entitlement chip (Core, Operations Plus, Enterprise, AI add-on). Later screens whose rules are unresolved carry a **"Provisional, rules unresolved"** badge. A provisional screen is never presented as approved.
4. **Task-shaped layouts.** Use an editor for entry, a master-detail pane for review, a register for lists and a form for settings. Do not repeat cards, then bars, then a table. Use bars only where a quantity against a total is the point, and make the arithmetic match the label.
5. **Existing foundation stays.** Inter. The neutral and teal foundation. Untitled UI free-kit components. Semantic colours: success is never red.
6. **No new rules.** No tax defaults, approval thresholds or accounting policy appear in design. Fields are empty or marked sample until finance approves them.
7. **Every screen specifies its states** (`UX-09`): loading, empty, filtered-empty, validation, denied, stale/conflict, offline, partial upload, expired session and success, where applicable.
8. **Every control goes somewhere.** In a prototype each button leads to a screen or is shown disabled with a reason. Every failure state has a recovery path.
9. **Native ERP screens are not rebuilt by default.** See the Desk, configured and custom split in the coverage file §2.

---

## 2. Role-based navigation

Five separate shells share one design system. **No admin item appears inside the employee shell and no employee item inside an admin shell.** A user reaches another shell only through a separate permission, never through a role switcher. The mobile app hosts the employee shell only (`ACC-01`, proposed).

### 2.1 Shells

| Shell | Users | Mode | Device | Navigation (workflow IDs) |
|---|---|---|---|---|
| **Vendor control plane** | `VOPS`, `VBIL` | SaaS only | Desktop | Tenants (PLT-01) · Entitlements and plans (PLT-02) · Billing operations (PLT-06) · Fleet health (PLT-04) · Support access (PLT-03) · Releases (PLT-05) · Lifecycle (PLT-07) |
| **Installation console** | `INST` (customer) | Standalone only | Desktop | Health (STD-01) · Licence (STD-02) · Upgrades (STD-03) · Backups and recovery (STD-04) · Connectivity and push (STD-05) · Extensions and diagnostics (STD-06) · Portability (PORT-01) · About and licences (LIC-01) |
| **Company administration** | `ORGA`, `ERPA` | Both | Desktop | Home (CAD-00) · Company and country (CAD-01) · Users and roles (CAD-02) · Approval policy (CAD-03) · Modules (CAD-04) · Integrations (CAD-05) · Audit and retention (CAD-06) · Security and devices (CAD-07) · Data export (CAD-08) · Help (CMN-03) |
| **Subscription and billing** | `BILA` | SaaS only | Desktop | Subscription and invoices (BIL-01) · Plan and capacity (BIL-02) · Notices (BIL-03). Shown to `BILA` only, as its own group. Whether it sits inside the Company administration shell is a decision (§5). |
| **Employee and operations** | Business roles | Both | Desktop, tablet, mobile | See 2.2. |

### 2.2 Employee and operations navigation by role

Every role also has **Home** (ROL-01), **Approvals** where the role can approve (APR-01) and **Alerts** where assigned (OWN-03).

| Role | Navigation |
|---|---|
| **Owner** | Dashboard (OWN-01) · Projects (PRJ-04) · Approvals, high-value only (APR-01) · Alerts (OWN-03) · Reports, read (FIN-04) |
| **Finance manager and accountant** | Invoices (INV-02) · Receipts and collections (COL-01, COL-02) · Retention (RET-01) · Advances (COL-03) · Payments (PRC-06, PRC-08) · Petty cash (FIN-02) · Month close (FIN-03) · Reports (FIN-04) · Ledger in Desk (FIN-01) · Migration reconciliation (FIN-05) |
| **Quantity surveyor** | Measurements (MSR-01, MSR-02) · Certificates (CRT-01, CRT-02) · Invoice eligibility (INV-01) · Changes and claims (CHG-01…06) · Subcontract certification (SUB-02) · BOQ and contract (BOQ-01…03) · Submittals (DOC-03) |
| **Project manager** | Project hub (PRJ-03) · Daily report review (SIT-02) · Lookahead (SIT-06) · Requisitions (PRC-01) · RFIs (DOC-02) · Drawings (DOC-01) · Changes (CHG-01) · Safety actions (SAF-02) · Closeout (CLO-01…03) |
| **Procurement** | Requisitions (PRC-01) · Quotes (PRC-02) · Purchase orders (PRC-03) · Suppliers (PRC-04) · Receiving (PRC-05) · Stock (PRC-07) |
| **Operations manager** | Portfolio (PRJ-04) · Site issues (SIT-05) · Equipment (EQP-01) · Alerts (OWN-03) |
| **Site supervisor** | **Mobile first.** Today · Projects · Capture · Inbox · More (MOB-04). Web: light report entry (SIT-01), attendance (SIT-03). Safety capture (SAF-01) |
| **Unresolved roles** | Safety owner, document controller, QA inspector, storekeeper and sales role are not named in the PRD. Their items sit under the project manager or QS until `DEC-06` and decision 17 settle roles. |

### 2.3 Mobile navigation (employee shell only)

Tabs: **Today · Projects · Capture · Inbox · More** (`MOB-04`, labels final after usability testing). Approvals live inside **Inbox**, online only. Account and organization switching live in **More**. R2 adds Urdu RTL mirroring of this navigation (WF-MOB-14, PRD v4.0).

---

## 3. Design batches

Release tags are the earliest PRD release for the batch's core workflows. Each batch lists exact screens and alternate states, requirements, dependencies, prototype entry and exit, and a review checklist.

### Shared review checklist (applies to every batch)

- [ ] Every screen lists the `UX-09` states that apply, or records why one does not.
- [ ] Vocabulary matches `CIP_PLAN_RECONCILIATION.md` §6 (billing chain, availability levels, roles).
- [ ] No financial approval, certification, posting or safety release is possible offline or through an admin role.
- [ ] No tax rate, threshold or accounting policy is pre-filled.
- [ ] Release and entitlement chips are present. Provisional rules are badged.
- [ ] Any progress bar's numerator and denominator match its label. Success is never red.
- [ ] Layout fits the task (editor, review pane, register or form), not the repeated card-bar-table pattern.
- [ ] Untitled UI free-kit components, Inter and the teal foundation are used.
- [ ] Layouts use auto-layout so RTL mirroring is possible later.
- [ ] Every control leads somewhere or is disabled with a reason. Every failure has a recovery path.
- [ ] Touch targets are 44px on mobile. Contrast meets WCAG 2.2 AA.
- [ ] The named reviewers for the batch have signed off.

---

### B0 — Shared specification (no journey, no screens)

- **Workflows:** WF-CMN-02.
- **Content:** the ten-state kit, status chips for each state vocabulary, number and currency formats, release and entitlement chips, the "claimed, not certified" label pattern, and the "sample, not validated" pattern.
- **Needs approval of:** the vocabulary in reconciliation §6.
- **Review:** UX lead and finance/QS lead.

---

### B1 — Field report: capture, sync, review (**proposed first batch**)

- **Release:** R1 (web), R1 beta and R2 (mobile). **Journey:** a site supervisor records a day's work offline, the report syncs, the project manager accepts or returns it, and the supervisor amends it.
- **Workflows:** WF-SIT-01, WF-SIT-02, WF-SIT-04, WF-MOB-05, WF-MOB-07, WF-MOB-08, WF-MOB-10.
- **Requirements covered:** `OPS-01`, `PROJECT-03`, `UX-03`, `UX-09`, `MOB-S04`, `MOB-S05`, `MOB-S09`, `SYNC-05/06/07/08`, `MOB-03` (supervisor), §10.2 offline authority.
- **Dependencies:** B0. Needs fixture projects, sites and BOQ lines (their setup is B8). Needs a lease in state `valid` (the lease screens are B15).
- **Existing frames corrected here:** Daily Report `10645:1265` (E-09). Mobile Capture `10646:1322` (E-12). Both are corrected by new frames. The originals are preserved.

**Exact screens and alternate states**

| # | Screen | Device | Alternate states |
|---|---|---|---|
| 1 | Daily report editor | D, T | New (empty). Draft with save status. Validation (missing unit or quantity). **Duplicate** (a report exists for the same site, date, shift and unit). Stale reference (BOQ line superseded). Save failed. Expired session with form state kept. |
| 2 | Submit dialog | D, T | Summary of what will be sent. Submitting. Submitted for review. Denied (no permission). |
| 3 | Report detail | D, T | One state chip: Draft, Submitted, Under review, Returned, Accepted, Amended (revision n). Revision-history drawer. |
| 4 | Review queue | D | Default. Empty. Filtered-empty. Loading. |
| 5 | Report review pane | D, T | Quantities against plan. Evidence gallery with an original-retained indicator. Changes since the prior revision. Accept and Return dialogs. Denied. **Stale revision conflict** with refresh. |
| 6 | Amend returned report | D, T | Return-reason banner. Editing. Resubmit. New revision created. |
| 7 | Capture hub | P | Items for the role. Empty. |
| 8 | Daily report form | P | Section status (activities, quantities, manpower, blockers, evidence). Draft. Validation. |
| 9 | Record progress | P | **Saved on this device**, then **Uploading (n of m)**, then **Accepted by server** or **Awaiting validation**. Offline banner reads "Not yet sent". Never "saved" before the local save. |
| 10 | Evidence capture | P | Camera. **Permission denied** with manual alternative. Annotate as a copy, original kept. Partial upload and resume. |
| 11 | Sync centre | P | Queued, uploading, awaiting server validation, synced, failed, conflict, access revoked, action required. Retry and safe-cancel dialogs. Low-storage state. Seven-day overdue prompt. |
| 12 | Quantity conflict resolution | P | Local against current values. Base version. Choose, merge, discard. Explanation. |
| 13 | Locked states | P | Lease expired. Access revoked. |

**Prototype entry and exit**

- **Entry:** mobile Today → Capture → Daily report.
- **Path:** fill the form → save in airplane mode → Sync centre shows queued → reconnect → uploading → awaiting validation → web Review queue → open the report → Accept **or** Return → mobile shows Returned → Amend → Resubmit → Accepted.
- **Branch:** a two-device quantity conflict opens screen 12, then returns to Sync centre.
- **Exit:** an accepted report with its revision number, ready to be cited by a measurement (B2).
- Observed quantities are labelled **"Observed, not measured and not billable"**.

**Acceptance criteria (design acceptance, not implementation)**

1. All thirteen screens exist with the listed states. Nothing is "saved" before it is saved.
2. The three mobile save states are separate and visible on both web and mobile.
3. State vocabulary matches `OPS-01` and `MOB-S04`. No contradictory label such as "Submitted" beside "Draft".
4. The report identity fields (project, site, date, shift, reporting unit) are present. The duplicate state is designed.
5. No approval, certification or posting action appears offline. Review accept and return are not financial approvals.
6. Any bar's maths matches its labels. Success is not red.
7. Every control leads somewhere or is disabled with a reason. Each failure has a recovery path.
8. Layouts use auto-layout and kit components so RTL can follow (B15).
9. `SP-05` tasks 1 to 3 (save offline, identify the accepted report, resolve a conflict) can be completed in the clickable prototype by a reviewer without coaching. This is a design check. The `SP-05` pass thresholds themselves (at least 4 of 5 supervisors and all 3 QS/finance users) are measured later with real users.
10. Sign-off by the product sponsor, the mobile lead and a supervisor representative.

**Review checklist (batch-specific):** the shared list above, plus
- [ ] The duplicate-report state shows the existing report and offers open or amend.
- [ ] Evidence shows that originals are retained and annotations are copies.
- [ ] The Sync centre never shows "synced" for an item that is only uploaded.

---

### B2 — Verified measurement to certificate preparation

- **Release:** R1. **Journey:** a QS turns accepted observations into a measurement, a verifier verifies it, and the QS prepares a certificate.
- **Workflows:** WF-MSR-01, WF-MSR-02, WF-CRT-01.
- **Requirements:** `PROJECT-04`, `BILL-02`, `BILL-04`, `OUT-01`, `UAT-04`, `UAT-05` foundation.
- **Dependencies:** B1 (accepted report), fixture BOQ lines, vocabulary §6.2.
- **Existing frame corrected:** Commercial Workbench `10645:1044` (E-01), the certificate-preparation half.

| # | Screen | Alternate states |
|---|---|---|
| 1 | Measurement sheet | Draft. Over-allowable exception. Evidence attached. Stale BOQ line. |
| 2 | Measurement review queue and verification pane | Observed against verified quantity. Variance reason. Verify, return, supersede dialogs. Self-verification blocked. |
| 3 | Certificate editor | **Claimed, verified and certified columns.** Gross work value, eligible variations, retention, advance recovery, other deductions, net. Draft labelled "Claimed, not certified". Tax area empty until configured. |
| 4 | Certificate preview (output) | Draft marking. Source revisions. Approval status. |
| 5 | Submit-for-certification dialog | Missing verified lines. Stale measurement conflict. |

- **Prototype:** entry from an accepted report → measurement → verify → certificate editor → submit. Exit: a submitted certificate ready for B3 decision.
- **Acceptance:** no draft shows "certified". Claimed, verified and certified never share a column. The editor does not reserve invoice quantity. Net equals gross minus listed deductions.
- **Checklist additions:** [ ] verifier is not the author [ ] a superseded measurement keeps history.

---

### B3 — Approvals and certification decision

- **Release:** R1. **Journey:** a user signs in, sees a role home with an action queue, opens the approval inbox, reviews evidence and decides.
- **Workflows:** WF-CMN-01, WF-ROL-01, WF-APR-01, WF-APR-02, WF-CRT-02.
- **Requirements:** `SEC-01`, `UX-02/03`, `UX-08`, `APR-02/03/04`, `BILL-02`, `UAT-07`, `V3-06`.
- **Dependencies:** B2 (a certificate to decide). Policy screens are B14.
- **Existing frames corrected:** Overview `10651:1245` (E-04). Approvals `10651:1908` (E-06).

| # | Screen | Alternate states |
|---|---|---|
| 1 | Sign-in, MFA, expired session, denied | MFA required for privileged roles. Session expired with form kept. |
| 2 | Role home with action queue | Per role. Empty queue. Each item shows owner, next action, deadline. |
| 3 | Approval inbox (master list) | Filters by type, project, amount, age. Empty. Filtered-empty. |
| 4 | Decision review (detail pane) | Amount, budget impact, changed fields, policy version, evidence, prior decisions. Re-authentication for high-risk. |
| 5 | Certificate decision dialogs | Certify, part-certify, reject, dispute. Reason required. |
| 6 | Conflict and stale | Stale revision conflict with refresh. Self-approval blocked. Revoked access. |
| 7 | Delegation dialog and list | Scope, period, value limit. Split-request flag review. |

- **Prototype:** sign in → role home → inbox → open the B2 certificate → decide → certified. Exit: a certified certificate ready for B4. A rejected branch returns to B2.
- **Acceptance:** a decision binds a revision and policy version. A stale action cannot succeed. No admin role can approve. Daily reports sit in the review queue (B1), not here. Nothing is approvable offline.

---

### B4 — Certified work to invoice eligibility, reservation, ERP invoice and correction

- **Release:** R1. **Journey:** a certified certificate becomes eligible, quantity is reserved, a draft invoice links to the ERP, and a later error is corrected by credit and rebill.
- **Workflows:** WF-INV-01, WF-INV-02, WF-INV-03.
- **Requirements:** `BILL-03/04/08/10/11`, `FIN-03`, `UAT-03`, `UAT-04`, `UAT-05`.
- **Dependencies:** B3.
- **Existing frame corrected:** Commercial Workbench `10645:1044` (E-01), the reservation half.

| # | Screen | Alternate states |
|---|---|---|
| 1 | Eligibility view | Per line: net entitlement, posted, live reservations, remaining eligible. Stale and duplicate request. |
| 2 | Reserve dialog | Idempotency feedback. Over-eligible blocked. |
| 3 | Invoice draft preview | Net after retention, advance and deductions. Tax area empty until configured. |
| 4 | Link to ERP sales invoice (Desk) | Posted. Link failure with retry. |
| 5 | Correction request | Credit and rebill preview. Period-lock warning. Approval. |

- **Prototype:** entry from a certified certificate → eligibility → reserve → invoice draft → Desk link → posted → correction branch. Exit: a posted invoice, then B7.
- **Acceptance:** posted + reserved + remaining equals entitlement. A reservation is never labelled an invoice. A locked period shows the controlled-reopen path.
- **`SP-05` slice:** B1 + B2 + B3 + B4 plus the stale-drawing slice of B5 form the clickable flow `SP-05` needs.

---

### B5 — Drawing revision, stale warning, RFI, change origin

- **Release:** R1. **Journey:** a new drawing revision supersedes an old one, a user sees a stale warning, raises an RFI and starts a change candidate.
- **Workflows:** WF-DOC-01, WF-DOC-02, WF-MOB-12, WF-SIT-05, WF-CHG-01.
- **Requirements:** `DOC-01/02`, `RFI-01`, `CHG-01`, `MOB-S06`, `UAT-16`.
- **Dependencies:** B1.
- **Screens:** drawing register (superseded, stale), revision upload and supersede dialog, mobile drawing viewer (stale label, supersession on reconnect, tablet layout), RFI form and response, issue form, change-event intake. States: stale, offline, denied, empty.
- **Prototype:** entry from the mobile drawing viewer → stale warning → RFI → change candidate. Exit: a change event ready for B6.
- **Acceptance (`UAT-16`):** an old revision is marked superseded. An RFI response creates a linked change candidate. There is no automatic contract increase.

### B6 — Change assessment, claim, response, recovery

- **Release:** R1 (scenarios R3). **Workflows:** WF-CHG-02, WF-CHG-03, WF-CHG-04, WF-CHG-05, WF-CHG-06.
- **Requirements:** `CHG-02…05`, `BOQ-04`, `UX-07`, `UAT-02`.
- **Dependencies:** B5, B3 (approval pattern).
- **Screens:** assessment editor, notice tracker, claim by revision (requested, approved, rejected, disputed separate), response entry, baseline-update confirmation, closure and recovery view, commercial register.
- **Prototype:** entry from the B5 change event → assess → notice → claim → partial approval → baseline update → close. Exit: an updated contract baseline.
- **Acceptance (`UAT-02`):** a partial approval increases the approved contract once. The disputed remainder stays separate. Rejected recovery keeps actual cost.
- **Existing frame corrected:** the register half of Commercial Workbench (E-01).

### B7 — Posted invoice to cash, advances, retention

- **Release:** R1. **Workflows:** WF-COL-01, WF-COL-02, WF-COL-03, WF-RET-01.
- **Requirements:** `BILL-04/05/06/07`, `FIN-03`, `HAND-02` (R2 link).
- **Dependencies:** B4.
- **Screens:** receipt allocation, withholding evidence dialog, four collection worklists, advance and recovery view, retention schedule and release.
- **Prototype:** entry from a posted invoice → receipt → partial allocation → collections → retention release request. Exit: reconciled receivable.
- **Acceptance:** allocations reconcile to the payment amount. Retention release cannot exceed the eligible balance. Release conditions marked unresolved until decision 10.

### B8 — Project, contract and BOQ setup

- **Release:** R1. **Workflows:** WF-PRJ-01, WF-PRJ-02, WF-BOQ-01, WF-BOQ-02, WF-BOQ-03.
- **Requirements:** `PROJECT-01/02`, `FIN-02`, `BOQ-01/02/03`, `BILL-01`, `BILL-09`, `EST-01` (import), `MIG-01`.
- **Dependencies:** B0. Provides the fixtures B1 to B4 assume.
- **Screens:** project form and archive dialog, site and location tree, cost-code and budget versions, contract record, BOQ import with mapping and validation, revision list and diff, approval review.
- **Prototype:** entry from the admin handoff → new project → contract → BOQ import → validation → revision approval. Exit: an approved baseline.
- **Acceptance:** an approved baseline cannot be edited in place. A billed-line removal is blocked. A missing cost-code mapping blocks import.

### B9 — Procurement to payment

- **Release:** R1. **Workflows:** WF-PRC-01 … WF-PRC-08.
- **Requirements:** `PROC-01…10`, `APR-02/04`, `UAT-06`, `UAT-07`.
- **Dependencies:** B3 (approval pattern), B8.
- **Screens:** requisition, quote comparison, PO editor and amendment diff, cancel-remaining, commitments register, supplier onboarding and bank verification, receiving, invoice matching, stock transfer and consumption (Desk links), payment preparation, verification and authorization.
- **Prototype:** entry from a requisition → PO → receipt → invoice match → payment steps. Exit: a payment authorized by a different person.
- **Existing frame corrected:** Procurement `10651:1687` (E-13).
- **Acceptance:** an edit after approval invalidates the approval. No invoice match before accepted goods. Payment preparation, verification and authorization are separate.

### B10 — Labour and subcontract

- **Release:** R1. **Workflows:** WF-SIT-03, WF-LAB-01, WF-LAB-02, WF-LAB-03, WF-SUB-01, WF-SUB-02, WF-SUB-03.
- **Requirements:** `LABOUR-01/02/04/05` (import), `LABOUR-06`.
- **Dependencies:** B1, B3.
- **Screens:** attendance and delivery observation, worker registry with restricted fields, overlap exception, payroll batch import, work order, four-state subcontract certification, variations, deductions, retention release.
- **Prototype:** entry from a work order → submission → verified quantity → certificate → payable → reversal correction. Exit: a corrected subcontract balance.
- **Acceptance:** submission, verified quantity, certificate and payable are separate states. A reversed certificate starts a correction document.

### B11 — Technical, quality, safety, closeout, outputs

- **Release:** R1 (some R2). **Workflows:** WF-SIT-06, WF-DOC-03, WF-DOC-04, WF-QUA-01, WF-QUA-02, WF-QUA-03, WF-SAF-01, WF-SAF-02, WF-SAF-03, WF-EQP-01, WF-CLO-01, WF-CLO-02, WF-CLO-03, WF-OUT-01.
- **Requirements:** `LOOK-01/02`, `SUB-01/02/03`, `DOC-03`, `QUAL-01/02/03`, `SAFE-01/02`, `EQP-01`, `HAND-01/02`, `PROJECT-05`, `OUT-01/02`, `V3-01`, `V3-02`, `V3-05`.
- **Dependencies:** B1, B5. Roles for safety, documents and QA are unresolved (decision 17).
- **Screens:** lookahead grid and constraint tracker, submittal register and gate, transmittal, inspection plan and result, NCR, safety record and actions, permit status references, equipment record, handover checklist, defects register, closeout gate, all output templates and previews.
- **Prototype:** entry from a failed inspection → gate blocks certification → corrective action → re-inspection → certification allowed. Exit: closeout checklist.
- **Acceptance (`V3-02`):** a failed portion blocks certification and an accepted portion proceeds. A safety record is not an emergency channel. R2 permit status references do not issue permits.

### B12 — Owner dashboard, forecast, alerts, portfolio

- **Release:** R1 (scenarios R3). **Workflows:** WF-OWN-01, WF-OWN-02, WF-OWN-03, WF-OWN-04, WF-PRJ-03, WF-PRJ-04.
- **Requirements:** `UX-01/02`, `MET-01/02`, `ALT-01`, `REP-01`, `UAT-01`, `UAT-15`, `V3-04`.
- **Dependencies:** B1 to B10 supply the figures. Designing earlier would reproduce the arithmetic errors in E-02 and E-03.
- **Existing frames corrected:** Project Hub `10645:477` (E-02). Projects `10651:1466` (E-03).
- **Screens:** owner dashboard, metric definition drawer, drill-down tables, alert list and detail, forecast editor and snapshot dialog, project hub with working tabs, portfolio list.
- **Prototype:** entry from the dashboard → a metric → definition → source rows. Exit: totals equal drill-down.
- **Acceptance:** forecast variance equals approved budget minus EAC. Missing ETC is never zero. Cash surplus is never labelled profit.

### B13 — Finance operations

- **Release:** R1 (petty cash placement unresolved). **Workflows:** WF-FIN-01 … WF-FIN-05.
- **Requirements:** `FIN-01…06`, `MIG-01…04`, `UAT-05`, `UAT-12`.
- **Dependencies:** B4, B7, B9.
- **Screens:** reconciliation status view, Desk entry links, petty cash, close checklist and controlled reopen, report viewer, migration reconciliation and sign-off.
- **Acceptance:** total equals drill-down. Backdated documents need controlled reopen. Invoiced work is not billable again after migration.

### B14 — Company administration

- **Release:** R1 and R2. **Workflows:** WF-CAD-00 … WF-CAD-08, WF-CMN-03.
- **Requirements:** `COM-05`, `APR-01/03`, `SEC-01/02/03`, `INT-01/02`, `PAR-02`, `V3-19`, `PA-02` (proposed).
- **Dependencies:** B3 (policy affects approvals). Decisions 1, 3, 4, 8, 11.
- **Existing frames corrected:** Company Admin Home `10623:841` (E-05). Users and Roles `10651:2129` (E-07). Country Settings `10651:2351` (E-08).
- **Screens:** admin home, company and country profile with availability badge, users and roles, approval policy editor, modules, integrations, audit, security and devices, export, help.
- **Acceptance:** admin home shows no approvals. No unreviewed tax rate is shown as fact. An SoD conflict cannot be saved.

### B15 — Mobile production completeness

- **Release:** R2 (R1 beta subset in B1). **Workflows:** WF-MOB-01, WF-MOB-02, WF-MOB-03, WF-MOB-04, WF-MOB-06, WF-MOB-09, WF-MOB-11, WF-MOB-13, WF-MOB-14, WF-MOB-15, WF-MOB-16.
- **Requirements:** `MOB-01…04`, `MOB-S01/02/03/08/10`, `SYNC-02`, `PUSH-01/02`, `MREL-04`, `V3-19`, `V3-20`, `V3-23`, `V3-24`.
- **Dependencies:** B1, B3. Decisions 2 and 14.
- **Existing frame corrected:** Mobile Today `10646:1231` (E-11).
- **Screens:** organization connection, sign-in and device registration, lease states, project packs, Today and tabs, Inbox and online approval, account and organization switching, push and deep links, PM and QS review surfaces, tablet layouts, **Urdu RTL mirrored variants of the field navigation and field screens** (PRD v4.0), guide content.
- **Acceptance:** an approval is never queued offline. Switching partitions drafts by identity. RTL strings keep Latin identifiers and numeric units readable.

### B16 — Vendor control plane and SaaS lifecycle

- **Release:** R2S. **Workflows:** WF-PLT-01 … WF-PLT-07, WF-BIL-01, WF-BIL-02, WF-BIL-03.
- **Requirements:** `TEN-01…04`, `COM-03/04/05`, `BIZ-01/02/03`, `V3-07`, `V3-09`, `V3-10`, `V3-15`.
- **Dependencies:** B14. Decisions 3, 11, 12.
- **Existing frame corrected:** Platform Admin Tenants `10651:2571` (E-10).
- **Acceptance:** vendor screens show metadata only. Support access is time-limited and visible to the customer. A downgrade shows affected capacity.

### B17 — Standalone installation, licensing, portability

- **Release:** R2L (portability for the dual-mode claim). **Workflows:** WF-STD-01 … WF-STD-06, WF-PORT-01, WF-LIC-01.
- **Requirements:** `DEP-01…06`, `LIC-01…07`, `PORT-01/02`, `V3-11`, `V3-12`, `V3-13`, `V3-14`, `V3-16`, `V3-23`.
- **Dependencies:** B14, B16 (transfer counterpart).
- **Acceptance:** the console is customer-operated and separate from the vendor control plane. Restrictions apply only where licensing permits. Read and export remain. A dual-mode statement appears only after both gates pass.

### B18 — Later releases (provisional)

- **Release:** R3 and R4. **Workflows:** WF-EST-01, WF-CRM-01, WF-BIL-R3, WF-LAB-04, WF-AI-01 … WF-AI-06, WF-PLN-01, WF-ECO-01, WF-ECO-02, WF-ECO-03, WF-GTM-01.
- **Rule:** every frame carries "Provisional, rules unresolved" and a release chip. AI screens show the manual fallback. Marketing is a separate, non-PRD track.
- **Dependencies:** their evaluation gates (`EVAL-01…06`) and paying-customer evidence.

### B19 — Cross-journey prototype integration

- **Workflows:** none new. **Content:** link B1 to B18 into role journeys, remove dead ends, and run `SP-05`-style tasks again on the connected flow.
- **Acceptance:** each role completes its primary journey end to end in the prototype with no dead end.

---

## 4. Batch index and coverage check

Every workflow ID in the coverage file is assigned to exactly one batch.

| Batch | Journey | Workflow count |
|---|---|---|
| B0 | Shared specification | 1 |
| B1 | Field report: capture, sync, review | 7 |
| B2 | Measurement to certificate preparation | 3 |
| B3 | Approvals and certification decision | 5 |
| B4 | Eligibility to invoice and correction | 3 |
| B5 | Drawing, RFI, change origin | 5 |
| B6 | Change to claim and recovery | 5 |
| B7 | Invoice to cash, advances, retention | 4 |
| B8 | Project, contract, BOQ setup | 5 |
| B9 | Procurement to payment | 8 |
| B10 | Labour and subcontract | 7 |
| B11 | Technical, quality, safety, closeout, outputs | 14 |
| B12 | Executive and portfolio | 6 |
| B13 | Finance operations | 5 |
| B14 | Company administration | 10 |
| B15 | Mobile production completeness | 11 |
| B16 | Vendor control plane and SaaS lifecycle | 10 |
| B17 | Standalone, licensing, portability | 8 |
| B18 | Later releases (provisional) | 15 |
| B19 | Cross-journey prototype integration | 0 (links existing work) |
| **Total** | | **132** |

The total matches the 132 workflows in `CIP_DESIGN_COVERAGE.md`. A mechanical check of the batch lists found no duplicate and no unassigned workflow ID.

---

## 5. Open decisions that gate batches

| Decision | Gates |
|---|---|
| 1. Approve or reject PA-01…PA-11 | All, vocabulary and scope |
| 2. Urdu RTL for R2 | B15 |
| 3. One admin console or separate vendor and installation consoles | B14, B16, B17 |
| 4. First validated country | B14 |
| 5. Collections depth | B7 |
| 6. Petty cash in R1 | B13 |
| 7. Safety ownership | B11 |
| 8. Approval-policy authority | B3, B14 |
| 9. Billing-chain label strings and tax basis | B0, B2, B4 |
| 10. Retention-release conditions | B7 |
| 11. Capacity metering | B14, B16 |
| 12. Regions | B16 |
| 13. Desk-reuse boundary | B9, B13 |
| 14. Mobile tab label | B15 |
| 17. Unnamed roles | B11 |

Full text is in `CIP_PLAN_RECONCILIATION.md` §8.

---

## 6. Limitations

- Batch order is a design sequence, not a delivery schedule and not an estimate.
- Screen lists are the minimum needed for each journey. Final screen counts follow design review.
- B1 is proposed because it fixes known defects and starts the PRD §17.1 spine. Another order is possible if the sponsor prefers it.
- Nothing in this file is designed, approved or prototype-verified. **The software design and implementation are not complete.**
