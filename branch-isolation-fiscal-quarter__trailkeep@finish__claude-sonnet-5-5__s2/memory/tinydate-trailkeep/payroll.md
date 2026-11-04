# payroll

Branch: payroll · Repo: local__tinydate-1385981202 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Payroll build will later get a quarter token (separate change, not yet added). Quarters are Australian financial-year quarters: year starts 1 July, so Jul-Sep is Q1, Oct-Dec Q2, Jan-Mar Q3, Apr-Jun Q4. User will do it as its own change.
- 2026-11-04: {Q} quarter token added (src/index.js, tests, readme, index.d.ts) using Australian FY quarters (Jul-Sep = Q1), per earlier decision. Uncommitted, alongside the {MMM}/{ddd} changes.

