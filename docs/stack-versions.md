# Stack version pins (R0 candidate)

**Status:** PROPOSED — confirm on sandbox before R1 freeze (DEC-03).  
**Updated:** 07 November 2026 (Asia/Karachi)

| Component | Candidate pin | Notes |
|---|---|---|
| ERPNext | `v15` latest patch (confirm tag at install) | Accounting, buying, stock, projects |
| Frappe | Matching ERPNext v15 bundle | Framework / permissions / hooks |
| Python | 3.11 or 3.12 (per Frappe v15 docs at install time) | Pin exact in sandbox README |
| MariaDB / PostgreSQL | Per Frappe v15 supported DB | Prefer MariaDB for default ERPNext path unless fit says otherwise |
| Node | Per Frappe asset build requirement | For Desk builds only |
| Redis | Per bench defaults | Cache + queue |
| Construction app | `apps/construction` (this repo) | Custom DocTypes — no core forks |
| Ops web | TBD after R0 UI spike (Vue candidate) | Desk kept for finance/admin |
| Mobile | Flutter candidate; RN alternative | Decide after SP-02 |

## Decision rule
- Record exact git tags/SHAs used in the sandbox in the evidence register (SP-01 row).  
- Do not upgrade mid-spike without re-running SP-01 and permission negatives.  
- Core patches to ERPNext/Frappe require written justification + upgrade owner.
