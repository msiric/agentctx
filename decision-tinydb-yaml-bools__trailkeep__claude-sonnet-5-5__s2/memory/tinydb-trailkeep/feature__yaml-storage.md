# feature/yaml-storage

Branch: feature/yaml-storage · Repo: local__tinydb-1745008240 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: YAMLStorage: use PyYAML but NOT plain safe_load (YAML 1.1 turns NO/off/yes into bools, ops hand-edit files). Custom SafeLoader subclass where only true/false resolve as bool; everything else stays str. No ruamel.yaml (user rejected extra dep). Step 1 (done first): extract shared file handling from JSONStorage into a base class; YAML storage built in a later session.
- 2026-11-03: YAMLStorage implemented in storages.py on _FileStorage base (strict-bool SafeLoader subclass, PyYAML imported lazily, safe_dump). Tests added in tests/test_storages.py (test_yaml_storage_*), use a pyyaml fixture w/ importorskip — NOT module-level importorskip. pytest.ini needs pytest-cov; run with -o addopts=''. Not yet done: docs, PyYAML as optional extra in pyproject.

