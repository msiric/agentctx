# grants

Branch: grants · Repo: local__tinydate-2001566278 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: My choice (not user-specified): {ddd} uses a fixed English DAYS array in src/index.js (Sun-first, indexed by getDay), same locale-independent approach as {MMM}. Revisit only if the user asks for other locales.
- 2026-11-06: User wants a quarter token later for the grants portal (not yet requested to build). Grants use the US federal fiscal year, starting 1 October, so Oct-Dec is Q1, Jul-Sep is Q4. This differs from the payroll branch (Australian FY, 1 July start); don't reuse that definition. Don't implement until the user asks.

