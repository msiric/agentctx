# main

Branch: main · Repo: local__xmltodict-3956322516 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Supplier catalog eval: xmltodict.parse handled 3000-deep nested XML (iterative), but unparse raised RecursionError at default limit (recursive); works on flat feeds. User decided parsing is all they need for now, so unparse not pursued.
- 2026-11-05: Added xmltodict.drop_keys(doc, names): iterative (not recursive) so 3000-deep parsed catalog docs don't hit RecursionError, like parse. Matches keys exactly (use '@id'); a str for names is one key; output uses plain dict/list.

