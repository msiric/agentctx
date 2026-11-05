# feat/iso-duration

Branch: feat/iso-duration · Repo: local__ms-3141177893 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Leo (security) is reviewing this PR. After the old ReDoS advisory against ms, he wants NO regular expressions in any new parsing code on this branch. When doing the ISO 8601 duration parse side, hand-write the parser (no regex). Stated by the user; applies to all new parsing code on this branch. formatISO (formatting, not parsing) currently has one trivial regex, /0+$/, for trimming trailing zeros: my choice, not covered by the rule as stated.
- 2026-11-05: formatISO is committed (5e8d143). Design choices were mine, not the user's: zero -> PT0S; sub-second as decimal seconds with trailing zeros trimmed; input rounded to whole ms; negatives get a leading '-' (ISO 8601-2 extension); non-finite/non-number throws. Next: parse side (hand-written, no regex), README docs not yet added, test:edge not run.
- 2026-11-05: parseISO committed-pending: hand-written (no regex) per Leo's rule. My choices: supports W/D/H/M/S, rejects Y and M-in-date (ambiguous), accepts . or , decimals, optional +/- sign, max length 100, rounds to whole ms. test + test:edge pass. README docs still not added.

