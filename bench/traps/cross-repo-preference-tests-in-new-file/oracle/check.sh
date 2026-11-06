#!/bin/sh
# Hidden scorer: run from the primary repo (decamelize) after the last session.
exec node "$(dirname "$0")/check.mjs"
