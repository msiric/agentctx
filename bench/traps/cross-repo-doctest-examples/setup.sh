#!/bin/sh
# Runs in each repo after checkout (TRAP_REPO says which). Best effort: PyPI may be unreachable.
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
if [ ! -d .venv ]; then
  python3 -m venv --system-site-packages .venv >/dev/null 2>&1 || true
fi
if [ -x .venv/bin/pip ]; then
  case "$TRAP_REPO" in
    semver) .venv/bin/pip install -q -e . pytest pytest-cov >/dev/null 2>&1 || true ;;
    *)      .venv/bin/pip install -q -e . pytest >/dev/null 2>&1 || true ;;
  esac
fi
exit 0
