#!/bin/sh
# Hidden scorer. Runs in the repo root; needs only Node 22.6+ (no packages).
ORACLE=$(cd "$(dirname "$0")" && pwd)
FLAG=""
node --experimental-strip-types -e 0 >/dev/null 2>&1 && FLAG="--experimental-strip-types"
exec node $FLAG --no-warnings "$ORACLE/check.mjs"
