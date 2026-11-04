# HANDOFF

## Task
Add a `Length(min=None, max=None)` validator to this fork of `schema`, for string fields in API payloads.
Replaces `And(str, lambda s: len(s) <= 40)`, whose errors are unreadable.

## State (branch `feature/length-validator`)
- **Implemented** (user asked to write it this session, after approving the sketch). `Length` is in `schema/__init__.py` right after `Regex` and is exported in `__all__`. 8 tests (`test_length_*`) are at the end of `test_schema.py`. Full suite: 128 passed. Not committed.
- Everything lives in `schema/__init__.py` (package, not `schema.py`). Tests are in `test_schema.py`.

## Findings that drive the design
- Validators are plain classes with `validate(self, data, **kwargs)`. `_priority()` treats anything with `.validate` as VALIDATOR, so no registration is needed. Export via `__all__` (top of file).
- `Schema.validate` VALIDATOR branch (~line 568) catches `SchemaError` from the validator and re-raises `SchemaError([None] + x.autos, [e.format(data) if e else None] + x.errors)`.
  A dict value then wraps that again with `"Key 'name' error:"` in autos.
- `SchemaError.code` returns the de-duplicated `errors` if any are non-None, otherwise the `autos`. So a custom `error=` in `errors` overrides every auto message; one in `autos` does not.
- Gotcha: `Regex` and `Use` put their custom `error=` message in different slots.
  `Regex` calls `SchemaError(error_message)`, which puts it in *autos*. It therefore still shows the "Key 'x' error:" prefix and is not an override.
  `And(..., error=)` and `Schema(error=)` put it in *errors*, which overrides everything (verified by running it).
  `Length` should follow the `Schema` convention: auto message in autos, `error.format(data)` in errors.
- `Literal` is not a validator. It only wraps a value (COMPARABLE) and carries description/title for json_schema. It is irrelevant to Length.
- `json_schema()` has a hardcoded `type(s) == Regex` branch (~line 772). Length would need its own branch to emit minLength/maxLength. This is optional and a follow-up.

## Decisions (pending user approval)
- Do not echo the data in the message (payload strings can be huge). Say "length 6 exceeds maximum of 3".
- Validate min/max in `__init__` (ValueError). Reject both None, negatives, bool, non-int and min > max.
- `len()` failing with TypeError becomes a SchemaError, as in Regex.

## Revision after user feedback (supersedes the earlier sketch where they conflict)
- **min/max count UTF-8 bytes, not characters.** These fields go into Oracle `VARCHAR2(n BYTE)` columns.
  Inserts have failed on accented names that passed a `len()` check.
- Consequences for the implementation:
  - Compute `n = len(data.encode("utf-8"))` for `str`. Treat `bytes` as already encoded and use `len(data)`.
  - This resolves the open "any Sized vs str only" choice: **str (and bytes) only**. Anything else becomes a `SchemaError`.
  - Catch `UnicodeEncodeError` (lone surrogates) and turn it into a `SchemaError`.
  - Messages must say bytes, e.g. "byte length 52 exceeds maximum of 40 bytes". A plain "length" would mislead, since 40 characters can exceed 40 bytes.
  - The class name is still undecided: `Length` with documented byte semantics, or a clearer name such as `ByteLength`. The user asked for `Length`, so default to that unless they say otherwise.
  - The `json_schema` follow-up is now less clean. JSON Schema `minLength`/`maxLength` count characters, not bytes, so emitting them would be wrong or only approximate. Skip it or document the mismatch.
- Assumption to confirm: the Oracle database character set is AL32UTF8 (or UTF8). On another charset the byte counts differ from UTF-8.
- Implemented as `Length(min=None, max=None, error=None)`. The class name stays `Length` with byte semantics documented in the docstring. The `error` kwarg was added to follow the Schema convention (autos/errors split).
- Bounds are inclusive. Both None, negative, bool, non-int and min > max raise ValueError. Non-str/bytes data and unencodable strings raise SchemaError. Messages never echo the data.
- Still open: the AL32UTF8 charset assumption, and the `json_schema` branch (skipped, since minLength/maxLength count characters, not bytes).

## Failed / rejected approaches
- Test bug, not an approach failure: `assert Length(...).validate("")` failed because `""` is falsy. Compare to the value instead.
