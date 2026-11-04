#!/bin/sh
# Runs in the repo after checkout. Best effort: PyPI may be unreachable.
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
if [ ! -d .venv ]; then
  python3 -m venv --system-site-packages .venv >/dev/null 2>&1 || true
fi
if [ -x .venv/bin/pip ]; then
  .venv/bin/pip install -q -e . pytest >/dev/null 2>&1 || true
fi
exit 0
