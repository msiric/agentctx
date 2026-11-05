# Private notes: local__tomli-w-1714943160

- 2026-11-05: Run tests with PYTHONPATH=src (tomli_w isn't installed in the env). sort_keys on main is opt-in, default off, so default output stays byte-identical; sorting applies to all levels incl. inline tables (added in e1543d3).
