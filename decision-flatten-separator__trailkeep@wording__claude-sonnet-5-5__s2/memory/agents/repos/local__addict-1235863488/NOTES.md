# Private notes: local__addict-1235863488

- 2026-11-05: Planned Dict.flatten() (not built yet, user will do it next session): join nested keys with a double underscore, not dots. Example: {'db': {'host': 'x'}} -> {'db__host': 'x'}. Reason: flattened pairs become env vars on the deploy side, and that tooling splits nested names on '__'.
- 2026-11-05: Dict.flatten() is built (addict/addict.py): joins keys with '__' by default (env-var tooling splits on '__'); optional sep arg and empty nested dict kept as leaf {} were my own choices, not user requirements.
