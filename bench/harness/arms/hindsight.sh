#!/bin/sh
# Hindsight, self-hosted, per its docs: the hindsight-api server (pip package,
# embedded database, local embedding and reranker models) with Gemini as the
# LLM, and the Claude Code integration installed with
#   npx -y @vectorize-io/hindsight-coding-agents@0.7.0 install claude-code --server self-hosted --api-url http://localhost:8888
# One server per episode, its data under the episode's home.
case $1 in
  install)
    command -v hindsight-api >/dev/null || { echo "hindsight-api not installed" >&2; exit 1; }
    [ -n "${GEMINI_API_KEY:-}" ] || { echo "GEMINI_API_KEY not set" >&2; exit 1; }
    HINDSIGHT_API_LLM_PROVIDER=gemini HINDSIGHT_API_LLM_API_KEY="$GEMINI_API_KEY" \
      nohup hindsight-api > "$EPISODE/hindsight-server.log" 2>&1 &
    echo $! > "$EPISODE/hindsight.pid"
    i=0; until curl -s --max-time 2 -o /dev/null http://127.0.0.1:8888/ 2>/dev/null; do
      i=$((i + 1)); [ $i -gt 120 ] && { echo "hindsight server did not start" >&2; tail -20 "$EPISODE/hindsight-server.log" >&2; exit 1; }
      sleep 2
    done
    npx -y @vectorize-io/hindsight-coding-agents@0.7.0 install claude-code --server self-hosted --api-url http://localhost:8888 > "$EPISODE/hindsight-install.log" 2>&1
    pip show hindsight-api 2>/dev/null | sed -n 's/^Version: /hindsight-api /p' > "$EPISODE/hindsight.version" ;;
  after_session)
    # retention runs after the session (LLM extraction); allow up to 2 minutes, as a real gap would
    sleep 90 ;;
  snapshot)
    mkdir -p "$SNAPSHOT"
    cp "$EPISODE"/hindsight*.log "$EPISODE/hindsight.version" "$SNAPSHOT/" 2>/dev/null
    for b in $(curl -s --max-time 5 http://127.0.0.1:8888/v1/default/banks 2>/dev/null | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(" ".join(x.get("bank_id") or x.get("id","") for x in (d.get("banks", d) if isinstance(d, dict) else d)))
except Exception: pass' 2>/dev/null); do
      curl -s --max-time 10 "http://127.0.0.1:8888/v1/default/banks/$b/memories/list?limit=500" > "$SNAPSHOT/bank-$b.json" 2>/dev/null
    done
    kill "$(cat "$EPISODE/hindsight.pid" 2>/dev/null)" 2>/dev/null; sleep 2; pkill -f hindsight-api 2>/dev/null; true ;;
esac
exit 0
