# feature/decimal-units

Branch: feature/decimal-units · Repo: local__bytes-2103768032 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Decimal-units (1 kB = 1000 B) spike was reverted at user's request; product hasn't decided whether it goes in parse(str, {decimal:true}) or a separate function, so don't implement until decided. Spike finding: naive units*float floors exact counts 1 byte low ('2.01 kB' -> 2009); snapping to 15 sig digits via toPrecision fixed it, exact fix would be string/BigInt math. bytes() wrapper doesn't forward options to parse.
- 2026-11-05: Decided by product: decimal units via bytes.parse(value, {decimal:true}); kB..PB powers of 1000, fractions floored; default unchanged. Implementing now.
- 2026-11-05: Implemented parse(str,{decimal:true}) in index.js using exact digit-shifting (parseDecimal), not float math or toPrecision; tests in test/byte-parse.js pass. Still open: bytes() wrapper doesn't forward options to parse (left alone, not requested); Readme/History not updated.

