#!/bin/sh
# Basic Memory, local, per its Claude Code integration docs:
#   claude mcp add basic-memory basic-memory mcp
#   bm install claude-code --yes      (plugin: session-start briefing, pre-compact checkpoint, skills;
#                                      --yes because there is no terminal to confirm in)
#   then /basic-memory:bm-setup once, to map the repo to a project.
# Notes are Markdown files under the user's home.
case $1 in
  install)
    command -v basic-memory >/dev/null || { echo "basic-memory not installed" >&2; exit 1; }
    claude mcp add -s user basic-memory basic-memory mcp >/dev/null
    bm install claude-code --yes > "$EPISODE/bm-install.log" 2>&1
    claude plugin list 2>/dev/null | grep -q 'basic-memory@basicmachines-co' ||
      { echo "basic-memory plugin did not install" >&2; cat "$EPISODE/bm-install.log" >&2; exit 1; }
    basic-memory --version > "$EPISODE/basic-memory.version" 2>&1 || true ;;
  before_session)
    # The README's one-time setup step, run once per repo before its first
    # session. bm-setup is a short interview; the scripted user accepts every
    # suggested default (the repo has no remote, so it is named after its directory).
    m="$EPISODE/.bm-setup-$(basename "$REPO_DIR")"
    if [ ! -f "$m" ]; then
      {
        printf '%s\n' '{"type":"user","message":{"role":"user","content":"/basic-memory:bm-setup"}}'
        printf '%s\n' '{"type":"user","message":{"role":"user","content":"Use your suggested default for every question. It is a code/dev project. There is no git remote, so use the directory name as the repository identifier."}}'
        printf '%s\n' '{"type":"user","message":{"role":"user","content":"Yes, go ahead and apply it."}}'
      } |
        CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p --model claude-sonnet-5-5 --input-format stream-json --output-format stream-json --verbose --dangerously-skip-permissions --max-turns 40 > "$m" 2>&1 || true
    fi ;;
  snapshot)
    mkdir -p "$SNAPSHOT"
    [ -d "$HOME/basic-memory" ] && cp -R "$HOME/basic-memory" "$SNAPSHOT/notes"
    [ -d "$HOME/.basic-memory" ] && cp "$HOME/.basic-memory"/*.json "$SNAPSHOT/" 2>/dev/null
    cp "$EPISODE"/.bm-setup-* "$EPISODE/basic-memory.version" "$EPISODE/bm-install.log" "$SNAPSHOT/" 2>/dev/null
    [ -d "$REPO_DIR/.claude" ] && cp -R "$REPO_DIR/.claude" "$SNAPSHOT/repo-claude" 2>/dev/null; true ;;
esac
exit 0
