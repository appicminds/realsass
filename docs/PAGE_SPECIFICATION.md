# Page specification (content and layout), derived from PRD v4.1 and design research

> **Superseded for planning:** use `CIP_DESIGN_COVERAGE.md` and `CIP_DESIGN_SEQUENCE.md`. This page spec cites `ACC-01` (v4.1 only, unapproved), and its W-/C-/P- page IDs are not PRD workflow IDs. See `CIP_PLAN_RECONCILIATION.md` D-18.

**Status:** DRAFT for sponsor approval. **No further Figma drawing until this is approved.**
**Sources:** `Construction_AI_ERP_Focused_Scope_PRD_v4.1.docx` (sections 3.0, 5, 6–10, 12), plus the research notes below.
**Rule:** every page below exists because a PRD requirement ID needs it. Content is taken from the PRD, not invented.

---

## 1. What went wrong in the first drawings

| Problem | Why it is wrong | Source |
|---|---|---|
| Every page reused one layout (4 metric cards, progress-bar card, table) | Pages have different jobs. PRD UX-02 and UX-07 describe different structures per page | PRD §12 |
| Progress-bar "dashboard" on non-dashboard pages | PRD 12.1: "prioritize clarity over decorative dashboards" | PRD §12.1 |
| Numbers without definition | UX-01: every number needs definition, period, currency, as-of time and drill-down | PRD UX-01 |
| One approval look for everything | UX-08: approval needs amount, budget impact, changed fields, policy version, evidence, prior decisions | PRD UX-08 |
| Placeholder content | Content must come from PRD fields and states | PRD §6–9 |

## 2. Research findings (applied to the pages)

| Finding | Source | Applied to |
|---|---|---|
| Design a project overview for **immediate action**: overdue items, risks, upcoming work top-left; 2 or 3 high-signal cards; reference data lower or right | Procore Project Overview docs; LookAheadWall dashboard guide | Overview, Project Hub |
| One or two things big and bold; a grid of 12 equal tiles means nothing is read | LookAheadWall | Owner dashboard, Overview |
| Color means status only; never color alone (icon + label); about 1 in 12 men is red-green colorblind | LookAheadWall, PM Milestone | All pages (matches WCAG 2.2 AA in UX-09) |
| Every number drills down to underlying rows | LookAheadWall, Hunger Engine | UX-01 Owner dashboard, Cost reports |
| Patterns: Priority grid, Left-detail, balanced row | Dashboard pattern library | Overview, Project Hub, Platform |
| Approval screens use **master-detail**: queue left, document inline, decision actions plus workflow stepper plus audit trail right; reject needs a reason; show what bulk-approve skipped | Approvdit, SAP approve-PO app, TaxItEasy, Flux | Approval inbox (UX-08) |
| Same record at two altitudes: desktop 3-pane (list, detail, history); mobile single card with the 2 things the tech needs | Jobber design analysis (dezzayn), Jobber help | Mobile vs web |
| Mobile Home: map and **Up next**, then **To do** with urgent items first; explicit offline indicator; offline limited to new work (no edits of existing records, no signatures) | Jobber help, Jobber Offline Mode (Jan 2026) | Mobile Today, Sync centre (matches PRD SYNC-01) |
| Construction products pair BOQ line progress, Gantt, finances and daily reports in one project workspace with tabs | Spaceio+ Lens, Core (Tuskus), Dribbble construction dashboards | Project detail tabs |

References: Procore Project Overview; lookaheadwall.com dashboard design; thehungerengine.com pattern library; approvdit.com request detail view; community.sap.com approve-PO split screen; taxiteasy.org review queue; dezzayn.com Jobber; help.getjobber.com; Dribbble "Buildbone", "Schedule - Construction Management SaaS"; core.tuskus.com; spaceioplus.com.

## 3. Page inventory (what exists, by plane)

Planes per PRD §3.0 and ACC-01: Platform Admin, Company Admin and Employee/Operations have **distinct navigations**. Mobile hosts Employee/Operations only.

### 3.1 Employee / Operations (web)
| ID | Page | PRD | Release |
|---|---|---|---|
| W-01 | Owner dashboard | UX-01 | R1 |
| W-02 | My work (landing) | UX-03, MOB-04 Today parity | R1 |
| W-03 | Projects list | PROJECT-01 | R1 |
| W-04 | Project detail workspace (tabs) | UX-02 | R1 |
| W-05 | BOQ and contract baseline (+ revision diff) | BOQ-01..04, UX-06 later | R1 |
| W-06 | Daily report | OPS-01, PROJECT-03, UX-03 | R1 |
| W-07 | Lookahead (2 to 6 weeks) | LOOK-01/02, PLAN-01 | R1 |
| W-08 | Change events | CHG-01..05, RFI-01 | R1 |
| W-09 | Commercial workbench | UX-07 | R1 |
| W-10 | Measurement sheet | BILL-02, PROJECT-04 | R1 |
| W-11 | Certificate (deduction waterfall) | BILL-04, BILL-01 | R1 |
| W-12 | Invoice eligibility and allocations | BILL-03, 10, 11 | R1 |
| W-13 | Collections and retention | BILL-05..07 | R1 |
| W-14 | Requisitions, RFQ and quote comparison | PROC-01, 02, 10 | R1 |
| W-15 | Purchase orders and commitments | PROC-03, 06, 07 | R1 |
| W-16 | Receiving and three-way match | PROC-04, 07 | R1 |
| W-17 | Inventory and stock | PROC-05, 08 | R1 |
| W-18 | Labour and attendance | LABOUR-01, 02 | R1 |
| W-19 | Subcontract work orders | LABOUR-04, 06 | R1 |
| W-20 | Submittals register | SUB-01..03 | R1 |
| W-21 | Drawings, documents, transmittals | DOC-01..03 | R1 |
| W-22 | Inspections and nonconformances | QUAL-01..03 | R1 |
| W-23 | Safety records | SAFE-01 | R1 |
| W-24 | Approval inbox | UX-08, APR-01..04 | R1 |
| W-25 | Cost, EAC and reports | FIN-06, §4.3 | R1 |
| W-26 | Closeout and handover | PROJECT-05, HAND-01 | R1 |
| W-27 | Output preview (PO, certificate, report) | OUT-01/02 | R1/R2 |
| W-28 | Finance desk (GL, tax, close) | FIN-01..05 | **Use ERPNext Desk, not custom** (PRD 12.1) |

### 3.2 Company Admin (web)
| ID | Page | PRD |
|---|---|---|
| C-01 | Admin home (setup checklist, seats, devices, audit snippets) | §3.0 |
| C-02 | Company profile and **country/jurisdiction profile** | ACC-01, §3.0 |
| C-03 | Users and invitations | §3.0 |
| C-04 | Roles and permission matrix | §5 |
| C-05 | Project entitlements | ACC-01 |
| C-06 | Approval policies, thresholds, delegation | APR-01, APR-03 |
| C-07 | Modules and integrations | §3.0 |
| C-08 | Audit log | SEC-02 |
| C-09 | Devices and offline policy (lease length, revoke) | SYNC-02 |

### 3.3 Platform Admin (web)
P-01 Tenants list, P-02 Tenant detail (entitlements, licence, health), P-03 Licences, P-04 Platform health and backups/upgrades, P-05 Time-bound support access, P-06 Releases. Standalone installation uses the same console scoped to one installation (PRD §18). Never shows customer project ledgers.

### 3.4 Mobile (Employee/Operations only)
Navigation (MOB-04): **Today, Projects, Capture, Inbox, More**.
MOB-S01 organization connection, S02 sign-in and device registration, S03 project pack, S04 daily report, S05 camera and evidence, S06 drawings and submittals, S07 inspection/safety capture, S08 approvals (online only), S09 sync centre, S10 account/settings.

### 3.5 Shared
Login, SSO and MFA, organization switch, empty/error/denied/offline states for every page (UX-09).

### 3.6 Later releases (do not draw now)
UX-04 AI invoice review, UX-05 assistant, CRM (R3), payroll generation (R3), client/subcontractor portals (R4).

## 4. Layout pattern per page (one pattern per job, not one for all)

| Page | Pattern |
|---|---|
| W-01 Owner dashboard | Priority grid: one headline row (cash, contract, cost, EAC, certification backlog, overdue receivables, retention), approvals queue, then drill-down tables. Each figure: definition, period, currency, as-of |
| W-02 My work | Action queue: Up next, needs attention (sorted by urgency), quick create. No KPI wall |
| W-03 Projects | Filter bar plus table or card grid toggle; health shown as status label plus reason |
| W-04 Project detail | Header, tab bar (Scope/BOQ, Work packages, Reports, Materials, Labour, Changes, Measurements, Billing, Documents, Audit), summary strip, one main panel per tab. Filters persist across tabs (UX-02) |
| W-05 BOQ | Dense grid (spreadsheet style): code, description, unit, qty, rate, amount, breakup; revision selector and diff toggle |
| W-06 Daily report | Sectioned form: site/date/shift/unit, activities, quantities and units, labour, blockers, photos; draft/submission status; copied values visibly marked |
| W-07 Lookahead | Timeline grid by site, location, trade; blockers with owner and date; readiness flags |
| W-08 Change events | List plus detail: source, evidence, estimate, requested/approved/rejected/disputed amounts, notice clock |
| W-09 Commercial workbench | Segmented sections: change events, claims, certificates, invoice eligibility, disputes, retention. Each row: owner, next action, deadline, evidence (UX-07) |
| W-10 Measurement sheet | Spreadsheet grid: BOQ line, previous, submitted cumulative, certified cumulative, this period, evidence link, state |
| W-11 Certificate | Document layout with deduction waterfall: gross, variations, retention, advance recovery, other deductions, tax, net (BILL-04) |
| W-14..W-16 Procurement | Pipeline board (requisition, RFQ, PO, delivery, invoice) plus list; quote comparison matrix; receipt vs PO vs invoice three-column match |
| W-24 Approval inbox | **Three-pane master-detail**: queue left, document or evidence center, decision right (amount, budget impact, changed fields, policy version, stepper, audit trail, approve/reject with reason/hold) |
| C-04 Roles | Roles list plus permission matrix (rows modules, columns view/draft/authorize), scope and SoD warnings |
| C-02 Country profile | Settings form with left sub-navigation and form sections; no KPI cards |
| P-01/P-02 Tenants | Table with filters plus detail drawer; support grants are time-bound with expiry |
| Mobile Today | Up next card, to-do with urgent first, sync status chip |
| Mobile Capture | Role-based capture list, then a short form; offline banner; photo strip |
| Mobile Inbox | Approvals, returned work, information (three segments); decision disabled offline |
| Mobile Sync centre | Per-item states: queued, uploading, awaiting validation, synced, failed, conflict, access revoked, action required |

## 5. Content per page (key pages; fields from the PRD)

### W-01 Owner dashboard (UX-01)
Approved contract value; actual cost; remaining commitments; incomplete forecasts; pending recovery; certification backlog; overdue receivables; retention held and eligible; actionable approvals. Rule: cash surplus is never labelled profit. Each number: definition tooltip, period, currency, as-of time, drill-down.

### W-04 Project detail (UX-02)
Header: project ID, client, manager, status, location, dates. Tabs listed in §4. Summary strip: contract value, actual (A), committed (C), uncommitted (U), EAC, ETC (formulas per PRD §4.2/§4.3). Hidden tabs for modules the tenant does not have (API still enforces).

### W-05 BOQ (BOQ-01..04)
Columns: item code, description, normalized unit, quantity, rate, amount, material/labour/subcontract breakup, overhead. States: draft, submitted, approved, superseded. Approved baseline is read-only; edits create a revision. Variation claims: direction, scope, amount, evidence, approval chain; unapproved claim is excluded from the revised contract.

### W-06 Daily report (OPS-01, MOB-S04)
Site, date, shift, reporting unit; work packages; quantities with units; labour counts; material observations; blockers; photos; author. Notes are observations until verified. One approved report per tenant/project/site/date/shift/unit. Offline origin and operation ID shown in status.

### W-08 Change events (CHG-01..05)
Source type, instruction date, location, description, evidence, affected work, owner, estimated cost, incurred cost links. Amounts: requested, approved, rejected, disputed (separately). Notice due date and escalation. Close requires disposition and remaining actions.

### W-09 Commercial workbench (UX-07)
Sections: change events, submitted claims, certificates, invoice eligibility, disputes, retention. Row columns: reference, owner, state, amount, next action, deadline, evidence.

### W-10 / W-11 Measurement and certificate (BILL-02, 04)
Measurement states: draft, submitted, verified, returned, superseded. Certificate states: draft, submitted, partly certified, certified, rejected, disputed, corrected. Waterfall rows: gross work value, eligible variations, retention, advance recovery, other deductions, tax treatment, net amount. Submitted cumulative and certified cumulative quantities shown separately.

### W-12 Invoice eligibility (BILL-03, 10, 11)
Per certificate line: certified entitlement, posted net allocations, live draft reservations, remaining eligible. Allocation states: reserved, consumed, released, reversed. Idempotent create-invoice; duplicate request returns the existing invoice.

### W-13 Collections and retention (BILL-05..07)
Separate worklists: unpaid invoices, uncertified submissions, disputed amounts, overdue retention. Retention: held, eligible, requested, approved, invoiced, received. Every follow-up has an owner and next action.

### W-14..W-16 Procurement (PROC-01..10)
Requisition: site, quantity, needed-by, inventory check, budget code, duplicate flag. Quote comparison: scope equivalence, units, freight, tax basis, exclusions, warranty, delivery. PO: ordered, accepted, rejected, returned, invoiced, outstanding quantities. Receiving: batch, unit, date, discrepancy photo. Three-way match with tolerances; over-tolerance goes on hold with reason and owner.

### W-24 Approval inbox (UX-08, APR-01..04)
Left: queue with type, requester, amount, age, flags (over threshold, stale). Center: document or evidence. Right: amount, budget impact, changed fields since submission, policy version, delegation in effect, prior decisions, workflow stepper, audit trail; actions approve, reject (reason required), hold. Stale revision returns conflict with refresh. Self-approval blocked. Payment preparation, bank verification and payment authorization are separate screens.

### C-02 Country and jurisdiction profile
Country, currency and FX policy, tax templates, retention rules, fiscal calendar, timezone, statutory ID types, locale pack. Mutations are web-only (ACC-01).

### C-04 Roles and permissions (§5)
Roles: Owner, Finance manager, Accountant, Operations manager, PM, QS, Procurement, Site supervisor, ERP administrator. Matrix columns: read scope, may draft/edit, may authorize. SoD warnings: no self-approval, QS cannot approve own variation, ERP admin has no payment approval.

### P-01/P-02 Platform admin
Tenants: name, plan, region, status, seats, last health check. Detail: entitlements, licence term, backup status, upgrade channel, time-bound support grants (start, expiry, scope, approver). No access to customer ledgers.

### Mobile (MOB-S01..S10)
Content exactly as PRD §10.3. Every screen implements: loading, empty, denied, offline, expired lease, conflict, partial upload, validation, success.

## 6. States every page must show (UX-09)
Loading, empty, filtered-empty, validation, denied, stale/conflict, offline, partial upload, expired session, success. Keyboard focus visible, WCAG 2.2 AA, 44px mobile targets, tabular numerals, status never by color alone.

## 7. Proposed drawing order (after approval)
1. Approval inbox (W-24): the most structurally different page, proves the shell can host master-detail.
2. Project detail (W-04) with BOQ tab (W-05).
3. Commercial workbench (W-09) and certificate (W-11).
4. Owner dashboard (W-01) and My work (W-02).
5. Procurement (W-14..W-16).
6. Company Admin: roles matrix (C-04), country profile (C-02), users (C-03).
7. Platform Admin (P-01/P-02).
8. Mobile: Today, Capture, Inbox/approvals, Sync centre.

## 8. Figma organisation
One Figma page per area: `CIP Web · Employee`, `CIP Web · Company Admin`, `CIP Web · Platform Admin`, `CIP Mobile`, `CIP States`. Each screen is a named frame (`W-24 Approval inbox`). The earlier same-layout frames are archived on the page `Archive v1`.

## 9. Decisions needed from the sponsor
1. Approve this page list and drawing order (or reorder / cut).
2. Confirm that W-28 Finance desk stays ERPNext Desk (not custom drawn), per PRD 12.1.
3. Confirm the R1 page set is enough for the first drawing round (R2/R3 pages deferred).
4. Decide: buy Untitled UI PRO ($129) before drawing so sidebar, metrics, filters and page headers are official components.
