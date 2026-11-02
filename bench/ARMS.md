# Arms: exact setup

Frozen before the pilot. Competitor versions get pinned here before the dev
matrix, and each change is logged in `DEVIATIONS.md`. Each arm's script lives
in `harness/arms/<arm>.sh` and has the hooks `install`, `env`,
`before_session`, `after_session` and `snapshot`.

**Every arm:**
- a fresh home directory per episode
- git identity "Bench User"
- the repo cloned at the pinned commit, with its `origin` remote removed
- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, except in `native` and `*+native`
- Claude Code run as `claude -p --input-format stream-json --output-format stream-json --dangerously-skip-permissions --model <model> --max-turns <budget>`, one process per session, the user turns sent one at a time, then "That's all for today, thanks."

| Arm | Setup | User actions needed |
|---|---|---|
| `none` | nothing | none |
| `native` | auto memory left on, as shipped | none |
| `handoff` | `~/.claude/CLAUDE.md` (and `~/.codex/AGENTS.md`) holds one paragraph: keep `HANDOFF.md` at the repo root with state, decisions and reasons, failed approaches; read it at start; update it before finishing | none after the one-time instruction |
| `trailkeep` | `sh bin/trailkeep install --no-codex --no-copilot` from the commit under test; defaults otherwise. Effort files are not pre-created: the agent sees the hint and decides | none |
| `oracle-note` | before the last session only, `~/.claude/CLAUDE.md` = "Notes from earlier sessions on this work:" + the trap's live facts, one per line | n/a (ceiling) |
| `resume` | the last session runs with `--resume <previous session id>` (same repo only) | n/a (ceiling) |
| `filler` | `~/.claude/CLAUDE.md` = "Reference notes (from an unrelated project):" + Python's `calendar` and `colorsys` docs, cut to `FILLER_CHARS` (set per trap to trailkeep's mean injected size in the dev matrix) | n/a (control) |
| `claude-mem` | `claude plugin marketplace add thedotmack/claude-mem`, `claude plugin install claude-mem@thedotmack`; defaults; up to 3 min after each session for its summary; Claude Code's credential store written from the session token (its worker reads only that); `~/.local/bin` on `PATH` (all arms) | none |
| `basic-memory` | `pip install basic-memory`, `claude mcp add -s user basic-memory basic-memory mcp`, `bm install claude-code --yes`, then `/basic-memory:bm-setup` once per repo, the scripted user accepting every suggested default | one-time setup command |
| `hindsight` | `pip install hindsight-api` (server with embedded database and local embedding/reranker models), its `claude-code` LLM provider with the sessions' subscription token, Claude Code integration via `npx @vectorize-io/hindsight-coding-agents@0.7.0 install claude-code --server self-hosted`; one server per episode; after each session, wait for its queue to empty (up to 5 min) | none |
| `trailkeep+native` | `trailkeep`, with auto memory on | none |

Codex CLI arms come after the Claude pilot. Codex native memories are off by
default (`[features] memories = true` turns them on) and may be unavailable in
some regions.
