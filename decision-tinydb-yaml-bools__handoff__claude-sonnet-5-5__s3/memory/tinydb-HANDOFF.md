# HANDOFF: YAML storage for TinyDB

Branch: `feature/yaml-storage`. Goal: a `YAMLStorage` next to `JSONStorage` so ops can hand-edit db files.

## Current state
- DONE: pulled the file handling out of `JSONStorage` into `FileStorage(Storage)` in `tinydb/storages.py`.
  It covers `touch`/`create_dirs`, the access-mode warning, opening the handle, and `close()`.
  `JSONStorage` now subclasses it and only adds `kwargs`, `read` and `write`.
  `FileStorage` is exported in `__all__`. Behaviour is unchanged. All 228 tests pass (`uv run pytest`).
- DONE: `YAMLStorage(FileStorage)` in `tinydb/storages.py` with strict-bool loader (only lowercase `true|false`),
  stock-resolver dumper (so `NO`/`off`/`'true'` get quoted), dict multi-representer on the private dumper,
  int doc-id -> str normalisation (error on collision), `YAMLError` re-raised as `ValueError` with path,
  lazy PyYAML import. Tests appended to `tests/test_storages.py` (importorskip yaml). 236 pass via `uv run pytest`.
- NOT DONE: docs, changelog, the `tinydb[yaml]` extra in pyproject (the ImportError message already mentions it).

## Decisions
- PyYAML, not ruamel.yaml. The user doesn't want an extra dependency. Cost: comments in the file are lost on each rewrite.
- Plain `yaml.safe_load` is NOT acceptable. Its YAML 1.1 rules turn `NO`, `off`, `yes`, `on` etc. into bools.
  Ops type `country: NO` and `maintenance: off`. Required behaviour: only `true`/`false` load as booleans,
  and everything else stays a string.
  Plan: a `SafeLoader` subclass with a copy of the implicit resolvers where the bool regex is replaced by one
  that matches only `true|false` (case rules to settle, probably lowercase only).
  Remove the old bool resolver from the copied table rather than adding a second one.
  The dumper needs the mirror image: strings like `NO` or `off` must be quoted when written. Test the round trip.
- Reading must use the safe loader (no arbitrary object construction). Writing uses a safe dumper subclass.
- Dumper deliberately keeps the stock YAML 1.1 resolvers (not the strict ones) so ambiguous strings are quoted.
- Do not swallow `YAMLError` in `read()`. Returning `None` would make the next write wipe a file with a typo.
  Let it propagate with the path.
- Doc IDs are `str` keys (`table.py:846`). Normalise keys to `str` in `read()`, because hand-edited `1:` loads as int
  and would duplicate `'1'`.
- Register the `Document` representer on the private dumper, not on PyYAML globally.
- Lazy `import yaml` in `__init__`, with an optional `tinydb[yaml]` extra. Not yet confirmed with the user.

## Failed or blocked
- `python -m pytest` fails here: `pytest.ini` needs `--cov` options and the plugins are only in the uv env.
  Use `uv run pytest`.

## Open items for next session
- Bool rule settled as lowercase `true|false` only (`True`/`TRUE` stay strings) - confirm with user. Also check what else YAML 1.1 resolves that could surprise:
  `~`/`null`, `0o17` octals, `1_000`, sexagesimal `1:30`, dates. The user only asked about booleans, so ask before changing the others.
- Decide on the `tinydb[yaml]` extra. Update `docs/extend.rst` (the toy storage there swallows `YAMLError`) and the changelog.
