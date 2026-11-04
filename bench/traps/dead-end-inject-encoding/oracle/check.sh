#!/bin/sh
# Hidden scorer. Runs in the regexparam repo; offline, no node_modules needed.
ORACLE_DIR=$(cd "$(dirname "$0")" && pwd)
exec node "$ORACLE_DIR/check.mjs"
