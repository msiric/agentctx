# HANDOFF

## Task
Add a `limit` option to `rangeParser` (index.js): max number of ranges in one Range header,
to stop download managers' hundreds-of-tiny-ranges headers from producing giant multipart responses.

## State
Implemented and tested (index.js, README.md `limit` section, test/range-parser.js). `npm test` + eslint pass.
Not committed. HISTORY.md not updated (left for release time).

## Decision (user)
If a header has more ranges than `limit`, collapse them into ONE range: lowest start to highest end.
Reason: the CDN can cache single-range responses but not multipart ones, and the video players
tolerate receiving a few extra bytes. (RFC 9110 allows servers to coalesce ranges.)

## Findings about the parser
- Returns array (with `.type`), `-1` (unsatisfiable -> 416) or `-2` (malformed/ignore -> full 200). Never throws except for non-string input.
- `split(',')` happens up front, so `arr.length` is known before any per-range parsing.
- `combine` runs after validation, as a separate step over the valid ranges.
- Because collapsing needs min start / max end of the VALID ranges, we can't bail out before parsing
  (unlike the earlier "-2 on raw count" idea). Parsing cost is still linear and bounded by header size.

## Resolved questions (my calls; change if you disagree)
- Counting: valid ranges AFTER `combine` (if set), so overlaps that shrink under the limit aren't collapsed.
- Default: no limit. Invalid `limit` (non-number, <1, NaN, string) is silently ignored, not an error, to keep the no-throw contract.
- Collapse happens in the same step after validation; -1/-2 results unchanged; `.type` preserved.
- Collapse applies whenever count > limit, always to exactly one range (not to `limit` ranges).

## Options considered and rejected
- Return `-2` (ignore header, full 200; Apache MaxRanges style): previous recommendation, superseded by CDN caching need.
- Return `-1` (416): wrong semantics, clients may not fall back.
- Truncate to first N: silently missing data.
- Throw: breaks no-throw contract for callers like send/express.
- New sentinel (e.g. -3): existing callers only check -1/-2 and would treat it as an array.
