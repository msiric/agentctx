# Handoff

## State
Added `elapsedTime` (ms since `pRetry` was called) to the context passed to `onFailedAttempt`, `shouldRetry` and `shouldConsumeRetry`. Done, `npm test` (xo, node --test, nz) passes.

Touched: `index.js`, `index.d.ts`, `index.test-d.ts`, `readme.md`, `test-timing.js` (new test).

## Decisions
- Measured with `performance.now() - startTime`, reusing the existing `startTime`, so it uses the same clock as `maxRetryTime`.
- Computed when each context object is built, so `shouldConsumeRetry`'s value is slightly lower than `onFailedAttempt`'s for the same failure. `shouldRetry` reuses the `onFailedAttempt` context, so it has the same value.

## Failed approaches
- First test version failed because the recording callback returned `undefined`, which `shouldRetry` reads as "don't retry". The callbacks must return `true`.

## Retry-After support: done, `npm test` passes
User asked to proceed and said p-retry should honour a numeric `error.retryAfter` (seconds) itself, so this **reverses the earlier rejection** of reading it automatically. No `getRetryDelay` option was added.
- `calculateRetryAfter` in `index.js`: positive finite number of seconds -> ms (ceil), anything else ignored. Read only when a retry can follow.
- Additive to the backoff (kept from the earlier plan: ~40 pods released at the same instant would be 429'd again; backoff spreads them). Needs `randomize: true` to actually spread.
- `maxTimeout` caps only the backoff part; the sum is capped at the setTimeout limit. `maxRetryTime` still truncates the sleep as before (the "fail early" alternative was not chosen; open if wanted).
- Flows into `delayTime`, so `retryDelay` in all contexts includes it.
- Docs: new "Retry-After" section and `retryDelay` note in `readme.md`. Tests in `test-timing.js`. Not done: `index.d.ts` has no change (no new option); could document `retryAfter` there if wanted.
- Earlier caveat stands: with `randomize: false` pods stay synchronized.
- The user had paused this for the 429 dashboards check; they have since said to go ahead.
