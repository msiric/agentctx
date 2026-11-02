#!/usr/bin/env python3
"""Summarise result.json files into results/summary.json and a markdown table.

    summarize.py [--runs bench/results/runs] [--baseline none]

Pass rates per arm with 95% cluster-bootstrap intervals over traps, and paired
differences against the baseline arm (same trap and seed). Control traps are
reported separately. Also: median last-session input tokens, median
first-request tokens (session-start injection), median tool calls before the
first edit in the last session.
"""
import argparse, glob, json, os, random, statistics as st
from collections import defaultdict

BENCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def boot(groups, stat, n=10000, seed=0):
    """Cluster bootstrap over traps: groups maps trap -> list of values."""
    keys = list(groups)
    if not keys:
        return None, None
    rnd = random.Random(seed)
    vals = []
    for _ in range(n):
        pick = [rnd.choice(keys) for _ in keys]
        xs = [x for k in pick for x in groups[k]]
        vals.append(stat(xs))
    vals.sort()
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def tokens(s):
    return sum((t.get("usage") or {}).get(k, 0) or 0 for t in s["turns"]
               for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=os.path.join(BENCH, "results", "runs"))
    ap.add_argument("--baseline", default="none")
    a = ap.parse_args()
    rs = [json.load(open(f)) for f in glob.glob(os.path.join(a.runs, "*", "result.json"))]
    out = {"n_results": len(rs), "arms": {}, "paired": {}}
    by = defaultdict(list)
    for r in rs:
        by[(r["arm"], r["model"], r["family"] == "control")].append(r)
    lines = ["| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |",
             "|---|---|---|---|---|---|---|---|"]
    for (arm, model, ctl), xs in sorted(by.items()):
        g = defaultdict(list)
        for r in xs:
            g[r["trap"]].append(1.0 if r["passed"] else 0.0)
        rate = st.mean(v for vs in g.values() for v in vs)
        lo, hi = boot(g, st.mean)
        last = [r["sessions"][-1] for r in xs if r["sessions"]]
        med = lambda v: st.median(v) if v else None
        row = {"traps": len(g), "runs": len(xs), "pass_rate": rate, "ci95": [lo, hi],
               "last_input_tokens_median": med([tokens(s) for s in last]),
               "first_request_tokens_median": med([s["first_request_input_tokens"] for s in last if s["first_request_input_tokens"]]),
               "calls_before_first_edit_median": med([s["tool_calls_before_first_edit"] for s in last if s["tool_calls_before_first_edit"] is not None])}
        name = arm + (" (control)" if ctl else "")
        out["arms"][f"{name}|{model}"] = row
        fmt = lambda x: "-" if x is None else f"{x:.0f}"
        lines.append(f"| {name} | {model} | {row['traps']} | {row['runs']} | {rate:.0%} ({lo:.0%}-{hi:.0%}) | {fmt(row['last_input_tokens_median'])} | {fmt(row['first_request_tokens_median'])} | {fmt(row['calls_before_first_edit_median'])} |")
    # paired differences vs baseline on non-control traps
    idx = {(r["trap"], r["arm"], r["model"], r["seed"]): r for r in rs if r["family"] != "control"}
    lines += ["", f"Paired difference in pass rate vs `{a.baseline}` (same trap and seed, non-control traps):", "",
              "| Arm | Model | Pairs | Difference (95% CI) |", "|---|---|---|---|"]
    for (arm, model, ctl) in sorted(by):
        if ctl or arm == a.baseline:
            continue
        g = defaultdict(list)
        for (trap, ar, mo, seed), r in idx.items():
            if ar == arm and mo == model and (trap, a.baseline, model, seed) in idx:
                g[trap].append(float(r["passed"]) - float(idx[(trap, a.baseline, model, seed)]["passed"]))
        if not g:
            continue
        d = st.mean(v for vs in g.values() for v in vs)
        lo, hi = boot(g, st.mean)
        out["paired"][f"{arm}|{model}"] = {"pairs": sum(map(len, g.values())), "diff": d, "ci95": [lo, hi]}
        lines.append(f"| {arm} | {model} | {sum(map(len, g.values()))} | {d:+.0%} ({lo:+.0%} to {hi:+.0%}) |")
    os.makedirs(os.path.join(BENCH, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(BENCH, "results", "summary.json"), "w"), indent=1)
    open(os.path.join(BENCH, "results", "summary.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
