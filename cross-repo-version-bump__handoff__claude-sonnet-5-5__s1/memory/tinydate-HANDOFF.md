# HANDOFF

## State
Unknown template tokens (e.g. `{foo}`) no longer throw `MAP[key] is not a function`; they are emitted as written. Fix in `src/index.js`. All tests pass (22).

## Decisions
- Token is "known" if it's in `custom` or is an *own* key of `MAP` (hasOwnProperty), so `{constructor}`/`{toString}` don't resolve to inherited Object methods.
- Unknown tokens are pushed as the literal string `'{' + key + '}'` at parse time (no per-call cost).
- The existing `customize` test asserted the old TypeError for `{MMMM}`; changed it to assert the token is left as written (plan 5 -> 4). Added an `unknown tokens` test.

## Failed approaches
- First edit of the test via script dropped the `customize` test's closing `});`; fixed.

## Versioning
User publishes straight from main after merge, so every change bumps package.json version (patch = fix, minor = feature). Bumped 1.3.0 -> 1.3.1 for this fix (edited by hand; no tag/commit created).
