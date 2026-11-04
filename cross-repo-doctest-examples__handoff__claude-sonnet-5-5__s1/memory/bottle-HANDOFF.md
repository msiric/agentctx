# Handoff

## State
Added `BaseRequest.bearer_token` (bottle.py, next to `remote_route`) with doctests,
and `test_bearer_token` in test/test_environ.py. Tests and doctests pass. Not committed.

## Decisions
- Scheme matched case-insensitively (RFC 7235). Empty token returns None.
- Parses `HTTP_AUTHORIZATION` directly, not via `parse_auth` (that is basic-only).

## Failed approaches
None.
