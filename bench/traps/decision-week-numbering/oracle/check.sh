#!/bin/sh
# Hidden scorer. Runs in the tinydate repo; offline, no node_modules needed.
ORACLE_DIR=$(cd "$(dirname "$0")" && pwd)
TZ=UTC exec node "$ORACLE_DIR/check.mjs"
