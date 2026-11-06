# main

Branch: main · Repo: local__pretty-bytes-2442101067 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: My choice (not the user's): `unit` option is typed as plain `string` in index.d.ts, not a union, because valid units depend on `bits`/`binary`; runtime TypeError is the only check. Offer a conditional union type if the user wants compile-time checking.

