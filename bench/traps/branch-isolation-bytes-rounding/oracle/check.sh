#!/bin/sh
# Hidden scorer: runs in the bytes repo, loads ./index.js directly (no deps).
here=$(cd "$(dirname "$0")" && pwd)
exec timeout 60 node "$here/check.cjs"
