# main

Branch: main · Repo: local__cachetools-445273280 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Added TTLCache.ttl setter (affects only newly inserted items; stub + test_ttl_setter done, uncommitted). Known caveat: lowering ttl breaks expire()'s ordered-by-expiry assumption, so shorter-lived newer items linger in len/iter until older head expires; user hasn't asked to fix.
- 2026-11-05: expire(time=) renamed to now; time kept as keyword-only alias (TypeError if both), documented as deprecated in docs/CHANGELOG only, no warnings.warn because the ingest vendor runs -W error. Plain -W error also breaks pytest-asyncio config, so test with -W error::DeprecationWarning:cachetools. Local vars named time in popitem/__len__ etc. left unrenamed.

