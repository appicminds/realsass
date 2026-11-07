# DEC-11 — Design references & component library

| Field | Value |
|---|---|
| **ID** | DEC-11 |
| **Status** | **ACCEPTED** |
| **Date** | 07 November 2026 (Asia/Karachi) |
| **Decided by** | Product sponsor (chat confirmation: “ok let's do it then”) |
| **Supersedes** | Soft proposals in PRD §12.1 / earlier DESIGN_APPROACH draft |

## Decision

### Layer A — Product UX references (patterns only, not clones)
| Surface | Primary | Secondary |
|---|---|---|
| Field mobile | **Jobber** | Fieldwire-class field apps |
| Construction / commercial web | **Procore** | Autodesk Build (docs/submittals) |
| Cost / billing / QS | **Procore** financial patterns + PRD metrics | QS workflow tools as process reference only |
| Finance / GL / AP-AR | **ERPNext Desk** (native) | — |
| Platform / Company Admin | Dense B2B admin IA (Stripe/Linear-class density) | ERPNext Desk |

**Not adopted as UI kit:** Jobber Atlantis (`@jobber/*`) — docs internal; React lock-in.

### Layer B — Implementable libraries
| Surface | Library |
|---|---|
| Ops / commercial / admin custom web | **Vue 3 + Element Plus** + CIP tokens |
| Finance / standard ERP | **ERPNext Desk** (do not rebuild) |
| Mobile | **Flutter** + **Material 3** baseline, themed to CIP tokens (confirm framework finally after SP-02; RN only if SP-02 fails Flutter) |

### Layer C — Brand
Per PRD §12.1: neutrals, deep-teal actions, semantic states, tabular figures, 4px grid, clarity over decoration. Kit name: **CIP Design System**.

## Process lock
- No production UI without **Design Gate** (Figma foundations + 5 key screens signed).  
- Post-gate visual changes require Figma update first, then code.  
- No freestyle hex/spacing/components outside the kit.

## Next actions
1. Open Figma file for CIP foundations + 5 key screens.  
2. Name Design Gate approver on `docs/r0-kickoff-checklist.md` if not the sponsor.  
3. Continue R0 engineering (sandbox, SP-01) in parallel — no visual freestyle.  
