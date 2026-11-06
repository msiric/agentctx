#!/bin/sh
# Make a project venv at the repo root. PyPI may be unreachable, so every step may fail.
mkdir -p .git/info
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
[ -d .venv ] || python3 -m venv --system-site-packages .venv >/dev/null 2>&1 || true
if [ -x .venv/bin/pip ]; then
  .venv/bin/pip install -q --retries 1 --timeout 20 pytest >/dev/null 2>&1 || true
  .venv/bin/pip install -q --retries 1 --timeout 20 -e . >/dev/null 2>&1 || true

fi
exit 0
