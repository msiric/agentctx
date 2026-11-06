# Handoff

## State
Added `elapsedTime` (ms since `pRetry` was called, from the existing `startTime`) to the context for `shouldConsumeRetry`, `onFailedAttempt` and `shouldRetry`. Changes are in `index.js`, `index.d.ts`, `index.test-d.ts`, `readme.md` and `test-timing.js`. The work is uncommitted.

## Decisions
- `onFailedAttempt` and `shouldRetry` share one frozen context object, and the existing test `each callback receives its own frozen context object` requires it. So they share one `elapsedTime`, measured before `onFailedAttempt` runs. It does not include time spent inside `onFailedAttempt`.
- `shouldConsumeRetry` has its own context, so its value is measured separately.

## Failed approach
Building a fresh context for `shouldRetry` so it would include `onFailedAttempt`'s duration broke that shared-object test. I reverted it.

## Retry-After (implemented, uncommitted)
The user asked for it directly: an error with a numeric `retryAfter` (seconds) is honoured before the next attempt. `npm test` passes (xo, node --test, tsd).

Decisions:
- Wait = `retryAfter * 1000 + normal backoff` (the user's earlier decision: the hint is the moment the rate window reopens, and the backoff spreads ~40 pods out). Not an override, not `max()`.
- Built-in read of `error.retryAfter` in `getRetryAfterDelay` (`index.js`), not the generic ms hook from the earlier plan, because the request named `retryAfter` on the error. A non-number, non-finite or <= 0 value is ignored. The hint is capped at the `setTimeout` limit.
- Applied where `delayTime` is computed, so `retryDelay` in every context shows the real wait. `maxTimeout` caps the backoff only. `maxRetryTime` still clamps the final wait.
- Closed the open item: with `shouldConsumeRetry` false the retry has no backoff but still waits the hint (`effectiveDelay = retryAfterDelay`). `onAttemptFailure` now always goes through `delayForRetry` and returns `consumeRetry`.

Still open:
- When the hint exceeds the time left under `maxRetryTime`, it is clamped and one last attempt is made, rather than throwing at once. Not changed.
- Jitter: with `randomize: false` every pod adds the same backoff and still returns together. The billing client should set `randomize: true`.
- Not read: an `AbortError`-wrapped or non-Error thrown value's `retryAfter` (the normalized `TypeError` for non-errors has none).
