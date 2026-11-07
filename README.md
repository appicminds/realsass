# Construction Intelligence Platform

International construction ERP (SaaS + standalone) with web, iOS, and Android.  
Foundation: ERPNext / Frappe + construction app + optional isolated AI.

## What we are doing first

**R0 foundation → SP-01**  
See **[docs/first-work.md](./docs/first-work.md)** for the ordered list.

Right now in this repo:
1. Planning docs (WBS + release map)  
2. Construction Frappe app **skeleton** (`apps/construction`)  
3. CI foundation checks  
4. SP-01 spike design  

**Blocked on you for full sandbox:** a machine with Docker/bench + named owners + sample BOQ/billing data.

## Planning docs

| Doc | Purpose |
|---|---|
| [PRD v4.1](./Construction_AI_ERP_Focused_Scope_PRD_v4.1.docx) | Requirements & acceptance |
| [Whole software WBS](./WHOLE_SOFTWARE_BUILD_PLAN.md) | 18 steps · 96 tasks · 5 phases |
| [Release plan](./RELEASE_PLAN.md) | R0→R4 task mapping |
| [First work](./docs/first-work.md) | **Start here for execution** |
| [Design approach](./docs/DESIGN_APPROACH.md) | **DEC-11 accepted** — Jobber/Procore refs, Vue+Element Plus, Flutter M3, Design Gate |
| [DEC-11](./docs/decisions/DEC-11-design-system.md) | Design decision record |
| [Stack versions](./docs/stack-versions.md) | ERPNext/Frappe pin candidates |
| [Evidence register](./docs/evidence-register.md) | VAL / SP / UAT log |
| [R0 checklist](./docs/r0-kickoff-checklist.md) | Owners & exit gate |
| [SP-01 design](./docs/spikes/SP-01-cost-billing.md) | First experiment |

## Repo layout

```text
apps/construction/   # Frappe construction domain app (skeleton)
docs/                # Plans, spikes, evidence
.github/workflows/   # CI
```

## Access planes

- **Platform Admin** — vendor SaaS / standalone installer  
- **Company Admin** — org, country profile, users, policies  
- **Employee / Operations** — project work on web + mobile  
