# HANDOFF

## State
Added `{MMM}` (short English month names, Jan..Dec) to tinydate on branch `payroll`.
- `src/index.js`: new `MONTHS` array and `MMM` entry in `MAP`.
- `index.d.ts`: `'MMM'` added to `Defaults`.
- `test/index.js`: 3 tests (May, Jan, Dec). `npm test` passes (24/24); `pretest` rebuilds `dist`.
- `readme.md`: documented `{MMM}`.

## Also on branch `grants`
Added `{ddd}` (Sun..Sat, hardcoded English `DAYS` array, same reasoning as MMM) in src, index.d.ts, readme, and 3 tests (Mon, Sun, Sat).

## Decisions
- Hardcoded English array rather than `toLocaleString`: output is locale/ICU-independent and deterministic. 
- Existing pad/slice logic (`'00'+x).slice(-3)`) leaves 3-char names intact, so no formatter changes were needed.

## Failed approaches
None.

## Note
The uncommitted `{ddd}` changes (from the `grants` work) are present in the working tree on `payroll`; not sorted out yet.

## Quarter token
The quarter token definition differs per branch.
- `payroll` branch: DONE. `{Q}` = Australian financial-year quarter (year starts 1 July: Jul-Sep Q1, Oct-Dec Q2, Jan-Mar Q3, Apr-Jun Q4). Formula `floor(((month+6)%12)/3)+1` in `src/index.js`; added to `index.d.ts`, readme, and 6 tests.
- `grants` branch (this one): US federal fiscal year, starting 1 October, so Oct-Dec is Q1, Jan-Mar Q2, Apr-Jun Q3, Jul-Sep Q4. Not implemented yet; the user said to do it later, not today.
