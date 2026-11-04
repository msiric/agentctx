# HANDOFF

## State
Added `scripts/export_invoices.py DB_PATH OUT_CSV` (columns: number, customer, amount, due_date)
and `scripts/sample_db.json` (3 invoices in an `invoices` table). Verified manually; output
correctly quotes commas/quotes. Not committed.

## Decisions
- Reads the JSON with `json` directly instead of TinyDB: read-only, no dependency on the package being importable.
- Rows ordered by doc id; missing fields become empty strings; exits 1 if no `invoices` table.

## Failed approaches
None.

## Update: German Excel
- Finance's Excel (German locale) showed everything in column A and mojibake (MÃ¼ller). Changed output to
  `;` delimiter and `utf-8-sig` (BOM). Sample db now includes "Müller GmbH". Verified BOM bytes and output.
- Open: amounts are written with a `.` decimal (1250.5); German Excel may read these as text/dates. Not changed; awaiting Finance's feedback.

## Update: Table.to_csv
- Added `Table.to_csv(path, fields=None)` in tinydb/table.py (+4 tests in tests/test_tables.py).
  Header + one row per doc; default fields = top-level keys in first-seen order; missing -> empty.
- Uses standard csv dialect (`,` delimiter, utf-8, no BOM), unlike scripts/export_invoices.py (`;` + BOM
  for German Excel). Not added as options since not requested; add `delimiter`/`encoding` params if Finance needs it.
- pytest.ini needs pytest-cov; ran tests with `-c /dev/null --rootdir=.` instead.
