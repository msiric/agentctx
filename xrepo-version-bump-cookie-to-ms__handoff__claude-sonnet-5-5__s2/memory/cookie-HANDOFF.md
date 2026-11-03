# Handoff

Task: `stringifySetCookie` accepts `expires` as `Date | number` (ms since epoch).

- Number is converted with `new Date(n)`; invalid (NaN, Infinity, out of range) throws the same "option expires is invalid" error.
- Check changed from `if (cookie.expires)` to `!= null` so `0` (epoch) works.
- `SetCookie.expires` type is shared with parse (which still returns Date).
- Updated JSDoc, README, and tests in src/stringify-set-cookie.spec.ts.
- Bumped version 2.0.1 -> 2.1.0 (minor, feature) in package.json and package-lock.json; release script publishes unpublished versions on main, so bump ships with the change.
