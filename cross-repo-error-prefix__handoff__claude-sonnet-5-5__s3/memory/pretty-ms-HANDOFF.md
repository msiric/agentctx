# Handoff

- Task: `prettyMilliseconds(ms, options)` now throws TypeError if `options` is defined but not an object (e.g. `prettyMilliseconds(ms, 2)`). Done, with test in `test.js` ("throw on invalid").
- Error messages are prefixed with `pretty-ms: ` (user convention across their packages; their log collector drops stack traces).
- Decision: `null` also throws (it is not a usable options object); `undefined` is still allowed. Arrays are not rejected.
- Failed approaches: none.
