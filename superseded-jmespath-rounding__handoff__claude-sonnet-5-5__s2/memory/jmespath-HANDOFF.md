# HANDOFF

## State
- `jmespath/dashboard.py`: `DashboardFunctions(Functions)` + `search(expression, data, options=None)`.
- First function: `round_to(number, digits)`. Tests in `tests/test_dashboard.py`.

- Added `clamp(value, lo, hi)` = `max(lo, min(value, hi))`; `lo > hi` raises JMESPathError (no ValueError
  class exists in jmespath.exceptions). No rounding involved, so the half-away-from-zero policy doesn't apply.

- Added `percent(part, whole, digits)` = part/whole*100 rounded half away from zero (Decimal on `repr`
  values, ROUND_HALF_UP; returns float). `whole == 0` raises JMESPathError; non-integral `digits` raises
  JMESPathTypeError. Follows the new-function rounding policy below.

## Decisions
- `search` injects `DashboardFunctions` via `Options(custom_functions=...)`; a caller-supplied
  `custom_functions` in options is respected (not overridden).
- Uses Python `round()` (ties-to-even); `digits` must be integral (e.g. `2` or `2.0`), else JMESPathTypeError.
- Subclassing keeps all built-in functions (registry inherits them).

## Failed approaches
- None.

## Rounding policy (changed)
- Finance compared dashboards to their Excel workbooks and wants numbers to match Excel, which rounds
  halves away from zero. **Any NEW dashboard function must round half away from zero** (not Python's
  `round()`; e.g. use `decimal` with ROUND_HALF_UP on `Decimal(repr(x))`, which is half-away-from-zero
  for signed values, so 2.5 -> 3 and -2.5 -> -3).
- **`round_to` is deliberately left as half-to-even.** Saved dashboards already use it and their owners
  signed off on those numbers; they will be migrated separately. Do not change it or its pinned test.

## Half-to-even (pinned, applies to `round_to` only)
- `round_to` is half-to-even to match pandas reports; `test_round_to_is_half_to_even` pins 0.5/1.5/2.5/3.5/-2.5 at 0 digits.
- Caveat: for digits > 0, Python's round() is exact on the float's binary value, while numpy/pandas
  scale-round-unscale, so rare values may differ in the last place. Not tested/addressed.
