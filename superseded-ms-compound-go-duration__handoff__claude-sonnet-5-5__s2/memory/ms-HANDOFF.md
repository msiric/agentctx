# Handoff

## State
- `compound: true` option added to `format`/`ms` (src/index.ts `fmtCompound`), with tests in
  src/format.test.ts and src/index.test.ts, plus a README section. Committed on feat/compound-format;
  not pushed, no PR opened.
- Output is Go `time.ParseDuration`-compatible (deploy logs are scraped by a Go service): no spaces,
  hours are the biggest unit, no `d`. E.g. `25h30m`. Implementation, tests, README, JSDoc updated
  (uncommitted until the wrap-up commit).
- `parse()` trims surrounding whitespace (committed, tests in src/parse.test.ts).

## Decisions
- Units h/m/s only (Go-compatible), so 400 days -> `9600h`.
- Leftover ms are floored away (on the absolute value, so negatives truncate toward zero too).
- Sub-second values (incl. negative) give `0s`, never `-0s` or an empty string.
- `compound` takes precedence over `long` (output is always short unit letters).
- parse whitespace: trim only the matched string; length check still applies to the raw input, and
  whitespace-only input returns NaN (not a throw).

## Failed approaches
None.
