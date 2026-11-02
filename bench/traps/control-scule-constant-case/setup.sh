#!/bin/sh
# Best-effort install of the repo's dev dependencies so its own test suite
# (vitest / jest) can run during the sessions. The oracle does not need them:
# it only needs Node >= 22.6.
if [ -f pnpm-lock.yaml ] && command -v pnpm >/dev/null 2>&1; then
  pnpm install --frozen-lockfile --config.manage-package-manager-versions=false >/dev/null 2>&1 || true
elif [ -f package.json ]; then
  npm install --no-audit --no-fund >/dev/null 2>&1 || true
fi
exit 0
