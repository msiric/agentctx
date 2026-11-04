# Handoff

## Task
Add `humanize.percent(value, precision=1)` for customer billing/usage pages (humanize is only used there).
Status: done. Implemented in `src/humanize/number.py`, exported in `src/humanize/__init__.py` (import + `__all__`), tests in `tests/test_number.py::test_percent`. 265 tests and doctests pass.

## Decisions
- Mirrors `scientific()`: non-numeric input returns `str(value)`; NaN/inf go through `_format_not_finite`. This matches the library's existing convention.
- Values outside 0..1 are not clamped (1.5 -> '150.0%'), because billing may show over-usage.
- Output uses "." as the decimal separator and ignores locale. Not localized; flag if the billing pages need that.

- Rounding is half up on the decimal repr of the float (`Decimal(repr(v))`), to match billing's invoice generator: 0.0625 -> '6.3%', 0.0125 -> '1.3%', 0.0375 -> '3.8%', 0.125 p0 -> '13%'. Billing's cases are in tests. Negatives round away from zero.

## Failed approaches / environment notes
- First version used `f"{v*100:.1f}"`: wrong, because binary float formatting rounds exact ties to even ('6.2%' for 0.0625) and v*100 can also introduce float error. Replaced with Decimal.
- `pytest` fails in this env unless run as `PYTHONPATH=src python -m pytest ... -p no:asyncio`. The package isn't installed, and pytest-asyncio raises an INTERNALERROR over an unset loop-scope option.
- Not added to README.md (it has per-function examples for other functions); optional follow-up.

---

# Task 2: `humanize.gigabytes(num_bytes, precision=1)`
Status: done. In `src/humanize/filesize.py`, exported in `__init__.py` (import + `__all__`), tests in `tests/test_filesize.py::test_gigabytes`. filesize + number tests (353) and filesize doctests pass.

## Decisions
- Always GB (10**9), even for small values (500000000 -> '0.5 GB'); no unit auto-scaling, since that is what `naturalsize` is for.
- Rounding is half up via `Decimal(repr(value))`, same as `percent`, for consistency with billing's invoice generator (1250000000 -> '1.3 GB'). The user didn't specify this for gigabytes; it is an assumption carried over from `percent`. Negatives round away from zero.
- Non-numeric input raises (`float()` ValueError/TypeError), unlike `percent`, which returns `str(value)`. Matches `naturalsize`, which also raises. NaN/inf are not handled (Decimal formatting would give 'NaN GB' / 'Infinity GB'). Flag if billing needs otherwise.
- Output is not localized (no i18n of "GB"), same as `naturalsize` suffixes aside from gettext; "." decimal separator.

## Notes
- Full `pytest --doctest-modules src tests` hit collection errors in test_i18n/test_time here (env/pre-existing, not investigated); ran the relevant files only, with `PYTHONPATH=src python -m pytest -p no:asyncio`.
