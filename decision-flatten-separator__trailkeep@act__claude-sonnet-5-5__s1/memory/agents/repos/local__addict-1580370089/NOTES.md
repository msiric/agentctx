# Private notes: local__addict-1580370089

- 2026-11-06: Dict.flatten() (planned, not built yet) must join nested keys with a double underscore, not dots: {'db': {'host': 'x'}} -> {'db__host': 'x'}. Reason: the flat pairs become environment variables, and the deploy tooling splits nested names on '__'. User's decision; build it in a later session.
- 2026-11-06: Dict.flatten() is built (addict/addict.py) and joins nested keys with '__' per the user's decision. These details were my own choices, not the user's, so change them if asked: a sep='__' parameter; keys passed through str(); an empty nested dict yields no entry; lists/tuples are leaves and are not recursed into.
