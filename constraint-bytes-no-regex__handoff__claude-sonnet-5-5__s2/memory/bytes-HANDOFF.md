# HANDOFF

## Task
AppSec ReDoS audit of index.js: parseRegExp, formatThousandsRegExp, formatDecimalsRegExp. Branch chore/redos-audit.

## State
Audit done, no code changes. Bench script lives outside the repo at /tmp/redos/bench.js (`node bench.js <path-to-index.js>`).

## Findings (measured, Node)
- parseRegExp: linear. 1M-char hostile inputs (digits, spaces, "1.1.1.", junk suffix) take <=5ms.
- formatThousandsRegExp: quadratic in isolation (100k digits = ~8s), but input is the integer part of Number.toFixed(), which is at most ~21 digits (larger values become "1e+21" form). Not reachable with long input.
- formatDecimalsRegExp: quadratic in isolation (".1" x 50k = ~4s), but input is toFixed() output (one '.', at most 100 decimals). Not reachable.
- format() worst cases (1e21, MAX_VALUE, decimalPlaces:100) are <0.4ms.

## Decisions
- No code change: the quadratic regexes only receive bounded, library-generated strings. Rewriting them risks behaviour change for no exploitable gain.

## Failed approaches
None.

## Update: policy and test
- Policy agreed with AppSec: no new or changed regexes in index.js without AppSec sign-off (their queue is ~3 weeks). New parsing in the meantime uses plain string handling.
- Added test "Should reject long junk strings quickly" in test/byte-parse.js: five 100k-char junk inputs must return null in under 100ms each. Passes (12 tests), eslint clean. index.js untouched.
- Note: a 100k run of digits plus junk (e.g. '1'*100000+'!') is NOT rejected, because parse() falls back to parseInt and returns a number. So it isn't in the test.

## Update: IEC units (branch feature/iec-units)
- parse() now accepts KiB/MiB/GiB/TiB/PiB (case-insensitive), same values as KB..PB.
- Decision: parseRegExp left UNCHANGED (AppSec policy above). parse() normalizes a trailing `<k|m|g|t|p>i?b` to `<k|m|g|t|p>b` with charAt/slice, then uses the existing regex. Could be folded into the regex later once AppSec signs off.
- Side effect: like "1kb!" today, strings that don't match fall back to parseInt; "1xiB" -> 1 (unchanged behaviour).
- Tests added in test/byte-parse.js (3 IEC tests). 34 passing, eslint clean.
- Not done: format() does not emit IEC units (not requested); Readme/History.md not updated.
