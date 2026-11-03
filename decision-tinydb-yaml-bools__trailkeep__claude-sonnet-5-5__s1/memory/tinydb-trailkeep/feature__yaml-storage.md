# feature/yaml-storage

Branch: feature/yaml-storage · Repo: local__tinydb-1959258553 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: YAMLStorage: use PyYAML (no ruamel); safe loader must treat only true/false as booleans (NO/off/yes/on stay strings, YAML 1.1 bool resolver override). Ops hand-edit files e.g. 'country: NO'. Refactored file handling into shared base class first; YAML storage built later.

