# Handoff

## Test migration: tape -> node:test (DONE)
- All of test/{index,num,unknown}.js use `node:test` + `node:assert` (strict deepStrictEqual/strictEqual). uvu was dropped (security review blocks new devDeps).
- `npm test` = build (pretest) + `node --test` (23 tests pass). Note: `node --test test/` only ran index.js on Node 24; plain `node --test` discovers all files.
- Removed tape and tap-spec from devDependencies. pnpm-lock.yaml is untracked/ignored and had no tape entry; `pnpm install --lockfile-only` was a no-op.
- CI (.github/workflows/ci.yml) bumped from Node 6 to 20, since `node:test` needs Node >=18. `engines.node` in package.json is still ">=4" (applies to the library at runtime, not tests) — left unchanged; decide whether to bump.
- tape's loose `deepEqual` was replaced by strict equality; all tests still pass.
- Commented-out old tests still contain `t.end()` comments; left as is.

## Fix: `--foo=` explicit empty value (NOT PRESENT in working tree)
- An earlier note claimed src/lib were changed so `mri(['--foo=', 'bar'])` gives `{ _: ['bar'], foo: '' }`. Verified this session: src/ and lib/ have no such change (git shows them unmodified; current output is `{ _: [], foo: 'bar' }`). The fix was lost or never saved. A regression test was tried and removed since it fails. Redo the fix and add the test if still wanted.
