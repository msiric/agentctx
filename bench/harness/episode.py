#!/usr/bin/env python3
"""Run one trap under one arm: every session, then the hidden check.

    episode.py --trap bench/traps/<id> --arm trailkeep --seed 1 --out results/runs [--model claude-sonnet-5]

Writes <out>/<trap>__<arm>__<model>__s<seed>/ with one transcript per session,
the arm's memory snapshot, and result.json. Exit codes: 0 ok (whatever the
check said), 75 rate-limited or out of usage (retry later, nothing recorded),
1 harness error.

Auth comes from the caller's environment: CLAUDE_CODE_OAUTH_TOKEN or
ANTHROPIC_API_KEY (plus ANTHROPIC_BASE_URL for the mock). Nothing else leaks
into the agent's environment.
"""
import argparse, json, os, queue, shutil, subprocess, sys, tempfile, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.dirname(HERE)
ROOT = os.path.dirname(BENCH)  # the trailkeep checkout under test
CLOSING = "That's all for today, thanks."
PASS_ENV = ("CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "OPENAI_API_KEY", "GEMINI_API_KEY")
LIMIT_MARKERS = ("usage limit", "rate limit", "rate_limit", "overloaded", "limit reached", "credit balance")


class RateLimited(Exception):
    pass


def sh(cmd, cwd=None, env=None, check=True, timeout=600):
    r = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout,
                       shell=isinstance(cmd, str))
    if check and r.returncode != 0:
        raise RuntimeError(f"failed: {cmd}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    return r


def agent_env(home, extra):
    env = {
        "HOME": home, "USER": os.environ.get("USER", "runner"), "TERM": "dumb", "LANG": "C.UTF-8",
        "PATH": f"{home}/.local/bin:" + os.environ["PATH"], "IS_SANDBOX": "1",
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_AUTOUPDATER": "1",
        "TRAILKEEP_SYNC": "1",
    }
    env.update({k: os.environ[k] for k in PASS_ENV if k in os.environ})
    env.update(extra)
    return env


def arm_hook(arm, hook, ctx, env):
    """Run arms/<arm>.sh <hook> if it defines that hook; returns stdout."""
    # "trailkeep@capture" runs arms/trailkeep.sh; the label after @ keeps a
    # changed version's cells apart from the earlier version's.
    script = os.path.join(HERE, "arms", arm.split("+")[0].split("@")[0] + ".sh")
    if not os.path.exists(script):
        raise SystemExit(f"unknown arm {arm}")
    e = dict(env, **{"ARM": arm, "TRAILKEEP_ROOT": ROOT, "BENCH": BENCH, **{k.upper(): str(v) for k, v in ctx.items()}})
    return sh(["sh", script, hook], cwd=ctx.get("repo_dir") or ctx["episode"], env=e).stdout


def arm_env(arm, env, ctx):
    """Arms print KEY=VALUE lines from their 'env' hook."""
    out = arm_hook(arm, "env", ctx, env)
    extra = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    if "+native" not in arm and not arm.startswith("native"):
        extra.setdefault("CLAUDE_CODE_DISABLE_AUTO_MEMORY", "1")
    return extra


def reader(stream, q):
    for line in stream:
        q.put(line)
    q.put(None)


def run_claude_session(cwd, env, turns, model, max_turns, log_path, resume=None, deadline=1200, extra_args=()):
    args = ["claude", "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
            "--dangerously-skip-permissions", "--model", model, "--max-turns", str(max_turns), *extra_args]
    if resume:
        args += ["--resume", resume]
    p = subprocess.Popen(args, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, bufsize=1)
    q = queue.Queue()
    threading.Thread(target=reader, args=(p.stdout, q), daemon=True).start()
    errq = queue.Queue()
    threading.Thread(target=reader, args=(p.stderr, errq), daemon=True).start()
    stats = {"session_id": None, "turns": [], "first_request_input_tokens": None, "tool_calls": 0,
             "tool_calls_before_first_edit": None, "error": None}
    start = time.time()
    with open(log_path, "w") as log:
        for text in list(turns) + [CLOSING]:
            p.stdin.write(json.dumps({"type": "user", "message": {"role": "user", "content": text}}) + "\n")
            p.stdin.flush()
            while True:
                left = deadline - (time.time() - start)
                if left <= 0:
                    p.kill(); stats["error"] = "timeout"; break
                try:
                    line = q.get(timeout=left)
                except queue.Empty:
                    continue
                if line is None:
                    stats["error"] = stats["error"] or "agent exited early"; break
                log.write(line)
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                stats["session_id"] = ev.get("session_id") or stats["session_id"]
                if ev.get("type") == "system" and ev.get("subtype") == "init":
                    stats["model_served"] = ev.get("model")
                if ev.get("type") == "assistant":
                    msg = ev.get("message", {})
                    u = msg.get("usage") or {}
                    if stats["first_request_input_tokens"] is None and u:
                        stats["first_request_input_tokens"] = sum(u.get(k, 0) or 0 for k in
                            ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                    for b in msg.get("content", []):
                        if b.get("type") == "tool_use":
                            stats["tool_calls"] += 1
                            if stats["tool_calls_before_first_edit"] is None and b.get("name") in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                                stats["tool_calls_before_first_edit"] = stats["tool_calls"] - 1
                if ev.get("type") == "rate_limit_event" and (ev.get("rate_limit_info") or {}).get("status") == "rejected":
                    p.kill(); raise RateLimited(json.dumps(ev)[:300])
                if ev.get("type") == "result":
                    res = str(ev.get("result") or "")
                    if ev.get("is_error") and any(m in res.lower() for m in LIMIT_MARKERS):
                        p.kill(); raise RateLimited(res[:300])
                    stats["turns"].append({k: ev.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms", "usage", "total_cost_usd")})
                    break
            if stats["error"]:
                break
        try:
            p.stdin.close()
        except OSError:
            pass
        try:
            p.wait(timeout=60)
        except subprocess.TimeoutExpired:
            p.kill()
    stats["wall_s"] = round(time.time() - start, 1)
    stats["stderr_tail"] = "".join(x for x in list(errq.queue)[-20:] if x)[-2000:]
    if any(m in stats["stderr_tail"].lower() for m in LIMIT_MARKERS) and not stats["turns"]:
        raise RateLimited(stats["stderr_tail"][:300])
    return stats


def checkout(repo_dir, branch, env):
    if sh(["git", "rev-parse", "-q", "--verify", "refs/heads/" + branch], cwd=repo_dir, check=False).returncode == 0:
        r = sh(["git", "checkout", "-q", branch], cwd=repo_dir, env=env, check=False)
        if r.returncode:  # uncommitted work in the way: carry it over, as `git checkout` would refuse
            sh(["git", "stash", "-q", "--include-untracked"], cwd=repo_dir, env=env)
            sh(["git", "checkout", "-q", branch], cwd=repo_dir, env=env)
            sh(["git", "stash", "pop", "-q"], cwd=repo_dir, env=env, check=False)
    else:
        sh(["git", "checkout", "-q", "-b", branch], cwd=repo_dir, env=env)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trap", required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--out", default=os.path.join(BENCH, "results", "runs"))
    ap.add_argument("--keep", action="store_true", help="keep the episode workspace")
    a = ap.parse_args()

    trap_dir = os.path.abspath(a.trap)
    t = json.load(open(os.path.join(trap_dir, "trap.json")))
    cell = f"{t['id']}__{a.arm}__{a.model}__s{a.seed}"
    out = os.path.join(os.path.abspath(a.out), cell)
    if os.path.exists(os.path.join(out, "result.json")):
        print(f"{cell}: done already"); return 0
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)

    ep = tempfile.mkdtemp(prefix="ep-")
    home = os.path.join(ep, "home"); os.makedirs(home)
    work = os.path.join(ep, "work"); os.makedirs(work)
    base_env = agent_env(home, {})
    sh(["git", "config", "--global", "user.name", "Bench User"], env=base_env)
    sh(["git", "config", "--global", "user.email", "bench@example.com"], env=base_env)
    sh(["git", "config", "--global", "init.defaultBranch", "main"], env=base_env)

    result = {"cell": cell, "trap": t["id"], "family": t["family"], "arm": a.arm, "model": a.model, "seed": a.seed,
              "trailkeep_commit": sh(["git", "rev-parse", "HEAD"], cwd=ROOT).stdout.strip(),
              "claude_version": sh(["claude", "--version"], check=False).stdout.strip(),
              "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sessions": []}
    try:
        for r in t["repos"]:
            d = os.path.join(work, r["name"])
            sh(["git", "clone", "-q", r["url"], d], env=base_env)
            sh(["git", "checkout", "-q", r["commit"]], cwd=d, env=base_env)
            sh(["git", "checkout", "-q", "-B", "main"], cwd=d, env=base_env)
            sh(["git", "remote", "remove", "origin"], cwd=d, env=base_env)  # no peeking upstream
            if os.path.exists(os.path.join(trap_dir, "setup.sh")):
                sh(["sh", os.path.join(trap_dir, "setup.sh")], cwd=d, env=dict(base_env, TRAP_REPO=r["name"]), timeout=1200)
        ctx = {"episode": ep, "home": home, "trap_dir_public": "", "facts_file": ""}
        arm_hook(a.arm, "install", ctx, base_env)
        budget = t.get("budget", {}).get("max_turns_per_session", 60)
        prev_sid = None
        n = len(t["sessions"])
        for i, s in enumerate(t["sessions"], 1):
            d = os.path.join(work, s["repo"])
            checkout(d, s["branch"], base_env)
            sctx = dict(ctx, repo_dir=d, session=i, last=int(i == n), branch=s["branch"])
            if i == n and a.arm.startswith("oracle-note"):
                fact_note = os.path.join(ep, "facts.txt")
                live = [f for f in t["facts"] if not f.get("superseded_by")]
                open(fact_note, "w").write("\n".join("- " + f["text"] for f in live) + "\n")
                sctx["facts_file"] = fact_note
            arm_hook(a.arm, "before_session", sctx, base_env)
            env = agent_env(home, arm_env(a.arm, base_env, sctx))
            resume = prev_sid if (i == n and a.arm.startswith("resume")) else None
            st = run_claude_session(d, env, s["turns"], a.model, budget, os.path.join(out, f"session{i}.jsonl"), resume=resume)
            st["repo"], st["branch"] = s["repo"], s["branch"]
            result["sessions"].append(st)
            prev_sid = st["session_id"]
            arm_hook(a.arm, "after_session", sctx, base_env)
        # memory snapshot, for the failure taxonomy (never shown to the agent)
        snap = os.path.join(out, "memory")
        arm_hook(a.arm, "snapshot", dict(ctx, repo_dir=os.path.join(work, t["sessions"][-1]["repo"]), snapshot=snap), base_env)
        # hidden check, from a copy outside the agent's reach
        primary = os.path.join(work, t["sessions"][-1]["repo"])
        oracle = tempfile.mkdtemp(prefix="oracle-")
        shutil.copytree(os.path.join(trap_dir, "oracle"), oracle, dirs_exist_ok=True)
        r = sh(["sh", os.path.join(oracle, "check.sh")], cwd=primary, env=dict(base_env, ORACLE_DIR=oracle), check=False, timeout=900)
        lines = []
        for l in r.stdout.splitlines():
            try:
                lines.append(json.loads(l))
            except ValueError:
                pass
        result.update(passed=r.returncode == 0, check_lines=lines, check_tail=(r.stdout + r.stderr)[-3000:])
        sh(["git", "add", "-A"], cwd=primary, env=base_env, check=False)
        open(os.path.join(out, "final.diff"), "w").write(sh(["git", "diff", "--cached", "main"], cwd=primary, check=False).stdout)
        shutil.rmtree(oracle, ignore_errors=True)
    except RateLimited as e:
        print(f"{cell}: rate limited: {e}", file=sys.stderr)
        shutil.rmtree(out, ignore_errors=True)
        return 75
    except Exception as e:  # harness error: keep what we have, don't record a result
        open(os.path.join(out, "harness-error.txt"), "w").write(repr(e))
        print(f"{cell}: harness error: {e}", file=sys.stderr)
        return 1
    finally:
        if not a.keep:
            shutil.rmtree(ep, ignore_errors=True)
        else:
            print("kept", ep)
    result["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    json.dump(result, open(os.path.join(out, "result.json"), "w"), indent=1)
    print(f"{cell}: {'PASS' if result['passed'] else 'fail'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
