# HANDOFF

## Task
Add a `YAMLStorage` next to `JSONStorage` in `tinydb/storages.py` so ops can hand-edit DB files.
**Status:** `YAMLStorage` written in `tinydb/storages.py` with 3 tests in `tests/test_storages.py`; suite passes (231). Not committed. Still TODO: docs (docs/extend.rst/changelog), user review.

## Done
- Extracted `_FileStorage(Storage)` in `tinydb/storages.py` (touch/create_dirs, access-mode warning, opening `self._handle`, `close()`). `JSONStorage` now subclasses it and only adds `kwargs`, `read`, `write`. Not in `__all__`. Behaviour unchanged; full suite passes (228, via `uv run --frozen pytest`; plain `python -m pytest` lacks pytest-cov).

## Updated requirements from user (override the earlier plan)
- Stay with PyYAML, NO ruamel.yaml. Comment loss on write is accepted.
- Ops type `country: NO`, `maintenance: off`; YAML 1.1 turns these into bools. Only `true`/`false` must load as booleans; yes/no/on/off/y/n etc. must stay strings. Plan: subclass `yaml.SafeLoader` (and CSafeLoader variant if used) with a copy of `yaml_implicit_resolvers` where the bool resolver regex is replaced by one matching only true/false (any case decision TBD). Must copy the resolver dict per class, not mutate SafeLoader's global one. Dumper should quote strings like 'NO'/'off' on write so they round-trip (check `safe_dump` does; PyYAML's own resolver will quote them, which is fine).

## Decisions (proposed, pending user approval)
- Library: PyYAML (`pyyaml~=6.0`, already a dev dependency; `types-PyYAML` too).
- Load with a safe loader subclass (see above), not plain `yaml.safe_load` (or `yaml.load(..., Loader=yaml.CSafeLoader)` if available). Never `yaml.load` with the full/unsafe loader: ops-edited files are an input boundary.
- Dump with `yaml.safe_dump` (`sort_keys=False`, `allow_unicode=True`, `default_flow_style=False`) so no `!!python/...` tags appear.
- Keep PyYAML an optional import (README promises "no external dependencies"): import lazily in `YAMLStorage.__init__`, raise a clear ImportError; expose an optional extra `tinydb[yaml]`.
- Mirror JSONStorage: path, create_dirs, encoding, access_mode, `touch()`, return None for empty file, seek/write/flush/fsync/truncate.

## Findings from reading the code
- `Storage` ABC: `read()` -> dict or None, `write(data)`, optional `close()`.
- `tests/test_storages.py::test_yaml` and `docs/extend.rst` already contain an ad-hoc YAML storage example (safe_load + yaml.dump). The test's `yaml.dump` needs a `Document` representer; `safe_dump` would need one too (Document subclasses dict, which safe_dump rejects) - plan to convert/ register a representer on the SafeDumper.
- `table.py` looks up docs by `str(doc_id)`; hand-edited unquoted numeric keys (`1:`) load as int in YAML, so the storage (or Table) must normalise keys to str on read.

## Implemented (this session)
- `_get_yaml_classes()` lazily imports PyYAML, builds a loader subclass (CSafeLoader if present) with per-class copy of implicit resolvers where bool matches only true/True/TRUE/false/False/FALSE (case decision: YAML 1.2 core style), and a SafeDumper subclass with a dict multi-representer (covers `Document`).
- `read()` normalises table names and doc ids to str; rejects non-mapping top level. `pyproject.toml` got a `yaml` extra.
- Python tags are rejected by the safe loader (tested).

## Failed approaches
None yet.
