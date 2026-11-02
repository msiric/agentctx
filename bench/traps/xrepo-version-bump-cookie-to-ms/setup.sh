#!/bin/sh
# Install dev dependencies so the agent can run the repo's own test suite.
# Failure is tolerated: oracle/check.sh needs no installed packages.
if [ -f pnpm-lock.yaml ]; then
  timeout 600 pnpm install --frozen-lockfile >/dev/null 2>&1 \
    || timeout 600 pnpm install >/dev/null 2>&1 || true
elif [ -f package-lock.json ]; then
  timeout 600 npm ci --no-audit --no-fund >/dev/null 2>&1 \
    || timeout 600 npm install --no-audit --no-fund >/dev/null 2>&1 || true
else
  timeout 600 npm install --no-audit --no-fund >/dev/null 2>&1 || true
fi
# Installing must not leave tracked files modified (e.g. a rewritten lockfile).
git checkout -q -- . 2>/dev/null || true
exit 0
