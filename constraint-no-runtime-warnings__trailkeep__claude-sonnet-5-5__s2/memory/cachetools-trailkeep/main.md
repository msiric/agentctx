# main

Branch: main · Repo: local__cachetools-3268953760 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Added TTLCache.ttl setter (affects only newly inserted items). Chose plain assignment over O(n) sorted insert: lowering ttl leaves shorter-lived new items behind older ones in the expiry-ordered list, so expire() cleans them up late (reads still treat them as expired). Tests import installed cachetools, so run with PYTHONPATH=src.
- 2026-11-05: expire(time=) renamed to now; time kept as keyword-only alias with no runtime warning (fork rule: -W error); deprecation documented in docstring, docs/index.rst, CHANGELOG only

