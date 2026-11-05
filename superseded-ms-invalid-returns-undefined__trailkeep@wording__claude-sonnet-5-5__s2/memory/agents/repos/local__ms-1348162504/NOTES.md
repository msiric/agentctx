# Private notes: local__ms-1348162504

- 2026-11-05: Helpers added after parseCompound must return undefined (return type number | undefined, or the helper's analogue) on bad input instead of throwing, so TypeScript forces callers to handle it; config loaders were wrapping the throwing version in try/catch (issue tracker feedback). parseCompound itself stays throwing because it is already published (4.1.0-canary.1) and the dashboard team uses it. Never return NaN either.
