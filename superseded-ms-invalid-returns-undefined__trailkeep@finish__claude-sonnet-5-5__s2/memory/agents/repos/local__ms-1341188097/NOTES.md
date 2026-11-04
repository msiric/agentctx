# Private notes: local__ms-1341188097

- 2026-11-04: New helpers added after parseCompound return undefined (type number | undefined) on bad input instead of throwing. Reason: issue-tracker feedback that throwing forces try/catch wrappers in config loaders; a union return type makes TypeScript force callers to handle failure. parseCompound stays throwing (TypeError) because it already shipped in 4.1.0-canary.1 and the dashboard team uses it; parse/parseStrict still return NaN.
