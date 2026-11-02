#!/bin/sh
# trailkeep, default install, from the checkout under test.
case $1 in
  install) sh "$TRAILKEEP_ROOT/bin/trailkeep" install --no-codex --no-copilot >/dev/null ;;
  snapshot)
    mkdir -p "$SNAPSHOT"
    [ -d "$HOME/.agents" ] && cp -R "$HOME/.agents" "$SNAPSHOT/agents" && rm -rf "$SNAPSHOT/agents/trailkeep"
    for d in "$EPISODE"/work/*/.trailkeep; do [ -d "$d" ] && cp -R "$d" "$SNAPSHOT/$(basename "$(dirname "$d")")-trailkeep"; done ;;
esac
exit 0
