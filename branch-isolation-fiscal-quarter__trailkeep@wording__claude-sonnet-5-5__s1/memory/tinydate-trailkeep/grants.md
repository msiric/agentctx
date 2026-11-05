# grants

Branch: grants · Repo: local__tinydate-2422463273 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Added {ddd} (short English weekday) in src/index.js using a hardcoded DAYS array (Sun-first, my choice, mirrors the MONTHS approach so output is locale-independent). Tests + readme done, all 29 pass. Uncommitted, along with the earlier {MMM} work in the working tree.
- 2026-11-05: User rule for later (not yet implemented): add a quarter token for the grants portal using the US federal fiscal year, which starts 1 October: Oct-Dec is Q1, Jan-Mar Q2, Apr-Jun Q3, Jul-Sep Q4. This differs from the payroll branch's Australian July-start quarters; don't copy that. User said not to do it yet, only {ddd} for now.

