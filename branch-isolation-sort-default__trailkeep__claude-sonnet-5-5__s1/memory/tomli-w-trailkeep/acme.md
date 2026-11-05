# acme

Branch: acme · Repo: local__tomli-w-3756000610 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Acme build branch: sort_keys option must default to True here (main/upstream: option added first, default off). Reason: Acme tooling calls plain dumps() and we can't change their call sites. Key-order churn in Acme diffs comes from how our side builds dicts, plus writer regrouping literals before tables.
- 2026-11-05: sort_keys cherry-picked from main (c883e1a) and default flipped to True; tests relying on insertion order pass sort_keys=False explicitly. README/CHANGELOG still not updated.

