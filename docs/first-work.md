# What we do first (active)

**Now:** R0 foundation — WBS tasks **1.1 → 1.5**, then first experiment **SP-01**.

## Order

| # | Do this | WBS | Owner type |
|---|---|---|---|
| 1 | Repo layout, gitignore, README, CI | 1.1, 1.4 | Engineering (started) |
| 2 | Pin ERPNext/Frappe candidates | 1.3 | Tech lead |
| 3 | Construction app skeleton in `apps/construction` | 1.3 | Engineering (started) |
| 4 | Evidence register + kickoff checklist in use | 1.5 | Product + QA |
| 5 | Stand up sandbox (bench/docker on a machine with Docker) | 1.2, 1.3 | DevOps / tech lead |
| 6 | Load finance fixtures → run **SP-01** | SP-01 | ERP + finance/QS |
| 7 | Clickable flows → **SP-05** | SP-05 | UX + ops |

## Not first
- Full BOQ/billing product UI  
- Production mobile  
- AI  
- Large marketing website  
- Multi-country packs content  

## You need to provide
1. Named owners on `docs/r0-kickoff-checklist.md`  
2. A host/VM **with Docker** (or existing bench) for the ERPNext sandbox — this cloud agent image has no Docker daemon right now  
3. Sanitized BOQ / certificate / invoice samples for SP-01  
