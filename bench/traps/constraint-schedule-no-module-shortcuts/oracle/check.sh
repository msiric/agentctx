#!/bin/sh
# Hidden scorer entry point; runs in the primary repo.
HERE=$(cd "$(dirname "$0")" && pwd)
PY=.venv/bin/python
[ -x "$PY" ] || PY=python3
exec "$PY" "$HERE/score.py"
