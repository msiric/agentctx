#!/bin/sh
# Hidden scorer: run from the primary repo (camelcase, branch release/10.x) after the last session.
exec node "$(dirname "$0")/check.mjs"
