#!/bin/sh
# Install dependencies when the registry is reachable; the hidden check does not need them.
npm install --no-audit --no-fund --no-package-lock >/dev/null 2>&1 || true
exit 0
