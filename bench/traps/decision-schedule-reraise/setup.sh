#!/bin/sh
# Local dev environment: a venv at .venv inside the repo.
set -e
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -q --retries 1 --timeout 15 pytest pytz >/dev/null 2>&1 || true
SITE=$(.venv/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
echo "$PWD" > "$SITE/schedule-dev.pth"
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
.venv/bin/python -c 'import pytest, schedule'
