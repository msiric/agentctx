# Handoff

## State
Fork CI matrix (Node 18, 20, 22, 24) lives in `.github/workflows/fork-ci.yml`. Done.
Upstream `ci.yml` (Node 6 only) is left untouched, so it still runs alongside.

## `--` option (minimist parity)
Done. `src/index.js`: when `opts['--']` is truthy, `out['--']` is initialised to `[]` (like minimist, always present)
and args after the first bare `--` go there instead of `out._`. Tests in new file `test/dashdash.js`.
Readme and `index.d.ts` deliberately NOT updated (must match upstream; see below) so the option is undocumented/untyped here.
`lib/` is gitignored build output (`npm test` rebuilds it via pretest).

## Decisions
- This fork rebases onto upstream (lukeed/mri) weekly. Only `src/index.js` is patched in upstream files;
  everything else of ours goes in NEW files (own workflow files, own test files). readme, types
  (`index.d.ts`) and `package.json` must stay identical to upstream. Hence a separate workflow, not an edit to `ci.yml`.
- Workflow uses `actions/checkout@v4` / `actions/setup-node@v4` (v2 is deprecated) and `fail-fast: false`.
- `engines.node` (`>=4`) not changed, since package.json must match upstream.

## Verification
`npm test` passes locally (100/100, includes new dashdash tests) on Node 24.22.1. Node 18/20/22 not run locally; workflow not yet run on GitHub.
