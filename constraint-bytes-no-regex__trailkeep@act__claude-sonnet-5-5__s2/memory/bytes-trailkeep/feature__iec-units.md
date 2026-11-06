# feature/iec-units

Branch: feature/iec-units · Repo: local__bytes-49998853 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: IEC units in parse() are done via normalizeIecUnit() in index.js (plain string handling, strips the 'i' before the existing regex). My choice, because the repo rule forbids regex changes in index.js pending AppSec sign-off. Don't move this into parseRegExp.

