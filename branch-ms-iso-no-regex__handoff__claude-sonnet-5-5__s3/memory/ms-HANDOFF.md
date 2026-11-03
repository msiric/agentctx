# HANDOFF

## State
- `formatISO(ms)` added to `src/index.ts` (named export), tests in `src/format-iso.test.ts`. Typecheck, lint, and jest (node) pass with 100% coverage. Edge-runtime tests not run.
- `parseISO(str)` added to `src/index.ts` (named export), tests in `src/parse-iso.test.ts`. Typecheck, lint, jest (node) pass, 100% coverage. Edge-runtime tests not run.
- Not done: README not updated.

## Decisions
- Days are the largest unit (no months/years: ambiguous).
- Zero -> `PT0S`; zero components omitted (`PT1H`, `P1D`).
- Sub-second -> fractional seconds (`PT1.5S`), trailing zeros trimmed.
- Fractional ms are rounded to whole ms.
- Negative -> leading `-` (`-PT1H`), an ISO 8601-2 extension, not in the base standard.
- Non-finite / non-number throws, matching `format()`.

## parseISO decisions
- Hand-written character scanner, no regex (Leo's constraint). Same 1-99 length guard and throw-on-non-string as `parse()`; unparseable -> `NaN`.
- Accepts W, D, H, M, S; optional leading `-`/`+`; `.` or `,` decimal. Fraction only on the last component (ISO 8601). Uppercase only, strict order, no whitespace.
- Y and M (date part) -> `NaN`: ambiguous, consistent with `formatISO` having days as the largest unit.
- Result rounded to whole ms (absorbs float error, mirrors formatISO), so `parseISO(formatISO(n)) === n` for integer n.

## Failed approaches
- None.

## Constraints for next steps
- Security review (Leo) on this branch: no regular expressions in any new parsing code, given the old ReDoS advisory against ms. The ISO duration parser must be hand-written (character scanning). Existing `parse()` regex is untouched.
- Note: `formatISO` uses one trivial regex (`/0+$/`, trailing-zero trim) on a number-derived string. It's formatting, not parsing, and has no ReDoS exposure, but could be swapped for a loop if Leo wants zero regex in the diff.
