# HANDOFF

## State
Added `{MMM}` (short English month name: Jan..Dec) to tinydate on branch `payroll`.
Touched: `src/index.js`, `index.d.ts`, `readme.md`, `test/index.js`. All 25 tests pass (`npm test`).

## Update: `{ddd}`
Added `{ddd}` (Sun..Sat, via `getDay()`, fixed English array like `MMM`) in `src/index.js`, `index.d.ts`, `readme.md`, `test/index.js`. 29 tests pass. Current git branch is `grants` (earlier note said `payroll`); changes are uncommitted.

## Decisions
- Implemented as a MAP function using a fixed English array, not `toLocaleString`: output is locale/ICU independent and tiny.
- Existing pad/slice(-key.length) logic works unchanged since names are 3 chars.
- Users can still override `MMM` via the `custom` argument.

## Failed approaches
None.

## Update: `{Q}` (branch `payroll`)
Added `{Q}` (single digit 1-4) in `src/index.js`, `index.d.ts`, `readme.md`, `test/index.js`. 38 tests pass. Uncommitted.
- Uses Australian financial-year quarters (year starts 1 July): Jul-Sep=1, Oct-Dec=2, Jan-Mar=3, Apr-Jun=4. Formula: `floor(((month + 6) % 12) / 3) + 1`, where month is 0-based.
- Reason: payroll note below specified AU FY. The existing pad/slice(-key.length) logic yields one digit for a 1-char key.
- Failed approaches: none.

## Upcoming (not started)
Grants (branch `grants`) will also need a quarter token later, but on the US federal fiscal year, which starts 1 October: Oct-Dec = Q1, Jan-Mar = Q2, Apr-Jun = Q3, Jul-Sep = Q4. This differs from the Australian quarters implemented on `payroll`, so the two builds must not share one implementation. Not started.
