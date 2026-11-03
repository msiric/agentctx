# HANDOFF

## State
- Added `scripts/export_invoices.py DB_PATH OUT_CSV`: writes number, customer, amount, due_date for each doc in the `invoices` table.
- Added `scripts/sample_db.json` as a sample db (3 invoices, incl. a comma and quote in customer names to exercise CSV quoting). Tested manually; output is correct.

## Decisions
- Reads db.json with the stdlib `json` module rather than TinyDB, so the script has no install dependency. Relies on TinyDB's format `{table: {doc_id: doc}}`.
- Rows ordered by doc id. Extra fields ignored; missing fields become empty cells.

- CSV is written with `;` delimiter and `utf-8-sig` (BOM) because finance uses Excel with a German locale; plain comma/UTF-8 put everything in column A and garbled umlauts (MÃ¼ller). Sample db now has "Müller GmbH" to cover this.

## Failed approaches
- Comma-separated plain UTF-8 CSV: broken in German-locale Excel (see above).

## Table.to_csv (tinydb/table.py)
- `Table.to_csv(path, fields=None, *, delimiter=';', encoding='utf-8-sig')`. Header + one row per doc (doc ID order); default fields = top-level keys in first-seen order; missing -> empty cell. Tests in tests/test_tables.py (`test_to_csv_*`).
- Defaults to `;` + BOM for the same German-Excel reason as the script; keyword-only overrides for plain CSV. Not changed: scripts/export_invoices.py still standalone (no TinyDB dependency).
- Nested values are written via `str()` by csv.writer (no flattening).
- Run tests with `python -m pytest -q tests -c /dev/null --rootdir=.` (pytest.ini needs pytest-cov, not installed here).
