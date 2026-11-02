#!/bin/sh
# The agent's built-in memory as shipped: Claude Code auto memory stays on.
case $1 in
  snapshot) mkdir -p "$SNAPSHOT" && for d in "$HOME"/.claude/projects/*/memory; do [ -d "$d" ] && cp -R "$d" "$SNAPSHOT/$(basename "$(dirname "$d")")"; done ;;
esac
exit 0
