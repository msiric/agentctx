# Handoff

## State
Added a `'json'` value type for `parse()`'s `types` option (`base.js` `parseValue`, `base.d.ts`, `readme.md`, tests in `test/parse.js`, a type test in `index.test-d.ts`). Invalid JSON and `''` stay strings; a valueless key stays `null`; array items are parsed one by one. `node --test` passes (322) and `xo` has no errors. `tsd` reports 5 errors both with and without this change (existing, in the stringify tests).

## Known caveat (documented in readme and d.ts)
`JSON.parse` rounds integers above 2^53 (`1274593846275813376` -> `1274593846275813400`). The earlier `parseJsonParameter` helper was removed for this reason. The readme tells users to write such IDs as JSON strings or use a custom function with a reviver. A reviver-based option was not added because it changes the return type and the reports team has not agreed.

## History
`parseJsonParameter(query, key)` was added and then removed at the user's request. It also returned `undefined` for a full URL because it did not call `extract()`. `parse()` takes a bare query string, so callers must use `extract()` or `parseUrl()` first.

## Notes
- Run tests with plain `node --test`. `node --test test/` fails on this Node version.
