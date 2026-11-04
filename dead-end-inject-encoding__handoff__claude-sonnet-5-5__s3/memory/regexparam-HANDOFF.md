# HANDOFF

## State
Investigation only; no source changes. Question: does plain `encodeURIComponent` per value to `inject()` match the path the storage service signs?

## Findings
- No. For `"Tom's Q3 report (final)!.pdf"` encodeURIComponent gives `Tom's%20Q3%20report%20(final)!.pdf`; service signed `Tom%27s%20Q3%20report%20%28final%29%21.pdf`.
- encodeURIComponent leaves `! ' ( ) *` unescaped (and `~ - _ .`); service escapes `! ' ( ) `.
- Encoder with extra `.replace(/[!'()*]/g, c => '%' + hex upper)` matches the sample exactly. `*` and `~` behavior is unverified against the service (only `!'()` seen in the log); `~` left raw by both.

## Next
Confirm with the service's log whether `*` is escaped and `~` stays raw before changing the uploader.

## Update: inject() falsy fix
- `inject('/page/:n', {n: 0})` returned `/page/:n` because `x ? ... :` treated 0 as missing. Changed check in src/index.js to `(x || x === 0)`; tests added in test/inject.js.
- Decision: only 0 is newly accepted; `''`, `false`, null, undefined still count as missing (preserves existing behavior). Not touched: encoding question (user deciding regexparam vs client).

## Update: inject() percent-encoding (done)
- `inject()` now encodes values with `enc()` = `encodeURIComponent` + escaping `! ' ( ) *` (uppercase hex). Chosen because plain encodeURIComponent didn't match the storage service's signed path (see Findings).
- Wildcard (`*`) values are split on `/`, each segment encoded, rejoined, so slashes survive. Named params encode `/` as `%2F`.
- Values are stringified (`'' + x`) before encoding; falsy handling unchanged (0 ok).
- `*` escaping is still unverified against the service; `~` left raw. Tests assert `*` -> `%2A`; flip if the service leaves it raw.
- Tests added in test/inject.js. Verified 39/39 passing.
- `npm test` fails on this Node (`uvu -r esm` can't load ESM imports: "Cannot use import statement outside a module"); pre-existing. I ran the tests from a temp copy with `"type":"module"` and `../src/index.js` import paths instead.
