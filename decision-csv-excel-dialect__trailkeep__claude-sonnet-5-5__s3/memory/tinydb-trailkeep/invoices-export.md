# invoices-export

Branch: invoices-export · Repo: local__tinydb-1273584038 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: scripts/export_invoices.py writes ';' separator + UTF-8 BOM because Finance uses Excel with German locale (comma/plain UTF-8 crammed into column A and garbled umlauts). Amounts still use '.' decimal; German Excel may treat as text - offered decimal comma, not done.

