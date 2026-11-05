#!/bin/sh
# Install dev dependencies (mocha, eslint). Offline failures are tolerated.
printf 'node_modules/\npnpm-lock.yaml\npackage-lock.json\n' >> .git/info/exclude
if command -v pnpm >/dev/null 2>&1; then
  pnpm install --silent >/dev/null 2>&1 || npm install --silent >/dev/null 2>&1 || true
else
  npm install --silent >/dev/null 2>&1 || true
fi
exit 0
