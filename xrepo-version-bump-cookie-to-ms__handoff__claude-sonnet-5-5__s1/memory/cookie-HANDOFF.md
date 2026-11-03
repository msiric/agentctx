# Handoff

## State

`stringifySetCookie` accepts `expires` as `Date | number` (ms since epoch). Done: src/index.ts, README, tests in src/stringify-set-cookie.spec.ts. Typecheck and tests pass.

## Decisions

- Numbers are converted with `new Date(n)` and then validated, so NaN, Infinity and out-of-range values (>8.64e15) throw the same `option expires is invalid` TypeError as an invalid Date.
- The guard is `typeof expires === "number" || expires`. The old truthiness check alone would skip `0` (a valid epoch) and `NaN` (which must throw).

## Failed approaches

None.

## Versioning

Bumped 2.0.1 -> 2.1.0 (minor, new feature) in package.json and package-lock.json, in the same commit as the change. The release script publishes whatever version on main isn't on npm yet, so the bump must ship with the change. Minor for features, patch for fixes.
