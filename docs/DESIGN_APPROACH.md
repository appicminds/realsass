# Professional Design Approach (mandatory)

**Status:** Proposed standard for this project — **no production UI until the Design Gate passes**.  
**Date:** 07 November 2026 (Asia/Karachi)  
**Why:** Avoid one-off “AI invents screens” work that forces endless redesign. Design is reference-led, system-led, and approval-gated.

---

## 1. Rule

| Allowed | Not allowed |
|---|---|
| Build UI from **approved references** + **chosen component library** + **Figma kit** | Freestyle colors/layouts/components in code |
| Match patterns from named products (below) | Copying proprietary assets, logos, or trademarked illustration |
| Change design only via versioned design decision | “Just make it nicer” mid-implementation without updating the kit |

**Design Gate (before ops web / mobile screens ship):**  
Sponsor + product sign off on (1) reference map, (2) component library, (3) Figma foundations + 5 key screens.

---

## 2. Best approach (recommended)

Use a **three-layer** model:

```text
Layer A — Product UX references (what the product should feel like)
Layer B — Implementable design system (how we build components)
Layer C — Our brand tokens (color, type, density) applied on B
```

- **A** stops random UX.  
- **B** stops random components.  
- **C** makes it our product, not a clone.

Atlantis (Jobber) docs are **not public** anymore; npm packages exist but force React and are a dependency risk. Use Jobber as **UX reference only**, not as our UI kit — unless we explicitly choose a React stack later.

---

## 3. Layer A — Product references (proposed)

Pick **one primary** and **one secondary** per surface. Patterns only (IA, density, workflows) — not pixel clones.

| Surface | Primary reference | Secondary reference | What we learn |
|---|---|---|---|
| Field mobile (supervisor) | **Jobber** | Fieldwire / similar field apps | Fast capture, today queue, offline-friendly status, photo+note flows |
| Construction commercial / project web | **Procore** (financial/project workflows) | Autodesk Build (docs/submittals) | Project hub, RFIs, submittals, drawings, change/cost exposure |
| Cost / billing / QS workbench | **Procore** financial patterns + our PRD metrics | Specialist QS tools (Candy/CostX as *workflow* references only) | Measurement → certificate → claim discipline, auditability |
| Finance / GL / AP-AR admin | **ERPNext Desk** (native) | — | Do not rebuild ledger screens; restyle only if Desk theme APIs allow |
| Platform / Company Admin | Clean B2B admin (e.g. Stripe Dashboard / Linear density as *admin IA* reference) | ERPNext Desk | Entitlements, users, audit — dense, boring, correct |

**Decision needed from you:** confirm or replace the primary references in the table (DEC-11).

---

## 4. Layer B — Component library (proposed options)

Must match the web stack decision.

| Option | Fits stack | Pros | Cons | Verdict |
|---|---|---|---|---|
| **A. Keep Desk + Vue ops + Element Plus or Naive UI** | Matches PRD Vue candidate | Mature Vue admin kits, tables/forms strong | Two visual worlds (Desk vs ops) unless tokens aligned | **Recommended default** |
| **B. React ops UI + Ant Design or MUI** | Diverges from Vue proposal | Huge ecosystem | Extra frontend maintenance; PRD warned against unjustified React | Only if R0 spike proves benefit |
| **C. Adopt `@jobber/*` Atlantis packages** | React-only | Jobber look “for free” | Docs internal; Jobber-shaped product; React lock-in; may fight Frappe | **Not recommended** as system of record |
| **D. Fully custom components** | Any | Total control | Slow, inconsistent, high redesign risk | **Forbidden for R1** |

**Recommended lock:**  
- Finance/admin: **ERPNext Desk**  
- Ops/commercial web: **Vue 3 + Element Plus** (or Naive UI) with our tokens  
- Mobile: **Flutter** Material 3 *as baseline*, customized to our tokens (confirm after SP-02)

---

## 5. Layer C — Our brand tokens (from PRD §12.1)

Already directionally set — refine in Figma, don’t reinvent:

- Restrained neutral surfaces  
- Deep-teal action color  
- Clear semantic states (success/warn/danger/info)  
- Readable tables, tabular numerals  
- 4px spacing grid  
- Clarity over decorative dashboards  
- English default; RTL-ready locale packs later  

Name the kit: **“CIP Design System”** (Construction Intelligence Platform) — internal name only.

---

## 6. Process (so you don’t get stuck changing screens)

### Phase D0 — Reference lock (this week)
1. You confirm Layer A table (or send alternate apps).  
2. We freeze Layer B library choice.  
3. Record as **DEC-11** in evidence register.

### Phase D1 — Figma foundations (before UI code)
Deliverables:
- Foundations: color, type, space, elevation, icon rules  
- Components: button, input, select, table, tabs, badge, empty/error, nav shells (3 planes)  
- **5 key screens** only:  
  1. Company Admin home  
  2. Project hub  
  3. Daily report (web)  
  4. Commercial / certificate workbench  
  5. Mobile Today + Capture  

### Phase D2 — Design Gate review
Sponsor signs: “Build these; no drive-by redesign.”  
Changes after gate = new ticket + Figma update first.

### Phase D3 — Implementation
Engineers implement from Figma + component library only.  
PR checklist: screenshot vs Figma, tokens used, no one-off hex values.

### Phase D4 — SP-05 usability
Test against the 5 screens with supervisors/QS — redesign only failing flows.

---

## 7. What engineering must wait for

Until Design Gate passes, engineering continues on:
- R0 sandbox, SP-01 money spikes  
- Domain DocTypes, APIs, permissions  
- App skeletons without visual polish  

**Do not** spend time on marketing-site art or custom dashboards yet.

---

## 8. Your decision checklist (reply with choices)

1. **Field mobile primary reference:** Jobber / other: ______  
2. **Construction web primary reference:** Procore / other: ______  
3. **Ops web library:** Element Plus / Naive UI / other: ______  
4. **Mobile UI baseline:** Flutter Material 3 customized / other: ______  
5. **Figma owner:** who approves the Design Gate? ______  

After you answer, we lock DEC-11 and open the Figma foundations task — still no freestyle UI in code.
