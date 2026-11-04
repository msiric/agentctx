# Private notes: local__ms-2418025384

- 2026-11-04: New duration helpers added after parseCompound return undefined on bad input (return type number | undefined) instead of throwing. Reason: issue-tracker feedback that throwing forces try/catch in config loaders; a union return type makes TypeScript force callers to handle failure. parseCompound stays throwing because it is already published (4.1.0-canary.1) and the dashboard team uses it; changing it would break them.
