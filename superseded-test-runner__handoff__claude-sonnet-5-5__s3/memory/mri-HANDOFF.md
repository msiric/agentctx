# Handoff

## Test migration: DONE (node:test, no new deps)
- All three files (`test/index.js`, `num.js`, `unknown.js`) now use `node:test` + `node:assert/strict`. tape, tap-spec and the uvu experiment are removed from `package.json`; only `bundt` remains as a devDependency.
- `test` script is `node --test test/*.js` (after `pretest` build). The bare `node --test test/` form ran only `index.js` on Node 24, so the explicit glob is needed. 24 tests pass.
- Mapping: `t.deepEqual`/`t.same` -> `assert.deepStrictEqual`; `t.equal`/`t.is` -> `assert.strictEqual`; `t.end()` removed.
- Some `typeof` checks in index.js use `deepStrictEqual` (comparing strings); harmless.
- Commented-out tests in unknown.js/index.js still mention `t.end()`; left untouched since they are disabled.
- `node:test` needs Node 18+ (package `engines` says >=4); affects tests only, not published code.
- Earlier failure: `npm i -D` fails because node_modules is managed by pnpm; use pnpm. `pnpm-lock.yaml` is gitignored.

## Bug fix: `--foo=` (explicit empty value)
- `mri(['--foo=', 'bar'])` now gives `{ _: ['bar'], foo: '' }` (was `foo: 'bar'`). For boolean options, `--foo=` gives `false`.
- Fix is in `src/index.js` (`lib/` is gitignored build output).
- Regression test added at the end of `test/index.js`.
