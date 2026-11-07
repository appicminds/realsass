# SP-01 — Cost and billing concurrency (design)

**Owner streams:** ERP lead + finance/QS + QA  
**PRD links:** BILL-10/11, MET-01/02, UAT-01, UAT-03  
**Status:** NOT STARTED (awaiting sandbox)

## Goal
Prove on pinned ERPNext/Frappe that:
1. Partial receipt → invoice → transfer → consumption reconciles **A / C / U** without double cost  
2. Certify 140 with 100 already billed; race two drafts for remaining **40**; only 40 allocated  
3. Crash/retry/cancel cannot duplicate allocation  
4. Same rules via Desk, API, and import paths  

## Pass
- No duplicate allocation/cost  
- Allocations never exceed remaining eligible qty/value  
- Recovery preserves eligibility + audit  
- Finance approves reconciliation  

## Fail response
Stop live posting design; fix transaction boundaries before R1 billing build.

## Fixture sketch (synthetic)
| Item | Value |
|---|---|
| Prior certified & invoiced | 100 units |
| New certification | 140 units |
| Remaining eligible | 40 units |
| Concurrent draft invoice requests | 2 × try to take 40 |
| Cost move example | 200,000 previously in C → posts to A; EAC unchanged if forecast unchanged |

## Preconditions
- [ ] Sandbox installed with pinned versions (`docs/stack-versions.md`)  
- [ ] Construction app installed (skeleton OK; allocation DocTypes may be spike branch)  
- [ ] Finance policy examples agreed (DEC-02 draft)  
- [ ] Evidence row SP-01 set to IN PROGRESS  

## Evidence to attach
Build/config, steps, expected vs actual, ledger screenshots/exports, defect IDs, reviewer sign-off.
