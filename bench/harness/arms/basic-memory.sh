#!/bin/sh
# Basic Memory, local, per its Claude Code integration docs:
#   claude mcp add basic-memory basic-memory mcp
#   bm install claude-code            (plugin: session-start briefing, pre-compact checkpoint, skills)
#   then /basic-memory:bm-setup once, to map the repo to a project.
# Notes are Markdown files under the user's home.
case $1 in
  install)
    command -v basic-memory >/dev/null || { echo "basic-memory not installed" >&2; exit 1; }
    claude mcp add -s user basic-memory basic-memory mcp >/dev/null
    bm install claude-code >/dev/null
    basic-memory --version > "$EPISODE/basic-memory.version" 2>&1 || true ;;
  before_session)
    # the README's one-time setup step, run once per repo before its first session
    m="$EPISODE/.bm-setup-$(basename "$REPO_DIR")"
    if [ ! -f "$m" ]; then
      printf '%s\n' '{"type":"user","message":{"role":"user","content":"/basic-memory:bm-setup"}}' |
        CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p --model claude-sonnet-5-5 --input-format stream-json --output-format stream-json --verbose --dangerously-skip-permissions --max-turns 15 > "$m" 2>&1 || true
    fi ;;
  snapshot)
    mkdir -p "$SNAPSHOT"
    [ -d "$HOME/basic-memory" ] && cp -R "$HOME/basic-memory" "$SNAPSHOT/notes"
    [ -d "$HOME/.basic-memory" ] && cp "$HOME/.basic-memory"/*.json "$SNAPSHOT/" 2>/dev/null
    cp "$EPISODE"/.bm-setup-* "$EPISODE/basic-memory.version" "$SNAPSHOT/" 2>/dev/null; true ;;
esac
exit 0
