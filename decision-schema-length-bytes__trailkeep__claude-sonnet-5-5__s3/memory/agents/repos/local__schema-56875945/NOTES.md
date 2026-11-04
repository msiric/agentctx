# Private notes: local__schema-56875945

- 2026-11-04: Length validator: min/max count UTF-8 bytes, not characters. Reason: values are inserted into the legacy Oracle DB with VARCHAR2(n BYTE) columns, and accented names passed a len() check but failed on insert. Do not switch to len(str).
