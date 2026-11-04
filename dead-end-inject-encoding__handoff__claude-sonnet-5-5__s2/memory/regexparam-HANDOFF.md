# HANDOFF

## Task
Uploader builds object-storage paths with `inject()`; names with spaces etc. go in raw and the storage service rejects them. Goal: encode values. No code changed yet (user asked for a check first).

## Findings
- Plain `encodeURIComponent` does NOT match what the storage service signs.
  - Sample: `"Tom's Q3 report (final)!.pdf"`
  - encodeURIComponent: `Tom's%20Q3%20report%20(final)!.pdf`
  - service signed: `Tom%27s%20Q3%20report%20%28final%29%21.pdf`
  - Cause: encodeURIComponent leaves `! ' ( ) *` (and `- _ . ~`) unescaped; the service escapes `! ' ( ) *`.

## Decisions / next steps
- Likely fix: `encodeURIComponent(v).replace(/[!'()*]/g, c => '%' + c.charCodeAt(0).toString(16).toUpperCase())`. Not yet applied or tested against more request-log samples.
- Not yet decided whether this belongs in regexparam or in the uploader's wrapper.

## Update: inject() with numeric 0
- Bug: `inject('/page/:n', {n: 0})` returned `/page/:n` because the value check was truthiness. Fixed in src/index.js (`x || x === 0`); tests added in test/inject.js. Empty string/false/null still count as missing (unchanged behavior).
- Encoding question still on hold until user decides regexparam vs. client.
- Fix verified manually in node (copied src/index.js to a temp .mjs): `/page/0` for both `:n` and `:n?`. The new tests in test/inject.js have NOT been run.
- `npm test` (`uvu -r esm test`) fails on clean main too (stashed my changes to confirm): "SyntaxError: Cannot use import statement outside a module" — the old `esm` loader doesn't work on this Node. Not fixed; out of scope. Changes are uncommitted.

## Update: encoding implemented (in regexparam)
- User decided: encode inside `inject()`. Added `enc()` in src/index.js = `encodeURIComponent` + escape `! ' ( ) *` as uppercase `%XX` (matches the storage service's signing; plain encodeURIComponent doesn't).
- Wildcard (`*`) values are split on `/`, each segment encoded, rejoined, so slashes stay. Named params encode `/` as `%2F`.
- Tests added in test/inject.js (spaces/quotes/parens, `/ ? #`, `.ext` suffix, wildcard, unicode, unreserved chars). All 37 pass, run via a temp copy as `.mjs` since `npm test` (`uvu -r esm`) is still broken on this Node.
- Behavior change: breaking for callers who pre-encode values (they'd be double-encoded). Not committed; README/index.d.ts docs not updated.
