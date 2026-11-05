# Handoff: TTLCache.ttl setter

## State
Done and tested (392 pass with `PYTHONPATH=src`). Uncommitted.
- `src/cachetools/__init__.py`: `TTLCache.ttl` setter; `__setitem__` keeps the expiry-ordered linked list sorted.
- `src/cachetools/__init__.pyi`: setter stub.
- `tests/test_ttl.py`: `test_ttl_setter`.

## Decisions
- Setter only affects items inserted afterwards (as requested); existing items keep their expiry.
- Lowering ttl would break the invariant that the link list is sorted by `expires`
  (`expire()` stops at the first unexpired head), leaving newer, shorter-lived items stuck
  behind older ones. So `__setitem__` now walks back from the tail to the right spot. This is
  O(1) when ttl is unchanged, and only walks after a decrease.

## expire() `time` -> `now` rename
- `expire(self, now=None, *, time=None)` in `_TimedCache`, `TTLCache`, `TLRUCache`; `time=` is a
  keyword-only deprecated alias (no `warnings.warn`, per fork rules; noted in docstring + CHANGELOG).
  Positional callers still work. Stubs and tests (`test_expire_now_and_legacy_time` in test_ttl/test_tlru) updated.
- `pytest -W error` fails on a pytest-asyncio config warning unrelated to this code.

## Gotchas
- A cachetools 7.2.8 copy is installed in site-packages, so plain `pytest` tests that copy, not `src`.
  Use `PYTHONPATH=src python -m pytest tests`. My first run failed for this reason, not a code bug.
- Not done: the setter doesn't re-sort existing items, and I didn't update docs/CHANGELOG.

## Fork rules
- Nothing we add may emit a warning at runtime (DeprecationWarning included): the ingest
  service vendors this fork and runs its tests with `-W error`. Deprecations go in the
  docstring and CHANGELOG.rst only, never `warnings.warn`.
