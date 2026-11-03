# HANDOFF

## State
`formatISO(ms)` added to `src/index.ts` (named export, next to `format`), with tests in `src/format-iso.test.ts`. Tests, tsc and biome lint pass. `parseISO(str)` added next to it (named export), tests in `src/parse-iso.test.ts`. Tests (node), tsc and biome lint pass.

## Decisions
- Days are the largest unit (no months/years: ambiguous). 400 days -> `P400D`.
- Zero -> `PT0S` (bare `P` is invalid ISO).
- Sub-second values are decimal seconds (`PT1.5S`), trailing zeros trimmed; input is rounded to the nearest ms.
- Negative -> leading `-` (`-PT1H30M`), per ISO 8601-2 / common practice.
- Non-number / non-finite input throws, like `format`.

- parseISO: hand-written scanner, no regex (see constraint below). Accepts optional +/- sign, W/D and H/M/S with optional decimal fractions (`.` or `,`), components in order. Years/months rejected (ambiguous, and formatISO never emits them). Result rounded to ms; -0 normalized to 0.
- parseISO throws on invalid input (length 1..99 like `parse`), rather than returning NaN.

## Failed approaches
None.

## Constraint for the parse side
Leo (security) is reviewing this PR and, after the old ReDoS advisory against ms, wants NO regular expressions in any new parsing code on this branch. The ISO duration parser must be hand-written (character scanning). `formatISO` also avoids regex (trailing-zero trim is a loop) to keep the diff regex-free.
