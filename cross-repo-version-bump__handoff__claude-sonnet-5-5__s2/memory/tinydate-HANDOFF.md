# Handoff

## State
Fixed: unknown tokens (e.g. `{foo}`) no longer throw `MAP[key] is not a function`; they are emitted as written. All tests pass.

## Changes
- `src/index.js`: in the replace callback, if the key is neither in `custom` nor `MAP`, push the literal `'{' + key + '}'` and return.
- `test/index.js`: the `customize` test previously asserted the TypeError for an unknown `{MMMM}`; it now asserts the token is kept as written, plus a `{foo} {HH}` case (plan 5 kept).

## Decisions
- Handled at template-compile time (not render time), so there's no per-call cost.

## Failed approaches
- None. First test edit had a wrong expectation (HH is 16 for the fixture date, not 00).

## Versioning
User's convention (all packages): publish from main after merge, so every change bumps package.json version itself — patch for fixes, minor for features. This fix bumped 1.3.0 -> 1.3.1 (no git tag created; tags like v1.3.0 exist for past releases).
