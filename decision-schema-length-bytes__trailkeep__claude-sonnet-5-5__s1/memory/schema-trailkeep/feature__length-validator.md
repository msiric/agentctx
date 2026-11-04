# feature/length-validator

Branch: feature/length-validator · Repo: local__schema-1363888398 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Length(min, max) validator counts UTF-8 bytes, not characters: the fields go into Oracle VARCHAR2(n BYTE) columns, and inserts failed on accented names that passed a len() check. Sketch agreed otherwise (Use-style error placement, inclusive bounds, ctor validation); implementation not yet written.

