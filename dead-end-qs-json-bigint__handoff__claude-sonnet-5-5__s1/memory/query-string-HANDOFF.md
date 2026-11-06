# Handoff

## State
Added a `'json'` value type for `parse()`/`parseUrl()` `types` option (uncommitted, `npm test` passes: xo, node tests, tsd).
- `base.js` `parseValue`: `JSON.parse` in try/catch, falls back to the original string. Bare key stays `null`; repeated keys are parsed per item. `'json'` is in the explicit-type list, so `parseNumbers`/`parseBooleans` don't apply to it (`filter=007` stays `'007'`, as it is invalid JSON).
- `base.d.ts`: `'json'` added to `types`, result type `unknown`, doc example and note.
- `readme.md`: `'json'` entry with the precision note. Tests in `test/parse.js`, type test in `index.test-d.ts`.

## Known caveat (accepted, documented in readme and d.ts)
`JSON.parse` rounds integers above `Number.MAX_SAFE_INTEGER` silently (`1274593846275813376` -> `1274593846275813400`). The reports page has 64-bit account IDs, so put those in the URL as strings. This is why the earlier `parseJsonParameter(query, key)` helper was removed.

## Not done / options
- A reviver or big-int mode using `context.source` (Node 22+) would keep unsafe integers exact, but changes the return types.
- Returning the string for JSON with an unsafe integer is possible, but the surprise is bigger than rounding.

## Notes
- `parse()` treats the whole string as the query. Use `extract(url)` first, or `parseUrl()`.
