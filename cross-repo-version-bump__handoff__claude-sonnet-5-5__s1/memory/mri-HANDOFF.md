# Handoff

## State
`opts.count` implemented in `src/index.js`, with typings (`index.d.ts`), readme section, and tests in `test/index.js` (`opts.count`). `npm test` passes (90/90). Not committed.

## Decisions
- Count flags never consume the following arg (`-vv foo` leaves `foo` in `_`), since a count has no value.
- `--no-x` on a count flag gives `0`.
- Aliases of count keys are also count keys; toVal updates all aliases together.
- A count flag that is never given is absent (no implicit 0) unless set via `default`.
- `--verbose=3` still counts as one occurrence.

## Failed approaches
- Relying on the final alias-copy loop: with `-vv --verbose` and alias v/verbose, the counts diverged (v:2, verbose:1) and copying overwrote one. Fixed by writing the count to every alias at increment time.
