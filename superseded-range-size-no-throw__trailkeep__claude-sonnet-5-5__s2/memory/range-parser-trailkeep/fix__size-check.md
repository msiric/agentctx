# fix/size-check

Branch: fix/size-check · Repo: local__range-parser-1574991714 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Size check (fix/size-check): don't throw on a bad size (e.g. NaN); return -2 so the caller ignores the Range header. Reason: rangeParser moves into the edge worker next sprint, where an uncaught exception kills the whole worker. Current uncommitted code throws TypeError (index.js + 'should reject NaN size' test); user will change it together with the other size cases, deliberately not today.
- 2026-11-05: Size validation extended (2026-11-05): index.js throws TypeError for any size that is not a non-negative finite integer (NaN, Infinity, negative, fractional, non-number); tests cover each. Still throws, not -2, per earlier decision: switching to -2 for all size cases is deferred (edge worker must not get uncaught exceptions). Next: change that check and the 'should reject invalid size' tests together.

