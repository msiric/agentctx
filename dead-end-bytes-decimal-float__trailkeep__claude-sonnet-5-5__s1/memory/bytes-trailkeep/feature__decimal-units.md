# feature/decimal-units

Branch: feature/decimal-units · Repo: local__bytes-3071755089 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Spike of bytes.parse(str,{decimal:true}) (powers of 1000) was reverted; product undecided whether it goes in parse() or a separate function. Learned: naive units[unit]*float floors wrong (2.01 kB -> 2009); fix was parseFloat(result.toPrecision(15)) before Math.floor, only exact to ~15 sig digits. Vendor values to test: '2.01 kB'=2010, '4.1 MB'=4100000, '8.2 GB'=8200000000, '16.9 TB'=16900000000000.
- 2026-11-05: Decided (product): decimal units are bytes.parse(value,{decimal:true}), not a separate function. Implemented with decimalMap + parseFloat(x.toPrecision(15)) before Math.floor (naive multiply gives 2.01kB->2009); exact only to ~15 sig digits. bytes(str, opts) forwards opts to parse. Tests in test/byte-parse.js.

