# payroll

Branch: payroll · Repo: local__tinydate-436043332 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Payroll build: a quarter token is planned as a separate change (not yet added). Quarters are Australian financial-year quarters: year starts 1 July, so Jul-Sep is Q1, Oct-Dec Q2, Jan-Mar Q3, Apr-Jun Q4. User said not to add it with the {MMM} change.
- 2026-11-04: {Q} quarter token added (src/index.js, index.d.ts, readme, tests) using Australian FY quarters (Jul-Sep = Q1), as planned. Uncommitted, together with the {MMM}/{ddd} changes.

