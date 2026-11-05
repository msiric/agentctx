# main

Branch: main · Repo: local__tomli-w-3209662499 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: None values are skipped in tables and inline tables (dump/dumps); None inside arrays deliberately still raises TypeError 'for now' per user. Not yet in README/CHANGELOG. Run tests with PYTHONPATH=src (package not installed).
- 2026-11-05: SUPERSEDES the 'None skipped' decision. New rule: None values will be written as an empty string (key = ""), which the downstream loader treats as explicitly unset. Reason: skipping keys bit us; loader can't tell a dropped key from one never set, and in staging a None timeout silently fell back to the 30s default. Code intentionally NOT changed yet (still skips None); user will switch it over together with the None-in-arrays case in a later session.
- 2026-11-05: Implemented the empty-string rule: None -> "" everywhere (tables, inline tables, arrays, dump/dumps); no longer skipped or raising. Tests in tests/test_types.py. README/CHANGELOG still not updated.

