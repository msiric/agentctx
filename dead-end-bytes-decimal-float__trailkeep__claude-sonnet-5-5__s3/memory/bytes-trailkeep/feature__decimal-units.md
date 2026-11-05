# feature/decimal-units

Branch: feature/decimal-units · Repo: local__bytes-2908287376 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Decimal-units spike (parse(str,{decimal:true}), kB=1000) reverted; product undecided whether it goes in parse() or a separate function. Learned: naive float multiply floors wrong (2.01*1e3=2009.9999999999998 -> 2009); needs toPrecision(15) snap or exact integer/fraction string math. Vendor values 2.01 kB/4.1 MB/8.2 GB/16.9 TB must be exact.
- 2026-11-05: Product decided 2026-11-05: decimal units ship in parse() as bytes.parse(v,{decimal:true}) (kB..PB = 1000^n, floor fractional bytes, default unchanged). Implemented via exact digit-shift string math (parseDecimal in index.js), not float multiply: 2.01*1e3=2009.99.. floors wrong. Supersedes the earlier 'undecided' note.

