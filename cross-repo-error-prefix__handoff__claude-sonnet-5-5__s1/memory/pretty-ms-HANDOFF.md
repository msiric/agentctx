# Handoff
- `prettyMilliseconds` now throws TypeError if `options` is defined but not a non-null object (catches `prettyMilliseconds(ms, 2)`).
- `null` also throws (decision: not an object). `undefined` is allowed.
- Test added in test.js ("throw on non-object options").
- Error messages are prefixed with `pretty-ms: ` (user convention: log collector drops stack traces). Tests assert the messages.
