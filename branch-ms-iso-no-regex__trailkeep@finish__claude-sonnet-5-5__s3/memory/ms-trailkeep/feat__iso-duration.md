# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-3063729221 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Leo (security) is reviewing this PR: no regular expressions in any new parsing code on this branch (reason: old ReDoS advisory against ms). ISO duration parse must be hand-written. formatISO currently has one trivial regex, /0+$/ in the fractional-seconds trim; it's formatting, not parsing.
- 2026-11-04: parseISO is hand-written (no regex, per Leo's review). Throws on invalid input (unlike parse's NaN); Y/M use parse's average lengths; accepts W, '.'/',' fractions, leading +/-.

