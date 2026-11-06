# Private notes: local__p-retry-3365189220

- 2026-11-06: In this fork index.d.ts is generated from the schema in platform-types repo (types-sync job; CI fails on hand edits). When adding options, never edit index.d.ts and add no type tests (index.test-d.ts) for options not yet in it; the user adds them to the schema themselves.
