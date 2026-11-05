# Private notes: local__xmltodict-3380727126

- 2026-11-05: drop_keys in xmltodict.py is iterative (explicit stack), not recursive: catalog docs can nest 3000+ deep and recursion hits RecursionError (same reason unparse fails there).
