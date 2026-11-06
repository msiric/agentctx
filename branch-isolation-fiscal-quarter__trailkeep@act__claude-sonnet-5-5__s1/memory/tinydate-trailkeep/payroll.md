# payroll

Branch: payroll · Repo: local__tinydate-432980511 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Payroll build: the upcoming quarter token must use Australian financial-year quarters (year starts 1 July, so Jul-Sep is Q1). User will add the quarter token themselves as a separate change; do not add it unless asked.
- 2026-11-06: My choice (not a user rule): {MMM} uses a hardcoded English MONTHS array in src/index.js rather than toLocaleString, so output doesn't depend on runtime locale. Changes to MMM (src, test, index.d.ts, readme) are uncommitted on payroll.
- 2026-11-06: Quarter token {Q} added (src, test, index.d.ts, readme), uncommitted on payroll; uses Australian FY quarters (Jul-Sep = Q1) per user's payroll requirement.

