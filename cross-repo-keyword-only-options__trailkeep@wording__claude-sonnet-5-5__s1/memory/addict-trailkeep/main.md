# main

Branch: main · Repo: local__addict-2417375296 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: My choice (not the user's): to_dict(skip_none=True) drops only dict keys with None values; bare None items inside lists/tuples are kept, since removing them would shift positions. Revisit if the user wants them removed too.

