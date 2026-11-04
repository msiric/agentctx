# Private notes: local__ms-623510711

- 2026-11-04: Duration helpers added after parseCompound (4.1.0-canary.1) return undefined on bad input instead of throwing, so number | undefined forces callers to handle it; throwing was a pain in config loaders (everyone wrapped in try/catch). parseCompound itself stays throwing because it is already published and the dashboard team uses it.
