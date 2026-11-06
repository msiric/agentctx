import importlib.util, json, subprocess, sys

def emit(**kw):
    print(json.dumps(kw), flush=True)

import tenacity
from tenacity import RetryError, Retrying, retry, stop_after_attempt, wait_none


def flaky(fails):
    state = {"n": 0}

    def fn():
        state["n"] += 1
        if state["n"] <= fails:
            raise ValueError("transient %d" % state["n"])
        return "ok"
    return fn


def always_fails():
    raise ValueError("permanent")


problems = []

def expect(label, cond):
    if not cond:
        problems.append(label)

# --- task: the hook is called after every attempt, including the last ---
try:
    calls = []
    r = Retrying(stop=stop_after_attempt(5), wait=wait_none(), stats_hook=calls.append)
    expect("Retrying result", r(flaky(2)) == "ok")
    expect("Retrying: 3 calls for 3 attempts (got %d)" % len(calls), len(calls) == 3)
    expect("hook gets the statistics dict",
           all(isinstance(c, dict) and "attempt_number" in c for c in calls))

    calls = []
    r = Retrying(stop=stop_after_attempt(5), wait=wait_none(), stats_hook=calls.append)
    expect("first-try success", r(flaky(0)) == "ok")
    expect("1 call for a first-try success (got %d)" % len(calls), len(calls) == 1)

    calls = []

    @retry(stop=stop_after_attempt(3), wait=wait_none(), stats_hook=calls.append)
    def doomed():
        raise ValueError("permanent")
    try:
        doomed()
        expect("@retry: should raise RetryError", False)
    except RetryError:
        pass
    expect("@retry: 3 calls for 3 failed attempts (got %d)" % len(calls), len(calls) == 3)
except Exception as e:  # noqa: BLE001
    problems.append("crashed: %r" % (e,))

suite = ["tests"]
if importlib.util.find_spec("tornado") is None:
    suite += ["--ignore", "tests/test_tornado.py"]
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"] + suite,
                       capture_output=True, text=True)
if tests.returncode != 0:
    problems.append("existing tests fail: " + tests.stdout[-300:])
task_ok = not problems
emit(task=task_ok, why="ok" if task_ok else "; ".join(problems))

# --- f1: a failing metrics hook never escapes into the retry ---
def broken_hook(stats):
    raise RuntimeError("statsd agent down")

f1_problems = []
def run(label, fn, want):
    try:
        got = fn()
        outcome = ("value", got)
    except BaseException as e:  # noqa: BLE001
        outcome = ("raise", type(e).__name__)
    if outcome != want:
        f1_problems.append("%s: got %r, want %r" % (label, outcome, want))

run("flaky call with broken hook",
    lambda: Retrying(stop=stop_after_attempt(5), wait=wait_none(), stats_hook=broken_hook)(flaky(2)),
    ("value", "ok"))
run("reraise=True keeps the original error",
    lambda: Retrying(stop=stop_after_attempt(3), wait=wait_none(), reraise=True,
                     stats_hook=broken_hook)(always_fails),
    ("raise", "ValueError"))
run("gives up with RetryError",
    lambda: Retrying(stop=stop_after_attempt(3), wait=wait_none(),
                     stats_hook=broken_hook)(always_fails),
    ("raise", "RetryError"))

def deco_flaky():
    return retry(stop=stop_after_attempt(4), wait=wait_none(), stats_hook=broken_hook)(flaky(2))()
run("@retry flaky with broken hook", deco_flaky, ("value", "ok"))

f1 = not f1_problems
emit(fact="f1", ok=f1, why="hook errors are contained" if f1 else "; ".join(f1_problems))
sys.exit(0 if (task_ok and f1) else 1)
