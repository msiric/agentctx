# main

Branch: main · Repo: local__tomli-w-2993171557 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: sort_keys added to dump/dumps (keyword-only, default False so default output is unchanged); sorts at every level incl. inline tables via sorted_items() in _writer.py. AoT element order is preserved, only keys are sorted.

