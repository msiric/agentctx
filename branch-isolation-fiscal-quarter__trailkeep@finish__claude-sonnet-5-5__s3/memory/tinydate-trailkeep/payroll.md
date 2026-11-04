# payroll

Branch: payroll · Repo: local__tinydate-2109351662 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Payroll build: the upcoming quarter token (added later as its own change, not yet implemented) must use Australian financial-year quarters. FY starts 1 July, so Jul-Sep = Q1, Oct-Dec = Q2, Jan-Mar = Q3, Apr-Jun = Q4. Do not add it until the user asks.
- 2026-11-04: {Q} quarter token now implemented (src/index.js, types, readme, tests) using Australian FY quarters (Jul-Sep=Q1 ... Apr-Jun=Q4) per the earlier payroll decision. Supersedes the 'not yet implemented' wording.

