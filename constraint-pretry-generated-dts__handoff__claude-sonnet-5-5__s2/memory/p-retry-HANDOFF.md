# HANDOFF

## State
`onRetry` and `initialDelay` options added (index.js, readme.md, test.js). Both done; `npm test` is the check (xo lint + node --test, all passing). Uncommitted on branch `retry-hooks`.

## Decisions
- `onRetry(context)` is called in `onAttemptFailure` after `shouldRetry` and the final `maxRetryTime` check, immediately before the wait. That is the only point where another attempt is certain, so the final failure never triggers it.
- It also fires when `shouldConsumeRetry` returns `false`: the next attempt still happens (with no delay), so it is still a retry for metrics purposes.
- Receives the same frozen `context` as `onFailedAttempt`/`shouldRetry` (so `retryDelay` is the real wait).
- Awaited; a throw aborts retries like the other callbacks; the signal is re-checked after it.

- `initialDelay` (default 0, finite number ≥ 0, `null` = default): waited once in `pRetry` before the first attempt, via `delayForRetry`, so a signal abort during it rejects with the abort reason. The wait happens before `startTime` is taken, so it does not count against `maxRetryTime`. Rounded up and clamped to the timer maximum like other delays.
- The wait is skipped entirely (no `await`) when `initialDelay` is 0, so the first attempt still starts synchronously.

## Failed approach
- `initialDelay`: first version always awaited `delayForRetry` (which returns early for 0). That still yields a microtask, so the first attempt started late and `test-abort.js` "an abort does not interrupt an attempt that is already running" failed (abort landed before the attempt began). Fixed by guarding with `if (initialDelay > 0)`.
- First test used `retries: 0` with `shouldConsumeRetry: () => false`, expecting retries; existing behavior stops when `retriesLeft` is 0 regardless, so the test used `retries: 1`.

## Constraints
- `index.d.ts` is generated in this fork (types-sync job from the platform-types schema; CI fails on hand edits). Never edit it, and add no type tests (`index.test-d.ts`) for options not yet in it. The maintainer adds new options to the schema; `onRetry` and `initialDelay` types are pending there.
