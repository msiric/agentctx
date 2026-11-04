# sorted-json

Branch: sorted-json · Repo: local__tinydb-496647493 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: JSONStorage sorted-keys change backed out before release; revisit. json sort_keys=True fails on mixed int/str keys (e.g. hits {200:1,'other':3}); needs custom key sort that orders by json's string form. Opt-out via sort_keys=False.
- 2026-11-04: JSONStorage sorts keys by default again; implemented via custom recursive sort by json string form (_sort_keys in storages.py) so mixed int/str keys work; sort_keys=False opts out. Tests added in test_storages.py.

