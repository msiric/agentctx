# Private notes: local__schema-2739537169

- 2026-11-04: Length validator (planned, not yet written): min/max count UTF-8 bytes, not characters. Reason: values land in Oracle VARCHAR2(n BYTE) columns; accented names passed a len() check but blew up on insert. So str-only, measure len(data.encode('utf-8')).
