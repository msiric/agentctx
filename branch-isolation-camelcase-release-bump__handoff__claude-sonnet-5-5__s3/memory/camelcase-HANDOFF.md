# Handoff

## State
`capitalizeAfterNumber` now defaults to `false` (planned for 11.0, on branch `next`). `foo2bar` stays `foo2bar`. Changes: `index.js` default, `index.d.ts` and `readme.md` (default, `@default`, example), `test.js`. `index.test-d.ts` needed no change (it always passes the option explicitly). `npm test` (xo, node --test, nz) passes. Not committed.

## Decisions
- Tests that relied on the old default now pass `capitalizeAfterNumber: true` explicitly, so they still cover the true path. Don't remove those to make them "default" tests.
- `booleanOptionSets` in `test.js` lists `capitalizeAfterNumber` explicitly in every set, because an omitted key now means false and the true path would silently go untested.
- Added a `capitalizeAfterNumber defaults to false` test.
- The "settings agree when there is no digit" and `preserveConsecutiveUppercase` tests compare false against an explicit true; with the default flipped, comparing against an omitted option would pass trivially.

## Failed / notes
- Flipping the default alone broke 11 tests. Fixed by making the true-path tests explicit, not by changing expectations.
- Still to do for the release: changelog or migration note if the project keeps one (none in the repo).

## Constraints
- Do not edit the version in `package.json` on this branch. The release job derives it from the changesets and fails if it is bumped by hand. No `.changeset` directory exists in the repo, so ask where changesets live before adding one.

## Slash separator (bug report on 10.x)
- `/` is now a separator: `SEPARATORS` in `index.js` and the mirror in `test.js` are `/[ \-.\/_]+/v` (escaped, and ordered to satisfy xo's `regexp/sort-character-class-elements`; an unescaped `/` is a parse error in a regex literal). `aws/region` → `awsRegion` / `AwsRegion`.
- Added tests in the separators test and `/` in the `separatorRuns` cross product. Readme and `index.d.ts` tagline mention slash. `npm test` passes.
- Note: this worktree is on `release/10.x` but still holds the uncommitted `capitalizeAfterNumber` default flip (planned for 11.0). The two changes are mixed in the same files, so split them before committing the slash fix to 10.x. Not committed.
