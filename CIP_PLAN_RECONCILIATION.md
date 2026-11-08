# CIP Plan Reconciliation

**Status:** Review draft for sponsor. Nothing in this document is approved, and it does not change any requirement.
**Prepared:** 7 November 2026 (machine clock, UTC).
**Scope of this pass:** reconcile planning documents and produce the design inventory. No application code was written. No Figma screens were created or edited. The 13 existing Figma frames are preserved.
**Companion documents:** `CIP_DESIGN_COVERAGE.md` (workflow inventory) and `CIP_DESIGN_SEQUENCE.md` (navigation and ordered design batches).

---

## 0. Governing rule used in this review

1. The last independently verified PRD, **v4.0**, governs. The sponsor-supplied position is that v4.0 is the last independently verified version. This review confirms only that v4.0 is the upload by `aliraza5786`; it cannot confirm the verification itself.
2. **v4.1 is treated as a set of proposed amendments.** Its changes are listed in section 2 and carry the IDs `PA-01`…`PA-11`. Where v4.0 and v4.1 differ, this review applies v4.0 and records the v4.1 wording as a proposal.
3. The plans (`WHOLE_SOFTWARE_BUILD_PLAN.md`, `RELEASE_PLAN.md`, `DEVELOPMENT_PLAN.md`) sequence and decompose the PRD. They may not redefine it. Anything in a plan that adds scope or changes behaviour is recorded in section 3 as a proposal.
4. The PRD files were **not edited** and no plan was rewritten to look compliant. Each plan gets a short pointer to this document and its text is otherwise unchanged.
5. Anything this review could not trace to a source is marked **UNRESOLVED**. No mapping, number or rule was invented to fill a gap.

---

**Amendment status.** PA-01…PA-11 remain pending. Work built on v4.0 (for example the B1 field-report journey) proceeds without approving them.

## 1. Source inventory

| Source | State found | Notes |
|---|---|---|
| `Construction_AI_ERP_Focused_Scope_PRD_v4.1.docx` | **Only PRD file in the working tree** | Added in commit `2818c77` by "Cursor Agent". |
| `Construction_AI_ERP_Focused_Scope_PRD_v4.docx` (v4.0) | **Not in the working tree. Recoverable from git history only** | Added in `f47c80f` by `aliraza5786`. The same commit `2818c77` deleted it. Read it with `git show f47c80f:Construction_AI_ERP_Focused_Scope_PRD_v4.docx > v4.docx`. |
| `WHOLE_SOFTWARE_BUILD_PLAN.md` | Read in full | 366 lines. |
| `DEVELOPMENT_PLAN.md` | Read in full | 463 lines. |
| `RELEASE_PLAN.md` | **Exists.** Read in full | 260 lines. Some earlier statements imply it did not exist yet (see D-03). |
| `docs/PAGE_SPECIFICATION.md`, `docs/DESIGN_APPROACH.md`, `docs/decisions/DEC-11-design-system.md`, `docs/evidence-register.md`, `docs/first-work.md`, `docs/r0-kickoff-checklist.md`, `README.md` | Scanned for IDs and framing | `PAGE_SPECIFICATION.md` is superseded by the three CIP documents. See D-18. |
| Figma `CIP-SASS` file, page "CIP SaaS Screens" (`10656:11704`) | Read-only audit of structure and text content | 13 top-level frames. Colour and prototype-reaction checks were **not** repeated. See section 7. |

PRD text was extracted from both `.docx` files (v4.0 from git) and compared line by line. Every requirement ID cited by the plans and docs was then checked against the PRD text. The results are in section 4.

---

## 2. PRD version control: v4.0 and v4.1

### 2.1 What exists and what approval evidence exists

| Question | Finding |
|---|---|
| Which PRD files exist in the workspace? | v4.1 only. v4.0 is recoverable from git. |
| Who authored v4.1? | Commit `2818c77`, "Reframe PRD as international ERP with clear access planes", authored by "Cursor Agent" (2026-11-06 20:08 UTC). It replaced v4.0 in the tree. |
| Is there an approval record for v4.1? | **None in the repository.** There is no change-control entry, no decision-register entry, no evidence-register entry and no sign-off. `docs/evidence-register.md` records only DEC-11 (design lock), not v4.1. |
| Was there a sponsor request? | A sponsor chat instruction prompted the edit. That chat is not in the repo. A chat instruction to draft is not approval of the resulting text, and it is unknown whether the sponsor reviewed the diff. |
| What does v4.1 itself say about approval? | v4.1 repeats the v4.0 rule: "Any change to price, scope, release or readiness status requires its evidence and approval record." No such record exists for v4.1. |
| Is v4.1 internally consistent? | **No.** It still keeps Urdu RTL in `V3-24` and Urdu/English in `UAT-11`, while its section 10.3 relaxes the Urdu requirement. See PA-06. |

**Limitation stated plainly:** no approval evidence for v4.1 is available to this review. The approved PRD (v4.0) governs until a sponsor-signed amendment exists.

### 2.2 Substantive v4.1 changes, recorded as Proposed Amendments

63 lines differ between v4.0 and v4.1. They group into 11 substantive changes. None is treated as approved.

| ID | v4.1 change | v4.0 text it changes or adds to | Effect on plans and design | Risk if adopted unreviewed |
|---|---|---|---|---|
| PA-01 | Product framed as international, with "phased market entry". The pilot's second independent company should "ideally" be in a second country. VAL-01 records country and prefers a contractor outside the first country. DEC-01 row reworded. | v4.0 §1: a Pakistan-contractor beachhead hypothesis. DEC-01: Pakistan building contractors. | Plans say "international" and treat country packs as a product concept. | Changes discovery sampling and the pilot gate. Segment and market entry are decision `DEC-01`. |
| PA-02 | Company carries a **country/jurisdiction profile**: currency defaults, tax/retention templates, fiscal calendar, timezone, document locale and statutory ID field definitions. | v4.0 §4.1: a company is a legal accounting entity. No profile is defined. | Adds WBS 5.4 and an admin screen. | Profile content (tax defaults) must not be authored without finance/legal sign-off. |
| PA-03 | New narrative section 3.0 "Access planes, desktop and mobile": Platform Admin, Company Admin, Employee/Operations. | v4.0 has roles in §5, administrator roles in COM-05, and provider access in TEN-03. It has no "plane" model. | The plans' three-plane model comes from here. | Merges vendor operations and standalone installation administration in one plane. See D-07. |
| PA-04 | `ACC-01 [R1 P0]`: distinct navigations per plane. Mobile hosts Employee/Operations only. Entitlement, country-profile, tax-template and licensing mutations are web-only. | New requirement ID. | Constrains mobile scope and where admin screens live. | New R1 P0 requirement with no approval. |
| PA-05 | `ACC-02 [R1 P0]`: one authenticated tenant context per session. | New requirement ID. | Affects org/server switching design. | New R1 P0 requirement with no approval. |
| PA-06 | §10.3 relaxed: "English/Urdu text" and "R2 field-navigation labels support Urdu RTL" become "English as the default UI language … at least one RTL locale in the pilot matrix **when that locale is sold**". | v4.0 §10.3 requires English/Urdu and Urdu RTL for R2 field navigation. | Plans drop Urdu and RTL for R2. See D-06. | **Weakens an approved requirement. Not approved.** |
| PA-07 | `MREL-04` guides: "English and Urdu" become "English plus each sold locale pack". | v4.0 MREL-04. | Field guides lose Urdu. | Weakens an approved R2 P0 deliverable. |
| PA-08 | §11 voice diary: "Urdu/English/code-switching" becomes "supported locale pairs". | v4.0 §11. | R3 only. | Low, but unapproved. |
| PA-09 | "CNIC" becomes "government ID" or "government/tax IDs" in §10.3, `AI-OPS-02` and `SEC-03`. | v4.0 wording. | Terminology only. | Low, but unapproved. |
| PA-10 | Owner-actions sentence changed to "beachhead countries and packaging" and "the international core data model". | v4.0 owner actions. | Narrative. | Low. |
| PA-11 | Front-matter: "What changed in version 4.1" replaces "What changed in version 4". The version banner is updated. | v4.0 summary of v4 changes. | The v4 change summary is no longer in the file. | Loses the v3→v4 change note. |

**Not changed by v4.1 (checked):** every `UAT`, `V3`, `BILL`, `SYNC`, `MOB-S`, `COM`, `TEN`, `LIC`, `DEP`, `PAR`, `PORT` and `DEC-01…09` ID, apart from the DEC-01 wording above. The Appendix A catalogue is also unchanged.

**What this means for the plans:** every plan lists v4.1 as "Requirements authority". That must read "PRD v4.0 (approved); v4.1 proposed amendments `PA-01…PA-11` pending approval". See D-05.

---

## 3. Discrepancy register

Each entry gives: source document and section, the PRD requirement or reference, the type (**conflict**, **omission** or **proposed extension**), the recommended correction, and the decision owner with the unresolved question. PRD references are to v4.0 unless marked.

### D-01 — WBS rows sum to 103, not 96 (arithmetic)

- **Source:** `WHOLE_SOFTWARE_BUILD_PLAN.md`, "Totals", "Count summary by step" and "Document control". Also `RELEASE_PLAN.md` §11 ("18/96/5").
- **PRD reference:** none. This is internal arithmetic.
- **Type:** conflict. The plan's own step tables list 103 task rows.
- **Evidence:** per-step counts 5, 5, 6, 6, 5, 5, 7, 7, 4, 7, 5, 5, 8, 5, 5, 6, 6, 6 give **103**. The plan's summary table adds to 96. 103 × 5 = **515** task-phases. Adding 6 campaigns × 5 = 30 gives **545** planning units, not 480 or 510.
- **Correction:** state 18 steps, **103 tasks**, **515 task-phases**, **30 campaign-phases** and **545 planning units**. If the splits and additions in section 5.3 are accepted the figures must be recomputed. The proposed recount is 116 / 580 / 610.
- **Decision owner:** product/BA lead.
- **Question:** are the splits and additions in section 5.3 accepted?

### D-02 — Release plan counts do not match its own lists

- **Source:** `RELEASE_PLAN.md` §1 and §10 compared with §2–§6.
- **Type:** conflict.
- **Evidence (counted from the lists, section 5.2):**

| Release | Plan claims | Lists actually contain |
|---|---|---|
| R0 | 12 | 19 task IDs (6 are precursors of R1 tasks) |
| R1 | 48 | **69** tasks, plus 3 system-test campaigns |
| R2 shared | +22 | 10 tasks new to R2, plus 8 R1 tasks re-listed for hardening (13.1–13.6, 13.8 and 18.3), so 18 distinct |
| R2S | +8 | 5 tasks (14.1–14.5), plus shared 18.6 and ST-E |
| R2L | +7 | 5 tasks (15.1–15.5), plus shared 18.6 and ST-E |
| R3 | +14 | 10 tasks plus ST-F |
| R4 | +6 | 2 tasks (17.5, 17.6) |

  Task 18.6 appears in three releases and 8.7 appears in none (see D-04).
- **Correction:** replace the claimed counts with the recomputed ones in section 5.2 and mark task re-use explicitly: "completes in R_n, evidence in R_m".
- **Decision owner:** product/BA lead.
- **Question:** should R0 "12" be restated as 19 precursor items?

### D-03 — Contradictory statements about whether release mapping is done

- **Sources and statements:**
  - `WHOLE_SOFTWARE_BUILD_PLAN.md` header: "Next step (later): Map this WBS onto releases." The same file's "Next planning action" says "Done: release plan … Now executing: R0 kickoff". The "Totals" section says releases "will later select subsets".
  - `RELEASE_PLAN.md` header: "Status: Active release map", while its counts do not match its lists (D-02).
  - `DEVELOPMENT_PLAN.md` §5 carries its **own** R1/R2/R3 scope lists. `RELEASE_PLAN.md` §11 calls the Development Plan "reconciled by this map". The two do not agree (D-13).
- **PRD reference:** none. PRD §2.2 and §16 own release allocation. The plans only sequence it.
- **Type:** conflict.
- **Correction:** one status for the mapping: **"Draft release map. Not reconciled: counts incorrect, 8.7 unmapped, R1 collections deferred against the PRD."** Replace "Done" and "Active" with this status until the section 5 corrections are accepted. The WBS "later" sentence should read "A draft map exists in `RELEASE_PLAN.md`."
- **Decision owner:** product sponsor.
- **Question:** who signs the release map as accepted?

### D-04 — R1 map omits tasks the PRD makes R1 P0; collections deferred against the PRD

- **Source:** `RELEASE_PLAN.md` §3.1 and §3.2. `DEVELOPMENT_PLAN.md` §5.2.
- **PRD reference:** §2.2 "Commercial control" (R1 pilot and R2 core): "verified measurement, certificates, reservations, **invoice/receipt links, retention, advances and corrections**". `BILL-05` receipts, `BILL-06` retention tracking and `BILL-07` collection worklists are all `[R1 P0]`. QA-02 requires "certification, invoice, receipt, reversal, period lock" in the R1 rehearsal. `UAT-05` needs correction and period lock. `UAT-03` needs concurrency.
- **Type:** conflict and omission.
  - `RELEASE_PLAN.md` §3.2 defers WBS 8.6 "collection worklists depth" to R2. The PRD has no R2 deferral for BILL-05/06/07.
  - WBS **8.7** (billing concurrency, correction, period-lock tests) is in **no** release list. It is only an R0 spike. R1 cannot meet its own acceptance pack without it.
- **Correction (proposed):** put 8.7 in R1. Split 8.6 into receipt and allocation (R1, BILL-05) and collection worklists (R1, BILL-07). Keep only "depth" items, such as scheduled exports, as R2 if the PRD supports that. Retention release (BILL-06) is R1.
- **Decision owner:** finance/QS lead with product sponsor.
- **Question:** is any part of collections genuinely R2? Nothing in the PRD says so.

### D-05 — Plans cite v4.1 as requirements authority

- **Source:** `WHOLE_SOFTWARE_BUILD_PLAN.md` header and Document control. `DEVELOPMENT_PLAN.md` header and §15. `RELEASE_PLAN.md` §11. `README.md`. `docs/PAGE_SPECIFICATION.md` (cites `ACC-01`).
- **PRD reference:** section 2 above. `ACC-01/02` exist only in v4.1.
- **Type:** conflict. The authority is an unapproved draft.
- **Correction:** authority line becomes "PRD v4.0 (governing); v4.1 changes tracked as proposed amendments PA-01…PA-11 in `CIP_PLAN_RECONCILIATION.md`." Pointer notices were added to each plan. Their bodies are unchanged.
- **Decision owner:** product sponsor.
- **Question:** approve, amend or reject each of PA-01…PA-11.

### D-06 — R2 Urdu field navigation, RTL and field guides dropped from the plans

- **Source:**
  - `DEVELOPMENT_PLAN.md` §5.3 "Localization: English GA; additional locale packs as entitlements".
  - `DEVELOPMENT_PLAN.md` §5.2 E6 "English UI; locale hook ready" (acceptable for R1).
  - `RELEASE_PLAN.md` R2 18.3 "KB + help expansion", with no Urdu field guide.
  - `WHOLE_SOFTWARE_BUILD_PLAN.md` 13.1 and 18.3 have no RTL or Urdu item.
  - None of the 13 Figma frames shows Urdu or RTL.
- **PRD reference (v4.0):**
  - §10.3: "English/Urdu text. **R2 field-navigation labels support Urdu RTL**, while mixed identifiers and numeric units remain readable and tested; full finance translation is a later localization pack."
  - `MREL-04 [R2 P0]`: "role-based quick-start guides in English **and Urdu**".
  - `V3-24 [R2]`: measured journeys "with **Urdu RTL**, screen readers, enlarged text…". v4.1 left this line unchanged.
  - `UAT-11` (R3): noisy Urdu/English report. §11 voice: "Urdu/English/code-switching".
  - `UX-09 [R1 P0]` requires every screen to specify its states, with 44px mobile targets.
- **Type:** conflict. The plans silently follow the unapproved PA-06/PA-07 relaxation.
- **Correction:**
  - Restore as governing: R2 mobile field navigation in English and Urdu with RTL; mixed Latin identifiers and numeric units tested inside RTL strings; English and Urdu quick-start guides.
  - Keep "full finance translation is a later localization pack" (v4.0 already says so).
  - Add to the design inventory (WF-MOB-14 and WF-MOB-15) RTL variants of the field navigation and the MOB-S01…S10 field screens.
  - Add a WBS task or sub-task for RTL and Urdu content (proposed, section 5.3).
  - Record PA-06 and PA-07 as pending, not applied.
- **Decision owner:** product sponsor and mobile lead.
- **Question:** has the sponsor explicitly approved dropping Urdu RTL for R2? If yes, record it through PRD change control and update `V3-24` and `MREL-04` together.

### D-07 — Administrative roles are conflated

- **Source:**
  - `DEVELOPMENT_PLAN.md` §1.2 and §2: Platform Admin = "Vendor (SaaS) **or** installation admin (standalone)".
  - `WHOLE_SOFTWARE_BUILD_PLAN.md` Step 2 "Platform Admin plane (vendor / installation)".
  - Existing frames: "Company Admin Home" shows an **approval queue**. "Overview" carries "Company admin" navigation next to a supervisor persona.
  - A customer billing administrator and the vendor's provider-billing and provider-operations staff are not distinguished.
- **PRD reference (v4.0):**
  - `COM-05`: customer organization administrator manages invitations, roles and approved integrations but **cannot bypass project finance segregation**. Customer billing administrator manages subscription and invoice contacts "without implicit payroll access". Provider billing staff see commercial metadata. Provider operations staff see health and provisioning status.
  - `TEN-03`: provider operations sees metadata, not payroll or project records. Support access is time-limited, purpose-bound and logged.
  - `APR-04`: "An application administrator has no implicit finance authorization".
  - §5: the ERP administrator has "No accounting payment approval".
  - `DEP-03`: in unmanaged standalone, the **customer** owns infrastructure, backups, keys and networking.
- **Type:** conflict (plans) and omission.
- **Correction:** separate five roles and surfaces plus the business roles. See section 6.1. In short:
  1. Vendor platform operations (SaaS only).
  2. Customer organization administration.
  3. Customer subscription and billing administration.
  4. Standalone installation administration.
  5. Operational and finance business roles.
  Standalone installation administration is the **customer's** role. It must not share a console with vendor SaaS control-plane staff. "Installation administrator" is a **proposed term**; the v4.0 PRD does not name it.
- **Decision owner:** product sponsor with the security lead.
- **Question:** do we keep two admin shells (vendor control plane vs customer installation console) or one shell with entitlement-gated modules? v4.1 PA-03 chose one plane, which is unapproved.

### D-08 — "International-ready" is presented as "validated countries at launch"

- **Source:**
  - Existing Figma "Country Settings" (`10651:2350`): "United Arab Emirates profile", "VAT 5% Standard rated", "Tax and e-invoicing: Configured, Done (4)". "Company Admin Home" repeats "UAE · AED". Fixtures read as a configured, validated pack.
  - `DEVELOPMENT_PLAN.md` §11: "Country pack | After jurisdiction content exists" as a priced offer line.
  - `DEVELOPMENT_PLAN.md` §1.2: "International core + country/jurisdiction packs".
  - `RELEASE_PLAN.md` R1 5.4 "Country model".
- **PRD reference (v4.0):**
  - DEC-01 is still **Pakistan building contractors**, proposed and unvalidated.
  - Worked examples are PKR.
  - `COM-02` lists bundles as Core Construction, Operations Plus and Enterprise Options, with AI as a metered add-on. There is **no country-pack SKU or price**.
  - `SP-06` and `DEC-07` own pricing evidence.
  - §2.2 and `DEC-02` require finance-approved policy. The PRD invents no tax defaults.
- **Type:** conflict and proposed extension.
- **Correction:** use three explicit levels everywhere (UI badges, plans, quotes):

| Level | Meaning | Evidence needed |
|---|---|---|
| **Architecture-ready** | The data model carries currency, tax templates, fiscal calendar, timezone, locale and ID types as configuration. | R0 schema decision (WBS 5.4). |
| **Pack available** | Reviewed content exists for one jurisdiction. | Finance/legal review recorded. |
| **Validated at launch** | Pack used in a pilot or launch with local finance sign-off and UAT. | Evidence-register entry per country. |

  The UAE screen must be relabelled **"sample profile, not a validated pack"** or shown unconfigured. The design must not display tax rates, e-invoicing status or statutory ID types as facts unless they come from a reviewed pack. Country-pack pricing is **a proposal**. Record it under `SP-06`/`DEC-07`, not as a requirement.
- **Decision owner:** product sponsor (DEC-01) with the commercial lead (DEC-07).
- **Question:** which country is validated first? Which pack content is reviewed, and by whom?

### D-09 — Observed progress, verified measurement, certified work, invoice eligibility, posted invoice and payment are blurred

- **Source:** `RELEASE_PLAN.md` R1 spine ("measurement → certificate → allocation → invoice link"). `DEVELOPMENT_PLAN.md` §1.1. Figma "Commercial Workbench" (`10645:1044`).
- **PRD reference:**
  - `BILL-02`: measurement states draft, submitted, verified, returned or superseded. Certificate states draft, submitted, partly certified, certified, rejected, disputed or corrected.
  - `BILL-03`: billable increment = current eligible cumulative certification − previously invoiced eligible.
  - `BILL-05`: posted invoices and receipts remain distinct from certificates.
  - §4.2 definitions: **Certified value** is distinct from claims, invoices and revenue recognition. **Billed amount** is posted sales invoices less credit notes. **Recognized revenue** is never inferred from certification or cash.
  - §10.2 offline authority table: attendance, delivery and measurement from the field are "nonbinding observation or draft" and "no automatic payroll/stock/certification".
  - `BOQ-04`: an unapproved claim is excluded from the revised signed contract.
- **Type:** conflict (design) and omission (plans).
- **Correction:** adopt one vocabulary (section 6.2). Each term maps to one object, one set of states and one actor. Labels must be exact. A draft certificate says **"Claimed, not certified"**. "Certified" appears only on certified lines. See E-01.
- **Decision owner:** finance/QS lead.
- **Question:** confirm the exact label strings and the tax basis shown for each amount (signed contract value "displays tax basis explicitly").

### D-10 — Safety, subcontract controls, collections, retention release, petty cash, close and reconciliation are not explicit tasks

- **Source:** `WHOLE_SOFTWARE_BUILD_PLAN.md` Steps 7, 8, 10 and 11. `RELEASE_PLAN.md` throughout.
- **PRD reference and gap:**

| Area | PRD | WBS coverage found | Gap |
|---|---|---|---|
| Safety | `SAFE-01 [R1 P0]`; `SAFE-02 [R2 P0 / R3 permits]`; §10.2 "inspection/safety reporting: draft only offline"; `MOB-S07` | 7.6 "Inspections / NCR / quality gates" only | **No safety task.** |
| Subcontract controls | `LABOUR-06 [R1 P0]`: basis, scope ceiling, certified quantities, retention, deductions, variations; submission vs verified quantity vs approved certificate vs payable; reversals via correction documents | 10.7 one line "work orders, certification, retention" | Under-specified. |
| Collection | `BILL-07 [R1 P0]` four separate worklists | 8.6 "Receipts allocation & collection worklists", deferred to R2 | Deferred against PRD (D-04). |
| Retention release | `BILL-06 [R1 P0]`; `HAND-02 [R2]` links release eligibility to defect-liability conditions | 8.5 "display & balances" only | Release workflow missing. |
| Petty cash | `FIN-04` core requirement; Appendix A exception "Petty cash receipt submitted twice" | **None** | No task. |
| Month close and period lock | `FIN-05`; `UAT-05`; `QA-02` | **None** | No task. |
| Reconciliation | `FIN-06`, `FIN-02`, `MIG-02/03`, `UAT-12`, `MET-01` | 11.5 reporting tests, 18.1 migration | Finance reconciliation and sign-off workflows not explicit. |
| Payments | `APR-04` prepare, verify bank details, authorize as separate actions; `PROC-09` | **None** | No task. |
| Alerts | `ALT-01 [R1 P0]` lifecycle | 9.3 "exposure dashboard" | Alert lifecycle missing. |
| Outputs | `OUT-01 [R1]`, `OUT-02 [R2]` | Bundled in 7.7 | Not separable. |
| Closeout | `PROJECT-05`, `HAND-01` (R1), `HAND-02` (R2) | 7.7 "handover checklist" | Defect liability and final bill missing. |

  **Release caveat:** §6 says core functions are R1 P0 "within the section 2 package". The §2.2 table does not name petty cash. `QA-02` and `UAT-05` do name period lock. So FIN-04 placement is **UNRESOLVED** and FIN-05 is R1.
- **Type:** omission.
- **Correction:** proposed additions are in section 5.3. The workflows are explicit in `CIP_DESIGN_COVERAGE.md`.
- **Decision owner:** finance/QS lead (FIN, BILL), operations/qualified leads (safety, `DEC-06`).
- **Question:** does R1 include petty cash? Who owns safety, and is it native or an integration (`SAFE-01` onboarding choice)?

### D-11 — Reference verification: non-PRD IDs in the plans

- **Source:** all plan and docs files scanned.
- **Result:** 90 distinct requirement, decision, test and spike IDs were checked against the PRD text. **87 resolve to the PRD.** Three do not:

| Cited ID | Where | Finding |
|---|---|---|
| `DEC-10` "GTM website scope" | `DEVELOPMENT_PLAN.md` §13 | **Plan-local.** The PRD register ends at DEC-09. |
| `DEC-11` "Design references and component library lock" | `README.md`, `docs/*`, `evidence-register.md` | **Plan-local.** Collides with the PRD namespace. |
| `ACC-01` | `docs/PAGE_SPECIFICATION.md` | Exists **only in v4.1** (PA-04). |

  Other references to check by hand: `RELEASE_PLAN.md` R3 gate "UAT CRM" is not an ID (no `UAT-CRM` exists; the PRD has `CRM-01…03` with acceptance text only). All `UAT-01…16` and `V3-01…24` and every `DEC-01…09` reference resolved.
- **Type:** conflict (namespace) and unresolved mappings.
- **Correction:** rename plan-local decisions to a separate namespace (for example `LD-01`, `LD-02`), or file them as PRD amendments. Cite `CRM-01…03` acceptance text for the CRM gate. Mark `ACC-01` as v4.1-only.
- **Decision owner:** product/BA lead.
- **Question:** adopt the `LD-nn` namespace?

### D-12 — Gate language: R2S, R2L and dual-mode are blurred

- **Source:** `DEVELOPMENT_PLAN.md` §5.3 "R2 exit gate" is a single list. `RELEASE_PLAN.md` §4.4 omits the signed product schedule. 18.6 and ST-E appear in several columns.
- **PRD reference (v4.0 §16 gate table):**
  - **R2S SaaS launch** (shared core/mobile acceptance, tenant isolation/load, billing/entitlements, export/offboarding, support/security readiness, pricing and legal review). Decision authority: product, security, operations and commercial.
  - **R2L standalone launch** (shared core/mobile acceptance, installation/upgrade/recovery, offline licensing, OSS/source fulfilment, customer operating guide, support matrix). Decision authority: technical, licensing reviewer and commercial.
  - **Dual-mode claim:** "R2S and R2L evidence **plus tested migration both ways**; **signed product schedule** accurately states differences". Decision authority: product sponsor.
  - Shared production mobile gates: `MOB-*`, `SYNC-01…08`, `MAPI`, `MSEC`, `PUSH`, `MREL`, `MTEST`, `V3-17…24`.
- **Type:** conflict (loses independence and the dual-mode condition).
- **Correction:** keep **three independent gates** plus **one shared gate** (core and production mobile). A mode may launch when shared plus its own gate pass. **Dual-mode availability** may be claimed only when all of these hold: R2S evidence, R2L evidence, `V3-14` portability passed **in both directions** (`PORT-01/02`) and a signed product schedule describing differences (`PAR-01/02`, `COM-01`). Quotes and UI must not show "SaaS + standalone" before then. Modules not yet released do not appear as available in quotes (§17.2).
- **Decision owner:** product sponsor.
- **Question:** who is the named licensing reviewer and the security approver for each gate (assign before R0)?

### D-13 — Development Plan and Release Plan disagree on R1 build order

- **Source:** `DEVELOPMENT_PLAN.md` §5.2 vertical slice. `RELEASE_PLAN.md` §3.1 spine order and §8.
- **Conflict:** the Development Plan builds change events (step 6) **before** certificate and allocation (step 7). The Release Plan builds measurement/certificate/billing (8) → cost (11) → change (9) → procurement (10).
- **PRD reference:** §17.1: "The first implementation increment must connect one field report through measurement to an eligible invoice and reconciled cost view." Change events are R1 P0, but the PRD does not order them before billing.
- **Correction:** adopt the PRD §17.1 spine as the order: **report → measurement → certificate → invoice eligibility → cost view**, then change, then procurement. Update `DEVELOPMENT_PLAN.md` §5.2 (proposal).
- **Decision owner:** tech lead and finance/QS lead.
- **Question:** confirm the order.

### D-14 — R1 mobile scope in the Release Plan exceeds the PRD; mobile tab label differs

- **Source:** `RELEASE_PLAN.md` R1: 13.1–13.6 as "P0 beta" (shell, auth and org/server switch, lease/outbox, sync, capture, conflicts). Figma "Mobile Today" tab bar "Today · Projects · Capture · **Approvals** · More".
- **PRD reference:** §2.2 Mobile: "R1 diary/evidence, downloaded drawings, inspection drafts and sync centre on iOS/Android. **R2 expands to section 10 core roles**". `MOB-04 [R2 P0]`: navigation is "Today, Projects, **Capture, Inbox** and More, with labels finalized in usability testing". `MOB-S10`/`V3-20` org/server switching is R2. `MOB-S08` approvals are online-only.
- **Type:** conflict (mild) and proposed extension.
- **Correction:** R1 beta covers: capture, drawings, inspection drafts, sync centre, plus whatever lease and outbox they need. Organization and server switching, push and the full MOB-04 navigation are R2. The Figma tab label becomes **"Inbox"** (PRD wording) until usability testing changes it. Approvals live inside Inbox, online only.
- **Decision owner:** mobile lead.
- **Question:** is R1 mobile single-organization? (Assumed yes, per R1 "one legal entity".)

### D-15 — Capacity model in the Platform Admin design differs from COM-03

- **Source:** Figma "Platform Admin Tenants" (`10651:2571`): "Seats licensed 9,840, 92% utilised"; "Company Admin Home": "48 / 52 seats".
- **PRD reference:** `COM-03`: proposed capacity measures are **active projects, named back-office users and storage**. "Field participation is included within a declared fair-use envelope to avoid discouraging reporting."
- **Type:** proposed extension.
- **Correction:** show capacity as the three COM-03 measures, with field participation in an envelope rather than seats. Mark as proposed (COM-03 is "proposed"). Resolve the Figma seat arithmetic (E-07).
- **Decision owner:** commercial lead.
- **Question:** are named seats or the COM-03 measures the metered unit (`SP-06`, `DEC-07`)?

### D-16 — No region or data-residency decision for provisioning

- **Source:** the provisioning design needs a region choice.
- **PRD reference:** `SEC-03` says "review residency/processing terms". `DEP-06` says residency settings are deployment-scoped. No region list exists.
- **Type:** omission (**UNRESOLVED**, not invented).
- **Correction:** the provisioning screen shows region as an unresolved field.
- **Decision owner:** security/operations lead.
- **Question:** which regions, if any, ship at R2S?

### D-17 — Approval-policy authority is not named

- **Source:** `WBS` 3.3 "Approval policies & delegation" in Company Admin.
- **PRD reference:** `APR-01`: effective-dated rules; "illustrative thresholds from v1 are not approved production policy". §5: the ERP administrator provisions permission and has no approval rights. The PRD names no single policy author.
- **Type:** omission (**UNRESOLVED**).
- **Correction:** design the policy screen as author, review, activate with an effective date and an audit trail. Do not pre-fill thresholds.
- **Decision owner:** product sponsor and finance manager.
- **Question:** who authors and who approves a policy change? The requester cannot approve their own change.

### D-18 — `docs/PAGE_SPECIFICATION.md` is superseded

- **Source:** `docs/PAGE_SPECIFICATION.md` (commit `a460045`).
- **Issues:** it relies on v4.1 `ACC-01`; assigns pages to the three-plane model; includes "W-28 finance desk = ERPNext Desk" without the PRD §12.1 caveat that Desk use is a proposal to validate; tags R-levels without checking the §2.2 table.
- **Correction:** a pointer banner was added. The three CIP documents replace it.
- **Decision owner:** product/BA lead.

---

## 4. Reference verification summary

| Check | Result |
|---|---|
| IDs cited across plans and docs | 90 distinct |
| Resolve to PRD text (v4.0 or v4.1) | 87 |
| Exist only in v4.1 | `ACC-01` (also `ACC-02` defined there) |
| Plan-local, not in PRD | `DEC-10`, `DEC-11` |
| Not an ID | "UAT CRM" (RELEASE_PLAN R3) |
| `UAT-01…16`, `V3-01…24`, `DEC-01…09` | All cited items resolve |
| R1 acceptance pack in `DEVELOPMENT_PLAN.md` §5.2 | Matches PRD `QA-01` and `QA-02` (UAT-01–08, 12–13, 15 manual, 16; V3-01, 02, 04, 06, 17 beta) |
| R2 exit "V3-07…16 and V3-18…24" | Consistent with Appendix C tags (V3-17 is R1 beta and R2) |
| `V3-03` R3 lump-sum | Consistent. R1 reservation concurrency is `UAT-03`/`SP-01` |
| `V3-05` transmittal evidence is R2 | Release Plan puts transmittals (7.7) in R1. `DOC-03` is R1, `OUT-02` and `V3-05` are R2. Treat as R1 build, R2 acceptance |
| Appendix A | 84 exceptions in 7 families: CRM, BOQ, PROC, LABOUR, ACCOUNTING, AI, SECURITY. Individual `EC-` IDs are cited by family only in the coverage file |

No requirement, decision, UAT or V3 mapping was invented. Unresolved items are marked **UNRESOLVED**.

---

## 5. Corrected arithmetic and release map (proposal)

### 5.1 WBS recount

| Step | Tasks |
|---|---|
| 1 Program setup | 5 |
| 2 Platform admin | 5 |
| 3 Company admin | 6 |
| 4 Identity and security | 6 |
| 5 Masters, country packs | 5 |
| 6 BOQ and contract | 5 |
| 7 Site and documents | 7 |
| 8 Measurement and billing | 7 |
| 9 Change events | 4 |
| 10 Procurement, labour, subcontract | 7 |
| 11 Cost and reporting | 5 |
| 12 API and web shell | 5 |
| 13 Native mobile | 8 |
| 14 SaaS lifecycle | 5 |
| 15 Standalone and portability | 5 |
| 16 AI | 6 |
| 17 Later depth | 6 |
| 18 QA, migration, GTM | 6 |
| **Total** | **103** |

103 tasks × 5 phases = **515**. 6 campaigns × 5 phases = **30**. **Planning units = 545.**

### 5.2 Release map as listed (counted mechanically from `RELEASE_PLAN.md`)

| Release | Distinct tasks listed | Notes |
|---|---|---|
| R0 | 19 | Precursors and spikes. Do not add to totals. |
| R1 | 69 (+ ST-A, ST-B, ST-C) | Plan claimed 48. |
| R2 shared, new | 10: 2.3, 2.4, 2.5, 3.5, 3.6, 8.6, 13.7, 18.2, 18.5, 18.6 | Plus 8 R1 tasks re-listed for hardening (13.1–13.6, 13.8, 18.3). Plan claimed 22. |
| R2S | 5 (14.1–14.5) | Plus shared 18.6 and ST-E. Plan claimed 8. |
| R2L | 5 (15.1–15.5) | Plus shared 18.6 and ST-E. Plan claimed 7. |
| R3 | 10 (16.1–16.6, 17.1–17.4) | Plus ST-F. Plan claimed 14. |
| R4 | 2 (17.5, 17.6) | Plan claimed 6. |
| GTM | 18.4 | Not a PRD requirement (see D-03 and the coverage file). |
| **Unmapped** | **8.7** | In no release list. |

Distinct tasks assigned: 69 + 10 + 5 + 5 + 10 + 2 + 1 = 102. With 8.7 unmapped the total is 103.

### 5.3 Proposed WBS additions and splits (not applied)

Recompute if any change is rejected. Applying all of them gives **116 tasks, 580 task-phases and 610 planning units**.

| Change | Reason (PRD) | Net |
|---|---|---|
| Split 8.6 into 8.6a receipts/advances allocation and 8.6b collection worklists. Both R1. | `BILL-05`, `BILL-07` | +1 |
| New 8.8 Retention release and defect-liability linkage | `BILL-06`, `HAND-02` | +1 |
| Split 10.7 into 10.7a work order and scope ceiling, 10.7b submission → verified → certificate → payable, 10.7c retention, deductions, variations and reversals | `LABOUR-06`, `LABOUR-04` | +2 |
| New 7.8 Safety records (R1) with SAFE-02 status references (R2) | `SAFE-01/02` | +1 |
| New 7.9 Output templates and preview | `OUT-01/02` | +1 |
| New 7.10 Closeout, final bill and defect liability | `PROJECT-05`, `HAND-01/02` | +1 |
| New 11.6 Alert lifecycle | `ALT-01` | +1 |
| New Step 19 Finance operations: 19.1 attribution and ledger reconciliation configuration | `FIN-01/02/06` | +1 |
| 19.2 Supplier onboarding and payment preparation/authorization separation | `PROC-09`, `APR-04` | +1 |
| 19.3 Site petty cash | `FIN-04` (placement UNRESOLVED) | +1 |
| 19.4 Month close and period lock | `FIN-05`, `UAT-05` | +1 |
| 19.5 Finance reconciliation reports and opening-balance sign-off | `FIN-06`, `MIG-02/03`, `UAT-12` | +1 |
| Urdu/RTL field navigation and guides: add as acceptance items on 13.1, 13.6 and 18.3, not new tasks | `§10.3`, `MREL-04`, `V3-24` | 0 |
| **Total** | | **+13** |

Also proposed: assign **8.7 to R1**, and move 8.6a, 8.6b and 8.8 to R1.

---

## 6. Separated terms

### 6.1 Administrative and business roles

| Role | Surface | Scope | May | Must not | PRD basis |
|---|---|---|---|---|---|
| **Vendor platform operations** (provider operations staff) | Vendor control plane, **SaaS only** | Tenant health, provisioning status, entitlement and metering metadata | Provision, suspend, run recovery, request time-bound support access | See project ledger, payroll or project records by default. Approve customer payments. Rewrite project financials. | `TEN-03`, `COM-05` |
| **Vendor billing staff** (provider billing) | Vendor control plane, SaaS only | Commercial metadata only | Manage subscription, invoices, payment verification | Read project data | `COM-05`, `BIZ-01` |
| **Customer organization administrator** | Company admin | The customer's own organization | Invitations, roles, project entitlements, module settings, approved integration settings, audit visibility | Gain approval rights from administrative access alone. Bypass project-finance segregation. | `COM-05`, `APR-04`, §5 ERP administrator |
| **Customer billing administrator** | Subscription and invoices (SaaS) | Subscription and invoice contacts | Update contacts, review plan, capacity and invoices | Payroll access. Project data. | `COM-05`, `BIZ-01/02` |
| **Standalone installation administrator** *(proposed term)* | Installation console, **standalone only**. Run by the **customer** | The customer's installation: infrastructure, keys, backups, licence, upgrades | Install, activate licence, back up and restore, upgrade, connect mobile | Be the vendor. Approve finance. | `DEP-01…06`, `LIC-03/04/05`, `PORT` |
| **Operational business roles** | Employee/Operations | Assigned projects | Owner, operations manager, PM, QS, procurement and site supervisor per §5 | Gain rights from an admin menu | §5 |
| **Finance business roles** | Employee/Operations plus ERPNext Desk | Finance scope | Finance manager and accountant per §5 | Self-approve vendor setup and payment | §5, `APR-04` |

**Rule:** administrative access confers no implicit business approval rights. Approving, certifying and releasing are business-role actions bound to a revision and a policy version. A user who separately holds an authorized business role may act in it, and permission checks and segregation of duties still apply.

### 6.2 The billing chain, in design vocabulary

| # | Term | Object and states | Actor | What it is **not** | PRD |
|---|---|---|---|---|---|
| 1 | **Observed progress** | Site-reported quantity in a daily report or mobile draft. Nonbinding. | Site supervisor | Not measured, not billable | `OPS-01`, §10.2 |
| 2 | **Verified measurement** | Measurement: draft → submitted → verified / returned / superseded | QS verifies | Not certified | `BILL-02` |
| 3 | **Certified work** | Certificate line: draft → submitted → partly certified → certified / rejected / disputed / corrected. **Certified value** is cumulative authorized amount. | Authorized certifier | Not claimed, invoiced or revenue | `BILL-02`, §4.2 |
| 4 | **Invoice eligibility** | Eligible cumulative certification − previously invoiced eligible. Allocations: reserved, consumed, released, reversed. | System; QS and finance act | Not posted | `BILL-03`, `BILL-10/11` |
| 5 | **Posted invoice** | ERPNext sales invoice. **Billed amount** = posted less credit notes. Drafts shown separately. | Finance posts | Not revenue recognition | `BILL-03`, `FIN-03`, §4.2 |
| 6 | **Payment** | Receipt (partial, on-account or allocated). Separate from the invoice. | Finance | Not certification | `BILL-05` |
| — | **Claimed / submitted** | Claim or "uncertified submission" amounts | Contractor | Never shown as certified | `BOQ-04`, `BILL-07`, `CHG-03` |
| — | **Recognized revenue** | Posted under the approved recognition policy | Finance | Never inferred from certification or cash | §4.2 |

Invariant to display and test: posted allocations + live reservations + remaining eligible = net entitlement (`BILL-11`).

### 6.3 Availability levels (international-ready vs validated)

See D-08. A UI badge, quote line or plan statement uses exactly one of: **Architecture-ready**, **Pack available**, **Validated at launch**.

---

## 7. Existing Figma page audit (read-only)

File `nW0n4I3aarR2CqvEt9d9ZY`, page "CIP SaaS Screens" `10656:11704`. 13 frames: eleven desktop frames of 1440×1500 and two mobile frames of 390×844. All 13 are **preserved**. The audit read frame structure and text. The findings below are checked against that text. Items marked *owner-reported* come from the sponsor's review and were not re-verified here.

| ID | Frame (node) | Finding | Correction | Batch |
|---|---|---|---|---|
| E-01 | Commercial Workbench `10645:1044` | A **draft v3** payment certificate shows "Gross certified AED 4.82M". Certificate preparation is mixed with invoice reservation: "Billing allocation: Allocated to PC-07 4.82M, Reserved (22), Released (4)". Released lines count inside "Allocated". | Split certificate preparation from invoice eligibility/reservation. Draft shows **Claimed / Verified / Certified** as separate columns. "Certified" only after certification. | B2, B3 |
| E-02 | Project Hub `10645:477` | A + C + U = 21.6 + 9.8 + 12.7 = 44.1 matches EAC. The "Actual" bar splits 21.6 posted and 26.6 remaining. 21.6 + 26.6 = 48.2 which is **contract value, not approved budget**. **Forecast variance (approved budget − EAC) is not shown.** "Revised +1.4M approved" leaves unclear whether 48.2M includes it. | Bars use approved budget as the denominator. Show budget − EAC with sign, as-of time and tax basis. State the contract-value basis. | B11 |
| E-03 | Projects `10651:1466` | "At-risk projects: 1 over budget" vs "Projects on track 9 of 12 / Off track (3)" vs "Programme delay 3 projects". "Budget committed AED 98M" beside "Open (190M)" mixes denominators. | One status definition per metric. Counts reconcile to drill-down (`MET-01`, `UX-01`). | B11 |
| E-04 | Overview `10651:1245` | A supervisor/PM "My day" page sits in the same shell that carries "Company admin", "Users & roles" and "Settings". Layout is cards → bars → table. | Role home inside an employee shell. Task-shaped work queue, not progress bars. | B1, B4 |
| E-05 | Company Admin Home `10623:841` | An **approval queue** (7 pending) and "Offline sync health" appear on the admin plane. | Admin home shows administration items only. Approvals stay in the business-role inbox. | B13 |
| E-06 | Approvals `10651:1908` | Grouped bars by request type. No evidence, changed fields, policy version or budget impact. "Daily reports" listed as an approval type although they are accepted or returned. | Master-detail review (`UX-08`). Daily reports go to a review queue, not the approval queue. | B4 |
| E-07 | Users and Roles `10651:2129` | Seat arithmetic: "48 of 52 seats used" while the role bars are 22 + 12 + 8 + 6 = 48 with active 20 + 12 + 7 + 6 = 45 and invited 3. Roles shown omit owner, operations manager, procurement, accountant and ERP administrator. | Define whether invited users take seats (D-15). Show all §5 roles. | B13 |
| E-08 | Country Settings `10651:2350` (frame; `10651:2351` is its Sidebar child) | UAE, AED, "VAT 5% Standard rated", "Tax and e-invoicing: Configured" and "Asia/Dubai" read as a validated pack. | Relabel "sample profile". Show unconfigured and unreviewed states (D-08). | B13 |
| E-09 | Daily Report `10645:1265` | Header reads "Submitted by Jonas Weber · **Draft**". The page is a read-only progress summary. There is no entry form and no return or amend flow. "Done / Remaining / Behind plan" mix three meanings. | Separate entry, review and amendment screens (`OPS-01`, `PROJECT-03`). One state at a time. | B1 |
| E-10 | Platform Admin Tenants `10651:2571` | "Seats licensed 9,840, 92% utilised". Capacity model differs from `COM-03` (D-15). Only a list exists. Provisioning, support grants and entitlements are not designed. | Capacity measures per `COM-03`. Add the real workflows. | B15 |
| E-11 | Mobile Today `10646:1231` | Tab bar reads "Approvals". PRD `MOB-04` says **Inbox**. | Rename to Inbox (D-14). | B14 |
| E-12 | Mobile Capture `10646:1322` | "Offline. **Saved to outbox** and syncs when connected" appears **before** a save. | Three separate states: *Saved on this device*, *Uploading*, *Accepted by server* (`MOB-S09`, `SYNC-05`). Do not say "saved" until saved. | B1 |
| E-13 | Procurement `10651:1687` | Commitments by cost-code group mix POs and subcontracts. "Invoices to match: Three-way match" has no match editor. Subcontract "Certified / Retained" has no certification state flow. | Register plus editor. Separate subcontract certification (`LABOUR-06`). | B8, B9 |
| E-14 | All 13 | Same card → bars → table pattern on every page. Same shell on employee, admin and platform pages. *Owner-reported:* progress bars whose maths do not match labels, and red used for success. No prototype connections or recovery paths were audited. | Task-shaped layouts per batch. Semantic colours. Real prototype links. | All |

---

## 8. Decisions needed from the owners

| # | Decision | Owner |
|---|---|---|
| 1 | Approve, amend or reject PA-01…PA-11, **before** any plan cites v4.1. | Product sponsor |
| 2 | Is R2 Urdu RTL field navigation and the English/Urdu guide still required (v4.0 says yes)? | Product sponsor, mobile lead |
| 3 | One admin console or separate vendor control plane and customer installation console? | Product sponsor, security lead |
| 4 | First validated country and who reviews its pack (DEC-01). May fixtures show a named country? | Product sponsor, finance/QS |
| 5 | Is collections/receipt worklist depth really R2? (PRD says R1.) | Finance/QS lead |
| 6 | Is petty cash (FIN-04) in the R1 package? | Finance/QS lead |
| 7 | Safety ownership and native vs integration (`SAFE-01`, DEC-06). Who is the safety role? | Operations/qualified leads |
| 8 | Who authors and approves approval-policy changes (`APR-01`)? | Sponsor, finance manager |
| 9 | Label strings for the billing chain and the tax basis shown (DEC-02). | Finance/QS lead |
| 10 | Retention-release authority and defect-liability conditions (`BILL-06`, `HAND-02`). | Finance/QS, operations |
| 11 | Do invited users consume capacity? Are seats or `COM-03` measures metered (`SP-06`, `DEC-07`)? | Commercial lead |
| 12 | Which regions exist for provisioning (`SEC-03`, `DEP-06`)? | Security/operations |
| 13 | Is the Desk-reuse boundary of PRD §12.1 accepted for finance screens? (The PRD marks it "proposed … validate".) | Tech lead, finance |
| 14 | Mobile tab label "Inbox" vs "Approvals" (`MOB-04` leaves final labels to usability testing). | Mobile lead, UX |
| 15 | Rename plan-local `DEC-10/11` to a separate namespace (for example `LD-nn`). | Product/BA lead |
| 16 | Accept the WBS recount and the section 5.3 additions (116 / 580 / 610), or reject them. | Product/BA lead |
| 17 | Is a document controller, QA inspector or safety officer a named role? The PRD §5 table has none. | Operations/qualified leads |

---

## 9. Limitations of this review

- v4.0 text was read from git history, not from the workspace. A reader must extract it with the command in section 1.
- v4.0's "independent verification" is the sponsor's statement. It is not independently re-verified here.
- The Figma audit covered frame structure and text. Colour semantics and prototype connections were not rechecked.
- No external source was consulted. ERPNext behaviour is not validated. PRD §13.6 puts that validation in R0.
- The figures in section 5 are counts from the documents. They are not effort estimates.
- No application code was written and no Figma screens were created. The design plan is a proposal for review. **The software design and implementation are not complete.**
