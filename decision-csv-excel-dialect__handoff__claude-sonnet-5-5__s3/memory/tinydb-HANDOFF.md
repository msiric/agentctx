# HANDOFF

## State
- Added `scripts/export_invoices.py DB_PATH OUT_CSV` (columns: number, customer, amount, due_date) and sample db `scripts/sample/db.json`. Tested on the sample.

## Decisions
- Reads the db with `json` instead of `TinyDB(...)` so it never creates/modifies the input file.
- Assumes table is named `invoices` and docs use the four column names as keys; missing keys become empty cells. Rows ordered by doc id.

## Mistakes / failed approaches
- First sample was generated into /tmp/sample/db.json, which already existed (not mine); my 3 inserts were appended. I removed doc ids 5-7 to restore it (rewritten compactly via json.dump, so formatting may differ from the original). Sample now lives in the repo.

## Update: German Excel
- Output is now `;`-delimited with `utf-8-sig` (BOM) because Finance's German-locale Excel put everything in column A and garbled umlauts. Amounts are still written with `.` as decimal point (e.g. 1250.5); German Excel may read those as text/dates, not yet verified.

## Update: Table.to_csv
- Added `Table.to_csv(path, fields=None)` in tinydb/table.py (+ tests in tests/test_tables.py). Header + one row per doc; default fields = top-level keys in first-seen order; missing -> empty cell; nested values are written via str().
- Decision: library method uses standard CSV (comma, UTF-8, no BOM), unlike scripts/export_invoices.py (`;` + BOM for German Excel). Not added as options since the spec was `(path, fields=None)`; could add `delimiter`/`encoding` kwargs if Finance wants this to replace the script.
- Gotcha: repo pytest.ini needs pytest-cov; I ran `pytest tests -c /dev/null --rootdir .`. Tests' `read_text` translates `\r\n`, so compare via splitlines.
