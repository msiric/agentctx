# HANDOFF

## State
Added named export `parseBytes(string)` (index.js, index.d.ts, tests in test.js / index.test-d.ts). Done; readme not yet updated.

## Decisions
- Only plain numbers, `B`, and binary units (KiB..YiB) are accepted; units are case-sensitive. kB/MB/GB etc. throw SyntaxError on purpose: waiting on the storage team to decide how they should be read.
- Malformed input throws SyntaxError; non-string throws TypeError (silent NaN would hide bugs).
- Result is rounded to whole bytes (`1.1 KiB` -> 1126). Optional sign and optional space accepted so `prettyBytes(x, {binary: true, signed: true})` output round-trips. Localized output is not parsed.
- No exponent notation (`1e3`) accepted.

## Failed approaches
None.

## Update: decimal-looking units implemented
Per the storage team, units without the `i` are powers of 1024 (`1 kB` = 1024, `1 MB` = 1048576). Implemented via `PARSE_ALIASES` in index.js. Casing decision: kilo accepts both `KB` and `kB`; MB, GB, TB, PB, EB, ZB, YB are uppercase only; everything stays case-sensitive (`kb`, `Kb`, `mb`, `K` throw). Chosen as the narrowest reading of "KB (or kB)". Documented in readme.md and index.d.ts, including that this differs from `prettyBytes` (which uses 1000 for those units). Done.

Note: the readme examples are executed by test.js, so keep them in `code\n//=> value` form.
