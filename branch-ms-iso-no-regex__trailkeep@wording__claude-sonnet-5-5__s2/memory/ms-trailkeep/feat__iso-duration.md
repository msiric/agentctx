# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-1225239132 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: formatISO (src/index.ts): my choices, not user rules — zero => PT0S, fractional seconds as decimals, negatives get leading '-', ms rounded to integer, non-finite throws. User rule: days are largest unit (months/years ambiguous). Parsing ISO durations is the planned next step.
- 2026-11-05: Rule from Leo (security reviewer of this PR), after the old ReDoS advisory: no regular expressions in any new parsing code on this branch. The ISO duration parse side must be hand-written (manual char scanning).
- 2026-11-05: parseISO (src/index.ts): hand-written char scan, no regex, per Leo's rule. My choices: accepts W and D (not Y/M, ambiguous), optional +/- sign, '.' or ',' fraction only on last component, strict designator order, throws on invalid, length cap 100. Note formatISO still has one regex (.replace(/0+$/)) in pre-existing code, only a trailing-zero trim.
- 2026-11-05: Don't run 'prettier --write' on src/index.ts: it reformats ~76 unrelated lines. Format only new code by hand or check the diff afterwards.

