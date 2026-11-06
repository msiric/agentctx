#!/bin/sh
# Hidden scorer: runs oracle/check.py against the repo in the current directory.
ORACLE="$(cd "$(dirname "$0")" && pwd)"
if [ -x .venv/bin/python ] && .venv/bin/python -c 'import pytest' >/dev/null 2>&1; then
  PY=.venv/bin/python
else
  PY=python3
fi
PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH PYTHONDONTWRITEBYTECODE
exec "$PY" "$ORACLE/check.py"
