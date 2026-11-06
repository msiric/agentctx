# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-1764781742 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Security (Leo) is reviewing this PR after the old ReDoS advisory against ms: no regular expressions in any new parsing code on this branch. The ISO 8601 duration parse side (next task) must be hand-written. Note: formatISO in src/index.ts uses one regex (.replace(/0+$/, '')) for trimming zeros; it is formatting not parsing, so left as is, but may be worth removing.
- 2026-11-06: My own choices in formatISO (not user-specified; revisit if asked): zero is PT0S, negatives get a leading '-', input rounds to nearest ms, fractional seconds kept with trailing zeros trimmed, non-finite/non-number throws. Parse side should accept what formatISO emits (round-trip), hand-written, no regex. Committed as 78a8b38; edge-runtime tests not run.
- 2026-11-06: parseISO added in src/index.ts (+ src/parse-iso.test.ts), hand-written scanner, no regex. My choices: accepts W/D/H/M/S, optional +/- sign, '.' or ',' fractions; rejects Y/M-in-date (ambiguous), wrong order, empty 'P'/'PT'. Also (mine) removed the one regex in formatISO (trailing-zero trim) so the branch has none. Not committed yet.

