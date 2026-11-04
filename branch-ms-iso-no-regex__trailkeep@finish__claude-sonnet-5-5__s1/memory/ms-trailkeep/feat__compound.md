# feat/compound

Branch: feat/compound · Repo: local__ms-2524551485 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseCompound: hand-written linear scanner, no regex (same ReDoS concern as feat/iso-duration); delegates each segment to parse(). Branch reset to main so PR is separate from formatISO. Multi-segment requires units on every segment.
- 2026-11-04: Superseded earlier note: user asked for a single anchored regex (length-capped) in parseCompound, matching parse() style; reviewer Ana prefers regex over loops. No-regex rule was specific to feat/iso-duration. Every segment needs a unit to avoid ambiguous splits/backtracking.

