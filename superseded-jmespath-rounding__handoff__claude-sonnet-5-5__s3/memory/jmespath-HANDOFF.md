# HANDOFF

## State
- Added `jmespath/dashboard.py`: `DashboardFunctions(Functions)` and `search(expression, data)` helper (passes it via `Options(custom_functions=...)`).
- Functions so far: `round_to(number, digits)`. Verified manually: `round_to(3.14159, 2)` -> 3.14. No tests added yet.

## Decisions
- `digits` is a `number` type per JMESPath (no integer type), so it is cast with `int()`.
- Helper builds its own parser/Options rather than touching the global `jmespath.search`.

## Failed approaches
- None.

## Update: half-to-even
- `round_to` already used Python's `round()`, which is half-to-even, so no code change. Pinned in `tests/test_dashboard.py` (2.5 -> 2, 0.125 -> 0.12, etc.).
- Caveat: non-exact decimals (e.g. 2.675) round per their binary float value, same as Python/pandas.

## Update: rounding policy change (half away from zero)
- Finance compared dashboards with their Excel workbooks; they want numbers to match Excel, which rounds halves away from zero.
- Rule: **any new dashboard function that rounds must round half away from zero** (2.5 -> 3, -2.5 -> -3).
- **`round_to` is intentionally left as half-to-even.** Saved dashboards already use it and their owners signed off on those numbers; migrating them is a separate task. Do not "fix" it without that migration.
- No code changed in this update; no new rounding function exists yet.
- Implementation note for the next rounding function: don't use `round()`. Use `decimal.Decimal(str(x)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)` (ROUND_HALF_UP is away from zero for negatives in `decimal`). Going via `str()` matches what Excel shows for values like 2.675 (-> 2.68), unlike binary-float rounding.

## Update: clamp
- Added `clamp(value, lo, hi)` to `DashboardFunctions` (all `number` args, bounds inclusive, returns `max(lo, min(value, hi))`). Tests in `tests/test_dashboard.py` (7 pass).
- Decision: `lo > hi` raises `ValueError` rather than silently picking an order, so bad dashboard expressions are loud.
- No rounding involved, so the half-away-from-zero policy doesn't apply; `round_to` untouched.

## Update: percent
- Added `percent(part, whole, digits)` = part/whole*100 rounded to `digits`. It rounds, so it follows the policy: half away from zero via `Decimal(str(x))` + `ROUND_HALF_UP` (2.675% -> 2.68). Returns a float. Tests added (11 pass total).
- Decision: `whole == 0` raises `ValueError` (loud, like `clamp`), not None/inf.
- `round_to` still untouched (half-to-even), per the migration note above.
