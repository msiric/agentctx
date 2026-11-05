# Private notes: local__addict-2165590172

- 2026-11-05: Planned Dict.flatten(): join nested keys with '__' (not '.'), e.g. {'db': {'host': 'x'}} -> {'db__host': 'x'}. Reason: flattened pairs become env vars and the deploy tooling splits nested names on double underscore. Not built yet; deferred to a later session.
- 2026-11-05: Dict.flatten() implemented: joins keys with '__' by default (sep param overrides); empty nested dicts yield no entries. Reason for '__': flattened pairs become env vars and deploy tooling splits on double underscore.
