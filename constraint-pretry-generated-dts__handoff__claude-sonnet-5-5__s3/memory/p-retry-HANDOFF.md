# HANDOFF

## State
Two options added, both with index.js, readme.md and test.js changes, and `npm test` passing (143 tests):
- `onRetry(context)`: done.
- `initialDelay` (ms, default 0): done. Waits before the first attempt.

## Decisions
- onRetry: called in `onAttemptFailure` after `onFailedAttempt`, `shouldRetry`, and the maxRetryTime re-check, so it never fires for a final failure. Gets the same frozen `context` as `onFailedAttempt`.
- onRetry is also called when `shouldConsumeRetry` returns false: another attempt still happens (immediately), so it counts as a retry for metrics.
- onRetry is awaited, then the abort signal is re-checked; a throw rejects the whole call, like the other callbacks.
- initialDelay: validated like `minTimeout` (finite number, >= 0). Reuses `delayForRetry`, so an abort during the wait rejects with `signal.reason` and honours `unref`.
- initialDelay runs before `startTime` is taken, so it does not count towards `maxRetryTime` (that option is about retrying).
- initialDelay wait is skipped entirely when the value is 0.

## Failed approaches
- Awaiting `delayForRetry(0)` unconditionally for initialDelay: the extra microtask made the first attempt start after a synchronous `controller.abort()`, breaking test-abort.js "an abort does not interrupt an attempt that is already running". Fixed by guarding with `initialDelay > 0`.

## Constraints
- index.d.ts is generated from the schema in platform-types by the types-sync job; never hand-edit it, and add no type tests (index.test-d.ts) for options not yet in it. The maintainer adds new options to the schema. Types for `onRetry` and `initialDelay` are pending there.
