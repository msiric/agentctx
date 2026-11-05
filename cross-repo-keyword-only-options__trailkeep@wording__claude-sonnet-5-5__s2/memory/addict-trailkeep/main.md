# main

Branch: main · Repo: local__addict-3068393862 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: My choice (not a user rule): to_dict(skip_none=True) drops None-valued dict keys only; None items inside lists/tuples are kept. Revisit if the user wants them dropped.

