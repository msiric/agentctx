# Handoff

## State
Added `{Q}` (payroll quarter, Australian FY, 1 July start: Jul-Sep=1, Oct-Dec=2, Jan-Mar=3, Apr-Jun=4) in `src/index.js` with tests, `Defaults` type, readme line. `npm test` passes (35/35). Earlier: `{ddd}`, `{MMM}` (fixed English arrays, locale-independent).

## Earlier state
Also added `{ddd}` (short English weekday: Sun..Sat) via a fixed `DAYS` array in `src/index.js`, with tests, `Defaults` type, and readme entry. `npm test` passes (28/28; `dist` is rebuilt by pretest and gitignored).

Earlier: added `{MMM}` (short English month name: Jan..Dec) to `src/index.js`, with tests in `test/index.js`, the `Defaults` type in `index.d.ts`, and a readme entry. `npm test` passes (24/24).

## Decisions
- `{ddd}` also uses a fixed English array (not `toLocaleString`) for the same locale-independence reason.
- Used a fixed English `MONTHS` array rather than `toLocaleString`, so output doesn't depend on the runtime's locale/ICU (this build is vendored into the payroll app).
- Existing padding logic (`'00' + x).slice(-key.length)`) works unchanged for 3-letter names.

## Failed approaches
None.

## Upcoming (not started)
Grants portal also needs a quarter token (not for today), but it uses the US federal fiscal year, which starts 1 October: Oct-Dec = Q1, Jan-Mar = Q2, Apr-Jun = Q3, Jul-Sep = Q4. This differs from the `{Q}` mapping now in this payroll build, so the two must not share one mapping.
