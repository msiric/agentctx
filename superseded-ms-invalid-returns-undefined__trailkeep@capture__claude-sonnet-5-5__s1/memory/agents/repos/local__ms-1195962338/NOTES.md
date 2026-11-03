# Private notes: local__ms-1195962338

- 2026-11-02: Convention: new parse helpers added after parseCompound return number | undefined on bad input instead of throwing (issue-tracker feedback: throwing forces try/catch in config loaders; undefined makes TypeScript force callers to handle it). parseCompound stays throwing because it already shipped in 4.1.0-canary.1 and the dashboard team uses it.
