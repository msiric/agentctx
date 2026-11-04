# HANDOFF

## State
`opts.count` implemented in `src/index.js` (+ types, readme, `test/count.js`). All tests pass.

## Decisions
- Count keys are also pushed into `opts.boolean` so they never swallow the next arg (`-v foo` -> `_: ['foo']`).
- Aliases are updated in lockstep in `toVal` so `-v --verbose` gives 2 on both; the final alias-copy step would otherwise overwrite with one side's count.
- `--no-v` sets count to 0 (not false).
- Unused count keys are absent unless `default` supplies them.

## Failed
- First version counted each alias separately; the alias copy then dropped counts (test caught it).
