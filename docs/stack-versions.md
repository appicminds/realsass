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
| Ops web | **Vue 3 + Element Plus** + CIP tokens (DEC-11) | Desk kept for finance/admin |
| Mobile | **Flutter + Material 3** themed (DEC-11); RN only if SP-02 fails Flutter | Confirm after SP-02 |

## Decision rule
- Record exact git tags/SHAs used in the sandbox in the evidence register (SP-01 row).  
- Do not upgrade mid-spike without re-running SP-01 and permission negatives.  
- Core patches to ERPNext/Frappe require written justification + upgrade owner.
