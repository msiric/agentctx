# feat/parse-compound

Branch: feat/parse-compound · Repo: local__ms-3063729221 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseCompound is on its own branch off main (separate from feat/iso-duration/formatISO). Written as a hand-rolled scanner without regex, matching the ReDoS concern from the iso-duration review; it delegates each part to parse().
- 2026-11-04: parseCompound: Ana reviews and prefers regex over hand-rolled loops if anchored and length-capped (100). Uses one anchored validation regex; superseded the earlier no-regex scanner (that rule was Leo's, for feat/iso-duration only).

