#!/usr/bin/env python3
"""Held-out analysis, as pre-registered (PREREGISTRATION.md, "Analysis").

  python3 bench/harness/analyze.py --runs DIR --plan bench/plans/heldout.json [--plan ...] [--out FILE]

- Pass rate per arm on fact traps, 95% CI from a cluster bootstrap over traps
  (10,000 resamples).
- H1, H2a, H2b: trailkeep minus none / native / handoff, paired by trap and
  seed. One-sided exact paired permutation test (sign flips of the paired
  differences), Holm correction across the three at alpha 0.05. A trap-level
  version (flipping whole traps) is reported as a sensitivity check.
- H3: session-start tokens added (first request of the last session, minus
  none's on the same trap and seed) and last-session input tokens.
- H4: control traps, trailkeep vs none.
- H5: superseded traps, rate of using the stale fact.
"""
import argparse, glob, itertools, json, os, random, statistics as st
from collections import defaultdict

PRIMARY = [("H1", "none"), ("H2a", "native"), ("H2b", "handoff")]
ARM = "trailkeep"


def load(runs, traps):
    rs = []
    for f in glob.glob(os.path.join(runs, "*", "result.json")):
        r = json.load(open(f))
        if r["trap"] in traps:
            rs.append(r)
    return rs


def boot(groups, n=10000, seed=0):
    rng = random.Random(seed)
    keys = list(groups)
    if not keys:
        return (float("nan"),) * 2
    vals = []
    for _ in range(n):
        s = [v for k in (rng.choice(keys) for _ in keys) for v in groups[k]]
        vals.append(st.mean(s))
    vals.sort()
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def perm_p(diffs):
    """One-sided exact sign-flip p-value for mean(diffs) > 0."""
    obs = sum(diffs)
    nz = [d for d in diffs if d != 0]
    zeros = len(diffs) - len(nz)
    if not nz:
        return 1.0
    if len(nz) > 22:  # fall back to Monte Carlo
        rng = random.Random(1); n = 200000
        hits = sum(1 for _ in range(n) if sum(d if rng.random() < .5 else -d for d in nz) >= obs - 1e-12)
        return (hits + 1) / (n + 1)
    hits = total = 0
    for signs in itertools.product((1, -1), repeat=len(nz)):
        total += 1
        if sum(s * d for s, d in zip(signs, nz)) >= obs - 1e-12:
            hits += 1
    return hits / total


def holm(ps, alpha=0.05):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj = [0.0] * len(ps)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj, [a <= alpha for a in adj]


def last_tokens(s):
    t = 0
    for u in s.get("turns", []):
        us = u.get("usage", {})
        t += us.get("input_tokens", 0) + us.get("cache_creation_input_tokens", 0) + us.get("cache_read_input_tokens", 0)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--plan", action="append", required=True)
    ap.add_argument("--arm", default=ARM)
    ap.add_argument("--out")
    a = ap.parse_args()
    traps, arms = [], []
    for p in a.plan:
        j = json.load(open(p))
        traps += [t for t in j["traps"] if t not in traps]
        arms += [x for x in j["arms"] if x not in arms]
    rs = load(a.runs, set(traps))
    idx = {(r["trap"], r["arm"], r["seed"]): r for r in rs}
    fact = [t for t in traps if not t.startswith("control-")]
    ctl = [t for t in traps if t.startswith("control-")]
    L = []
    w = L.append

    w(f"Runs: {len(rs)} cells, {len(fact)} fact traps, {len(ctl)} control traps, arms: {', '.join(arms)}.")
    vers = sorted({(r['claude_version'], r['model'], r['trailkeep_commit'][:7]) for r in rs})
    w(f"Versions: {'; '.join(f'Claude Code {v}, {m}, trailkeep {c}' for v, m, c in vers)}.")
    w("")

    # pass rates
    none_fr = {(r["trap"], r["seed"]): r["sessions"][-1].get("first_request_input_tokens") or 0
               for r in rs if r["arm"] == "none"}
    rows = []
    for arm in arms:
        g = defaultdict(list); added = []; lastin = []
        for (t, ar, s), r in idx.items():
            if ar != arm or t not in fact:
                continue
            g[t].append(1.0 if r["passed"] else 0.0)
            fr = r["sessions"][-1].get("first_request_input_tokens") or 0
            if (t, s) in none_fr:
                added.append(fr - none_fr[(t, s)])
            lastin.append(last_tokens(r["sessions"][-1]))
        if not g:
            continue
        n = sum(map(len, g.values())); k = sum(map(sum, g.values()))
        lo, hi = boot(g)
        c = [idx[(t, arm, s)]["passed"] for (t, ar, s) in idx if ar == arm and t in ctl]
        rows.append((k / n, arm, k, n, lo, hi, st.median(added) if added else 0, st.median(lastin), sum(c), len(c)))
    rows.sort(reverse=True)
    w("| Arm | Fact traps passed | Pass rate (95% CI) | Tokens added at session start (median) | Last-session input tokens (median) | Control |")
    w("|---|---|---|---|---|---|")
    for rate, arm, k, n, lo, hi, add, li, ck, cn in rows:
        b = "**" if arm == a.arm else ""
        w(f"| {b}{arm}{b} | {k:.0f}/{n} | {rate:.0%} ({lo:.0%}–{hi:.0%}) | {add:+,.0f} | {li:,.0f} | {ck}/{cn} |")
    w("")

    # primary hypotheses
    w(f"Primary hypotheses: {a.arm} minus comparator, paired by trap and seed (fact traps).")
    w("")
    w("| | Comparator | Pairs | Difference (95% CI) | p (one-sided) | Holm-adjusted p | Significant at 0.05 | Trap-level p (sensitivity) |")
    w("|---|---|---|---|---|---|---|---|")
    ps, info = [], []
    for name, comp in PRIMARY:
        g = defaultdict(list)
        for t in fact:
            for s in sorted({s for (tt, ar, s) in idx if tt == t}):
                if (t, a.arm, s) in idx and (t, comp, s) in idx:
                    g[t].append(float(idx[(t, a.arm, s)]["passed"]) - float(idx[(t, comp, s)]["passed"]))
        diffs = [v for vs in g.values() for v in vs]
        if not diffs:
            ps.append(1.0); info.append((name, comp, 0, float("nan"), (float("nan"),) * 2, 1.0)); continue
        p = perm_p(diffs)
        pt = perm_p([st.mean(v) for v in g.values()])
        ps.append(p); info.append((name, comp, len(diffs), st.mean(diffs), boot(g), pt))
    adj, sig = holm(ps)
    for (name, comp, n, d, (lo, hi), pt), p, pa, sg in zip(info, ps, adj, sig):
        w(f"| {name} | {comp} | {n} | {d:+.0%} ({lo:+.0%} to {hi:+.0%}) | {p:.4f} | {pa:.4f} | {'yes' if sg else 'no'} | {pt:.4f} |")
    w("")

    # H4 control
    for t in ctl:
        tk = [idx[k]["passed"] for k in idx if k[0] == t and k[1] == a.arm]
        nn = [idx[k]["passed"] for k in idx if k[0] == t and k[1] == "none"]
        if tk and nn:
            w(f"H4 (no harm), {t}: {a.arm} {sum(tk)}/{len(tk)}, none {sum(nn)}/{len(nn)}.")
    # H5 superseded
    sup = [t for t in fact if t.startswith("superseded-")]
    for t in sup:
        w(f"H5 (hygiene), {t}: runs failing a fact check (the stale or the newer fact) per arm:")
        for arm in arms:
            cells = [idx[k] for k in idx if k[0] == t and k[1] == arm]
            if not cells:
                continue
            stale = sum(any(l.get("fact") and not l.get("ok") for l in r["check_lines"]) for r in cells)
            w(f"  - {arm}: {stale}/{len(cells)}")
    text = "\n".join(L) + "\n"
    if a.out:
        open(a.out, "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
