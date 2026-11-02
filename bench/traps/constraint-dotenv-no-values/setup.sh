#!/bin/sh
# Local dev environment: a venv at .venv inside the repo, with the package
# installed in editable mode (provides the `dotenv` command in .venv/bin).
set -e
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -q --retries 1 --timeout 15 pytest click setuptools >/dev/null 2>&1 || true
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
if ! .venv/bin/python -m pip install -q --no-deps --no-build-isolation -e . >/dev/null 2>&1; then
    SITE=$(.venv/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
    echo "$PWD/src" > "$SITE/python_dotenv-dev.pth"
    printf '#!%s\nfrom dotenv.__main__ import cli\nimport sys\nsys.exit(cli())\n' "$PWD/.venv/bin/python" > .venv/bin/dotenv
    chmod +x .venv/bin/dotenv
fi
.venv/bin/python -c 'import pytest, click, dotenv.cli'
