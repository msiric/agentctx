# HANDOFF

## Task
Add a `limit` option to rangeParser (max ranges in one Range header) so headers with hundreds of tiny ranges can't force a giant multipart response. Branch: feature/range-limit.

## State
Design discussion only. No code written. Open question: what to do when a header exceeds the limit.

## Parser facts (index.js)
- Returns an array (with `.type`), `-1` (unsatisfiable) or `-2` (malformed). Callers typically map -1 to 416 and -2 to "ignore Range, send 200".
- `str.slice(index + 1).split(',')` runs before any counting, so the limit check could go before the split.
- Invalid entries are skipped and unsatisfiable ones set `valid`; neither is in the output.
- `combine` runs after parsing, so the limit can apply to raw entries, parsed ranges, or combined ranges.

## Options considered
1. Return -2: caller ignores Range and serves 200. No new return value.
2. Return -1: caller sends 416.
3. Truncate to the first N ranges: silent, and clients may not expect it.
4. New return code or throw: lets callers choose, but breaks callers that only check -1/-2.
5. Combine first, then count (works with any of the above).

## Decisions
- Over the limit: merge into ONE range from the lowest start to the highest end (a covering range) and return it as a one-element array. Reason: the user's CDN can cache single-range responses but not multipart, and video players tolerate the extra bytes in the gaps. This replaces the earlier lean towards returning -2.
- Rejected: -2 (serves the whole file), -1 (misleading 416), truncation (silent, clients may break), new return code (breaks callers).

## Implemented (uncommitted, on feature/range-limit)
- index.js: after parsing and optional `combine`, if `limit` is a number >= 1 and `ranges.length > limit`, `coverRanges` replaces them with one {min start, max end} range, keeping `.type`.
- Settled: count is post-combine; default is unlimited; invalid/unsatisfiable entries are not counted; -1/-2 results unchanged; limit < 1 or non-number is ignored (not an error).
- Tests added in test/range-parser.js ("when limit is set"); README `limit` section; HISTORY.md "unreleased" entry. 44 tests pass, eslint clean.
- Note: the raw header is still split fully before the limit applies, so this bounds the response, not parse cost.

## Next step
Review and commit if happy.
