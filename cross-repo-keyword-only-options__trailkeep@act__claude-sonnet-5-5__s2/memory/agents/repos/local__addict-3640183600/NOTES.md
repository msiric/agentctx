# Private notes: local__addict-3640183600

- 2026-11-06: My choice (not the user's): Dict.to_dict(skip_none=True) drops only None-valued dict keys; None items inside lists/tuples are kept. Reason: the flag is about keys, and removing list items would shift positions. Ask the user if they want it changed.
