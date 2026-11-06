# Private notes: local__addict-2042986535

- 2026-11-06: User's decision (not mine): Dict.flatten() joins nested keys with '__' (double underscore), not dots. Reason: flat pairs become env variables on the deploy side, and that tooling splits nested names on '__'. Example: {'db': {'host': 'x'}} -> {'db__host': 'x'}. Not built yet; user said to implement it in a later session.
- 2026-11-06: Dict.flatten() built (addict/addict.py). Default separator '__' per user's decision. My own choices (not user's): separator is an optional arg; empty nested dicts are omitted since they have no leaves; keys are str()-ed. Revisit if the user wants otherwise.
