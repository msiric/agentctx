# Handoff

## State
Added a `TTLCache.ttl` setter (src/cachetools/__init__.py), the matching
setter in the .pyi stub, and `test_ttl_setter` in tests/test_ttl.py.
Full suite passes (392) when run with `PYTHONPATH=src`.

## Decisions
- Setter only assigns `self.__ttl`. Expiry is computed at insertion
  (`time + self.__ttl`), so existing items keep their old expiry, as requested.
  No re-sorting of the link list needed.
- No locking added; callers sharing the cache across threads already need
  their own lock.

## Gotchas / failed approaches
- Plain `pytest tests` imports the installed cachetools 7.2.8 from
  site-packages, not `src/`, so the new test failed with "no setter". Use
  `PYTHONPATH=src`. The test also needs its own `timer` variable, since
  `cache.timer` is a wrapper without `tick()`.

## Project rules
- The ingest service vendors this fork and runs its tests with `-W error`.
  Nothing we add may emit a warning at runtime (DeprecationWarning included).
  Deprecations are documented in the docstring and CHANGELOG.rst only, never
  via `warnings.warn`.

## expire(time) -> expire(now) rename
- `TTLCache.expire` / `TLRUCache.expire` (and `_TimedCache` base) are now
  `expire(self, now=None, *, time=None)`. `time=` is a silent deprecated alias
  (no `warnings.warn`, per project rules); documented in docstrings, docs/index.rst,
  CHANGELOG.rst. Stubs and tests updated; `test_expire_time_alias` covers the
  alias under `simplefilter("error")`.
- Pitfall: a blanket replace of `time < ...` also hit `__getitem__`-style
  helpers that legitimately use a local `time`; only the two expire() bodies change.
- mypy not installed here, so the .pyi change is unchecked.
