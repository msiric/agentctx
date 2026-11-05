# Private notes: local__tomli-w-3756000610

- 2026-11-05: sort_keys option (dump/dumps, keyword-only) added on main in c883e1a, default off so default output stays byte-for-byte unchanged. Sorts keys in every table incl. inline tables; array element order is NOT changed. Mixed-type keys raise Python's '<' TypeError when sorting. README/CHANGELOG not yet updated. Run tests with PYTHONPATH=src (package not installed).
