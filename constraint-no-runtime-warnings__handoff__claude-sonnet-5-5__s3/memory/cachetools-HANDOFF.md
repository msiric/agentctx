# HANDOFF

Task: add a setter for `TTLCache.ttl` (runtime retuning from config reloader).

- Done: setter in `src/cachetools/__init__.py`, stub in `__init__.pyi`, test `test_ttl_setter` in `tests/test_ttl.py`.
- Decision: setter only assigns `__ttl`; existing items keep their original expiry (as requested). No validation, matching the constructor.
- Not done: docs/CHANGELOG not updated; TLRUCache has no ttl property.

## Task 2: rename `expire(time)` -> `expire(now)` (TTLCache, TLRUCache, _TimedCache, stubs)
- Signature is `expire(self, now=None, *, time=None)`; `time` is a keyword-only deprecated alias (`now` wins if both given). Positional callers unaffected.
- Decision: no `warnings.warn` (standing rule below); deprecation noted in docstrings + CHANGELOG.rst only.
- Pitfall: a blanket s/time/now/ also hit `__iter__`, where `time` is a local from `with self.timer as time`; reverted those.
- Tests: `test_expire_time_keyword` in test_ttl.py/test_tlru.py (asserts no warning for `time=`).
- Run tests with `PYTHONPATH=src`; site-packages has an installed cachetools that shadows the tree otherwise.
- `-W error` via unittest has 4 pre-existing errors in test_cached.NoneWrapperTest (unrelated); pytest -W error fails on a pytest-asyncio config warning.

## Standing rule for this fork
The ingest service vendors this fork and runs its tests with `-W error`, so nothing we add may emit a warning at runtime (DeprecationWarning included). Deprecations are documented only in the docstring and CHANGELOG.rst; never via `warnings.warn`.
