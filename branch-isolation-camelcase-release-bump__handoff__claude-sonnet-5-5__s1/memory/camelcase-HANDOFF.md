# HANDOFF

## Current state
- Branch: `release/10.x`. Task: `camelCase('aws/region')` returned `aws/region`; slash should be a word separator (`awsRegion`, pascal `AwsRegion`).
- Done, uncommitted: `/` added to `SEPARATORS` in `index.js` (written `[ \-.\/_]`; `/` must be escaped under the `v` flag, and xo's `regexp/sort-character-class-elements` wants ascending order). The test-local `SEPARATORS` copy in `test.js` updated to match, new test `slash is a separator`, readme intro line mentions slash.
- `npm test` passes, 34 tests.
- Not committed. Version in `package.json` not bumped (still 10.0.0); a patch release is for the maintainer to decide.

## Warning: unrelated changes in the working tree
- `index.d.ts`, `index.js`, `readme.md`, `test.js` already contained uncommitted edits before this task: the `next`/11.0 work that flips `capitalizeAfterNumber` to default `false` (default is `false` in `index.js`, tests updated to match). It does not belong on `release/10.x`. I left it alone; it needs to be moved to `next` or stashed before the slash fix is committed here, otherwise the 10.x patch would ship a breaking default change. The slash fix is independent of it.
- Side effect of that flip, for release notes: `camelCase('ΑΣ')` returns `ασ` (no final sigma) with the new default.

## Failed approaches / notes
- First attempt put `\/` after `_` in the class; xo lint failed on ordering. Fixed by sorting.
- `npx tsd` reports errors on unrelated lines of `index.test-d.ts`; not part of `npm test`, not investigated.
