# Handoff

- Task: rangeParser throws TypeError for NaN size (send calls it with NaN when NFS stat fails).
- Done: check at top of rangeParser in index.js (before the str check); test "should reject NaN size" in test/range-parser.js.
- Decision: only NaN number is rejected (typeof number && isNaN), so other non-number sizes keep existing behavior.

## Combine tests (follow-up)
- Added 5 tests under "when combine: true" in test/range-parser.js: adjacent (0-4,5-9 -> 0-9), adjacent out of order, one-byte gap not combined, suffix overlapping a normal range (-50,20-110 on 150 -> 20-149), suffix adjacent to normal range (0-99,-50 -> 0-149).
- No change to combineRanges; all 42 tests pass against the current implementation.

## Size validation (done)
- Invalid size (non-number, NaN, +/-Infinity, negative, fractional) now returns -2 instead of throwing (edge worker: an uncaught exception kills the worker, so the caller should ignore the Range header). Supersedes the earlier throw-on-NaN decision.
- Size 0 stays valid (returns -1 for a satisfiable-less range).
- A non-string str still throws TypeError and is checked first (programmer error, not data-dependent).
- Tests: replaced "should reject NaN size" with "should return -2 for invalid sizes" and "should accept size 0". 43 tests pass.
