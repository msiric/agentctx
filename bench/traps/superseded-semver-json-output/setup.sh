#!/bin/sh
# Runs in the repo after checkout. Best effort: PyPI may be unreachable.
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
if [ ! -d .venv ]; then
  python3 -m venv --system-site-packages .venv >/dev/null 2>&1 || true
fi
if [ -x .venv/bin/pip ]; then
  # .pytest.ini adds --cov options, so pytest-cov is needed to run the suite.
  .venv/bin/pip install -q -e . pytest pytest-cov >/dev/null 2>&1 || true
fi
exit 0
