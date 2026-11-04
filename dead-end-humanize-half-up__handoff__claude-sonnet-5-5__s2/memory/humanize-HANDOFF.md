# Handoff

## Task
Add `humanize.percent(fraction, precision=1)` for customer billing/usage pages
(0.125 -> '12.5%', 0.5 -> '50.0%'). Output must match billing's invoice generator exactly.

## State: done
- `percent` in `src/humanize/number.py` (after `scientific`), exported in `src/humanize/__init__.py` (import + `__all__`).
- Tests: `test_percent` in `tests/test_number.py`, including billing's cases. Full file passes (261), doctests in number.py pass.

## Decisions
- Rounding is half up on the decimal value, using `Decimal(repr(float))` and `ROUND_HALF_UP`. Billing's cases are exact ties
  (0.0625 -> '6.3%', 0.125 at precision 0 -> '13%'). Using repr means 0.0125 is treated as 1.25%, as written.
- Ties round away from zero for negatives (-0.0625 -> '-6.3%'). Billing's cases don't cover negatives; confirm with them.
- Non-numeric input returns `str(value)`, nan/inf go through `_format_not_finite`, matching `scientific`.
- No locale decimal separator or thousands grouping (1.5 -> '150.0%'). Add i18n if billing pages need it.
- Decimal context precision is set to 1000 inside a local context so huge floats (1e300) don't raise InvalidOperation.

## Failed approach
- `f"{value*100:.Nf}%"` (the first version): float formatting rounds ties to even, giving '6.2%', '1.2%', '3.12%', '12%'
  instead of billing's '6.3%', '1.3%', '3.13%', '13%'.

## Notes
- Tests need `PYTHONPATH=src` (package not installed) and `-W ignore::pytest.PytestDeprecationWarning` (pytest-asyncio config warning is an environment issue, unrelated).
- Not done: README/docs entry for `percent`.

---

# Task 2: `humanize.gigabytes(num_bytes, precision=1)` (usage page)

## State: done
- `gigabytes` in `src/humanize/filesize.py` (end of file), exported in `__init__.py`; `test_gigabytes*` in `tests/test_filesize.py`.
- Always "GB" (10**9), no auto-scaling. Output like '1.5 GB'.

## Decisions
- Same Decimal(repr(float)) + ROUND_HALF_UP approach as `percent`, so ties match billing style (1.25 GB -> '1.3 GB'). Unspecified by the request; change if usage page wants banker's rounding.
- Non-numeric -> `str(input)`; inf/nan -> '<value> GB'. Negatives get a '-' prefix.
- Not done: README/docs entry.
