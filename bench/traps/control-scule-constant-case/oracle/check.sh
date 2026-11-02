#!/bin/sh
# Hidden scorer. Runs in the primary repo; prints one JSON line per fact plus
# a {"task": ...} line; exits 0 only if the task is done and every fact holds.
ORACLE=$(cd "$(dirname "$0")" && pwd)
exec node --no-warnings "$ORACLE/check.mjs"
