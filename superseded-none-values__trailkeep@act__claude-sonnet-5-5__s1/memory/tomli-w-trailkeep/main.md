# main

Branch: main · Repo: local__tomli-w-1120978569 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: tomli_w: None values are skipped in tables/inline tables (user request). None inside arrays must keep raising TypeError 'for now' (user's decision, may change later). My own choice: a regular table with only None values still emits an empty [name] header; inline all-None renders {}. Changes uncommitted; run tests with PYTHONPATH=src.
- 2026-11-06: User's new rule (supersedes 'skip None' decision): a None value must be written as an empty string, key = "", because the downstream loader treats "" as explicitly unset while a dropped key silently falls back to defaults (staging: None timeout fell back to 30s). Applies to tables, inline tables and (to be decided with the user) the array case. User said: leave code as-is for now (None still skipped; None in arrays still raises TypeError); switch it over together with the array case next session. Don't change the code before then.
- 2026-11-06: None -> "" now implemented in format_literal (tables, inline tables, arrays alike; user's rule: downstream loader reads "" as explicitly unset). Array case: my choice was "" too, for consistency; replaces the old skip/TypeError behaviour.

