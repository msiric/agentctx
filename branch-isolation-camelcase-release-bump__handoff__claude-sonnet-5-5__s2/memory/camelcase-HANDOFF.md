# Handoff

## State
`capitalizeAfterNumber` now defaults to `false` (planned for 11.0, on `next`). Not committed, version not bumped.

- `index.js`: default flipped.
- `index.d.ts`, `readme.md`: `@default false`, "(default)" label moved to the `false` case.
- `test.js`: tests that relied on the old default now pass `capitalizeAfterNumber: true` explicitly (done with a one-off script that only rewrote assertions that failed under the new default and passed with `true`). Added a "defaults to false" test.

## Decisions
- Kept the existing tests' intent by making the old behaviour explicit rather than rewriting expected values.
- Reference-model and sweep tests pass `capitalizeAfterNumber: true` because the reference models that path.

## Notes
- `index.test-d.ts` needed no change (it already passes the option explicitly).
- The breaking change still needs a release-notes entry.
- Do NOT bump `version` in package.json on this branch: the release job derives it from changesets and fails on a manual bump. No `.changeset` dir exists yet; add one only if the release job needs it (format unconfirmed).

## Slash as separator (bug report: `camelCase('aws/region')` unchanged)
- `index.js`: added `/` to `SEPARATORS` (`/[ \-.\/_]+/v`). All separator logic derives from that one regex, so `aws/region` → `awsRegion`, pascalCase → `AwsRegion`.
- `test.js`: added assertions in the `foo_bar` camelCase and pascalCase tests. `readme.md`/`index.d.ts` description now says dash/dot/underscore/slash/space.
- Lint (xo) constraints: `/` must be escaped in the class, and `regexp/sort-character-class-elements` wants it before `_` (an unescaped `/` is a parse error; first order tried failed lint).
- Behavior change: inputs containing `/` (e.g. paths) now get camelized, which is user-visible. Worth a release-notes line. Leading `/` is stripped like other leading separators.
- The uncommitted `capitalizeAfterNumber` default flip above is a separate, unrelated change in the same working tree; it is not part of this fix, and the new tests don't depend on it.
