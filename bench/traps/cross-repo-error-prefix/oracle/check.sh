#!/bin/sh
# Hidden scorer: runs in the parse-ms repo, imports ./index.js directly (no deps).
here=$(cd "$(dirname "$0")" && pwd)
exec timeout 60 node "$here/check.mjs"
