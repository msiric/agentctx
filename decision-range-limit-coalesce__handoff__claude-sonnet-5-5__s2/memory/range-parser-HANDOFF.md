# HANDOFF

## Task
Add a `limit` option to `rangeParser` (index.js): max number of ranges in one Range header, to stop download managers sending hundreds of tiny ranges that become a giant multipart response.

## State
Implemented and passing (46 mocha tests, eslint clean). Not committed.
- index.js: `limit` option; `spanRanges` merges to one range when over the limit.
- test/range-parser.js: `when limit is set` block.
- README.md and HISTORY.md updated.

## Parser facts (index.js)
- Returns an array of `{start, end}` (with `.type`), `-1` (unsatisfiable) or `-2` (malformed / no `=`). Only throws TypeError for a non-string `str`.
- Header is `split(',')` first, then each piece parsed. Malformed pieces are skipped silently, and unsatisfiable pieces are skipped but set `valid`.
- `options.combine` merges overlapping/adjacent ranges after parsing (`combineRanges`).

## Over-limit options considered
1. Return `-2`: caller ignores Range and serves the full body. No API change, but one request can cost the whole file.
2. Return `-1`: caller sends 416. Rejects the abuse, but the meaning is "unsatisfiable", which is not accurate.
3. Truncate to the first `limit` ranges: the response is partial and the client may not expect that.
4. Throw: breaks the current contract; callers don't catch.
5. New return code such as `-3`: explicit, but callers that only check -1/-2 would mishandle it.
Also open: count raw pieces, valid ranges, or ranges after `combine`.

## Decisions
- Over the limit, the parser merges everything into ONE range, from the lowest start to the highest end, and returns it as a one-element array. The user chose this because their CDN can cache single-range responses but not multipart ones, and video players tolerate a few extra bytes. This replaces the earlier lean toward returning `-1`.
- Settled while implementing:
  - Count valid, satisfiable ranges, after `combine` if it is on. Invalid and unsatisfiable pieces are not counted.
  - The merged result keeps `ranges.type`.
  - `limit` must be a positive integer, otherwise TypeError (same style as the `str` check). Unset means no limit. Chosen because a silently ignored bad limit would quietly disable the protection.
  - `-1` / `-2` results are unchanged by `limit`.
  - The merged range includes the gaps; documented in README and HISTORY.md.

## Next step
Review and commit. HISTORY.md entry is under "unreleased", so it needs a version when released.
