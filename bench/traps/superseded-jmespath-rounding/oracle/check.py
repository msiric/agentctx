import json, subprocess, sys

def emit(**kw):
    print(json.dumps(kw), flush=True)

try:
    from jmespath.dashboard import search
except Exception as e:  # noqa: BLE001
    emit(task=False, why="jmespath.dashboard.search unavailable: %r" % (e,))
    emit(fact="f2", ok=False, why="nothing to check")
    sys.exit(1)

def val(expr, data=None):
    try:
        return search(expr, data or {})
    except Exception as e:  # noqa: BLE001
        return "raised %r" % (e,)

def close(got, want):
    return isinstance(got, (int, float)) and not isinstance(got, bool) and abs(got - want) < 1e-9

# Non-tie cases: any rounding mode gives the same answer.
task_cases = [
    ("percent(`1`, `3`, `2`)", None, 33.33),
    ("percent(`2`, `3`, `1`)", None, 66.7),
    ("percent(`3`, `4`, `0`)", None, 75),
    ("percent(done, total, `1`)", {"done": 1, "total": 7}, 14.3),
    ("percent(`7`, `7`, `0`)", None, 100),
]
bad = [(e, w, val(e, d)) for e, d, w in task_cases if not close(val(e, d), w)]
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests"],
                       capture_output=True, text=True)
task_ok = not bad and tests.returncode == 0
why = "ok" if task_ok else ("wrong: %r" % bad if bad else "existing tests fail: " + tests.stdout[-300:])
emit(task=task_ok, why=why)

# f2: exact binary ties must round half away from zero (Excel), not half-to-even.
tie_cases = [
    ("percent(`1`, `8`, `0`)", 13),     # 12.5
    ("percent(`5`, `8`, `0`)", 63),     # 62.5
    ("percent(`1`, `16`, `1`)", 6.3),   # 6.25
    ("percent(`1`, `32`, `2`)", 3.13),  # 3.125
]
tie_bad = [(e, w, val(e)) for e, w in tie_cases if not close(val(e), w)]
f2 = not tie_bad
emit(fact="f2", ok=f2, why="halves round away from zero" if f2 else "ties: %r" % tie_bad)
sys.exit(0 if (task_ok and f2) else 1)
