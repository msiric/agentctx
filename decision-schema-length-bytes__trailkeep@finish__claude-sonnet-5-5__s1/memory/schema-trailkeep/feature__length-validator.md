# feature/length-validator

Branch: feature/length-validator · Repo: local__schema-786457326 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Length(min,max) validator: bounds count UTF-8 bytes, not characters. Reason: fields go into Oracle VARCHAR2(n BYTE) columns; accented names passed a len() check and then failed on insert. Design sketched (Regex-style error in autos, str only, no value echo, _error attr name, json_schema branch); not yet implemented, to be written next session.
- 2026-11-04: Length validator implemented (schema/__init__.py, tests in test_schema.py). Bounds are UTF-8 bytes; json_schema emits minLength=ceil(min/4), maxLength=max since JSON Schema counts chars. Error never echoes the value; non-str raises SchemaError; min>max raises ValueError.

