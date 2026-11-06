# Handoff

## State
`parse()` supports `types: {key: 'json'}` (branch `reports-filter`, uncommitted). The value is decoded with `JSON.parse`. Invalid JSON, including an empty value, stays the string. A valueless key stays `null`. Repeated or separated items are each decoded. Changes are in `base.js`, `base.d.ts` (option type and `unknown` result type), `readme.md`, `test/parse.js`, and `index.test-d.ts`. `node --test` passes (324). `tsd` reports 5 errors that are the same with and without these changes (checked via `git stash`), so they were there before.

The earlier `parseJsonParameter` helper was added and then removed at the user's request.

## Known limitation (decision pending)
- `JSON.parse` loses precision for integers above `Number.MAX_SAFE_INTEGER`. The reports team's account IDs are 64-bit (e.g. `1274593846275813376`), so `…813377` and `…813376` decode to the same number. The readme tells users to carry such IDs as strings. Not fixed in code. Options: a reviver that keeps big integers as strings or `BigInt`, or encode IDs as strings in the filter JSON.
- `parse()` does not strip a URL path, so a full link needs `extract()` or `parseUrl()` first.

## Decisions
- A `'json'` type takes precedence over `parseNumbers` and `parseBooleans`, like the other explicit types.
- No `'json[]'` type was added, since it wasn't asked for.
