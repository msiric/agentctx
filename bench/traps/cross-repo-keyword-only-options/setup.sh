#!/bin/sh
# Private venv with pytest; must tolerate an offline machine.
python3 -m venv --system-site-packages .venv >/dev/null 2>&1 || python3 -m venv .venv >/dev/null 2>&1 || true
if [ -x .venv/bin/python ]; then
  .venv/bin/python -m pip install -q --disable-pip-version-check --retries 1 --timeout 20 pytest >/dev/null 2>&1 || true
fi
mkdir -p .git/info
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
exit 0
