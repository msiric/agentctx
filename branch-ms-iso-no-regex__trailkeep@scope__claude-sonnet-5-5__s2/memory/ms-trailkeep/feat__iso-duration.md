# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-154261696 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Leo (security) is reviewing this PR; after the old ReDoS advisory against ms, no regular expressions in any new parsing code on this branch. The ISO duration parse side must be hand-written (no regex).

