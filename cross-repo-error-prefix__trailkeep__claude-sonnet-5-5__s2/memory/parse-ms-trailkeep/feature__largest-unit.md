# feature/largest-unit

Branch: feature/largest-unit · Repo: local__parse-ms-2752511179 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: largestUnit: units above the chosen one stay in the result as 0/0n (shape unchanged), rather than being omitted. Existing 'Expected a finite number or bigint' error left without the parse-ms: prefix; not yet decided whether to add it. No type test added to index.test-d.ts yet.

