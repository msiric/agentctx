# Handoff

## State
Added `BaseRequest.bearer_token` (bottle.py, next to `auth`) with a doctest, plus `TestBearerToken` in test/test_auth.py. Tests and doctest pass.

## Decisions
- Scheme match is case-insensitive (RFC 7235). Header with scheme but no token returns None.
- Kept separate from `auth` (Basic/REMOTE_USER) to avoid changing its contract.

## Failed approaches
None.
