# feature/largest-unit

Branch: feature/largest-unit · Repo: local__parse-ms-2423301130 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: largestUnit (my design choices, not user-specified): units above the largest are 0/0n rather than omitted; largestUnit is validated before the milliseconds input, so an invalid option throws even with a bad input. Work is uncommitted on feature/largest-unit.

