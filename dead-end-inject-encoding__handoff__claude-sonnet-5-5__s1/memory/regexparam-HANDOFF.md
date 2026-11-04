# Handoff

## State
- Fixed `inject()` dropping a value of `0` (`inject('/page/:n', {n: 0})` returned `/page/:n`). Cause: truthiness check on the value in `src/index.js`. Now `(x || x === 0)`.
- Added tests in `test/inject.js` for `:n` and `:n?` with `n: 0`.
- `''`, `null`, `undefined`, `false` are still treated as missing (unchanged behavior, deliberately minimal).

## Decisions
- DONE: `inject()` now percent-encodes values (user asked for it in regexparam). Uses `encodeURIComponent` plus uppercase `%XX` for `! ' ( ) *` (strict RFC 3986), per the finding below. Wildcard (`*`) values are split on `/`, each segment encoded, slashes kept. Tests added in `test/inject.js`.
- Behavior change: callers that pass pre-encoded values will now get double encoding.
  - Finding: plain `encodeURIComponent` does not match the storage service's signed path; it leaves `! ' ( ) *` unescaped. Also escaping those with `%XX` (uppercase hex) matched the one sample from the log. Only one sample tested.

## Failed / caveats
- `npm test` fails in this environment before running any test (`uvu -r esm` can't handle ESM imports on this Node; fails identically without my changes). Verified the fix and encoding cases by running `inject` directly in node instead (the new test cases' expected values were checked that way, not via uvu).
