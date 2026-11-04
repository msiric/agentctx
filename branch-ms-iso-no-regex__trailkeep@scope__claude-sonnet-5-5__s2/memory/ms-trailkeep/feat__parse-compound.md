# feat/parse-compound

Branch: feat/parse-compound · Repo: local__ms-154261696 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseCompound may use a single anchored regex (length-capped at 100), per Ana's review preference; the no-regex rule was specific to feat/iso-duration (Leo's ReDoS concern)

