# HANDOFF

## Task
AppSec ReDoS audit of index.js: parseRegExp, formatThousandsRegExp, formatDecimalsRegExp. No code changes made.

## Findings (measured with /tmp/redos/bench.js, /tmp/redos/reach.js)
- parseRegExp: linear. 5M-char hostile input parses in ms. Safe.
- formatThousandsRegExp `/\B(?=(\d{3})+(?!\d))/g`: quadratic on a long digit run (10k digits ~83ms, 100k ~8s).
- formatDecimalsRegExp `/(?:\.0*|(\.[^0]+)0+)$/`: quadratic on many-dot input (10k ~178ms, 100k ~16s).
- Both format regexes only run on `Number.prototype.toFixed()` output (<=21 integer digits, one dot, decimalPlaces <= 100), so input length is bounded and the quadratic cost is unreachable from user input. Not exploitable as-is.

## Decisions
- No fix applied: not reachable. Revisit if these regexes are ever applied to caller-supplied strings.

## Failed/aborted
- First benchmark run at n=1e6 hung (quadratic cases); killed it. Use n <= 1e5 for those cases.

## Standing rule (agreed with AppSec)
- No new or changed regexes in index.js without AppSec sign-off (their queue is ~3 weeks). New parsing logic must use plain string handling.

## Tests added
- test/byte-parse.js, "with long hostile input": 100k-char junk and near-miss strings must parse in <250ms (junk returns null). Full suite passes (32).

## IEC units (KiB..PiB) in parse()
- Done: index.js parse() normalizes `<k|m|g|t|p>iB` to `<x>B` with plain string handling before the existing parseRegExp. Regex untouched, per the standing rule (no AppSec sign-off needed).
- Rejected: editing parseRegExp to `(k|m|g|t|p)i?b` — simplest, but would need AppSec sign-off.
- Tests: "IEC units" block in test/byte-parse.js. Full suite passes (39).
- format() unchanged (still outputs KB/MB/...).
