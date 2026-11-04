# HANDOFF

## State
Fork CI lives in a new file, `.github/workflows/fork-ci.yml`: tests on Node 18, 20, 22, 24. Upstream's `ci.yml` is untouched (still Node 6). Not committed.

## Fork rules (from the user)
We rebase onto upstream weekly, so edits to upstream files cause conflicts.
- `src/index.js` is the only upstream file we patch.
- Everything else of ours goes in new files (e.g. new tests in their own test file).
- README, types and package.json stay exactly as upstream.

## minimist `--` option
Done: `opts['--']` routes everything after a bare `--` to `argv['--']` (initialised to `[]` like minimist, even if no `--` is given). Patch is in `src/index.js` only; tests in new `test/dashdash.js`. README and `index.d.ts` deliberately not updated (fork rules), so the option is undocumented and untyped (TS users need a cast).

## Decisions
- Separate workflow instead of editing `ci.yml`, per the rules above. Consequence: upstream's Node 6 job still runs alongside ours; it can't be removed without editing `ci.yml`.
- `fail-fast: false` so one Node version failing doesn't hide the others.
- Used `actions/checkout@v4` / `setup-node@v4` (v2 runs on a deprecated runtime).
- `engines.node` in package.json left alone (upstream file).

## Verification
`npm install && npm test` on Node 24.22.1 locally: 84/84 pass before the `--` work; 91/91 pass after (Node 24 only). Node 18/20/22 not run locally; workflow not run on GitHub.
