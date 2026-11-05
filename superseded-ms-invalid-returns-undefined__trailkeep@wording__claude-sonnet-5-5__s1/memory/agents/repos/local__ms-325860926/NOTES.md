# Private notes: local__ms-325860926

- 2026-11-05: New duration helpers added after parseCompound (published in 4.1.0-canary.1) must return undefined on bad input instead of throwing, with a number | undefined return type so TypeScript forces callers to handle it. Reason: issue-tracker feedback that throwing is a pain in config loaders (everyone wraps it in try/catch). Exception: parseCompound itself stays throwing TypeError because it is already published and the dashboard team uses it.
