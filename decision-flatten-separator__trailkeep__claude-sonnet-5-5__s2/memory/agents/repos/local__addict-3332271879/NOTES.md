# Private notes: local__addict-3332271879

- 2026-11-05: Dict.flatten() (planned, not built yet) joins nested keys with a double underscore, not dots: {'db': {'host': 'x'}} -> {'db__host': 'x'}. Reason: the flat pairs become environment variables on the deploy side, and that tooling splits nested names on '__'.
- 2026-11-05: Dict.flatten() is built: joins keys with '__' by default (sep param overrides); empty nested dicts yield no entries
