#!/bin/sh
# trailkeep test suite. POSIX sh, no deps beyond git. Every test runs with a
# throwaway $HOME, so it never touches your real setup.
#
#   sh tests/run.sh            unit + integration tests (stubs for the agents)
#   TRAILKEEP_REAL=1 sh tests/run.sh
#                              also run against the real claude / codex CLIs
#                              if installed (offline: no model calls)

set -u
HERE=$(cd "$(dirname "$0")" && pwd -P)
ROOT=$(cd "$HERE/.." && pwd -P)
BIN=$ROOT/bin/trailkeep
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
  SB=$(cd "$(mktemp -d)" && pwd -P)   # macOS: /var is a symlink to /private/var
  export HOME="$SB/home"
  mkdir -p "$HOME" "$SB/stubs" "$HOME/.local/bin"
  unset TRAILKEEP_HOME CODEX_HOME COPILOT_HOME CLAUDE_CONFIG_DIR TRAILKEEP_EFFORT TRAILKEEP_MAX_CHARS CLAUDECODE
  export TRAILKEEP_SYNC=1   # run the background startup harvest in the foreground
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

ax() { ${TRAILKEEP_TEST_SHELL:-} "$BIN" "$@"; }

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
  "plugin list") [ -f "$HOME/.stub-installed" ] && echo "trailkeep@trailkeep" ;;
  "plugin marketplace")
    case $3 in
      list) [ -f "$HOME/.stub-mkt" ] && echo "trailkeep" ;;
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
  if [ "${4:-}" != skip-effort ]; then echo '{"cwd":"'"\$PWD"'"}' | "$BIN" harvest --for $3; fi
} | grep -o 'ACX-[A-Z0-9]*' | tr '\n' ' '
echo
EOF
  chmod +x "$SB/stubs/$1"
}

# ------------------------------------------------------------- tests ----

test_cli_basics() {
  t "cli basics"; sandbox
  out=$(ax --version); contains "$out" "trailkeep 0."
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
  eq "$f" "$SB/r/.trailkeep/feat__login.md" "lives in the worktree"
  contains "$(cat "$f")" "Branch: feat/login · Repo: github.com__me__app · Kind: branch"
  eq "$(git status --porcelain)" "" "git status stays clean"
  eq "$(git status --porcelain --ignored | grep -c trailkeep)" "1" "folder is ignored"
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
  out=$(TRAILKEEP_EFFORT=spike ax new); contains "$out" "spike.md"
  git checkout -q main
  out=$(ax prune); lacks "$out" "spike" "named efforts are never pruned"

  # worktrees get their own efforts
  git worktree add -q "$SB/wt" -b feat/wt
  (cd "$SB/wt" && ax new >/dev/null)
  is_file "$SB/wt/.trailkeep/feat__wt.md"
  out=$(cd / && ax list); contains "$out" "feat/wt"

  # close reports clearly when ~/.agents isn't writable (sandboxed agent)
  (cd "$SB/wt" && chmod -R a-w "$HOME/.agents/repos/github.com__me__app" 2>/dev/null
   out=$(ax close 2>&1); st=$?
   chmod -R u+w "$HOME/.agents/repos/github.com__me__app"
   if [ "$(id -u)" -ne 0 ]; then
     status $st 1 "close fails when sandboxed"; contains "$out" "Run 'trailkeep close' yourself"
     is_file "$SB/wt/.trailkeep/feat__wt.md"
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
  contains "$out" "over the trailkeep budget"; lacks "$out" "line 399"
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
  links_to "$HOME/.local/bin/trailkeep" "$HOME/.agents/trailkeep/bin/trailkeep"
  links_to "$HOME/.agents/skills/effort" "$HOME/.agents/trailkeep/skills/effort"
  is_file "$HOME/.agents/trailkeep/bin/trailkeep"; is_file "$HOME/.agents/trailkeep/.claude-plugin/plugin.json"
  contains "$(cat "$HOME/.agents/trailkeep/.trailkeep-runtime")" "source=git"
  contains "$(cat "$HOME/.codex/hooks.json")" "'$HOME/.agents/trailkeep/bin/trailkeep' context" "hooks use the stable runtime path"
  [ -d "$HOME/.agents/trailkeep/tests" ] && flunk "runtime should not carry tests"
  contains "$(cat "$HOME/.codex/hooks.json")" "context --for codex"
  contains "$(cat "$HOME/.copilot/hooks/trailkeep.json")" '"sessionStart"'
  contains "$(cat "$HOME/.copilot/hooks/trailkeep.json")" '"sessionEnd"'
  contains "$(cat "$HOME/.codex/hooks.json")" "harvest --for codex"
  calls=$(cat "$HOME/claude.calls")
  contains "$calls" "plugin marketplace add $HOME/.agents/trailkeep --scope user"
  contains "$calls" "plugin install trailkeep@trailkeep --scope user"
  if command -v python3 >/dev/null 2>&1; then
    for j in "$HOME/.codex/hooks.json" "$HOME/.copilot/hooks/trailkeep.json" "$ROOT/hooks/hooks.json" "$ROOT/.claude-plugin/plugin.json" "$ROOT/.claude-plugin/marketplace.json"; do
      if python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$j"; then pass; else flunk "invalid JSON $j"; fi
    done
  fi

  # idempotent: second run changes nothing (except the stub's call log)
  before=$(tree_snapshot | grep -v claude.calls)
  ax install >/dev/null 2>&1
  after=$(tree_snapshot | grep -v claude.calls)
  eq "$after" "$before" "second install is a no-op"
  contains "$(tail -n 2 "$HOME/claude.calls")" "plugin update trailkeep@trailkeep" "second run updates"
  n=$(grep -c 'trailkeep:begin' "$HOME/.claude/CLAUDE.md"); eq "$n" 1 "single block"

  t "appended lines survive"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  echo 'Appended rule.' >> "$HOME/.claude/CLAUDE.md"
  ax install >/dev/null 2>&1
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "Appended rule." "reinstall"
  ax uninstall >/dev/null 2>&1
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "Appended rule." "uninstall"

  t "broken block is not edited"; sandbox; prep_agent_dirs; stub_claude
  printf '<!-- trailkeep:begin (x) -->\n@~/.agents/AGENTS.md\nMy rule\n' > "$HOME/.claude/CLAUDE.md"
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
  contains "$out" "is not managed by trailkeep, left untouched"
  eq "$(cat "$HOME/.codex/AGENTS.md")" "Codex-only rule." "codex file untouched"
  eq "$(cat "$HOME/.codex/hooks.json")" '{"hooks":{"Stop":[]}}' "foreign hooks.json untouched"
  lacks "$out" "\"description\": \"managed by trailkeep" "snippet carries no ownership marker"
  contains "$out" "context --for codex"
  # user merges the snippet: still not ours
  printf '{"hooks":{"Stop":[],"SessionStart":[{"hooks":[{"type":"command","command":"%s context --for codex"}]}]}}\n' "'$HOME/.agents/trailkeep/bin/trailkeep'" > "$HOME/.codex/hooks.json"
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
  contains "$c" "Never add co-author trailers." "uninstall keeps user lines"; lacks "$c" "trailkeep:begin"
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
  no_file "$HOME/.codex/AGENTS.md"; no_file "$HOME/.copilot/hooks/trailkeep.json"; no_file "$HOME/.agents/skills/effort"

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
  is_file "$COPILOT_HOME/hooks/trailkeep.json"
  links_to "$COPILOT_HOME/skills/effort" "$HOME/.agents/trailkeep/skills/effort" "COPILOT_HOME skill link"
  unset CODEX_HOME COPILOT_HOME
}

test_uninstall() {
  t "uninstall"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  printf 'my rule\n' >> "$HOME/.agents/AGENTS.md"
  ax uninstall >/dev/null 2>&1
  no_file "$HOME/.codex/hooks.json"; no_file "$HOME/.copilot/hooks/trailkeep.json"
  [ -L "$HOME/.codex/AGENTS.md" ] && flunk "codex file still a link"
  contains "$(cat "$HOME/.codex/AGENTS.md")" "my rule" "codex keeps a copy"
  contains "$(cat "$HOME/.copilot/copilot-instructions.md")" "my rule" "copilot keeps a copy"
  no_file "$HOME/.agents/skills/effort"; no_file "$HOME/.local/bin/trailkeep"; no_file "$HOME/.agents/trailkeep"
  lacks "$(cat "$HOME/.claude/CLAUDE.md")" "trailkeep"
  contains "$(cat "$HOME/.claude/CLAUDE.md")" "my rule" "claude keeps a copy"
  contains "$(cat "$HOME/.agents/AGENTS.md")" "my rule" "data kept"
  calls=$(cat "$HOME/claude.calls"); contains "$calls" "plugin uninstall trailkeep@trailkeep"
}

test_doctor() {
  t "doctor"; sandbox; prep_agent_dirs; stub_claude
  ax install >/dev/null 2>&1
  new_repo "$SB/r" git@github.com:me/app.git
  cd "$SB/r" || return

  out=$(ax doctor 2>&1); contains "$out" "Claude Code imports it"; contains "$out" "Codex reads it"
  contains "$out" "Codex hooks not trusted yet"

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

  # .trailkeep not ignored -> fail
  ax new >/dev/null; rm -f .trailkeep/.gitignore
  out=$(ax doctor 2>&1); contains "$out" "not ignored by git"
  printf '*\n' > .trailkeep/.gitignore

  # trust entry present -> ok
  printf '[hooks.state."file:%s/.codex/hooks.json:session_start:0:0"]\ntrusted_hash = "abc"\n[hooks.state."file:%s/.codex/hooks.json:session_end:0:0"]\ntrusted_hash = "def"\n' "$HOME" "$HOME" > "$HOME/.codex/config.toml"
  out=$(ax doctor 2>&1); contains "$out" "trust entry"

  # hook pointing at a moved clone
  sed "s#'$HOME/.agents/trailkeep/bin/trailkeep'#'/nowhere/trailkeep'#" "$HOME/.codex/hooks.json" > "$SB/h" && cat "$SB/h" > "$HOME/.codex/hooks.json"
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
  n=$(find "$HOME/.agents/repos" -name '*trailkeep-verify*' | wc -l | tr -d ' '); eq "$n" 0 "verify data cleaned"

  stub_agent codex "$HOME/.codex/AGENTS.md" codex skip-effort
  out=$(ax verify --agents codex 2>&1); st=$?
  status $st 1 "verify fails when a layer is missing"; contains "$out" "/hooks"
  eq "$(cksum < "$HOME/.agents/AGENTS.md")" "$before" "restored after failure"
}

add_line() { # add_line FILE "## Section" LINE  (insert right after the heading's blank line)
  awk -v h="$2" -v l="$3" '{ print } $0 == h { getline; print; print "- " l }' "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

hook_json() { printf '{"session_id":"%s","transcript_path":"/tmp/%s.jsonl","cwd":"%s","source":"startup"}' "$1" "$1" "$PWD"; }

test_log() {
  t "decision log"; sandbox
  new_repo "$SB/r" git@github.com:me/app.git
  cd "$SB/r" || return
  echo a > a.ts; git add a.ts; git commit -qm a
  git checkout -q -b feat/auth
  out=$(hook_json s0 | ax context --for claude); contains "$out" "no effort file for branch feat/auth" "hint on feature branch"
  out=$(TRAILKEEP_HINT=0 ax context --for claude </dev/null); eq "$out" "" "hint can be turned off"
  git checkout -q main
  out=$(hook_json s0 | ax context --for claude); eq "$out" "" "no hint on default branch"
  git checkout -q feat/auth

  ax new >/dev/null; f=$(ax path)
  add_line "$f" "## Decisions and dead ends" "Chose cookie sessions over JWT: need server-side revoke"
  add_line "$f" "## Decisions and dead ends" "Dead end: edge middleware can't read httpOnly cookies"
  add_line "$f" "## Progress" "2026-11-01: login form done"
  mkdir -p src/auth; echo x > src/auth/session.ts; git add src; git commit -qm auth
  hook_json s1 | ax harvest --for claude; status $? 0 "harvest exits 0"
  hook_json s2 | ax harvest --for codex
  out=$(ax log); n=$(printf '%s\n' "$out" | wc -l | tr -d ' ')
  eq "$n" 3 "each line logged once"
  contains "$out" "decision  feat/auth"; contains "$out" "dead-end  feat/auth"; contains "$out" "progress"
  out=$(ax log --path src/auth --type dead-end); contains "$out" "edge middleware" "path + type filter"
  out=$(ax log --path src/auth/session.ts); contains "$out" "cookie sessions" "file under a logged path"
  out=$(ax log --grep JWT); contains "$out" "cookie sessions" "case-insensitive grep"
  out=$(ax log --grep nothing-like-this); contains "$out" "No matching"
  out=$(ax log -n 1); n=$(printf '%s\n' "$out" | wc -l | tr -d ' '); eq "$n" 1 "limit"
  id=$(ax log --type decision | cut -d' ' -f1)
  out=$(ax log show "$id"); contains "$out" "session:    claude:s1"; contains "$out" "transcript: /tmp/s1.jsonl"
  contains "$out" "paths:      src/auth/session.ts"; contains "$out" "git show"
  ax log show zzzzzz >/dev/null 2>&1; status $? 1 "unknown id"

  # tabs/newlines in text can't break the format
  add_line "$f" "## Decisions and dead ends" "tab	inside"
  hook_json s3 | ax harvest --for copilot
  bad=$(cat "$HOME"/.agents/repos/*/log/*.tsv | awk -F '\t' 'NF != 9' | wc -l | tr -d ' ')
  eq "$bad" 0 "every row has 9 fields"

  # session start mentions the log, and harvests leftovers from a killed session
  add_line "$f" "## Progress" "2026-11-02: left without a clean exit"
  out=$(hook_json s4 | ax context --for claude)
  contains "$out" "decision log (4 entries)"
  contains "$(ax log)" "left without a clean exit" "startup harvest"
  id=$(ax log --grep "clean exit" | cut -d' ' -f1)
  contains "$(ax log show "$id")" "session:    claude:s0" "recovered line credited to the last session started here"

  # concurrent harvests never duplicate
  i=0; while [ $i -lt 40 ]; do add_line "$f" "## Progress" "parallel line $i"; i=$((i + 1)); done
  hook_json p1 | ax harvest --for claude & hook_json p2 | ax harvest --for codex & hook_json p3 | ax harvest --for copilot & wait
  n=$(ax log --grep "parallel line" -n 500 | wc -l | tr -d ' '); eq "$n" 40 "no duplicates under concurrency"

  # path matching: exact file or directory, never a name prefix; relative paths work
  out=$(ax log --path src/au); contains "$out" "No matching" "prefix of a name doesn't match"
  out=$(ax log --path ./src/auth/); contains "$out" "cookie sessions" "./ and trailing slash"
  out=$(cd src && ax log --path auth/session.ts); contains "$out" "cookie sessions" "relative to subdirectory"
  ax log --grep >/dev/null 2>&1; status $? 1 "missing value is an error, not a loop"

  # manual add
  ax log add note "remember the staging flag" >/dev/null
  contains "$(ax log -n 1)" "remember the staging flag"

  # a decision written just before the branch is deleted still gets logged
  git checkout -q -b feat/late; ax new >/dev/null
  add_line "$(ax path)" "## Decisions and dead ends" "late decision before delete"
  git checkout -q main; git branch -q -D feat/late
  hook_json s9 | ax harvest --for claude
  contains "$(ax log --grep 'late decision')" "late decision" "harvested before archiving"
  git checkout -q feat/auth

  # renamed branch: the effort follows it
  git checkout -q -b feat/old; ax new >/dev/null
  add_line "$(ax path)" "## Decisions and dead ends" "rename-me decision"
  git branch -m feat/old feat/new
  hook_json s10 | ax context --for claude >/dev/null
  is_file "$SB/r/.trailkeep/feat__new.md"; no_file "$SB/r/.trailkeep/feat__old.md"
  contains "$(cat "$SB/r/.trailkeep/feat__new.md")" "Branch: feat/new" "header updated"
  out=$(hook_json s11 | ax context --for claude); contains "$out" "effort file for branch feat/new"
  git checkout -q feat/auth

  # close logs, deleted branches auto-archive
  out=$(ax close); contains "$(ax log -n 1)" "effort closed"
  git checkout -q -b feat/tmp; ax new >/dev/null; git checkout -q main; git branch -q -D feat/tmp
  hook_json s5 | ax context --for claude >/dev/null
  no_file "$SB/r/.trailkeep/feat__tmp.md"
  contains "$(ax log -n 1)" "auto-archived" "auto-archive on session start"

  # a brand-new repo's first branch has no commits yet: its effort must survive
  mkdir -p "$SB/fresh" && (cd "$SB/fresh" && git init -q && git symbolic-ref HEAD refs/heads/start)
  cd "$SB/fresh" || return
  ax new >/dev/null
  out=$(hook_json s6 | ax context --for claude)
  contains "$out" "effort file for branch start" "unborn branch keeps its effort"
  is_file "$SB/fresh/.trailkeep/start.md"
}

test_update() {
  t "update"; sandbox; mkdir -p "$HOME/.codex"
  # snapshot the working tree as a repo, so update pulls exactly what is being tested
  cp -R "$ROOT" "$SB/src" && rm -rf "$SB/src/.git"
  (cd "$SB/src" && git init -q && git add -A && git commit -qm snapshot) || { flunk "snapshot"; return; }
  git clone -q "$SB/src" "$SB/clone" 2>/dev/null || { flunk "clone"; return; }
  out=$("$SB/clone/bin/trailkeep" update --no-claude --no-copilot 2>&1); st=$?
  status $st 0 "update"; contains "$out" "Updating"; contains "$out" "install"
  links_to "$HOME/.codex/AGENTS.md" "$HOME/.agents/AGENTS.md"
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
  out=$(claude plugin list 2>&1); contains "$out" "trailkeep@trailkeep"; contains "$out" "enabled"
  out=$(claude plugin details trailkeep@trailkeep 2>&1); contains "$out" "SessionStart"; contains "$out" "effort"
  ax uninstall >/dev/null 2>&1
  out=$(claude plugin list 2>&1); lacks "$out" "trailkeep@trailkeep" "uninstalled"
}

test_npm_package() {
  command -v npm >/dev/null 2>&1 || { echo "skip  npm package: npm not installed"; return 0; }
  ndir=$(dirname "$(command -v npm)")
  t "npm package installs and sets up from a global install"; sandbox
  export PATH="$PATH:$ndir"
  export npm_config_cache="$SB/npm-cache" npm_config_update_notifier=false
  (cd "$ROOT" && npm pack --silent --pack-destination "$SB" >/dev/null 2>&1) || { flunk "npm pack"; return; }
  tgz=$(ls "$SB"/trailkeep-*.tgz)
  list=$(tar -tzf "$tgz")
  contains "$list" "package/bin/trailkeep"; contains "$list" "package/hooks/hooks.json"; contains "$list" "package/.claude-plugin/plugin.json"
  lacks "$list" "tests/" "tests are not shipped"
  npm install -g --silent --prefix "$SB/npm" "$tgz" >/dev/null 2>&1 || { flunk "npm install -g"; return; }
  pkg=$(sed -n 's/^PKG="\(.*\)"$/\1/p' "$ROOT/bin/trailkeep")
  if [ -x "$SB/npm/lib/node_modules/$pkg/bin/trailkeep" ]; then pass; else flunk "not installed under node_modules/$pkg (update would miss it)"; fi
  mkdir -p "$HOME/.codex"
  out=$("$SB/npm/bin/trailkeep" install --no-claude --no-copilot 2>&1); st=$?
  status $st 0 "install from npm"
  contains "$(cat "$HOME/.agents/trailkeep/.trailkeep-runtime")" "source=npm"
  contains "$(cat "$HOME/.codex/hooks.json")" "'$HOME/.agents/trailkeep/bin/trailkeep'"
  # the npm copy can disappear (Node upgrade, uninstall): hooks keep working
  rm -rf "$SB/npm"
  new_repo "$SB/r"; cd "$SB/r" || return
  "$HOME/.agents/trailkeep/bin/trailkeep" notes >/dev/null; printf 'still here\n' >> "$("$HOME/.agents/trailkeep/bin/trailkeep" notes --path)"
  out=$(printf '{"cwd":"%s","source":"startup"}' "$SB/r" | "$HOME/.agents/trailkeep/bin/trailkeep" context --for codex)
  contains "$out" "still here" "runtime survives the npm copy going away"
}

test_release() {
  t "versions and release script"; sandbox
  out=$(sh "$ROOT/scripts/check-version" 2>&1); status $? 0 "all version fields agree"
  cp -R "$ROOT" "$SB/nm" && sed -i.bak 's/^PKG=".*"$/PKG="@someone\/else"/' "$SB/nm/bin/trailkeep"
  out=$(sh "$SB/nm/scripts/check-version" 2>&1); status $? 1 "package name mismatch fails"; contains "$out" "package name mismatch"
  eq "$(ax --version)" "trailkeep $(sed -n 's/^  "version": "\(.*\)",$/\1/p' "$ROOT/package.json")" "cli matches package.json"
  cp -R "$ROOT" "$SB/rel" && rm -rf "$SB/rel/.git"
  (cd "$SB/rel" && git init -q -b main && git add -A && git commit -qm base) || { flunk "snapshot"; return; }
  printf 'dirty\n' >> "$SB/rel/README.md"
  out=$(cd "$SB/rel" && sh scripts/release 9.8.7 --no-push 2>&1); status $? 1 "refuses a dirty tree"
  (cd "$SB/rel" && git checkout -q README.md)
  out=$(cd "$SB/rel" && TRAILKEEP_RELEASE_SKIP_TESTS=1 sh scripts/release 9.8.7 --no-push 2>&1); st=$?
  status $st 0 "release"; contains "$out" "Tagged v9.8.7"
  eq "$("$SB/rel/bin/trailkeep" --version)" "trailkeep 9.8.7"
  contains "$(cat "$SB/rel/package.json")" '"version": "9.8.7"'; contains "$(cat "$SB/rel/.claude-plugin/plugin.json")" '"version": "9.8.7"'
  eq "$(cd "$SB/rel" && git tag)" "v9.8.7"; eq "$(cd "$SB/rel" && git log -1 --format=%s)" "Release v9.8.7"
  out=$(cd "$SB/rel" && TRAILKEEP_RELEASE_SKIP_TESTS=1 sh scripts/release 9.8.7 --no-push 2>&1); status $? 1 "refuses an existing tag"
  out=$(cd "$SB/rel" && sh scripts/release banana 2>&1); status $? 2 "rejects a bad version"
  # patch/minor/major bump from the current version
  for kind in patch minor major; do
    cp -R "$ROOT" "$SB/bump-$kind" && rm -rf "$SB/bump-$kind/.git"
    sed 's/^VERSION=".*"$/VERSION="1.4.2"/' "$ROOT/bin/trailkeep" > "$SB/bump-$kind/bin/trailkeep"
    (cd "$SB/bump-$kind" && git init -q -b main && git add -A && git commit -qm base)
    (cd "$SB/bump-$kind" && TRAILKEEP_RELEASE_SKIP_TESTS=1 sh scripts/release "$kind" --no-push >/dev/null 2>&1)
    case $kind in patch) want=1.4.3 ;; minor) want=1.5.0 ;; major) want=2.0.0 ;; esac
    eq "$("$SB/bump-$kind/bin/trailkeep" --version)" "trailkeep $want" "release $kind"
    eq "$(cd "$SB/bump-$kind" && git tag)" "v$want" "release $kind tag"
  done
  # releasing the version already in the files (the first release) tags without an empty commit
  cp -R "$ROOT" "$SB/rel2" && rm -rf "$SB/rel2/.git"
  (cd "$SB/rel2" && git init -q -b main && git add -A && git commit -qm base)
  cur=$("$SB/rel2/bin/trailkeep" --version | cut -d' ' -f2)
  out=$(cd "$SB/rel2" && TRAILKEEP_RELEASE_SKIP_TESTS=1 sh scripts/release "$cur" --no-push 2>&1); status $? 0 "release the current version"
  eq "$(cd "$SB/rel2" && git rev-list --count HEAD)" "1" "no empty commit"; eq "$(cd "$SB/rel2" && git tag)" "v$cur"
}

# --------------------------------------------------------------- run ----

for fn in test_cli_basics test_repo_key test_effort_lifecycle test_context test_install_fresh \
          test_install_preserves_user_files test_adopt test_dry_run_and_skip test_uninstall \
          test_doctor test_verify test_log test_update test_npm_package test_release; do
  ( $fn ) > "${TMPDIR:-/tmp}/trailkeep-test.$$" 2>&1
  cat "${TMPDIR:-/tmp}/trailkeep-test.$$"
  # each test runs in a subshell; count results from its output
  f=$(grep -c '^FAIL' "${TMPDIR:-/tmp}/trailkeep-test.$$")
  FAIL=$((FAIL + f))
  [ "$f" -eq 0 ] && printf 'ok    %s\n' "$fn"
done
if [ "${TRAILKEEP_REAL:-0}" = 1 ]; then
  for fn in test_real_codex test_real_claude; do
    PATH=$REAL_PATH
    ( $fn ) > "${TMPDIR:-/tmp}/trailkeep-test.$$" 2>&1
    cat "${TMPDIR:-/tmp}/trailkeep-test.$$"
    f=$(grep -c '^FAIL' "${TMPDIR:-/tmp}/trailkeep-test.$$")
    FAIL=$((FAIL + f))
    [ "$f" -eq 0 ] && ! grep -q '^skip' "${TMPDIR:-/tmp}/trailkeep-test.$$" && printf 'ok    %s\n' "$fn"
  done
fi
rm -f "${TMPDIR:-/tmp}/trailkeep-test.$$"
echo
if [ "$FAIL" -eq 0 ]; then echo "All tests passed."; else echo "$FAIL failure(s)."; exit 1; fi
