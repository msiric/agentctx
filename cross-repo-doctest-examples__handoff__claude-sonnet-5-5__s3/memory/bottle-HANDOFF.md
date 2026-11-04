# HANDOFF

## State
Added `BaseRequest.bearer_token` (bottle.py, next to `auth`) plus `test_bearer_token` in test/test_environ.py. Not committed.

## Decisions
- Scheme matched case-insensitively (RFC 7235). Empty token -> None.
- Independent of `auth`/`REMOTE_USER`; only reads HTTP_AUTHORIZATION.

## Failed approaches
None.
