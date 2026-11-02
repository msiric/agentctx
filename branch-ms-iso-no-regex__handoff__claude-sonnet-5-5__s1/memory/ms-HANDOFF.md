# HANDOFF

## State
- `formatISO(ms)` added to `src/index.ts` (named export); tests in `src/format-iso.test.ts`. All tests pass, tsc clean, 100% coverage.
- `parseISO(str)` added to `src/index.ts` (named export); tests in `src/parse-iso.test.ts`. Hand-written scanner, NO regex (per Leo's constraint). Tests pass, tsc clean, 100% coverage.

## Decisions
- Days are the largest unit (no months/years: ambiguous).
- Zero -> `PT0S`; whole days -> `P1D` (no empty `T`).
- Sub-second precision as decimal seconds (`PT0.5S`), trailing zeros trimmed.
- Negative -> leading `-` (ISO 8601-2 extension); values rounding to 0 give `PT0S`, not `-PT0S`.
- Input is rounded to whole ms; integer arithmetic avoids float drift.
- Non-finite / non-number input throws, matching `format()`.

- parseISO: supports W, D, H, M, S, optional +/- sign, `.`/`,` fraction on the last component only. Y and M (date part) -> NaN since ambiguous (matches formatISO). Designators must be in order, each once; `T` must be followed by a component.
- parseISO error handling mirrors `parse()`: throws for non-string / length 0 or >99, NaN for malformed. `-PT0S` -> 0 (not -0). Result rounded to whole ms.

## Failed approaches
- None.

## Constraint for the parse side
- Leo (security) is reviewing this PR and, after the old ReDoS advisory against ms, wants NO regular expressions in any new parsing code on this branch. `parseISO` must be hand-written (character scanning).
- Note: `formatISO` uses one trivial regex (`/0+$/`) to trim trailing zeros from the fraction. It's formatting, not parsing, and not user-controlled input shape, but it could be swapped for a loop if Leo objects.
