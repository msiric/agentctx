#!/bin/sh
# Hidden scorer. Runs in the schema repo on the final working tree.
HERE=$(cd "$(dirname "$0")" && pwd)
PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python
exec "$PY" "$HERE/check.py"
