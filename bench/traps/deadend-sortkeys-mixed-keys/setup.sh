#!/bin/sh
# Runs in the repo after checkout. Best effort: a .venv with tinydb (editable)
# and its test deps. Failure (e.g. no package index) is tolerated; the system
# python3 + pytest is the fallback.
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
python3 -m venv .venv >/dev/null 2>&1 || true
if [ -x .venv/bin/pip ]; then
  .venv/bin/pip install -q --disable-pip-version-check -e . pytest pytest-cov pyyaml >/dev/null 2>&1 || true
fi
exit 0
