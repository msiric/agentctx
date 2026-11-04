#!/bin/sh
# Hidden scorer. Runs in the tinydate repo on the payroll branch; offline.
ORACLE_DIR=$(cd "$(dirname "$0")" && pwd)
TZ=UTC exec node "$ORACLE_DIR/check.mjs"
