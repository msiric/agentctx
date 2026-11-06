# Handoff

## State
`ignoreEmpty` option for `parse()` is implemented (base.js), with types/docs (base.d.ts, readme.md), a runtime test (test/parse.js) and a type test (index.test-d.ts). Not committed.

## Decisions
- Dropped in the parse loop when the raw value is `''`; `?flag` has a `null` value, so it is kept.
- Only a wholly empty value drops the parameter; empty items inside array values (e.g. `a=1,,2`) are untouched. Bracket-format `a[]=` is dropped as it is a parameter with an empty value.
- Test results are compared via `structuredClone` because parse returns null-prototype objects.

- Policy (from the user, ahead of the 11.0.0 release): new parse/stringify behaviours are on by default, with an option to switch them off, because opt-in flags never get turned on. Exception: `ignoreEmpty` stays default `false`, as the reports service relies on it being off. Don't flip it.
- `ignoreEmpty` already covers bracket array items (`?tag[]=&tag[]=a` gives `{tag: ['a']}`); verified, full suite passes (322).

## Notes
- `npx tsd` reports 5 errors that also occur without this change (pre-existing).
- Don't use `npx ava`; the tests use `node:test`.

## stripTracking
- `parse()` option `stripTracking` (default `true`, per the policy above) drops `utm_*`, `fbclid`, `gclid`. Key matched after decoding, case-insensitive; valueless keys (`?utm_source`) also dropped. Implemented in the parse loop in base.js, with types, readme, runtime and type tests.
- Default-on is a behaviour change for anyone relying on those params; flagged to the user.
- Lint: `utm_source` as an object key trips camelcase/quote-props, so the test uses `Object.fromEntries`.
- `npx tsd`: still the same 5 pre-existing errors.
