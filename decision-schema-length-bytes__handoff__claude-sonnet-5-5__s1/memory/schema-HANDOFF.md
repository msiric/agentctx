# HANDOFF

## Task
Add a `Length(min=None, max=None, error=None)` validator to this fork of `schema`
(`schema/__init__.py`). It replaces `And(str, lambda s: len(s) <= 40)` in API
payload schemas, whose errors are unreadable.

**State: implemented** (`Length` in `schema/__init__.py` after `Regex`, in `__all__`; tests `test_length_*` at end of `test_schema.py`, all passing). Not committed. Still open: the questions below, plus README/CHANGELOG entry not yet written.

## Decisions
- **min/max count UTF-8 bytes, not characters.** The values go into Oracle
  `VARCHAR2(n BYTE)` columns. Inserts failed on accented names that passed a
  `len()` check.
- **Strings only.** Byte length only makes sense for `str`, so `validate` checks
  `isinstance(data, str)` and raises `SchemaError` otherwise. `bytes` is not accepted.
  Compute the length as `len(data.encode("utf-8"))`. Catch `UnicodeEncodeError`
  (lone surrogates) and raise `SchemaError`.
- Bounds are inclusive. Reject at construction: negative or non-int (incl. bool)
  bounds (`TypeError`), neither bound given (`TypeError`), `min > max` (`ValueError`).
- Plain validator class with no base class, like `Regex`/`Use`: `__init__`,
  `__repr__`, read-only `min`/`max` properties, `validate(data, **kwargs)`.
  `Schema._priority` treats anything with `.validate` as a VALIDATOR.
- **Error slots:** auto message in `autos`, custom `error.format(data)` in `errors`
  (the `Use` pattern). `Regex` puts the custom error in `autos`, so an outer `error=`
  overrides it; avoid that. `SchemaError.code` prefers `errors` over `autos`.
- Don't repeat the field name in the message. Inside a dict, `Schema.validate`
  already prefixes `Key 'name' error:` (lines ~502-508), but only when no custom error is set.
- Message should say bytes, e.g. `length 57 bytes is not at most 40 bytes`. Avoid echoing
  the whole value (long or sensitive payload strings); lean towards omitting it.
- Export: add `"Length"` to `__all__`. Tests go in `test_schema.py`: boundaries,
  multibyte input (e.g. 'é' is 2 bytes, an emoji is 4), non-str input, custom
  `error=`, nesting in dict/`And`/`Or` and checking `.code`.

## Open / to confirm
- **Oracle charset:** byte counts assume AL32UTF8 (real UTF-8). The older `UTF8`
  charset stores supplementary characters (emoji) as 6 bytes (CESU-8), so UTF-8 byte
  counts would under-count there. Confirm which charset the DB uses.
- **Class name:** `Length` is slightly misleading for a byte count. `Length` is what the
  user asked for; mention `ByteLength` as an alternative, or make it clear in the docstring.

## Notes from implementation
- `SchemaError.code` joins all errors, so with an outer `error=` the code is `outer\ninner` (outer first); tests assert on the first line.

## Not doing / rejected
- **`json_schema()` support:** `Schema.json_schema` special-cases `type(s) == Regex`
  (line ~772). A `Length` branch emitting `minLength`/`maxLength` would be wrong,
  because JSON Schema counts characters, not bytes. Leave `Length` unrepresented
  (falls through with no constraint) unless we add a custom keyword.
- **Any-sized-value (lists etc.) with `len()`:** dropped when we moved to bytes.
