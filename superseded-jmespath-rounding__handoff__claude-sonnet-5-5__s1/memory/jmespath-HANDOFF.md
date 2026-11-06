# HANDOFF

## State
- Added `jmespath/dashboard.py`: `DashboardFunctions(Functions)` and `search(expression, data, options=None)`.
- First function: `round_to(number, digits)` (uses Python `round`, so banker's rounding on exact ties).
- Tests in `tests/test_dashboard.py`; full suite passes.

## Decisions
- Subclass works with no extra registration: the `FunctionRegistry` metaclass rebuilds the function table per subclass, inheriting built-ins.
- `digits` is typed `number` (JMESPath has no int type); non-whole values raise `JMESPathError`.
- `search` injects `DashboardFunctions` only if the caller's `Options` has no `custom_functions`; otherwise the caller's options are used as given.
- Not exported from `jmespath/__init__.py`; import via `jmespath.dashboard`.

## Failed approaches
- None.

## Update: half-to-even pinned
- `round_to` already delegated to Python `round()` (half-to-even); added `test_round_to_half_to_even` in `tests/test_dashboard.py` to pin it (incl. `round_to(2.5, 0) == 2`, negatives, and negative digits).
- Not verified against pandas directly: pandas isn't installed in this environment. Binary float representation (e.g. 2.675 -> 2.67) applies to both Python and pandas/numpy, but numpy's decimals rounding scales by 10**n, so it can differ from Python on rare non-tie values.

## Update: rounding policy change (half away from zero)
- Decision (from user, driven by Finance): dashboards must match Excel, which rounds halves away from zero. Any NEW dashboard function that rounds must use half away from zero (e.g. `decimal.Decimal` with `ROUND_HALF_UP`, which is away-from-zero on ties; do not use Python `round()`).
- `round_to` is intentionally left unchanged (still half-to-even). Saved dashboards use it and their owners signed off on those numbers; migration will be handled separately. Do not "fix" it, and keep `test_round_to_half_to_even` as is.
- Caveat for future work: Excel rounds the decimal representation as displayed, so build from `Decimal(repr(x))`/`str(x)` rather than `Decimal(x)`, otherwise 2.675 style values will round differently from Excel.
- No code changed in this update; no new rounding function exists yet.

## Update: clamp added
- Added `clamp(value, lo, hi)` to `DashboardFunctions`: returns `max(lo, min(value, hi))`, preserves input numeric type; raises `JMESPathError` if `lo > hi` (chosen over silently picking an order). Tests added.
- No rounding involved, so the half-away-from-zero policy doesn't apply; `round_to` untouched.

## Update: percent added
- Added `percent(part, whole, digits)` = part/whole*100, rounded to `digits`. Follows the half-away-from-zero policy: `Decimal(repr(x))` arithmetic (prec 60) + `quantize(..., ROUND_HALF_UP)`; returns a float. Python `round()` deliberately not used. `round_to` untouched.
- Decisions: `whole == 0` raises `JMESPathError` (consistent with `clamp`; returning null is the alternative if dashboards prefer it). Non-whole `digits` raises, as in `round_to`. Negative `digits` supported.
- Tests added (ties, negatives, zero whole, type errors); full suite passes (1003 passed, 1 skipped).
- Caveat: result is a float, so e.g. 12.5 is exact but a value like 33.33 is the nearest binary float to the rounded decimal.
