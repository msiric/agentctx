#!/bin/sh
# Hidden scorer: run from the primary repo (p-retry) after the last session.
exec node "$(dirname "$0")/check.mjs"
