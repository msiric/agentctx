# feature/largest-unit

Branch: feature/largest-unit · Repo: local__parse-ms-942978515 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: largestUnit: larger units are zeroed (shape kept), not omitted. Old 'Expected a finite number or bigint' error left unprefixed to avoid changing existing behavior; new errors use 'parse-ms:' prefix per user's rule. Left open: xo warnings (rollUp 5 params, 215-char line), no type test in index.test-d.ts, nothing committed.

