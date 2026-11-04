#!/bin/sh
# Install the repo's dev dependencies. The registry may be unreachable;
# the oracle does not need node_modules, so failure is tolerated.
if command -v pnpm >/dev/null 2>&1; then
  pnpm install >/dev/null 2>&1 || npm install >/dev/null 2>&1 || true
else
  npm install >/dev/null 2>&1 || true
fi
exit 0
