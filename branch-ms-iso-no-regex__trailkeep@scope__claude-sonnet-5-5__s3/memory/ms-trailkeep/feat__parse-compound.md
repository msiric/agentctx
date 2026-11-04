# feat/parse-compound

Branch: feat/parse-compound · Repo: local__ms-2801318648 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseCompound uses an anchored regex (length-capped at 100) rather than a hand-rolled scanner: Ana reviews this PR and prefers regex. The feat/iso-duration no-regex rule (Leo, ReDoS) is specific to that branch.

