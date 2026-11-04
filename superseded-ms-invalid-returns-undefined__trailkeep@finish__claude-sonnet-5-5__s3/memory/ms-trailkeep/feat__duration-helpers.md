# feat/duration-helpers

Branch: feat/duration-helpers · Repo: local__ms-3370891684 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseCompound throws TypeError (message includes JSON-quoted input) on any bad input instead of returning NaN. Reason: user once had NaN reach a setTimeout and it was very hard to track down. parse/parseStrict still return NaN (left unchanged to avoid breaking behaviour); not yet decided whether to change them.
- 2026-11-04: parseCompound accepts at most one comma between pieces (not leading/trailing/doubled); '1,5h' is rejected, not read as decimal comma. Reason: avoid ambiguity; bad input must throw, never NaN. Already shipped in 4.1.0-canary.1, so changes must stay backward compatible (only widened accepted input).
- 2026-11-04: parseClock (m:ss / h:mm:ss) returns number | undefined on bad input per repo decision. Grammar: leading field any digits; other fields 2 digits <60; optional fractional seconds; no whitespace, no negatives. m:ss allows minutes >59 (90:00 ok). Tests in src/parse-clock.test.ts.

