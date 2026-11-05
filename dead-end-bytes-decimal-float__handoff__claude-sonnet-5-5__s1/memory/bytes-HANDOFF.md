# HANDOFF

## State
Done, uncommitted: `bytes.parse(value, {decimal: true})` (also via `bytes(str, opts)`). 37 mocha tests pass (7 new, in test/byte-parse.js). Readme updated.

## Decisions
- Product chose the option form (`{decimal: true}`) over a separate function.
- Decimal parsing is exact: `parseDecimal` in index.js shifts the decimal point in the digit string by the unit's exponent (3..15) and floors, instead of multiplying floats. Reason: `2.01 * 1000` = 2009.9999999999998, so multiply+floor was off by one ('2.01 kB', '4.1 MB', '8.2 GB', '16.9 TB' all came out one low).
- Negatives keep Math.floor semantics (-1.0001kB -> -1001); -0 normalised to 0.
- Without the option nothing changes (binary table, float multiply).
- Only strings with a unit take the decimal path; unitless strings and numbers behave as before.
- `format` untouched (still 1024-based).

## Failed approaches
- Naive multiply + floor (off by one, above).
- `Math.floor(Number(x.toPrecision(15)))` worked on the vendor values but is a heuristic that breaks past ~15 significant digits; replaced by string shifting.

## Known limits
- Results above 2^53 lose integer precision (Number), same as the binary path.
