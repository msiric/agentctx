# feat/microseconds

Branch: feat/microseconds · Repo: local__ms-2264094991 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Microseconds: parse-only (us, µs, microsecond(s)); format()/fmtShort/fmtLong deliberately unchanged since not requested. Parse normalizes Greek mu U+03BC to micro sign U+00B5 because uppercase input (µS/ΜS) lowercases to U+03BC.

