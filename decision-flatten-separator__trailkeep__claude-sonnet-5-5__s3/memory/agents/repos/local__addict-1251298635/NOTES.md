# Private notes: local__addict-1251298635

- 2026-11-05: Dict.flatten() (planned, not built yet) joins nested keys with a double underscore, not dots: {'db': {'host': 'x'}} -> {'db__host': 'x'}. Reason: the flat pairs are exported as environment variables, and the deploy-side tooling splits nested names on '__'. Decided by the user; build it in a later session.
- 2026-11-05: Dict.flatten() is built (default sep '__', optional sep arg; empty nested dicts omitted; keys str()-ed). Lists/tuples are leaves.
