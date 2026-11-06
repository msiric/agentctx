# Private notes: local__ms-945211936

- 2026-11-06: New parse helpers added after parseCompound must return undefined on bad input (return type number | undefined), not throw, and never return NaN. Reason: issue-tracker feedback that throwing forces try/catch in config loaders; the union type makes TypeScript force callers to handle failure. Exception: parseCompound stays throwing TypeError (includes input) because it is already published in 4.1.0-canary.1 and the dashboard team uses it; do not change it.
