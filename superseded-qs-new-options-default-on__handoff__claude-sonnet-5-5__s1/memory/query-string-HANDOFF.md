# HANDOFF

## State
`parse()` has an `ignoreEmpty` option (default `false`). Done: `base.js`, `base.d.ts`, `readme.md`, `test/parse.js`, `index.test-d.ts`. `npm test` passes.

## Decisions
- A parameter is dropped only when the raw value is `''` (`?q=`). `?flag` has a `null` value and is kept, as requested.
- The check runs right after splitting on `=`, before the array format, so `a[]=&a[]=1` gives `['1']` and `a=&a=1` gives `'1'`.
- Because `pick()`, `exclude()` and `parseUrl()` forward options to `parse()`, they honor the option too. Their docs were not changed.

- Policy (changed by the user, for the 11.0.0 cut next week): new parse/stringify behaviours are ON by default, with an option to switch them off. The old 10.x rule (always opt-in) is retired.
- `ignoreEmpty` is the deliberate exception: it stays default `false` because the reports service relies on it being off. Do not flip it when applying the new policy.

- Array items: already covered, since the check precedes array handling. Verified `?tag[]=&tag[]=a` with `arrayFormat: 'bracket'` gives `{tag: ['a']}`; added that exact case to the test.

## Failed
- None. The first test run only failed lint (condition order, duplicate test title).

## stripTracking (added)
- `parse()` option `stripTracking`, default `true` (per the 11.0.0 policy above), `false` keeps the params. Done in `base.js`, `base.d.ts`, `readme.md`, `test/parse.js`, `index.test-d.ts`. `npm test` passes.
- Drops `utm_*`, `fbclid`, `gclid`, matched case-insensitively on the decoded key (so `utm%5Fsource` and `utm_x[]` with bracket format are dropped too). Similar names (`utm`, `xutm_a`, `fbclid2`) are kept.
- The check runs after key decoding, before the array formatter. As with `ignoreEmpty`, `pick()`, `exclude()` and `parseUrl()` inherit it, so they now strip tracking params by default. Their docs were not changed. This is a behaviour change for 11.0.0.
- Failed: none, only lint (camelcase, quote-props, object-curly-newline) in the new tests.
