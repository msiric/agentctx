# feat/microseconds

Branch: feat/microseconds · Repo: local__ms-1244661534 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Microseconds: parse-only (us, µs, microsecond(s)); Greek mu U+03BC/U+039C normalized to micro sign U+00B5 since the /i regex matches them. format() deliberately unchanged (0.5 -> '0.5ms'). Tests only added to parse.test.ts, uncommitted.

