# Professional Design Approach (mandatory)

**Status:** **ACCEPTED** via [DEC-11](./decisions/DEC-11-design-system.md) — 07 November 2026 (Asia/Karachi)  
**Figma file (current):** [CIP-SASS](https://www.figma.com/design/nW0n4I3aarR2CqvEt9d9ZY/CIP-SASS) (`nW0n4I3aarR2CqvEt9d9ZY`) — Untitled UI free kit copy, re-themed to CIP teal; Design Gate screens on page **CIP Screens** · team: Freelance Projects  
**Superseded:** [CIP Design System](https://www.figma.com/design/yoTMDkmw6OQZr6d8xhqPeB) (wireframe pass, rejected by sponsor)  
**Rule:** No production UI until the Design Gate passes. No freestyle UI in code.

---

## Locked choices (DEC-11)

| Layer | Choice |
|---|---|
| Field mobile UX reference | **Jobber** |
| Construction web UX reference | **Procore** (+ Autodesk Build for docs/submittals) |
| Finance UI | **ERPNext Desk** (native) |
| Ops web component library | **Vue 3 + Element Plus** + CIP tokens |
| Mobile UI baseline | **Flutter + Material 3**, themed to CIP (final framework after SP-02) |
| Jobber Atlantis as kit | **Rejected** (docs internal; React lock-in) |

---

## Three layers

```text
Layer A — Product UX references (Jobber / Procore / Desk)
Layer B — Component libraries (Element Plus / Desk / Flutter Material 3)
Layer C — CIP brand tokens (teal, neutrals, 4px grid)
```

---

## Design Gate (required before UI implementation)

Sponsor signs off on:
1. This DEC-11 lock (done)  
2. Figma foundations (color, type, space, elevation, icons)  
3. Element Plus theme tokens mapped to CIP  
4. **Five key screens:**  
   - Company Admin home  
   - Project hub  
   - Daily report (web)  
   - Commercial / certificate workbench  
   - Mobile Today + Capture  

Until then: domain/API/sandbox work only — no pixel inventing.

### After the gate
- Engineers implement from Figma + Element Plus / Flutter theme only  
- PRs need screenshot vs Figma  
- Redesigns = Figma first, then code  

### Usability
SP-05 runs against the five gated screens; only failing flows get redesign tickets.

---

## Brand tokens (CIP)

From PRD §12.1:
- Restrained neutral surfaces  
- Deep-teal action color  
- Accessible semantic states  
- Readable tables, tabular numerals  
- 4px spacing grid  
- Clarity over decorative dashboards  
- English default; RTL locale packs later  

---

## Parallel engineering (allowed now)

- R0 sandbox, SP-01 money spikes  
- Construction DocTypes / APIs / permissions  
- App skeletons without visual polish  

## Not allowed now

- Custom marketing art as product UI  
- One-off screens “to see how it looks” outside Figma  
- Adopting Atlantis packages as the system of record  
