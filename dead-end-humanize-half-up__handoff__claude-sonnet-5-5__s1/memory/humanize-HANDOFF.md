# HANDOFF

## State
Also added `humanize.gigabytes(num_bytes, precision=1)` in `src/humanize/filesize.py`
(exported from `__init__.py`, tests in `tests/test_filesize.py`). Tests: run with `PYTHONPATH=src`
(package isn't installed in this env) and `-W ignore::pytest.PytestDeprecationWarning`.

Added `humanize.percent(value, precision=1)` in `src/humanize/number.py`, exported
from `humanize/__init__.py` (import + `__all__`), tests in `tests/test_number.py`.

## Decisions
- Input is a fraction (0.125 -> '12.5%'). Rounding is half-up on Decimal(repr(value))*100 to match billing's invoice generator
  (0.0625 -> '6.3%'). Plain f-string formatting failed: half-even on binary floats gives '6.2%', '1.2%', '12%'.
- Negatives round half away from zero (-0.0625 -> '-6.3%'); billing's behavior there is unconfirmed.
- Invalid input / NaN / inf handled like `scientific` (str(value), `_format_not_finite`)
  for consistency with the rest of the module.
- No locale-specific decimal separator (the other number functions don't localize either, except intcomma).

- gigabytes: plain f-string `:.Nf` formatting (half-even on binary floats), unlike `percent`'s half-up,
  because the billing-matching requirement was stated only for percent. Fixed ' GB' suffix, not translated;
  negatives and string input work; no NaN/inf special-casing (float('nan') -> 'nan GB').

## Failed approaches
None.
