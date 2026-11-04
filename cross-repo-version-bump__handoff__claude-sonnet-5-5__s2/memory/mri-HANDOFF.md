# HANDOFF

## State
`opts.count` implemented in `src/index.js`, typed in `index.d.ts`, documented in `readme.md`, tested in `test/count.js`. All 95 tests pass (`npm test`; tests run against the built `lib/`).

## Decisions
- Count keys are also pushed onto `opts.boolean`, so they never swallow the next arg (`-v foo` -> `foo` goes to `_`).
- Counting happens in `toVal`; all aliases of a key are set to the same total there, so the end-of-parse alias copy can't overwrite with a stale count.
- `--no-<key>` on a count key sets `0` (not `false`).
- Absent count flags are omitted unless given in `opts.default`.

## Failed approaches
- First version summed the counts of every alias name; since all aliases already hold the same total, that double-counted (`-vv --verbose` gave 7). Fixed by using only the current key's total.
