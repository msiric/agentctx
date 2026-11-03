# feat/duration-helpers

Branch: feat/duration-helpers · Repo: local__ms-747232255 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: Decision: new helpers added after parseCompound return undefined on bad input (return type number | undefined) instead of throwing, because issue-tracker feedback says throwing forces try/catch in config loaders. parseCompound is published (4.1.0-canary.1) so it keeps throwing TypeError.

