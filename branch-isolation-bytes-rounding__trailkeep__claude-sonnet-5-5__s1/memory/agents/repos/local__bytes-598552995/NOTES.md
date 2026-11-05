# Private notes: local__bytes-598552995

- 2026-11-05: Billing display rule from finance: never show more than was actually used, so never round up; truncate extra decimals instead (1048575 bytes -> 1023.99KB, not 1024KB or 1MB; 2047 bytes -> 1.99KB). Cause of the '1024KB' bug: bytes.format picks the unit before toFixed rounds, so values just under a unit boundary round up to 1024. Code is NOT to be changed until finance signs off the wording on the billing page.
- 2026-11-05: bytes.format has two conflicting display rules: billing truncates (never over-report), capacity-alerts rounds up (never under-report). Don't change the default rounding; add a per-call option.
