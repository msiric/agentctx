#!/bin/sh
# Ceiling: the trap's live facts, written as a perfect note, loaded at the last session's start.
case $1 in
  before_session)
    mkdir -p "$HOME/.claude"
    if [ "$LAST" = 1 ] && [ -s "$FACTS_FILE" ]; then
      { printf 'Notes from earlier sessions on this work:\n'; cat "$FACTS_FILE"; } > "$HOME/.claude/CLAUDE.md"
    else
      rm -f "$HOME/.claude/CLAUDE.md"
    fi ;;
esac
exit 0
