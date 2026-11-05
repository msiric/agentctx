# main

Branch: main · Repo: local__xmltodict-1487588365 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: drop_keys(doc, names) added to xmltodict.py for catalog work (uncommitted, tests in tests/test_drop_keys.py). Decisions: a str for names is one name, not chars (avoids 'id' dropping 'i' and 'd'); elements emptied by removal become {} not None (pure key removal, no normalising); dict subclass kept, falls back to dict if it can't be built from pairs. README entry not added yet.

