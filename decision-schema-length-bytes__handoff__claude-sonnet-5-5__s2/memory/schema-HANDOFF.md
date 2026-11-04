# HANDOFF: `Length(min=None, max=None)` validator

Status: `Length` is implemented in `schema/__init__.py` (after `Regex`), exported in `__all__`, with tests in `test_schema.py` (`test_length_*`; full suite passes, 131 tests). Nothing committed. Still open: items 1-3 below (json_schema, charset confirmation, README/CHANGELOG).

## Goal
Add `Length` to our fork of `schema` for string fields in API payloads. It replaces `And(str, lambda s: len(s) <= 40)`, whose errors are unreadable.

## Requirement: bytes, not characters
`min` and `max` count **UTF-8 bytes**. The values go into Oracle `VARCHAR2(n BYTE)` columns. Inserts have failed on accented names that passed a `len()` check. So use `len(data.encode("utf-8"))`.

## How the existing code works (schema/__init__.py)
- `_priority` (~line 334) treats any object with a `validate` attribute as a VALIDATOR. `Length` therefore needs no registration. It is a plain class, like `Regex` and `Use`.
- Validator shape: `__init__(..., error=None)`, `__repr__`, `validate(self, data, **kwargs)` that returns the data or raises `SchemaError`.
- `error=`: stored as `self._error` and applied as `e.format(data)`, so `{}` in the message is replaced by the data. The `Schema` VALIDATOR branch (~568-578) re-wraps the `SchemaError` as `SchemaError([None] + x.autos, [e.format(data)] + x.errors)`.
- `SchemaError(autos, errors)`: `.code` returns the de-duplicated `errors` if any exist, otherwise the de-duplicated `autos`. A custom error anywhere in the chain overrides all auto messages.
- Inside a dict (~498-508) a failing value is wrapped as `["Key 'k' error:"] + x.autos`. So the auto message must be a self-contained sentence that does not repeat the key name.
- `Regex` puts its message in the single positional arg, so the message lands in `autos`. `Use` uses the two-arg form `(auto, custom)`, which is the correct one, so copy that.
- `Schema.json_schema` special-cases only `Regex` (~772). Any other validator is silently dropped (empty dict).

## Sketch (agreed except for the open items below)
```python
class Length:
    def __init__(self, min=None, max=None, error=None):
        # TypeError if both None; ValueError if min > max
    def __repr__(self): ...          # Length(min=3, max=40)
    min / max properties
    def validate(self, data, **kwargs):
        e = self._error
        if not isinstance(data, str):
            raise SchemaError(f"{short(data)} should be instance of 'str'", e.format(data) if e else None)
        try:
            n = len(data.encode("utf-8"))
        except UnicodeEncodeError:   # lone surrogates
            raise SchemaError(f"{short(data)} is not encodable as UTF-8", e.format(data) if e else None)
        if (min is not None and n < min) or (max is not None and n > max):
            raise SchemaError(
                f"{short(data)} is {n} bytes in UTF-8, expected {at least N | at most N | between A and B} bytes",
                e.format(data) if e else None)
        return data
```
- The message says "bytes" so it is not confused with a character count.
- Truncate the data repr to ~40 characters with a `short()` helper. A 5,000-character string would otherwise make a huge error.
- Include the character count in the message if that is cheap. It helps explain why 38 characters can fail a limit of 40.

## Decisions and reasons
- Strings only, as a consequence of the byte requirement. `len()` on a `list` or `dict` has no byte meaning. `bytes` input is rejected so the unit stays unambiguous.
- Encoding is fixed at UTF-8, with no `encoding=` parameter. YAGNI. Revisit if the DB charset is not AL32UTF8. A DB on a non-UTF-8 charset such as WE8ISO8859P1 would count bytes differently.
- Inclusive bounds. At least one of `min` and `max` is required.

## Open items for the next session
1. **json_schema**: add a branch for `Length`. `maxLength` counts characters, and characters <= bytes, so `maxLength = max` is valid but looser than the real rule. `minLength` must NOT be set to `min`, because a short string of multi-byte characters can have fewer characters than bytes. Either omit `minLength` or use `ceil(min/4)`. Needs a decision. A comment in the code should say the JSON schema is an approximation.
2. Confirm the Oracle DB charset is AL32UTF8 (UTF-8), or `Length` should not hard-code UTF-8.
3. Housekeeping: add `"Length"` to `__all__`, a README section, a CHANGELOG entry, and tests in `test_schema.py`. Tests should cover ASCII, accented (`"é"` is 2 bytes), CJK (3 bytes), emoji (4 bytes), a lone surrogate, a non-str value, a custom `error=` with `{}`, and dict-key composition.

## Implementation notes
- Follows the sketch. Messages use the two-arg `SchemaError(auto, custom)` form. The auto message includes both byte and character counts. `short()` became the `Length._short` classmethod (40 chars + `...`).
- Item 3 is partly done: `__all__` and tests are in. README and CHANGELOG are not.
- json_schema (item 1) was deliberately not touched; `Length` is currently dropped from generated JSON schema.

## Approaches that failed / rejected
- None tried in code yet. Rejected in design: using `And(str, lambda ...)` with the `error=` option. It gives one fixed message per `And` and cannot report the actual length.
