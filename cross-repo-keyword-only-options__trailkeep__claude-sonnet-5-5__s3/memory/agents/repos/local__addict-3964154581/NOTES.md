# Private notes: local__addict-3964154581

- 2026-11-05: to_dict(skip_none=True) drops None-valued dict keys at every level but keeps bare None items in lists/tuples. Reason: removing list items would shift indexes.
