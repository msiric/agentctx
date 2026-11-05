# HANDOFF

## State
Done: `bytes.parse(value, {decimal: true})` implemented in `index.js`, with tests (`test/byte-parse.js`)
and Readme docs. All 35 mocha tests pass. Not committed.

## Decisions
- Product chose the `parse` option (not a separate function). With `decimal`, kB/MB/GB/TB/PB are powers of 1000;
  result is still floored. Without it, behavior is unchanged.
- Implemented by shifting the decimal point of the numeric string (`parseDecimal`) instead of multiplying:
  `Math.floor(1e3 * 2.01)` gives 2009 (float error); the shift gives 2010. Same for 4.1 MB, 8.2 GB, 16.9 TB.
- Negatives floor toward -infinity (`'-1.0005kB'` -> -1001), matching the existing behavior.
- The `bytes()` wrapper now forwards `options` to `parse` for strings, so `bytes('1kB', {decimal: true})` works.
  Previously options were ignored for strings.
- `format` has no decimal mode (not requested).

## Known limits
- Results above 2^53 (~9 PB) lose precision as JS numbers.

## Failed approaches
- Naive multiplication by 1000^n (float errors above).
