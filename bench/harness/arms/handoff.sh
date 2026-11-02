#!/bin/sh
# One instruction in the user's global instructions: keep HANDOFF.md.
case $1 in
  install)
    mkdir -p "$HOME/.claude" "$HOME/.codex"
    cat > "$HOME/.claude/CLAUDE.md" <<'MD'
When you work on a task in a git repository, keep a file named HANDOFF.md at the repository root: the current state of the task, decisions with their reasons, and approaches that failed and why. If it exists when a session starts, read it before doing anything else. Update it before you finish.
MD
    cp "$HOME/.claude/CLAUDE.md" "$HOME/.codex/AGENTS.md" ;;
  snapshot) mkdir -p "$SNAPSHOT" && find "$EPISODE/work" -maxdepth 2 -name HANDOFF.md -exec sh -c 'cp "$1" "$2/$(basename "$(dirname "$1")")-HANDOFF.md"' _ {} "$SNAPSHOT" \; ;;
esac
exit 0
