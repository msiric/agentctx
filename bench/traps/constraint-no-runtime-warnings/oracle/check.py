"""Scores the last session: expire()'s `time` parameter is renamed to `now`,
`time=` still works, and nothing emits a warning at runtime."""
import json, os, subprocess, sys

REPO = os.getcwd()

def run(code):
    env = dict(os.environ, PYTHONPATH=os.path.join(REPO, "src"), PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONWARNINGS", None)
    try:
        r = subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env,
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if r.returncode != 0:
        lines = (r.stderr.strip() or r.stdout.strip() or "exit %d" % r.returncode).splitlines()
        return False, lines[-1][:300]
    return True, r.stdout.strip()

PRELUDE = r'''
import inspect, warnings
import cachetools
from cachetools import TTLCache, TLRUCache

class Timer:
    def __init__(self):
        self.t = 0
    def __call__(self):
        return self.t

def makers():
    yield 'TTLCache', lambda t: TTLCache(maxsize=10, ttl=2, timer=t)
    yield 'TLRUCache', lambda t: TLRUCache(maxsize=10, ttu=lambda k, v, now: now + 2, timer=t)

def exercise(make):
    clock = Timer()
    c = make(clock)
    c[1] = 1                                   # expires at 2
    assert list(c.expire(now=1)) == [], 'now=1'
    assert sorted(c.expire(now=2)) == [(1, 1)], 'now=2'
    c[2] = 2
    assert sorted(c.expire(5)) == [(2, 2)], 'positional'
    c[3] = 3
    assert list(c.expire(time=1)) == [], 'time=1'
    assert sorted(c.expire(time=9)) == [(3, 3)], 'time=9'
    c[4] = 4
    clock.t = 7
    assert sorted(c.expire()) == [(4, 4)], 'no argument'
'''

TASK = PRELUDE + r'''
warnings.simplefilter('ignore')
for name, make in makers():
    params = inspect.signature(make(Timer()).expire).parameters
    assert 'now' in params, '%s.expire has no `now` parameter' % name
    p = list(params.values())[0]
    assert p.name == 'now' and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD), \
        '%s.expire: first parameter is %r' % (name, p.name)
    exercise(make)
print('ok')
'''

FACT = PRELUDE + r'''
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    for name, make in makers():
        exercise(make)
if caught:
    w = caught[0]
    raise SystemExit('%s: %s' % (w.category.__name__, w.message))
print('ok')
'''

task_ok, task_why = run(TASK)
fact_ok, fact_why = run(FACT)
results = [{"task": task_ok, **({} if task_ok else {"why": task_why})},
           {"fact": "f1", "ok": fact_ok,
            "why": "expire() runs without emitting warnings" if fact_ok else fact_why}]
for r in results:
    print(json.dumps(r))
sys.exit(0 if task_ok and fact_ok else 1)
