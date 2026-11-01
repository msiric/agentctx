# agentctx

Context for coding agents in three layers: what's always true about you, what's always true about a repo, and what matters only for the branch you're on. It works the same in **Claude Code**, **Codex CLI** and **GitHub Copilot CLI**.

It's a single POSIX shell script that needs only `git`. It never changes your repos' tracked files, and it adds nothing to a session that has nothing to add.

## The three layers

| Layer | File | Who writes it | Loaded |
|---|---|---|---|
| **Personal**: you, in every repo | `~/.agents/AGENTS.md` | you | every session, by all three agents |
| **Repo**: true for every task here | the repo's own `AGENTS.md` (committed) | you and your team | natively by all three agents |
| **Private repo notes**: things you can't commit | `~/.agents/repos/<repo>/NOTES.md` | you | at session start, by a hook |
| **Effort**: this branch's goal, plan, progress, decisions | `.agentctx/<branch>.md` in the worktree, ignored by git | the agent, reviewed by you | at session start and after compaction, by a hook |

`<repo>` comes from the origin URL, so every clone and worktree of a repo shares the same private notes.

Effort files live inside the worktree because that's the only place every agent can write without asking. Codex's sandbox and Claude Code's and Copilot's permission rules block or prompt on edits outside the working folder, and Codex keeps `.git/`, `.agents/` and `.codex/` read-only even inside it (codex source, `PROTECTED_METADATA_PATH_NAMES`). `.agentctx/` contains a `.gitignore` with just `*`, so git ignores it and no repo file changes. Each worktree gets its own efforts. `close` copies finished ones to `~/.agents/repos/<repo>/archive/`, so they outlive the worktree. One caveat: `git clean -fdx` deletes `.agentctx/`.

## Install

```sh
git clone https://github.com/msiric/agentctx ~/src/agentctx
~/src/agentctx/bin/agentctx install --dry-run   # see what it would change
~/src/agentctx/bin/agentctx install             # do it (add --adopt to move an existing ~/.claude/CLAUDE.md into the shared file)
agentctx doctor                                 # check the setup
agentctx verify                                 # live test: asks each agent what it can see
```

Codex only runs hooks you've trusted. After installing, open `codex`, run `/hooks` and trust the agentctx hook once.

What `install` changes. Files it edits are backed up to `~/.agents/backups/` first:

- `~/.claude/CLAUDE.md` gets a 3-line block that imports `~/.agents/AGENTS.md`. Your own lines stay.
- `~/.codex/AGENTS.md` and `~/.copilot/copilot-instructions.md` become symlinks to `~/.agents/AGENTS.md`. Existing files with content are left alone, with a warning.
- The session-start hook goes in as a Claude Code plugin (installed from this folder), `~/.codex/hooks.json` and `~/.copilot/hooks/agentctx.json`. Existing hook files it didn't create are never edited; it prints the snippet to add instead.
- The `effort` skill is linked into `~/.agents/skills/`, which Codex and Copilot read. Claude Code gets it from the plugin.
- `agentctx` is linked into `~/.local/bin`.

## Daily use

```sh
git switch -c feat/login
agentctx new        # creates the effort file; or ask the agent ("start an effort for ...")
# work in as many fresh sessions as you like; each one starts with the effort file
agentctx show       # exactly what agents get here at session start
agentctx list       # every active effort across all repos, with its last progress line
agentctx close      # archive it; lists its decisions so you can promote the durable ones
agentctx prune      # efforts in this worktree whose branches were deleted (--apply to archive)
agentctx notes      # your private notes for this repo
```

The effort file has six short sections: Goal, Done when, Plan, Progress, Decisions and dead ends, Open questions. The agent keeps it current. When you're done, `close` (or the skill's close step) asks where each lasting decision belongs: the repo's `AGENTS.md`, your private notes, your personal file, or nowhere. That step is what keeps the permanent files small and correct.

## Why it's built this way

Every rule below comes from vendor documentation, the CLIs' source code or published evaluations. None of it is taste.

- **Global files stay short and hold only what code can't tell an agent.** In a controlled study, context files didn't improve task success but raised cost by over 20%. Repository overviews didn't help at all ([Gloaguen et al., ICLR 2026](https://arxiv.org/abs/2602.11988)). Anthropic says to keep CLAUDE.md under 200 lines and to stop describing architecture ([memory](https://code.claude.com/docs/en/memory), [best practices](https://code.claude.com/docs/en/best-practices)). `doctor` flags files over 200 lines.
- **Task state lives in a file, not in the chat.** Anthropic's long-running agent harness and OpenAI's ExecPlans both rebuild state from a progress file at the start of every session ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [OpenAI](https://developers.openai.com/cookbook/articles/codex_exec_plans)). The hook runs again after compaction (the `compact` matcher), so the agent gets the file fresh instead of a lossy summary of it ([hooks](https://code.claude.com/docs/en/hooks)).
- **Nothing is injected when there's nothing to inject.** No notes and no effort means no output, and a session costs zero extra tokens. The plugin's always-on cost is about 60 tokens for the skill's description (`claude plugin details agentctx@agentctx`).
- **The output fits each tool's limits.** Claude caps hook text at 10,000 characters ([hooks](https://code.claude.com/docs/en/hooks)). Codex moves hook text over about 2,500 tokens to a file (codex source, `DEFAULT_HOOK_OUTPUT_TOKEN_LIMIT`). agentctx stays under 9,000 characters (`AGENTCTX_MAX_CHARS`). A file larger than that is replaced with its path and an instruction to read it, never truncated.
- **AGENTS.md is the one repo file.** Claude Code reads AGENTS.md natively from v2.1.277, but only when no CLAUDE.md exists. Codex and Copilot read it too ([memory docs](https://code.claude.com/docs/en/memory)). `doctor` warns when a CLAUDE.md hides an AGENTS.md from Claude, and when a CLAUDE.md that only says `@AGENTS.md` is no longer needed.
- **Codex has a hard size limit.** Codex loads one file per directory from the git root down and stops at 32 KiB combined (`project_doc_max_bytes`, [docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)). `doctor` adds up the chain for your current directory.
- **Copilot needs JSON and ignores `~/` imports.** Copilot reads only `additionalContext` from session-start hooks, and doesn't load `@~/` or absolute imports ([hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference), [instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)). So it gets a symlink, not an import, and the hook prints JSON for it.

## What's tested

`sh tests/run.sh` runs every test in a throwaway `$HOME`:
- install, re-install (must change nothing), `--adopt`, dry run, uninstall
- user files are preserved: your CLAUDE.md lines, foreign hook files, your own symlinks
- repo keys for every URL form, worktrees, and directory names with spaces
- the effort lifecycle, and the context output for each agent, including JSON escaping and the size budget
- every doctor check, and `verify`

`AGENTCTX_REAL=1 sh tests/run.sh` also runs the real CLIs offline, with no model calls:
- Codex's own prompt renderer (`codex debug prompt-input`) must show the personal file through the symlink, plus root and nested AGENTS.md
- Claude Code must validate, install, enable and uninstall the plugin

CI runs the suite on Linux and macOS, under dash and `bash --posix`. It also runs a weekly job against the latest Claude Code and Codex releases, to catch upstream changes.

Last verified with Claude Code 2.1.316, Codex CLI 0.166.0 and Copilot CLI 1.0.105.

**These can't be tested offline, so `agentctx verify` checks them on your machine.** It plants a random marker in each layer, asks each agent which markers it sees without using tools, prints a table, and restores everything:
- that Claude Code follows the `@~/.agents/AGENTS.md` import and runs the plugin hook
- that Codex runs the trusted hook
- that Copilot follows the symlinked instructions file and runs its hook. If Copilot misses your personal file, set `COPILOT_CUSTOM_INSTRUCTIONS_DIRS=~/.agents` ([docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)).

Run `verify` again after upgrading any of the agents.

## Not included, on purpose

- No vector or graph memory, MCP server or database. A plain log did about as well as Mem0 on cross-session tasks ([DreamBench-SWE](https://arxiv.org/abs/2608.20664)), and MCP tool definitions cost context in every session ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)).
- No generated AGENTS.md content. LLM-generated context files slightly lowered success in the ETH study.
- No changes to auto memory (Claude) or memories (Codex). Both vendors treat them as recall aids, not a place for rules.

## Uninstall

```sh
agentctx uninstall   # removes hooks, plugin, skill and command; keeps ~/.agents
```

Uninstall replaces the links and the CLAUDE.md import with plain copies of your personal file, so each agent keeps your instructions. It never touches hook files it didn't create.

## Environment

`AGENTCTX_HOME` (default `~/.agents`), `AGENTCTX_MAX_CHARS` (default 9000, max 9500), `AGENTCTX_EFFORT` (use a named effort instead of the branch). It also honours `CLAUDE_CONFIG_DIR`, `CODEX_HOME` and `COPILOT_HOME`.

It works on Linux and macOS. On Windows, use it inside WSL.
