# Handoff

## State
Added `elapsedTime` (ms since `pRetry` was called) to the context passed to `shouldConsumeRetry`, `onFailedAttempt` and `shouldRetry`. Done; `npm test` (xo, node --test, type tests) passes.

- `index.js`: `elapsedTime: performance.now() - startTime` in both context objects in `onAttemptFailure`.
- `index.d.ts`: documented on `RetryContext`. `index.test-d.ts`: type assertion.
- `readme.md`: bullet in the context object list.
- `test-timing.js`: test using `withFakeTime`, checking all three callbacks.

## Decisions
- Read `performance.now()` separately for each of the two context objects rather than once, because `shouldConsumeRetry` can be slow and `onFailedAttempt`/`shouldRetry` should see the time that passed. They share the second object.
- Used `startTime` already captured in `pRetry` (same clock as `maxRetryTime`), so no new state.

## Failed approaches
None. First test draft had lint errors (unused var, indentation), fixed.

## Retry-After (done; `npm test` passes, 139 tests)
Billing client sets `error.retryAfter` (seconds) on 429s. Built into `index.js` (`getRetryAfter`, used in `onAttemptFailure`), as the user asked for built-in support, not a hook.

Decisions:
- Wait `retryAfter * 1000` PLUS the normal backoff, as a single timer. Reason: Retry-After is when billing's rate window reopens, and ~40 pods returning at that exact moment get 429'd again. The backoff (with `randomize`) spreads them out.
- `maxTimeout` clamps only the backoff, so Retry-After can exceed it.
- `maxRetryTime`: if the Retry-After wait is >= the time left (checked after `shouldRetry`), throw the error instead of retrying early or truncating. The backoff part is still truncated as before.
- Bad values (NaN, <= 0, Infinity, string, null): ignored, backoff only. The sum is capped at 2^31-1.
- `shouldConsumeRetry` false: Retry-After is still waited, backoff is not (the delay is the server's request, not the caller's pacing). To do that the wait now happens before `return consumeRetry`; previously a non-consumed retry returned before waiting, which was fine only because its delay was 0.
- `retryDelay` in the callback context includes `retryAfter`.

Failed approaches: first version only changed the delay and the non-consumed test failed with no wait, because of the early `return false` above. Also lint (`prefer-combined-guards`, `no-return-array-push`) forced small rewrites.

Docs: readme paragraph + `retryDelay` text, `index.d.ts` comment. Tests: six at the end of `test-timing.js`.
