# trailkeep

Context for coding agents that works the same in **Claude Code**, **Codex CLI** and **GitHub Copilot CLI**. It keeps three kinds of knowledge apart: what's always true about you, what's always true about a repo, and what matters only for the branch you're on. It also keeps an append-only log of why things were decided.

It's a single POSIX shell script that needs only `git`. It never changes your repos' tracked files. In a repo with no notes, effort or log, it adds at most one hint line to a session, and none at all with `TRAILKEEP_HINT=0`.

## Install (one command, once per machine)

```sh
npm install -g trailkeep && trailkeep install
```

Or without npm:

```sh
git clone https://github.com/trailkeep/trailkeep ~/.trailkeep && ~/.trailkeep/bin/trailkeep install
```

`install` copies the tool to `~/.agents/trailkeep/` and points every hook there. After that, the npm package or the clone can move, upgrade or disappear (a Node version switch with nvm or fnm, say) without breaking any hook or Codex's trust in them.

That's the whole setup, and it covers every repo on the machine: the hooks are user-level, so there's nothing to do per repo. If you already have instructions in `~/.claude/CLAUDE.md`, install offers to share them with all three agents.

Codex needs one manual step, because trusting hooks is a security gate Codex deliberately keeps for you. Open `codex`, run `/hooks` and trust the two trailkeep hooks once. After that, `trailkeep doctor` checks the setup and `trailkeep verify` runs a live test with each agent.

Later, `trailkeep update` gets the latest version the same way you installed it (npm or git) and re-applies the setup.

## The layers

| Layer | File | Who writes it | Loaded |
|---|---|---|---|
| **Personal**: you, in every repo | `~/.agents/AGENTS.md` | you | every session, by all three agents |
| **Repo**: true for every task here | the repo's own `AGENTS.md` (committed) | you and your team | natively by all three agents |
| **Private repo notes**: things you can't commit | `~/.agents/repos/<repo>/NOTES.md` | you | at session start, by a hook |
| **Effort**: this branch's goal, plan, progress, decisions | `.trailkeep/<branch>.md` in the worktree, ignored by git | the agent | at session start and after compaction, by a hook |
| **Decision log**: why things happened, append-only | `~/.agents/repos/<repo>/log/YYYY-MM.tsv` | the session-end hook | never loaded; agents search it |

`<repo>` comes from the origin URL, so every clone and worktree of a repo shares the same notes and log.

## What happens on its own

| When | What happens automatically |
|---|---|
| Any session starts in any repo | Notes and the branch's effort file are injected. A one-line pointer mentions the decision log if it has entries. Leftovers from a session that didn't exit cleanly are logged first. |
| You're on a feature branch with no effort file | One line tells the agent it can run `trailkeep new` for multi-session work. Turn it off with `TRAILKEEP_HINT=0`. |
| The agent works | It keeps the effort file current: plan ticks, a progress line per session, decisions and dead ends. That's the effort skill's job. |
| Context gets compacted | The effort file is re-injected fresh. |
| A session ends | New Decisions and Progress lines from every effort in the worktree go into the decision log, stamped with the commit, the branch's changed files, branch and session id. It takes under 0.1 s, well inside Codex's 3-second limit for this hook. Anything a killed session missed is picked up at the next start, in the background. |
| A branch is renamed | Its effort file follows the new name. Git's reflog records renames. |
| A branch is deleted, locally and on the remote | Its last lines are logged, then its effort file is archived and the archive is logged. |

The one deliberate manual step is promoting a lasting lesson into a permanent file (`AGENTS.md`, notes, personal). The agent proposes it at close, and you approve. Permanent files that agents edit without review drift and bloat. That's the failure this design exists to avoid.

## The decision log

Git already records what changed, when and where, and each agent keeps its own transcripts. The log adds the missing part, **why**, with pointers to both. It's write-everything, read-narrowly, because unfiltered history in context hurts more than it helps ([SWE Context Bench](https://arxiv.org/abs/2602.08316)), while a plain chronological log works well ([DreamBench-SWE](https://arxiv.org/abs/2608.20664)).

```sh
trailkeep log --path src/auth          # entries whose changed files include src/auth
trailkeep log --grep jwt --type dead-end --since 2026-10-01
trailkeep log show 73a8b76             # one entry in full: commit, files, session, transcript
git show <commit>                     # then the actual change
```

Results are one short line each, newest first, at most 20 by default. Agents learn this from the effort skill and the one-line pointer, and they never write the log directly. Writes happen in hooks, which run outside the agent's sandbox.

The format is one event per line, tab-separated, one file per month: `id time type branch commit paths text session transcript`. It needs no parser or database, `grep` works on it, and appends never rewrite history. In the effort file, start a line with `Dead end:` to log it as a failed approach.

## Across repos, sessions and machines

- **Repos:** nothing to set up per repo. An agent in a repo you've never touched just gets your personal file plus that repo's `AGENTS.md`.
- **Sessions and agents:** state lives in files, not chats. End a session in Claude and continue in Codex, and the effort file and log carry over.
- **Worktrees:** each one has its own `.trailkeep/`, so parallel agents on different branches never share task state. Notes and the log are shared per repo.
- **Machines:** `~/.agents` is local. To sync it, put it in a private git repo (it's plain text). Effort files travel with the worktree; the log and notes stay with `~/.agents`.

## Daily commands

```sh
trailkeep new        # start an effort for this branch (or ask the agent to)
trailkeep show       # exactly what agents get here at session start
trailkeep list       # active efforts across all repos, with their last progress line
trailkeep close      # archive the effort; lists decisions worth promoting
trailkeep notes      # private notes for this repo
trailkeep log ...    # search the decision log
trailkeep doctor     # check setup and this repo's instruction files
```

## Why it's built this way

Every rule below comes from vendor documentation, the CLIs' source code or published evaluations. None of it is taste.

- **Global files stay short and hold only what code can't tell an agent.** In a controlled study, context files didn't improve task success but raised cost by over 20% ([ICLR 2026](https://arxiv.org/abs/2602.11988)). Anthropic says to keep CLAUDE.md under 200 lines ([memory](https://code.claude.com/docs/en/memory)), and `doctor` flags files over 200 lines.
- **Task state lives in a file, not in the chat.** Anthropic's long-running harness and OpenAI's ExecPlans both rebuild state from a file at the start of every session ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [OpenAI](https://developers.openai.com/cookbook/articles/codex_exec_plans)).
- **Effort files live in the worktree** because that's the only place every agent can write without prompting. Codex also keeps `.git/`, `.agents/` and `.codex/` read-only inside the workspace (codex source, `PROTECTED_METADATA_PATH_NAMES`). `.trailkeep/` ignores itself with a one-line `.gitignore`. `git clean -fdx` deletes it.
- **Output fits each tool's limits.** Claude caps hook text at 10,000 characters ([hooks](https://code.claude.com/docs/en/hooks)), and Codex spills hook text over about 2,500 tokens to a file. trailkeep stays under 9,000 characters. A file larger than that is replaced with its path, never silently truncated.
- **AGENTS.md is the one repo file.** Claude Code reads it natively from v2.1.277, but only when no CLAUDE.md exists. `doctor` warns when a CLAUDE.md hides it. Codex stops at 32 KiB of project instructions (`project_doc_max_bytes`), and `doctor` adds up the files for your current directory.
- **Copilot is handled differently.** It needs JSON from hooks and ignores `~/` imports ([hooks](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference), [instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)), so it gets a symlink and JSON output.
- **There's no vector database, MCP server or generated AGENTS.md.** A plain log did about as well as a memory product, MCP tool definitions cost context in every session ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)), and LLM-generated context files slightly lowered success.

## What `install` changes

Files it edits are backed up to `~/.agents/backups/` first.

- `~/.claude/CLAUDE.md` gets a 3-line block importing `~/.agents/AGENTS.md`; your own lines stay. HTML comments are stripped by Claude, so the markers cost nothing.
- `~/.codex/AGENTS.md` and `~/.copilot/copilot-instructions.md` become symlinks to `~/.agents/AGENTS.md`. Existing files with content are left alone, with a warning.
- Hooks go in through a Claude Code plugin (installed from the clone), `~/.codex/hooks.json` and `~/.copilot/hooks/trailkeep.json`. Hook files it didn't create are never edited; it prints what to add instead.
- The `effort` skill is linked into `~/.agents/skills/`, which Codex and Copilot read. Claude Code gets it from the plugin, at about 60 always-on tokens.
- A copy of the tool goes to `~/.agents/trailkeep/`, and `trailkeep` is linked into `~/.local/bin`.

`trailkeep uninstall` removes all of that. It leaves each agent a plain copy of your personal instructions, and keeps `~/.agents` and any `.trailkeep/` folders.

## What's tested

`sh tests/run.sh` runs every test in a throwaway `$HOME`. It covers:
- install, re-install as a no-op, adopt, dry run, update and uninstall
- a real `npm pack` and global install, including hooks still working after the npm copy is deleted
- preservation of your files
- repo keys and worktrees
- the effort lifecycle, auto-archive and context output for each agent
- the decision log: harvesting, dedupe, filters, show, malformed text, and recovery from killed sessions
- every doctor check, and verify

`TRAILKEEP_REAL=1` also checks the real CLIs offline. Codex's own prompt renderer must show the personal and nested files, and must parse the hooks file. Claude Code must validate, install and remove the plugin.

CI runs the suite on Linux and macOS, under dash and `bash --posix`. A weekly job runs against the latest CLIs to catch upstream changes.

Last verified with Claude Code 2.1.316, Codex CLI 0.166.0 and Copilot CLI 1.0.105.

Live-session behavior can't be tested offline: hooks running, the Claude import being followed, Copilot reading the symlink. `trailkeep verify` checks it on your machine. It plants a random marker in each layer and a decision in an effort file, asks each agent what it sees, and checks the decision reached the log. Then it restores everything. If Copilot misses your personal file, set `COPILOT_CUSTOM_INSTRUCTIONS_DIRS=~/.agents`.

## Environment

- `TRAILKEEP_HOME` (default `~/.agents`)
- `TRAILKEEP_MAX_CHARS` (default 9000, max 9500)
- `TRAILKEEP_HINT=0` (no hint on branches without an effort file)
- `TRAILKEEP_EFFORT` (use a named effort instead of the branch)

It also honours `CLAUDE_CONFIG_DIR`, `CODEX_HOME` and `COPILOT_HOME`. It works on Linux and macOS; on Windows, use WSL.

## Releasing (maintainers)

```sh
sh scripts/release 0.3.0
```

The script bumps the version in all three places, runs the tests, commits, tags and pushes. The tag triggers the release workflow, which checks that the versions match, runs the tests again, publishes to npm and creates the GitHub release. No machine but GitHub's talks to npm.

npm authentication works one of two ways:
- **Trusted publishing (preferred):** on npmjs.com, open the package's Settings, then Trusted Publisher, then GitHub Actions. Enter owner `msiric`, repository `trailkeep`, workflow `release.yml`. No secret is needed. npm only offers this for packages that already exist.
- **An `NPM_TOKEN` repository secret,** for the first release only: a granular token with read-and-write access to packages and a short expiry. Delete it once trusted publishing is set up.
