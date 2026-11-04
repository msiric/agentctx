# HANDOFF
- Task: unknown tokens (e.g. `{foo}`) threw `MAP[key] is not a function`; they should stay in output as written.
- Fix (src/index.js): if a token is neither in `custom` nor an own property of `MAP`, push the literal `{key}` string. hasOwnProperty is used so keys like `constructor` aren't treated as known.
- Test: the 'customize' test in test/index.js asserted the old TypeError; replaced with an assertion that `{MMMM}` stays literal (plan 5 -> 4).
- Version bumped 1.3.0 -> 1.3.1 in package.json (patch: bug fix). Owner publishes from main after merge and bumps version in every change (patch=fix, minor=feature).
- Status: all 20 tests pass. No failed approaches.
