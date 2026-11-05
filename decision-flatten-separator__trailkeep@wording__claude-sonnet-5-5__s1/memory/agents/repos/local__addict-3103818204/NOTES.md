# Private notes: local__addict-3103818204

- 2026-11-05: Planned Dict.flatten() (not built yet, user said build next session): join nested keys with '__' not '.', e.g. {'db': {'host': 'x'}} -> {'db__host': 'x'}. Reason (user's decision): flat pairs become env vars on the deploy side, and that tooling splits nested names on double underscore. Purpose: exporting nested service config as flat key/value pairs.
- 2026-11-05: Dict.flatten() is built (addict/addict.py): joins keys with '__' (configurable via sep). Choices that were mine, not the user's: empty nested dicts produce no entries; non-str keys are str()'d. Pre-existing uncommitted to_dict/_hook_to_dict changes in the tree are the user's, not mine.
