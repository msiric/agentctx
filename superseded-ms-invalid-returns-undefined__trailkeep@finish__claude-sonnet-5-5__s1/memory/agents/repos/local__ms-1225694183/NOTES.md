# Private notes: local__ms-1225694183

- 2026-11-04: parseCompound must throw TypeError (with JSON-stringified input) on any invalid input, never return NaN: user once had NaN reach setTimeout and it was very hard to track down. Note parse() itself still returns NaN.
- 2026-11-04: New duration helpers added after parseCompound return undefined on bad input (return type number | undefined), never throw and never return NaN. Reason: issue-tracker feedback that throwing forces try/catch in config loaders; a number | undefined type makes TypeScript force callers to handle failure. parseCompound itself stays throwing TypeError because it is already published (4.1.0-canary.1) and the dashboard team uses it; changing it would break them.
