#!/bin/sh
# Hidden scorer: runs in the primary repo after the last session.
# Prefers the repo's .venv when it has pytest, else the system python3.
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=python3
if [ -x .venv/bin/python ] && .venv/bin/python -c 'import pytest' >/dev/null 2>&1; then
  PY=.venv/bin/python
fi
exec "$PY" "$HERE/run_checks.py"
