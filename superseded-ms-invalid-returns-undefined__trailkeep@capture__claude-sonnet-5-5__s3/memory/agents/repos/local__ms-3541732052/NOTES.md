# Private notes: local__ms-3541732052

- 2026-11-03: API convention: new duration helpers added after parseCompound return undefined on bad input (return type number | undefined, so TypeScript forces callers to handle it). Reason: issue tracker feedback that throwing is a pain in config loaders and everyone wraps it in try/catch. parseCompound itself stays throwing TypeError because it is already published (4.1.0-canary.1); do not change it. Supersedes the earlier branch decision to throw on bad input for new helpers.
