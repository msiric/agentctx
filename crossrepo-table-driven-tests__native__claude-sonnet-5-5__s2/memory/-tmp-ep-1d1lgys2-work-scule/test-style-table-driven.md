---
name: test-style-table-driven
description: "User wants tests written as one test.each table of cases per function, in every project"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a1d8a268-6022-48be-a75a-b413dc4ec3ca
  modified: 2026-11-03T03:53:04.848Z
---

Write tests as a single `test.each` table of cases per function (as in scule's test/scule.test.ts), not as many separate `it`/`test` blocks.

**Why:** A table is easier to scan and to add cases to. The user said this applies to every project they work on.

**How to apply:** When adding tests for a function, add one `describe` with one `test.each([...input, expected...])` table. To cover more cases, add rows to the table.
