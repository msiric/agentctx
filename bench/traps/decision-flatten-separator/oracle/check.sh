#!/bin/sh
# Hidden scorer: runs in the primary repo's working tree.
PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python
exec "$PY" "$(dirname "$0")/check.py"
