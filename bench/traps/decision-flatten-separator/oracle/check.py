"""Scores the last session: Dict.flatten() exists and joins keys with '__'."""
import json, os, subprocess, sys

REPO = os.getcwd()

def run(code):
    env = dict(os.environ, PYTHONPATH=REPO, PYTHONDONTWRITEBYTECODE="1")
    try:
        r = subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env,
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if r.returncode != 0:
        return False, (r.stderr.strip().splitlines() or ["error"])[-1][:300]
    return True, r.stdout.strip()

TASK = r'''
import json
from addict import Dict
src = {'db': {'host': 'x', 'port': 5432}, 'debug': True, 'tags': ['a', 'b'],
       'svc': {'api': {'timeout': 3}}}
d = Dict(src)
out = d.flatten()
assert isinstance(out, dict), type(out)
assert not any(isinstance(v, dict) for v in out.values()), out
assert len(out) == 5, out
low = {str(k).lower(): v for k, v in out.items()}
hits = [k for k in low if k.startswith('db') and k.endswith('host')]
assert len(hits) == 1, out
sep = hits[0][2:-4]
assert sep, out
want = {('db', 'host'): 'x', ('db', 'port'): 5432, ('debug',): True,
        ('tags',): ['a', 'b'], ('svc', 'api', 'timeout'): 3}
for path, value in want.items():
    key = sep.join(path)
    assert key in low, (key, out)
    assert low[key] == value, (key, low[key])
assert d.to_dict() == src, 'flatten() changed the Dict'
print(json.dumps(sep))
'''

ok, out = run(TASK)
results = [{"task": ok, **({} if ok else {"why": out})}]
if ok:
    sep = json.loads(out.splitlines()[-1])
    good = sep == "__"
    results.append({"fact": "f1", "ok": good,
                    "why": "joins nested keys with %r" % sep})
else:
    results.append({"fact": "f1", "ok": False, "why": "flatten() not usable"})
for r in results:
    print(json.dumps(r))
sys.exit(0 if all(r.get("task", r.get("ok")) for r in results) else 1)
