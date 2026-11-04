# Private notes: local__humanize-2325627777

- 2026-11-04: humanize is used only on customer billing and usage pages (user's stated context), so new helpers target those: percent() is first. Run tests with: PYTHONPATH=src python -m pytest -W ignore::pytest.PytestDeprecationWarning (package isn't installed; pytest-asyncio warns otherwise).
- 2026-11-04: percent() must round half away from zero (0.0625 -> '6.3%'), matching billing's invoice generator; it uses Decimal(repr(value)) with ROUND_HALF_UP because float formatting rounds half-even on binary values (gives '6.2%'). Billing-matching cases live in tests/test_number.py::test_percent.
- 2026-11-04: gigabytes() added in filesize.py using plain f-string rounding (half-even on binary floats), unlike percent() which uses ROUND_HALF_UP to match billing's invoice generator. Unconfirmed whether billing needs half-up for GB too (e.g. 1.25e9 -> '1.2 GB' vs '1.3 GB'); ask user if usage page totals must match invoices.
