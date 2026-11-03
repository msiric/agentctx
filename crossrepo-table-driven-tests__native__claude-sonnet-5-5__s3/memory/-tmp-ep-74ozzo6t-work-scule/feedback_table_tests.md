---
name: feedback-table-tests
description: User wants tests written as one test.each table per function, not separate it/test blocks
metadata:
  type: feedback
---

Write tests as a single `test.each` table of cases per function (matching existing style), not a pile of separate `it`/`test` blocks.

**Why:** Tables are easier to scan and to add cases to. User wants this in every project.

**How to apply:** Fold edge cases (e.g. empty input) into the table as rows rather than adding standalone tests.
