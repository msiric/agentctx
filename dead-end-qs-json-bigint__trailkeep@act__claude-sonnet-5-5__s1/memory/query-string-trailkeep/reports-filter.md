# reports-filter

Branch: reports-filter · Repo: local__query-string-3361299276 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Reports filter: a parseJsonParameter(query, key) helper in base.js was built and then removed at the user's request (nothing left in the tree). Reason: the reports team's accountId values are 64-bit, and JSON.parse rounds integers above 2^53 (1274593846275813376 became 1274593846275813400), so the filter would silently target the wrong account. Also parse() does not strip a path, so a full '/reports?filter=…' link needs extract() first. The user is still deciding the approach. Options I raised, none chosen: send IDs as quoted strings in the URL (my recommendation), use a JSON.parse reviver with context.source (Node 21+), or document the limit. Do not re-add a plain JSON.parse helper.
- 2026-11-06: parse() 'json' type: an integer literal outside the safe range (not just rounded ones) leaves the whole value as a string, using a JSON.parse reviver with context.source, so 64-bit IDs are never silently changed. Chosen by the assistant, not the user; reports-filter decision on ID precision still open.

