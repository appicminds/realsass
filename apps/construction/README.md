# Construction (Frappe app)

Custom construction domain app for the Construction Intelligence Platform.  
ERPNext remains system of record for GL, buying/selling, stock, and standard masters.

## Install (on a bench site)

```bash
# from bench folder, after cloning this repo's apps/construction into apps/
bench get-app /path/to/realsass/apps/construction
# or: place/copy this app under frappe-bench/apps/construction
bench --site <site> install-app construction
```

## R0 scope of this skeleton
- App package + hooks only  
- Placeholder module for commercial DocTypes (added after SP-01 design)  
- No production DocTypes until R0 go and metric/API contracts are drafted  

## Ownership
- Domain rules live here (BOQ, measurement, certificate allocations, change events, …)  
- Do not patch ERPNext core; use hooks and linked DocTypes  
