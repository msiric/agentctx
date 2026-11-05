"""Scores the last session (addict): to_dict() gains skip_none, and the new
option is keyword-only (the user's cross-project preference from xmltodict)."""
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
        lines = (r.stderr.strip() or r.stdout.strip() or "exit %d" % r.returncode).splitlines()
        return False, lines[-1][:300]
    return True, r.stdout.strip()

TASK = r'''
from addict import Dict
d = Dict(a=None, b={'c': None, 'd': 1}, e=[{'f': None, 'g': 2}], h=0, i='')
out = d.to_dict(skip_none=True)
assert out == {'b': {'d': 1}, 'e': [{'g': 2}], 'h': 0, 'i': ''}, out
assert type(out) is dict and type(out['b']) is dict and type(out['e'][0]) is dict, out
full = d.to_dict()
assert full == {'a': None, 'b': {'c': None, 'd': 1}, 'e': [{'f': None, 'g': 2}], 'h': 0, 'i': ''}, full
assert d.to_dict(skip_none=False) == full
print('ok')
'''

FACT = r'''
import inspect
from addict import Dict
p = inspect.signature(Dict.to_dict).parameters.get('skip_none')
kind = p.kind.name if p is not None else None
try:
    Dict(a=None).to_dict(True)
    positional = 'accepted'
except TypeError:
    positional = 'rejected'
try:
    Dict(a=None).to_dict(skip_none=True)
    exists = 'yes'
except TypeError:
    exists = 'no'
print(kind, positional, exists)
'''

task_ok, task_why = run(TASK)
fact_ok, fact_out = run(FACT)
results = [{"task": task_ok, **({} if task_ok else {"why": task_why})}]
if fact_ok:
    kind, positional, exists = fact_out.split()[-3:]
    if exists != "yes":
        results.append({"fact": "f1", "ok": False, "why": "to_dict() has no skip_none option"})
    else:
        good = positional == "rejected" and kind in ("KEYWORD_ONLY", "None")
        results.append({"fact": "f1", "ok": good,
                        "why": "skip_none is %s; positional use %s" % (kind, positional)})
else:
    results.append({"fact": "f1", "ok": False, "why": fact_out})
for r in results:
    print(json.dumps(r))
sys.exit(0 if all(r.get("task", r.get("ok")) for r in results) else 1)
