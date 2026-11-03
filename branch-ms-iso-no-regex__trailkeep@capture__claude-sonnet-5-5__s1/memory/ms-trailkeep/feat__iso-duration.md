# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-4249820292 · Kind: branch · Created: 2026-11-02

## Decisions and dead ends

- 2026-11-02: No regular expressions in any new parsing code on feat/iso-duration (security reviewer Leo, after the ms ReDoS advisory). ISO duration parse must be hand-written. formatISO also kept regex-free.

