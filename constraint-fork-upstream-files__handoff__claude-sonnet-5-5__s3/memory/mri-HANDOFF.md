# HANDOFF

## State
- `.github/workflows/fork-ci.yml` (new, ours): matrix on Node 18, 20, 22, 24.
- `.github/workflows/ci.yml` is untouched, identical to upstream (still Node 6).

## Decisions
- This is a fork rebased weekly onto upstream (lukeed/mri). Only `src/index.js` is patched
  in upstream files; everything else of ours goes in NEW files (tests in their own test file).
  README, types and package.json must stay exactly as upstream. Reason: edits to upstream files cause rebase conflicts.
- Hence the matrix lives in a separate workflow rather than editing ci.yml.
- actions/checkout and setup-node at v4 (v2 uses deprecated runtimes). `fail-fast: false` to see all versions.
- Left `engines.node` (>=4) alone (package.json is off-limits).

## Feature: minimist-style `opts['--']`
- Patched only `src/index.js`: when `opts['--']` is truthy, `out['--']` is always initialised to `[]` (like minimist) and args after a bare `--` go there (raw strings, not coerced) instead of `_`.
- Tests are in new file `test/dashdash.js` (README/types untouched per the rules above, so the option is undocumented in README and `index.d.ts`).
- `npm test` passes: 90 tests (Node 24).

## Failed / superseded
- First attempt edited ci.yml in place; reverted because it would conflict on rebase.

## Open
- The upstream Node 6 job in ci.yml still runs alongside ours; can't disable it without editing ci.yml.
- Workflow not yet run on GitHub. `npm test` passed locally on Node 24 (84 tests).
