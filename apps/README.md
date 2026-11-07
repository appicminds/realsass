# Applications

R0/R1 code lands here after version pinning.

Planned layout:

```text
apps/
  construction/     # Frappe construction domain app (custom DocTypes/services)
  ops_web/          # Operations web UI (employee/commercial)
  control_plane/    # SaaS / license admin (R2 weighting)
  mobile/           # iOS + Android (Flutter candidate; confirm in R0)
```

Do not implement production modules until R0 go-decision for that area.  
Skeleton only after tech lead pins ERPNext/Frappe versions (RELEASE_PLAN §9).
