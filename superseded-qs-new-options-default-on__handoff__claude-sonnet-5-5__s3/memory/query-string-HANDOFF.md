# Handoff

## State
`parse()` has an `ignoreEmpty` option (default `false`). Implemented in `base.js`, with types in `base.d.ts`, `index.test-d.ts`, readme and tests in `test/parse.js`. `node --test` and `xo` pass (xo only has warnings that were already there). Not committed.

## Decisions
- The check is `value === ''` right after `splitOnFirst`, before decoding and the array formatter. A key without `=` has a `null` value, so it is kept. A raw empty value is the same as a decoded one, and it also works for the `comma`/`separator` formats, which do not decode there.
- Skipping happens per parameter, so empty array items (`a[]=&a[]=1`) are dropped too.
- Opt-in: default is `false`, tests cover omitted, `false` and `undefined`, plus `parseUrl()`. This follows the 10.x rule (new behaviour is opt-in), which is now superseded (see Rules).
- Not decoded first: `a=%20` is a space, not empty, so it is kept.

## Failed
- Ran `npx ava` by mistake. The project uses `node --test`.

## Update
Request to cover array items (`?tag[]=&tag[]=a` with `arrayFormat: 'bracket'` gives `{tag: ['a']}`) was already satisfied by the per-parameter check. Re-verified by hand and with `node --test` (323 pass). No code change needed.

## Rules
- From 11.0.0 (cut next week), the user's rule is that new parse/stringify behaviours are on by default, with an option to switch them off, because opt-in flags never get enabled.
- Exception: `ignoreEmpty` stays default `false`, since the reports service relies on it being off. Do not flip it.

## stripTracking (added)
- `parse()` option `stripTracking`, drops `utm_*`, `fbclid`, `gclid`. Matched on the decoded key, case-insensitive, per parameter (so array items like `utm_a[]` go too). Code in `base.js` (`isTrackingParameter`), types, readme, tests in `test/parse.js`.
- Default is `true`, per the Rules above (new behaviours on by default from 11.0.0, with an option to turn off). This is a breaking change for 10.x users.
- `pick()`/`exclude()` force `stripTracking: false` for their internal `parseUrl`/`parse` calls. Otherwise the default would silently remove tracking params from their output and from the predicate's view. `parseUrl()` itself does strip by default.
- `node --test` (326 pass) and `xo` clean. Lint forced `Object.fromEntries` in two tests because of camelcase on `utm_source` keys. Not committed.
