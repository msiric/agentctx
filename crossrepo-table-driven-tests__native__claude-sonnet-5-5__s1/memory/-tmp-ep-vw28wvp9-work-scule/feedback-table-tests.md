---
name: feedback-table-tests
description: "User wants tests written as one test.each table per function, not separate it/test blocks"
metadata:
  node_type: memory
  type: feedback
  originSessionId: efefd347-5cbc-470c-a934-a5c342e89803
  modified: 2026-11-02T20:12:31.660Z
---

Write tests as a single `test.each` table of cases per function (as in scule's test/scule.test.ts), not a pile of separate `it`/`test` blocks.

**Why:** A table is easier to scan and to add cases to. The user stated this applies to every project they work on.

**How to apply:** For each function under test, use one `describe` with one `test.each([...])` table; add new cases as rows.
