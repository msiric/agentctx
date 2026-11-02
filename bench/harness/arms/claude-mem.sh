#!/bin/sh
# claude-mem (Claude Code plugin), installed per its README:
#   claude plugin marketplace add thedotmack/claude-mem && claude plugin install claude-mem
# Its worker (Bun, 127.0.0.1:37777) compresses observations by calling Claude with
# the same credentials as the session. Defaults otherwise.
worker_pid() { cat "$HOME/.claude-mem/.worker.pid" 2>/dev/null; }
stop_worker() {
  p=$(worker_pid); [ -n "$p" ] && kill "$p" 2>/dev/null
  pkill -f "$HOME/.claude/plugins" 2>/dev/null || true
}
case $1 in
  install)
    claude plugin marketplace add thedotmack/claude-mem >/dev/null
    claude plugin install claude-mem@thedotmack --scope user >/dev/null
    claude plugin list 2>/dev/null | grep -i -A2 claude-mem > "$EPISODE/claude-mem.version" || true ;;
  after_session)
    # The summary is written after the session ends; give the worker time to
    # finish, as the gap between real sessions would (up to 3 minutes).
    i=0
    while [ $i -lt 36 ]; do
      sleep 5; i=$((i + 1))
      q=$(curl -s --max-time 2 http://127.0.0.1:37777/api/processing-status 2>/dev/null || true)
      case $q in *'"isProcessing":false'*|*'"queueDepth":0'*) [ $i -ge 4 ] && break ;; esac
    done ;;
  snapshot)
    mkdir -p "$SNAPSHOT"
    [ -d "$HOME/.claude-mem" ] && cp -R "$HOME/.claude-mem" "$SNAPSHOT/claude-mem" 2>/dev/null
    cp "$EPISODE/claude-mem.version" "$SNAPSHOT/" 2>/dev/null
    find "$SNAPSHOT" \( -name '*.pid' -o -name '*.sock' -o -name chroma \) -prune -exec rm -rf {} + 2>/dev/null
    stop_worker ;;
esac
exit 0
