# invoices-export

Branch: invoices-export · Repo: local__tinydb-4174396054 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: Invoice CSV export (scripts/export_invoices.py) must be ';'-delimited UTF-8 with BOM: finance uses Excel with German locale, comma/no-BOM showed one column and mojibake (Müller)

