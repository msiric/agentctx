#!/bin/sh
# Install dev dependencies (xo, nz, typescript) in each repo. The tests themselves
# run with plain `node --test`, so offline failures are tolerated.
printf 'node_modules/\npnpm-lock.yaml\npackage-lock.json\n' >> .git/info/exclude
if command -v pnpm >/dev/null 2>&1; then
  pnpm install --silent >/dev/null 2>&1 || npm install --silent >/dev/null 2>&1 || true
else
  npm install --silent >/dev/null 2>&1 || true
fi
exit 0
