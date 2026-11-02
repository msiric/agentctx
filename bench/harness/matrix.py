#!/usr/bin/env python3
"""Run a plan's cells one at a time, resumably, within a time budget.

    matrix.py --plan bench/plans/pilot.json [--minutes 300] [--out bench/results/runs]

Cells with a result.json are skipped, so a run can stop anywhere (time budget,
usage limit) and pick up later. Order: for each seed, traps in plan order, and
arms in a seeded random order per (trap, seed), so drift in the model or the
CLI lands evenly across arms. Exit 0 when everything is done or paused cleanly.
"""
import argparse, json, os, random, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.dirname(HERE)


def cells(plan):
    out = []
    for seed in range(1, plan["seeds"] + 1):
        for trap in plan["traps"]:
            arms = list(plan["arms"])
            random.Random(f"{trap}:{seed}").shuffle(arms)
            for arm in arms:
                for model in plan.get("models", ["claude-sonnet-5-5"]):
                    out.append((trap, arm, model, seed))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--minutes", type=float, default=300)
    ap.add_argument("--out", default=os.path.join(BENCH, "results", "runs"))
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    stop_at = time.time() + a.minutes * 60
    todo = [c for c in cells(plan) if not os.path.exists(os.path.join(a.out, f"{c[0]}__{c[1]}__{c[2]}__s{c[3]}", "result.json"))]
    print(f"{len(todo)} cells to run")
    errors = 0
    for trap, arm, model, seed in todo:
        if time.time() > stop_at - 20 * 60:  # leave room for one more episode
            print("time budget reached; pausing"); break
        env = dict(os.environ)
        if arm == "filler":
            env["FILLER_CHARS"] = str(plan.get("filler_chars", {}).get(trap, plan.get("filler_chars_default", 4000)))
        r = subprocess.run([sys.executable, os.path.join(HERE, "episode.py"), "--trap", os.path.join(BENCH, "traps", trap),
                            "--arm", arm, "--model", model, "--seed", str(seed), "--out", a.out], env=env)
        if r.returncode == 75:
            print("usage limit reached; pausing until the next run"); break
        if r.returncode != 0:
            errors += 1
            if errors >= 3:
                print("three harness errors; stopping to avoid burning usage"); return 1
    left = [c for c in cells(plan) if not os.path.exists(os.path.join(a.out, f"{c[0]}__{c[1]}__{c[2]}__s{c[3]}", "result.json"))]
    print(f"{len(left)} cells left")
    return 0


if __name__ == "__main__":
    sys.exit(main())
