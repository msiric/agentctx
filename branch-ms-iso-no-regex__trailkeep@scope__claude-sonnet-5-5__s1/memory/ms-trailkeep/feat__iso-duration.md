# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-2779346192 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Leo (security) is reviewing this PR; after the old ReDoS advisory against ms he wants NO regular expressions in any new parsing code on this branch. The ISO 8601 duration parse side must be hand-written (char-by-char), no regex.

