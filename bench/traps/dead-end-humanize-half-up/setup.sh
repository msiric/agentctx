#!/bin/sh
# Runs in the repo after checkout. Best effort: PyPI may be unreachable.
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
# hatch-vcs normally generates this (it is gitignored); make the src tree importable without a build.
[ -f src/humanize/_version.py ] || printf '__version__ = "0.0.0.dev0"\n' > src/humanize/_version.py
if [ ! -d .venv ]; then
  python3 -m venv --system-site-packages .venv >/dev/null 2>&1 || true
fi
if [ -x .venv/bin/pip ]; then
  .venv/bin/pip install -q -e '.[tests]' >/dev/null 2>&1 || .venv/bin/pip install -q pytest freezegun >/dev/null 2>&1 || true
fi
exit 0
