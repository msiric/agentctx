# feature/length-validator

Branch: feature/length-validator · Repo: local__schema-2559051760 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Length validator (not yet written, sketch only): min/max must count UTF-8 bytes, not characters. Reason: these fields go into Oracle VARCHAR2(n BYTE) columns, and inserts failed on accented names that passed a len() check. So validate len(data.encode('utf-8')), and don't emit JSON-schema minLength/maxLength as if they were byte counts. The rest of the earlier sketch was approved: Use-style error placement, report length not data in the message, inclusive bounds.
- 2026-11-05: Length validator is now written in schema/__init__.py (+ test_length in test_schema.py), uncommitted. It counts UTF-8 bytes per the earlier decision and emits no JSON-schema minLength/maxLength. Choices I made myself, not user-approved: ValueError when min > max, and an optional error= param (formatted with data, placed Use-style in SchemaError.errors). json_schema() output for Length was not tested; check it doesn't crash.

