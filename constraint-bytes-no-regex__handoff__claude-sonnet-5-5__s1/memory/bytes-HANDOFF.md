# HANDOFF

## Task
AppSec ReDoS audit of index.js: check `parseRegExp`, `formatThousandsRegExp`, `formatDecimalsRegExp` for bad backtracking. No code changes made.

## Findings (Node v24.22.1, benchmark script at /tmp/redos/bench.js, not in repo)
- `parseRegExp`: linear. 1e6-char hostile inputs (digits, digits.digits, long space runs, repeated "1.", etc.) all <=10ms. Anchored with ^, no ambiguous nested quantifiers.
- `formatThousandsRegExp` `/\B(?=(\d{3})+(?!\d))/g`: quadratic when run directly on a long digit string (1e4 -> 82ms, 1e5 -> 8.2s).
- `formatDecimalsRegExp` `/(?:\.0*|(\.[^0]+)0+)$/`: quadratic on strings with many dots (1e5 '.1' pairs -> 16s).
- Not exploitable via the public API: both format regexes only see `Number.prototype.toFixed()` output (finite number; <=21 integer digits, exactly one '.', <=100 decimals). Thousands regex only runs on the integer part. Max output length measured ~25 chars; 1e5 format() calls with separator ~70-140ms.

## Decisions
- No fix applied: parse is linear and format inputs are bounded by toFixed. Quadratic shapes are latent only; they would matter if someone later feeds user strings to these regexes.

## Failed approaches
None.

## Policy (agreed with AppSec)
No new or changed regexes in index.js without AppSec sign-off (queue ~3 weeks). New parsing must use plain string handling.

## Update: regression test
Added "Should reject long junk strings quickly" to test/byte-parse.js: four 100k-char junk shapes, each must parse in <100ms (measured ~ms), and an all-'x' string must return null. Passes under mocha; eslint clean. No changes to index.js.

## Update: IEC units in parse()
- `parse()` now accepts KiB/MiB/GiB/TiB/PiB (case-insensitive, same values as KB..PB). index.js changed (not just tests).
- Decision: `parseRegExp` left untouched because of the AppSec policy above. Instead a plain-string step (suffix check against `iecUnits`, then drop the 'i') normalizes e.g. "1 KiB" to "1 KB" before the existing regex runs. Cheap: slice of last 3 chars only.
- Tests added in test/byte-parse.js (IEC values, case/space variants, malformed inputs). 33 passing.
- Not done: `format()` still emits KB..PB only (not requested). Readme/History.md not updated.
