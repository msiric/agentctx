---
name: effort
description: Start, hand off or close the per-branch effort file (goal, plan, progress, decisions) managed by agentctx. Use when the user wants to start or plan a task, save progress or hand off to a fresh session, or wrap up a branch.
---

# Effort files

An effort file holds the context for one branch: goal, definition of done,
plan, progress and decisions. It lives in `.agentctx/<branch>.md` at the
worktree root; that folder ignores itself, so it never shows up in git. If one
exists for the current branch, it was injected at session start. Edit it
directly with your file tools.

## Start

1. Run `agentctx new`. It prints the file path.
2. Ask the user for anything you can't infer, then fill in **Goal**,
   **Done when** (checkable outcomes, including the tests that must pass) and
   **Plan** (small checkbox steps).
3. Stop and let the user review the plan before writing code.

## While working and before you stop

- Tick Plan items as they are done.
- Add one line under **Progress** per session: `YYYY-MM-DD: what changed, what's next`.
- Record approaches that failed and why under **Decisions and dead ends**, so
  the next session doesn't retry them.
- Keep the file under about 150 lines: fold old Progress lines into one summary line.

## Hand off

When the user asks to hand off, or context is getting long: update the file
until a fresh session could continue from it alone, then say so. The user
will start a new session; the file is injected again automatically.

## Close

1. Read **Decisions and dead ends**. For each item, decide whether every
   future task needs it. Most don't.
2. Propose each keeper as a one-line diff to exactly one place:
   - the repo's `AGENTS.md` if it's team-wide and not derivable from the code
   - `agentctx notes --path` if it's private to the user, for this repo
   - `~/.agents/AGENTS.md` if it applies to the user in every repo
3. Apply only what the user approves, then run `agentctx close`. If that
   fails because your sandbox can't write to `~/.agents`, ask the user to run
   it in their terminal.
