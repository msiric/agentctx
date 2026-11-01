#!/bin/sh
# agentctx test suite. POSIX sh, no deps beyond git. Every test runs with a
# throwaway $HOME, so it never touches your real setup.
#
#   sh tests/run.sh            unit + integration tests (stubs for the agents)
#   AGENTCTX_REAL=1 sh tests/run.sh
#                              also run against the real claude / codex CLIs
#                              if installed (offline: no model calls)

set -u
HERE=$(cd "$(dirname "$0")" && pwd -P)
ROOT=$(cd "$HERE/.." && pwd -P)
BIN=$ROOT/bin/agentctx
REAL_PATH=$PATH
PASS=0; FAIL=0; CURRENT=

# ------------------------------------------------------------- harness ----

t() { CURRENT=$1; }
pass() { PASS=$((PASS + 1)); }
flunk() { FAIL=$((FAIL + 1)); printf 'FAIL  %s: %s\n' "$CURRENT" "$*"; }

eq()       { if [ "$1" = "$2" ]; then pass; else flunk "${3:-} expected [$2] got [$1]"; fi; }
contains() { case $1 in *"$2"*) pass ;; *) flunk "${3:-} expected to contain [$2] in: $1" ;; esac; }
lacks()    { case $1 in *"$2"*) flunk "${3:-} expected NOT to contain [$2] in: $1" ;; *) pass ;; esac; }
is_file()  { if [ -f "$1" ]; then pass; else flunk "missing file $1"; fi; }
no_file()  { if [ -e "$1" ] || [ -L "$1" ]; then flunk "unexpected file $1"; else pass; fi; }
links_to() { if [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]; then pass; else flunk "$1 should link to $2"; fi; }
status()   { if [ "$1" -eq "$2" ]; then pass; else flunk "${3:-} expected exit $2 got $1"; fi; }

# Fresh sandbox: new HOME, stub bin dir first on PATH, clean agent env vars.
sandbox() {
  SB=$(mktemp -d)
  export HOME="$SB/home"
  mkdir -p "$HOME" "$SB/stubs" "$HOME/.local/bin"
  unset AGENTCTX_HOME CODEX_HOME COPILOT_HOME CLAUDE_CONFIG_DIR AGENTCTX_EFFORT AGENTCTX_MAX_CHARS
  export PATH="$SB/stubs:$HOME/.local/bin:/usr/bin:/bin"
  export GIT_CONFIG_NOSYSTEM=1 GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
  git config --global init.defaultBranch main
  git config --global user.name t; git config --global user.email t@t
}

new_repo() { # new_repo DIR [REMOTE]
  mkdir -p "$1" && (cd "$1" && git init -q && git commit -q --allow-empty -m init)
  [ -n "${2:-}" ] && (cd "$1" && git remote add origin "$2")
  return 0
}

ax() { ${AGENTCTX_TEST_SHELL:-} "$BIN" "$@"; }

tree_snapshot() { # deterministic listing + contents of HOME
  (cd "$HOME" && find . \( -type f -o -type l \) | LC_ALL=C sort | while IFS= read -r f; do
    if [ -L "$f" ]; then printf 'L %s -> %s\n' "$f" "$(readlink "$f")"; else printf 'F %s %s\n' "$f" "$(cksum < "$f")"; fi
  done) | grep -v '/backups/'
}

# Stub "claude" that records its arguments and fakes plugin state.
stub_claude() {
  cat > "$SB/stubs/claude" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$HOME/claude.calls"
case "$1 $2" in
  "plugin list") [ -f "$HOME/.stub-installed" ] && echo "agentctx@agentctx" ;;
  "plugin marketplace")
    case $3 in
      list) [ -f "$HOME/.stub-mkt" ] && echo "agentctx" ;;
      add) touch "$HOME/.stub-mkt" ;;
      remove) rm -f "$HOME/.stub-mkt" ;;
    esac ;;
  "plugin install") touch "$HOME/.stub-installed" ;;
  "plugin uninstall") rm -f "$HOME/.stub-installed" ;;
esac
exit 0
EOF
  chmod +x "$SB/stubs/claude"
}

# Stub agents for `verify`: each emulates how the real tool loads context
# (global file through its own path, repo AGENTS.md, our hook) and echoes
# every ACX- token it "sees".
stub_agent() { # NAME GLOBAL_FILE HOOK_TARGET [skip-effort]
  cat > "$SB/stubs/$1" <<EOF
#!/bin/sh
{
  cat "$2" 2>/dev/null
  cat AGENTS.md 2>/dev/null
  if [ "${4:-}" != skip-effort ]; then echo '{"cwd":"'"\$PWD"'","source":"startup"}' | "$BIN" context --for $3; fi
} | grep -o 'ACX-[A-Z0-9]*' | tr '\n' ' '
echo
EOF
  chmod +x "$SB/stubs/$1"
}

# ------------------------------------------------------------- tests ----

test_cli_basics() {
  t "cli basics"; sandbox
  out=$(ax --version); contains "$out" "agentctx 0."
  out=$(ax help); contains "$out" "install"
  ax nope >/dev/null 2>&1; status $? 2
}

test_repo_key() {
  t "repo key"; sandbox
  for url in git@github.com:Msiric/Redue.git https://github.com/msiric/redue ssh://git@github.com/msiric/redue.git https://user@github.com/msiric/redue.git/; do
    rm -rf "$SB/r"; new_repo "$SB/r" "$url"
    key=$(cd "$SB/r" && ax path --repo)
    eq "$(basename "$key")" "github.com__msiric__redue" "$url"
  done
  rm -rf "$SB/r"; new_repo "$SB/r"
  key=$(basename "$(cd "$SB/r" && ax path --repo)")
  contains "$key" "local__r-" "no remote"
  # worktree shares the key with the main checkout
  (cd "$SB/r" && git worktree add -q "$SB/wt" -b feat/x)
  key2=$(basename "$(cd "$SB/wt" && ax path --repo)")
  eq "$key2" "$key" "worktree"
  # dir name with spaces
  new_repo "$SB/my repo"
  key3=$(basename "$(cd "$SB/my repo" && ax path --repo)")
  contains "$key3" "local__my_repo-"
}

test_effort_lifecycle() {
  t "effort lifecycle"; sandbox
  new_repo "$SB/r" git@github.com:me/app.git
  cd "$SB/r" || return
  git checkout -q -b feat/login
  out=$(ax new); contains "$out" "Created"
  f=$(ax path); is_file "$f"
  eq "$f" "$SB/r/.agentctx/feat__login.md" "lives in the worktree"
  contains "$(cat "$f")" "Branch: feat/login · Repo: github.com__me__app · Kind: branch"
  eq "$(git status --porcelain)" "" "git status stays clean"
  eq "$(git status --porcelain --ignored | grep -c agentctx)" "1" "folder is ignored"
  out=$(ax new); contains "$out" "already exists" "idempotent"

  printf '2026-11-01: wired the form, next: tests\n' > "$SB/p"
  awk -v l="$(cat "$SB/p")" '{ print } /^## Progress$/ { getline; print; print l }' "$f" > "$SB/f2" && cat "$SB/f2" > "$f"
  out=$(cd / && ax list); contains "$out" "github.com__me__app  feat/login"; contains "$out" "wired the form" "list works from anywhere"

  printf '%s\n' '- chose cookie sessions over JWT' > "$SB/d"
  awk -v l="$(cat "$SB/d")" '{ print } /^## Decisions and dead ends$/ { getline; print; print l }' "$f" > "$SB/f2" && cat "$SB/f2" > "$f"
  out=$(ax close); contains "$out" "Archived to"; contains "$out" "cookie sessions"
  no_file "$f"
  n=$(find "$(ax path --repo)/archive" -type f | wc -l | tr -d ' '); eq "$n" 1
  out=$(ax list); contains "$out" "No active efforts"

  # prune: effort for a deleted branch
  git checkout -q -b tmp-branch; ax new >/dev/null; git checkout -q main; git branch -q -D tmp-branch
  out=$(ax prune); contains "$out" "tmp-branch  (branch gone)"
  out=$(ax prune --apply); contains "$out" "archived"
  out=$(ax prune); contains "$out" "No efforts for deleted branches"

  # detached HEAD
  git checkout -q --detach
  ax new >/dev/null 2>&1; status $? 1 "detached new"
  out=$(AGENTCTX_EFFORT=spike ax new); contains "$out" "spike.md"
  git checkout -q main
  out=$(ax prune); lacks "$out" "spike" "named efforts are never pruned"

  # worktrees get their own efforts
  git worktree add -q "$SB/wt" -b feat/wt
  (cd "$SB/wt" && ax new >/dev/null)
  is_file "$SB/wt/.agentctx/feat__wt.md"
  out=$(cd / && ax list); contains "$out" "feat/wt"

  # close reports clearly when ~/.agents isn't writable (sandboxed agent)
  (cd "$SB/wt" && chmod -R a-w "$HOME/.agents/repos/github.com__me__app" 2>/dev/null
   out=$(ax close 2>&1); st=$?
   chmod -R u+w "$HOME/.agents/repos/github.com__me__app"
   if [ "$(id -u)" -ne 0 ]; then
     status $st 1 "close fails when sandboxed"; contains "$out" "Run 'agentctx close' yourself"
     is_file "$SB/wt/.agentctx/feat__wt.md"
   fi)
}

test_context() {
  t "context"; sandbox
  new_repo "$SB/r" git@github.com:me/app.git
  cd "$SB/r" || return
  out=$(ax context --for claude </dev/null); eq "$out" "" "nothing to inject"
  out=$(ax context --for copilot </dev/null); eq "$out" "" "copilot nothing"

  ax notes >/dev/null; printf 'Use pnpm, never npm.\n' >> "$(ax notes --path)"
  ax new >/dev/null
  out=$(ax context --for claude </dev/null)
  contains "$out" "Use pnpm, never npm."; contains "$out" "effort file for branch main"; contains "$out" "## Goal"

  out=$(ax context --for codex </dev/null); contains "$out" "Use pnpm"

  # stdin JSON: cwd is honoured, resume is skipped
  cd /
  out=$(printf '{"session_id":"x","cwd":"%s","source":"startup"}' "$SB/r" | ax context --for claude); contains "$out" "Use pnpm" "cwd from stdin"
  out=$(printf '{"cwd":"%s","source":"resume"}' "$SB/r" | ax context --for claude); eq "$out" "" "resume skipped"
  cd "$SB/r" || return
  out=$(printf 'not json at all' | ax context --for codex); contains "$out" "Use pnpm" "garbage stdin is ignored"
  out=$(printf '' | ax context --for copilot); contains "$out" "additionalContext" "empty stdin"
  ax context --for claude </dev/null >/dev/null 2>&1; status $? 0 "always exits 0"
  cd "$SB/r" || return

  # copilot: valid JSON with additionalContext, quotes/backslashes/tabs escaped
  printf 'Quote " back\\slash	tab\n' >> "$(ax path)"
  out=$(ax context --for copilot </dev/null)
  contains "$out" '{"additionalContext":"'
  contains "$out" 'Quote \" back\\slash\ttab'
  if command -v python3 >/dev/null 2>&1; then
    got=$(printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); print("Quote \" back\\slash\ttab" in d["additionalContext"])')
    eq "$got" "True" "copilot json parses"
  fi

  # over budget: pointer instead of content
  i=0; while [ $i -lt 400 ]; do echo "line $i of a very long effort file with lots of text" >> "$(ax path)"; i=$((i + 1)); done
  out=$(ax context --for claude </dev/null)
  contains "$out" "over the agentctx budget"; lacks "$out" "line 399"
  n=$(printf '%s' "$out" | wc -c | tr -d ' ')
  if [ "$n" -lt 10000 ]; then pass; else flunk "context must stay under Claude's 10000-char cap (got $n)"; fi

  # outside a repo: silent
  cd "$SB" || return
  out=$(ax context --for claude </dev/null); eq "$out" "" "outside repo"
}

prep_agent_dirs() { mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.copilot"; }

test_install_fresh() {
  t "install fresh"; sandbox; prep_agent_dirs; stub_claude
  out=$(ax install 2>&1); st=$?
  status $st 0 "install"
  is_file "$HOME/.agents/AGENTS.md"
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "@~/.agents/AGENTS.md"
  links_to "$HOME/.codex/AGENTS.md" "$HOME/.agents/AGENTS.md"
  links_to "$HOME/.copilot/copilot-instructions.md" "$HOME/.agents/AGENTS.md"
  links_to "$HOME/.local/bin/agentctx" "$BIN"
  links_to "$HOME/.agents/skills/effort" "$ROOT/skills/effort"
  contains "$(cat "$HOME/.codex/hooks.json")" "context --for codex"
  contains "$(cat "$HOME/.copilot/hooks/agentctx.json")" '"sessionStart"'
  calls=$(cat "$HOME/claude.calls")
  contains "$calls" "plugin marketplace add $ROOT --scope user"
  contains "$calls" "plugin install agentctx@agentctx --scope user"
  if command -v python3 >/dev/null 2>&1; then
    for j in "$HOME/.codex/hooks.json" "$HOME/.copilot/hooks/agentctx.json" "$ROOT/hooks/hooks.json" "$ROOT/.claude-plugin/plugin.json" "$ROOT/.claude-plugin/marketplace.json"; do
      if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$j"; then pass; else flunk "invalid JSON $j"; fi
    done
  fi

  # idempotent: second run changes nothing (except the stub's call log)
  before=$(tree_snapshot | grep -v claude.calls)
  ax install >/dev/null 2>&1
  after=$(tree_snapshot | grep -v claude.calls)
  eq "$after" "$before" "second install is a no-op"
  contains "$(tail -n 2 "$HOME/claude.calls")" "plugin update agentctx@agentctx" "second run updates"
  n=$(grep -c 'agentctx:begin' "$HOME/.claude/CLAUDE.md"); eq "$n" 1 "single block"

  t "appended lines survive"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  echo 'Appended rule.' >> "$HOME/.claude/CLAUDE.md"
  ax install >/dev/null 2>&1
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "Appended rule." "reinstall"
  ax uninstall >/dev/null 2>&1
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "Appended rule." "uninstall"

  t "broken block is not edited"; sandbox; prep_agent_dirs; stub_claude
  printf '<!-- agentctx:begin (x) -->\n@~/.agents/AGENTS.md\nMy rule\n' > "$HOME/.claude/CLAUDE.md"
  out=$(ax install 2>&1); st=$?
  status $st 1; contains "$out" "broken or duplicated"
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "My rule"
}

test_install_preserves_user_files() {
  t "install preserves user files"; sandbox; prep_agent_dirs; stub_claude
  printf 'Never add co-author trailers.\n' > "$HOME/.claude/CLAUDE.md"
  printf 'Codex-only rule.\n' > "$HOME/.codex/AGENTS.md"
  printf '{"hooks":{"Stop":[]}}\n' > "$HOME/.codex/hooks.json"
  out=$(ax install 2>&1)
  contains "$out" "has its own content, left untouched"
  contains "$out" "is not managed by agentctx, left untouched"
  eq "$(cat "$HOME/.codex/AGENTS.md")" "Codex-only rule." "codex file untouched"
  eq "$(cat "$HOME/.codex/hooks.json")" '{"hooks":{"Stop":[]}}' "foreign hooks.json untouched"
  lacks "$out" "\"description\": \"managed by agentctx" "snippet carries no ownership marker"
  contains "$out" "context --for codex"
  # user merges the snippet: still not ours
  printf '{"hooks":{"Stop":[],"SessionStart":[{"hooks":[{"type":"command","command":"%s context --for codex"}]}]}}\n' "'$BIN'" > "$HOME/.codex/hooks.json"
  cp "$HOME/.codex/hooks.json" "$SB/merged"
  ax install >/dev/null 2>&1
  eq "$(cat "$HOME/.codex/hooks.json")" "$(cat "$SB/merged")" "merged file never rewritten"
  c=$(cat "$HOME/.claude/CLAUDE.md")
  contains "$c" "Never add co-author trailers."; contains "$c" "@~/.agents/AGENTS.md"
  # a user's own symlink (e.g. dotfiles) is never replaced
  rm -f "$HOME/.copilot/copilot-instructions.md"; printf 'x\n' > "$SB/dotfile"; ln -s "$SB/dotfile" "$HOME/.copilot/copilot-instructions.md"
  out=$(ax install 2>&1); contains "$out" "is a link to"
  links_to "$HOME/.copilot/copilot-instructions.md" "$SB/dotfile"
  # uninstall keeps the user's own CLAUDE.md lines and drops only our block
  ax uninstall >/dev/null 2>&1
  c=$(cat "$HOME/.claude/CLAUDE.md")
  contains "$c" "Never add co-author trailers." "uninstall keeps user lines"; lacks "$c" "agentctx:begin"
  eq "$(cat "$HOME/.codex/hooks.json")" "$(cat "$SB/merged")" "merged file never deleted"
}

test_adopt() {
  t "adopt"; sandbox; prep_agent_dirs; stub_claude
  printf 'Rule A\nRule B\n' > "$HOME/.claude/CLAUDE.md"
  out=$(ax install --adopt 2>&1); status $? 0
  eq "$(cat "$HOME/.agents/AGENTS.md")" "Rule A
Rule B" "adopted content"
  lacks "$(cat "$HOME/.claude/CLAUDE.md")" "Rule A" "moved, not copied"
  if ls "$HOME"/.agents/backups/*/* >/dev/null 2>&1; then pass; else flunk "backup kept"; fi

  t "adopt refuses ambiguity"; sandbox; prep_agent_dirs; stub_claude
  printf 'Rule A\n' > "$HOME/.claude/CLAUDE.md"
  printf 'Rule C\n' > "$HOME/.codex/AGENTS.md"
  out=$(ax install --adopt 2>&1); status $? 1
  contains "$out" "more than one global file"
  no_file "$HOME/.agents/AGENTS.md"

  t "adopt moves codex file"; sandbox; mkdir -p "$HOME/.codex"
  printf 'Rule C\n' > "$HOME/.codex/AGENTS.md"
  ax install --adopt --no-claude --no-copilot >/dev/null 2>&1
  eq "$(cat "$HOME/.agents/AGENTS.md")" "Rule C"
  links_to "$HOME/.codex/AGENTS.md" "$HOME/.agents/AGENTS.md"
}

test_dry_run_and_skip() {
  t "dry run"; sandbox; prep_agent_dirs; stub_claude
  before=$(tree_snapshot | grep -v claude.calls)
  out=$(ax install --dry-run 2>&1)
  contains "$out" "Dry run"; contains "$out" "link"
  eq "$(tree_snapshot | grep -v claude.calls)" "$before" "dry run changes nothing"

  t "skip flags"; sandbox; prep_agent_dirs; stub_claude
  ax install --no-codex --no-copilot --no-skill >/dev/null 2>&1
  no_file "$HOME/.codex/AGENTS.md"; no_file "$HOME/.copilot/hooks/agentctx.json"; no_file "$HOME/.agents/skills/effort"

  t "only configures tools that exist"; sandbox
  mkdir -p "$HOME/.codex"
  out=$(ax install 2>&1)
  links_to "$HOME/.codex/AGENTS.md" "$HOME/.agents/AGENTS.md"
  no_file "$HOME/.claude/CLAUDE.md"; no_file "$HOME/.copilot"

  t "env overrides"; sandbox
  export CODEX_HOME="$SB/codexhome" COPILOT_HOME="$SB/cophome"
  mkdir -p "$CODEX_HOME" "$COPILOT_HOME"
  ax install --no-claude >/dev/null 2>&1
  links_to "$CODEX_HOME/AGENTS.md" "$HOME/.agents/AGENTS.md"
  is_file "$COPILOT_HOME/hooks/agentctx.json"
  links_to "$COPILOT_HOME/skills/effort" "$ROOT/skills/effort" "COPILOT_HOME skill link"
  unset CODEX_HOME COPILOT_HOME
}

test_uninstall() {
  t "uninstall"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  printf 'my rule\n' >> "$HOME/.agents/AGENTS.md"
  ax uninstall >/dev/null 2>&1
  no_file "$HOME/.codex/hooks.json"; no_file "$HOME/.copilot/hooks/agentctx.json"
  [ -L "$HOME/.codex/AGENTS.md" ] && flunk "codex file still a link"
  contains "$(cat "$HOME/.codex/AGENTS.md")" "my rule" "codex keeps a copy"
  contains "$(cat "$HOME/.copilot/copilot-instructions.md")" "my rule" "copilot keeps a copy"
  no_file "$HOME/.agents/skills/effort"; no_file "$HOME/.local/bin/agentctx"
  lacks "$(cat "$HOME/.claude/CLAUDE.md")" "agentctx"
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "my rule" "claude keeps a copy"
  contains "$(cat "$HOME/.agents/AGENTS.md")" "my rule" "data kept"
  calls=$(cat "$HOME/claude.calls"); contains "$calls" "plugin uninstall agentctx@agentctx"
}

test_doctor() {
  t "doctor"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  new_repo "$SB/r" git@github.com:me/app.git
  cd "$SB/r" || return

  out=$(ax doctor 2>&1); contains "$out" "Claude Code imports it"; contains "$out" "Codex reads it"
  contains "$out" "Codex hook not trusted yet"

  printf '# App\nRun `pnpm test`.\n' > AGENTS.md
  printf 'Claude bits\n' > CLAUDE.md
  out=$(ax doctor 2>&1); contains "$out" "Claude Code ignores AGENTS.md here"
  printf '@AGENTS.md\n' > CLAUDE.md
  out=$(ax doctor 2>&1); lacks "$out" "ignores AGENTS.md"; contains "$out" "only imports AGENTS.md"

  printf '@AGENTS.md\nSee @docs/missing.md and email dev@example.org and @msiric\n```\n@ignored/in/fence.md\n```\nInline `@also/ignored.md`\n' > CLAUDE.md
  out=$(ax doctor 2>&1)
  contains "$out" "'@docs/missing.md' looks like an import"
  lacks "$out" "fence.md"; lacks "$out" "also/ignored"; lacks "$out" "example.org"; lacks "$out" "'@msiric'"

  i=0; while [ $i -lt 210 ]; do echo "line $i" >> AGENTS.md; i=$((i + 1)); done
  out=$(ax doctor 2>&1); contains "$out" "AGENTS.md is 212 lines"

  awk 'BEGIN { for (i = 0; i < 700; i++) print "padding padding padding padding padding padding" }' > AGENTS.md
  out=$(ax doctor 2>&1); contains "$out" "Codex stops at 32768"
  ax doctor >/dev/null 2>&1; status $? 1 "doctor fails on problems"
  # the global file does not count toward Codex's project budget
  awk 'BEGIN { for (i = 0; i < 600; i++) print "padding padding padding padding padding padding" }' > AGENTS.md
  awk 'BEGIN { for (i = 0; i < 600; i++) print "padding padding padding padding padding padding" }' >> "$HOME/.agents/AGENTS.md"
  out=$(ax doctor 2>&1); lacks "$out" "Codex stops at 32768" "global excluded"
  printf '# Personal instructions\n' > "$HOME/.agents/AGENTS.md"

  printf 'small\n' > AGENTS.md; rm -f CLAUDE.md
  ax new >/dev/null
  awk 'BEGIN { for (i = 0; i < 300; i++) print "a long progress line that keeps going and going" }' >> "$(ax path)"
  out=$(ax doctor 2>&1); contains "$out" "agents only get a pointer"

  # notes too big are flagged too
  rm -f "$(ax path)"
  awk 'BEGIN { for (i = 0; i < 100; i++) print "a long private note line that keeps going and going" }' > "$(ax notes --path)"
  out=$(ax doctor 2>&1); contains "$out" "agents only get a pointer"
  rm -f "$(ax notes --path)"

  # .agentctx not ignored -> fail
  ax new >/dev/null; rm -f .agentctx/.gitignore
  out=$(ax doctor 2>&1); contains "$out" "not ignored by git"
  printf '*\n' > .agentctx/.gitignore

  # trust entry present -> ok
  printf '[hooks.state."file:%s/.codex/hooks.json:session_start:0:0"]\ntrusted_hash = "abc"\n' "$HOME" > "$HOME/.codex/config.toml"
  out=$(ax doctor 2>&1); contains "$out" "trust entry"

  # hook pointing at a moved clone
  sed "s#'$BIN'#'/nowhere/agentctx'#" "$HOME/.codex/hooks.json" > "$SB/h" && cat "$SB/h" > "$HOME/.codex/hooks.json"
  out=$(ax doctor 2>&1); contains "$out" "which no longer exists"

  t "doctor with spaces and parent CLAUDE.md"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  mkdir -p "$SB/my projects"; printf 'parent rules\n' > "$SB/my projects/CLAUDE.md"
  new_repo "$SB/my projects/a repo"
  cd "$SB/my projects/a repo" || return
  printf 'x\n' > AGENTS.md
  out=$(ax doctor 2>&1); st=$?
  lacks "$out" "arithmetic" "no crash"; contains "$out" "Codex project instructions: 2 of 32768"
  contains "$out" "so Claude Code ignores AGENTS.md here" "CLAUDE.md above the repo counts"
}

test_verify() {
  t "verify (stub agents)"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  printf 'my personal rule\n' >> "$HOME/.agents/AGENTS.md"
  before=$(cksum < "$HOME/.agents/AGENTS.md")
  rm -f "$SB/stubs/claude"
  stub_agent claude "$HOME/.agents/AGENTS.md" claude
  stub_agent codex "$HOME/.codex/AGENTS.md" codex
  stub_agent copilot "$HOME/.copilot/copilot-instructions.md" copilot
  out=$(ax verify 2>&1); st=$?
  status $st 0 "verify passes"; contains "$out" "Every agent sees every layer"
  eq "$(cksum < "$HOME/.agents/AGENTS.md")" "$before" "personal file restored"
  n=$(find "$HOME/.agents/repos" -name '*agentctx-verify*' | wc -l | tr -d ' '); eq "$n" 0 "verify data cleaned"

  stub_agent codex "$HOME/.codex/AGENTS.md" codex skip-effort
  out=$(ax verify --agents codex 2>&1); st=$?
  status $st 1 "verify fails when a layer is missing"; contains "$out" "/hooks"
  eq "$(cksum < "$HOME/.agents/AGENTS.md")" "$before" "restored after failure"
}

# ----------------------------------------------- real CLIs (offline only) ----

test_real_codex() {
  command -v codex >/dev/null 2>&1 || { echo "skip  real codex: not installed"; return 0; }
  cdir=$(dirname "$(command -v codex)")
  t "real codex loads personal + repo + nested instructions"; sandbox
  export PATH="$PATH:$cdir:$REAL_PATH"
  mkdir -p "$HOME/.codex"
  ax install --no-claude --no-copilot >/dev/null 2>&1
  printf 'Marker PERSONAL-OK\n' >> "$HOME/.agents/AGENTS.md"
  new_repo "$SB/r"; mkdir -p "$SB/r/pkg"
  printf 'Marker ROOT-OK\n' > "$SB/r/AGENTS.md"; printf 'Marker NESTED-OK\n' > "$SB/r/pkg/AGENTS.md"
  out=$(cd "$SB/r/pkg" && codex debug prompt-input "hi" 2>&1)
  contains "$out" "PERSONAL-OK" "global via symlink"; contains "$out" "ROOT-OK"; contains "$out" "NESTED-OK"
  lacks "$out" "failed to parse hooks config" "hooks.json parses"
}

test_real_claude() {
  command -v claude >/dev/null 2>&1 || { echo "skip  real claude: not installed"; return 0; }
  cdir=$(dirname "$(command -v claude)")
  t "real claude validates and installs the plugin"; sandbox
  export PATH="$PATH:$cdir:$REAL_PATH"
  out=$(claude plugin validate "$ROOT" 2>&1); contains "$out" "Validation passed"
  mkdir -p "$HOME/.claude"
  ax install --no-codex --no-copilot >/dev/null 2>&1
  out=$(claude plugin list 2>&1); contains "$out" "agentctx@agentctx"; contains "$out" "enabled"
  out=$(claude plugin details agentctx@agentctx 2>&1); contains "$out" "SessionStart"; contains "$out" "effort"
  ax uninstall >/dev/null 2>&1
  out=$(claude plugin list 2>&1); lacks "$out" "agentctx@agentctx" "uninstalled"
}

# --------------------------------------------------------------- run ----

for fn in test_cli_basics test_repo_key test_effort_lifecycle test_context test_install_fresh \
          test_install_preserves_user_files test_adopt test_dry_run_and_skip test_uninstall \
          test_doctor test_verify; do
  ( $fn ) > "${TMPDIR:-/tmp}/agentctx-test.$$" 2>&1
  cat "${TMPDIR:-/tmp}/agentctx-test.$$"
  # each test runs in a subshell; count results from its output
  f=$(grep -c '^FAIL' "${TMPDIR:-/tmp}/agentctx-test.$$")
  FAIL=$((FAIL + f))
  [ "$f" -eq 0 ] && printf 'ok    %s\n' "$fn"
done
if [ "${AGENTCTX_REAL:-0}" = 1 ]; then
  for fn in test_real_codex test_real_claude; do
    PATH=$REAL_PATH
    ( $fn ) > "${TMPDIR:-/tmp}/agentctx-test.$$" 2>&1
    cat "${TMPDIR:-/tmp}/agentctx-test.$$"
    f=$(grep -c '^FAIL' "${TMPDIR:-/tmp}/agentctx-test.$$")
    FAIL=$((FAIL + f))
    [ "$f" -eq 0 ] && ! grep -q '^skip' "${TMPDIR:-/tmp}/agentctx-test.$$" && printf 'ok    %s\n' "$fn"
  done
fi
rm -f "${TMPDIR:-/tmp}/agentctx-test.$$"
echo
if [ "$FAIL" -eq 0 ]; then echo "All tests passed."; else echo "$FAIL failure(s)."; exit 1; fi
