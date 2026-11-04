# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-2524551485 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: No regular expressions in any new parsing code on this branch (security reviewer Leo's requirement after the old ReDoS advisory against ms). The ISO duration parse side must be hand-written.
- 2026-11-04: parseISO (hand-written scanner, no regex) supports W/D/H/M/S and +/- sign only; years/months rejected as ambiguous, matching formatISO. Invalid input returns NaN like parse(); non-strings or length >99 throw. Not yet committed.

