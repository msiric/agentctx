# retry-hooks

Branch: retry-hooks · Repo: local__p-retry-1971491653 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: initialDelay (my choice, not user-specified): wait happens before startTime is taken, so it is not counted toward maxRetryTime; documented in readme. index.d.ts untouched per repo rule.

