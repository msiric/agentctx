# HANDOFF

## State
DONE (uncommitted): `bytes.parse(str, {decimal: true})` implemented in index.js; tests in test/byte-parse.js ("with decimal option"). All tests + lint pass.
Product decision: option on `parse()` (not a separate function). `bytes(str, opts)` now forwards options to `parse`.

## Decisions
- With `decimal`, kB/MB/GB/TB/PB are powers of 1000; fractional bytes floored toward -infinity (like the binary path). Without it, behavior is unchanged.
- Exact digit-string arithmetic (`parseDecimal`) instead of float multiply: `Math.floor(1000*parseFloat(..))` gives '2.01 kB' -> 2009, '4.1 MB' -> 4099999, etc.
- No BigInt: package.json engines is `node >= 0.8`. Shift the decimal point in the string, then Number().

## Not done
- `format` has no decimal support (out of scope).
- Binary path still uses float math (unchanged).
- README updated (Readme.md).
