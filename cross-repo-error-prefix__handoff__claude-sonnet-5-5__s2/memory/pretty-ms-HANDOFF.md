# Handoff

- Task: `prettyMilliseconds(ms, 2)` (number mistaken for unitCount) used to be silently ignored; now throws TypeError.
- Decision: only `undefined` is allowed as a non-object; `null` also throws (it's "passed" and not a usable options object).
- Change in `index.js` (check before `{...options}`), test in `test.js`.
- Error messages are prefixed with `pretty-ms: ` (user's convention across packages; their log collector drops stack traces).
