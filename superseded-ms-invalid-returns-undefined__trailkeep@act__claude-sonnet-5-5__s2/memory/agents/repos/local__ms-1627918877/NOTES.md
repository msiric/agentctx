# Private notes: local__ms-1627918877

- 2026-11-06: New helpers added after parseCompound must return undefined on bad input (typed number | undefined or similar) instead of throwing. Reason: issue-tracker feedback that throwing forces try/catch in config loaders; an undefined return type makes TypeScript force callers to handle it. parseCompound itself stays throwing TypeError because it is already published (4.1.0-canary.1) and in use; don't change it. Never return NaN either.
