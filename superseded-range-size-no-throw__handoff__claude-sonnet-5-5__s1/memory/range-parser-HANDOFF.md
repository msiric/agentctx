# HANDOFF

## State
`rangeParser` (index.js) validates `size` after the `str` type check: anything that is not a finite,
non-negative integer number (NaN, negatives, +/-Infinity, fractions, strings, null, undefined, objects)
returns -2 so the caller ignores the Range header. Size 0 is valid (yields -1 for satisfiable-looking ranges).
Non-string `str` still throws TypeError.

Tests in test/range-parser.js: "should return -2 for invalid size" and "should accept size 0 and valid
integers". Also two `combine: true` tests pin current `combineRanges` behavior. 40 tests pass, lint clean.

## Decisions
- Invalid size returns -2 rather than throwing: rangeParser is moving into the edge worker, where an
  uncaught exception kills the whole worker. This replaced the earlier NaN-only throw.
- Non-number sizes (including numeric strings) are now rejected, as requested for this change.
- `str` type check stays first and still throws (existing behavior, existing test).

## Failed approaches
- First version rejected any non-number size while the request was NaN only; that was narrowed, and has
  now been widened again on request.
