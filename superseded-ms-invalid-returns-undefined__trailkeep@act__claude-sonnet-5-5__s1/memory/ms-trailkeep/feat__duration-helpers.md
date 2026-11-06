# feat/duration-helpers

Branch: feat/duration-helpers · Repo: local__ms-945211936 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: parseCompound (src/index.ts) must throw TypeError including the input on any bad input (empty, 'abc', '1h foo'), never return NaN. Reason: user once had NaN reach setTimeout and it was very hard to debug.
- 2026-11-06: parseCompound keeps throwing TypeError (published in 4.1.0-canary.1); the undefined-on-bad-input rule applies only to later helpers (see repo note).
- 2026-11-06: My choice (not user-specified): parseCompound accepts a comma only between pieces; leading, trailing, doubled commas and '1,5h' throw TypeError. Reason: lenient comma handling would let malformed input through, against the throw-on-bad-input rule. Changes (commas, README section, tests) are uncommitted on feat/duration-helpers.
- 2026-11-06: My choice (not user-specified): parseClock returns undefined on bad input (per repo rule). m:ss allows any minutes (90:00 ok), ss must be 2 digits <60; h:mm:ss needs mm<60; optional fractional seconds; no negatives; no length cap (so overflow-to-Infinity is checked via isFinite). Tests in src/parse-clock.test.ts; README not yet updated for parseClock.

