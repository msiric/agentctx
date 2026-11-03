# HANDOFF

## Task
Add a `YAMLStorage` next to `JSONStorage` in `tinydb/storages.py` so ops can hand-edit DB files.

## Current state
- DONE: extracted `FileStorage(Storage)` (not in `__all__`) from `JSONStorage`. It holds `touch`/`create_dirs`, the access-mode warning and opening `self._handle`, plus `close()`. `JSONStorage` now subclasses it and only adds `kwargs`, `read` and `write`. Behaviour is unchanged. `uv run pytest` is green (228 passed).
- DONE: `YAMLStorage(FileStorage)` in `tinydb/storages.py` (exported in `__all__`), 7 tests in `tests/test_storages.py`, `tinydb[yaml]` extra in `pyproject.toml`, `docs/extend.rst` updated. `uv run pytest`: 235 passed.
- Implemented decisions: lazy PyYAML import via `_get_yaml_classes()` (cached Loader/Dumper subclasses with copied resolver tables); bool regex accepts `true|True|TRUE|false|False|FALSE`; dumper quotes 1.1 bool words (`NO`, `off`, `y`...) with double quotes; doc-id/table keys normalised to str on read; YAMLError not swallowed; dump happens before writing so a dump error cannot truncate the file; no atomic write (same as JSONStorage).
- NOT restricted (still stock YAML 1.1 via PyYAML): sexagesimal ints, `0777` octal, `1_000`, timestamps. Dumper quotes strings that would resolve to them, so round trips are safe. Open: whether to restrict on load. No changelog entry yet.

## Decisions (and why)
- Library: PyYAML only. `ruamel.yaml` is ruled out by the user (no extra dependency). PyYAML is already a dev dependency. Make it an optional extra (`tinydb[yaml]`) with a lazy import, unless the user says otherwise (still open).
- Always use the safe machinery, never `yaml.load` / `FullLoader`: hand-edited files are untrusted input.
- **Booleans: only `true`/`false` may load as bool.** PyYAML implements YAML 1.1, so `NO`, `off`, `yes`, `on`, `y`, `n` etc. load as bools. The ops team writes things like `country: NO` and `maintenance: off`, which must stay strings. Plan: subclass `yaml.SafeLoader`, copy the `yaml_implicit_resolvers` table (it is shared class state, so don't mutate the original), and replace the `tag:yaml.org,2002:bool` resolver regex with one matching only `true|false` (decide: lowercase only, or also `True`/`TRUE`; YAML 1.2 core allows `true|True|TRUE|false|False|FALSE`). Use that loader via `yaml.load(..., Loader=ThatLoader)`.
- Dumping needs the matching treatment: a string `"NO"` / `"off"` / `"yes"` must be written quoted, otherwise a YAML 1.1 reader re-parses it as a bool. `safe_dump` quotes by consulting the dumper's resolvers, so use a dumper subclass with the same restricted bool regex, and then quote the 1.1-only words explicitly (the restricted resolver would otherwise emit `NO` bare, which is fine for our loader but not for other tools). Needs a decision/test.
- Other YAML 1.1 surprises to check with the same approach: sexagesimal ints like `1:30`, `0777` octal, `1_000`, `~`/`null`, timestamps. Not decided whether to restrict them.
- Constructor mirrors `JSONStorage` (`path`, `create_dirs`, `encoding`, `access_mode`), returns `None` for an empty file. Dump options: `sort_keys=False`, `default_flow_style=False`, `allow_unicode=True`.

## Things to watch
- Table doc IDs are stored as string keys ("1", "2"). An unquoted `1:` parses as an int key, and `table.py` looks up `str(doc_id)`. Normalise keys to `str` on read.
- Don't swallow `yaml.YAMLError` on read (the docs example does): the next write would wipe the file.
- Atomic writes (temp file + `os.replace`) are an open question: it departs from the `JSONStorage` pattern. PyYAML loses comments on rewrite; document it.
- `docs/extend.rst` has an older YAML example using plain `safe_load`. Update it.

## Failed approaches
- `python -m pytest` outside `uv run` fails because `pytest.ini` needs pytest-cov. Use `uv run pytest`.
