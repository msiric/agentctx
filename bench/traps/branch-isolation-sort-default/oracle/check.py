"""Scores the last session (on branch `acme`): dumps/dump have sort_keys, and
on this branch it defaults to on (main's default-off must not leak in)."""
import json, os, subprocess, sys

REPO = os.getcwd()

def run(code):
    env = dict(os.environ, PYTHONPATH=os.path.join(REPO, "src"), PYTHONDONTWRITEBYTECODE="1")
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
import io, json, re
import tomli_w
OBJ = {"z": 1, "b": 2, "a": {"y": 2, "x": 1}, "c": [{"q": 1, "p": 2}]}

def orders(text):
    """Key order of: top-level values, the inline table, and table [a]."""
    top, table, section = [], [], None
    for line in text.splitlines():
        m = re.match(r'^\[(\w+)\]$', line)
        if m:
            section = m.group(1); continue
        m = re.match(r'^(\w+) = ', line)
        if m:
            (top if section is None else table).append(m.group(1))
    inline = re.search(r'\{ (.*) \}', text)
    inline = re.findall(r'(\w+) = ', inline.group(1)) if inline else None
    return top, inline, table

SORTED = (['b', 'c', 'z'], ['p', 'q'], ['x', 'y'])
INSERTION = (['z', 'b', 'c'], ['q', 'p'], ['y', 'x'])

def state(text):
    o = orders(text)
    o = (o[0], o[1], o[2])
    if o == SORTED:
        return 'sorted'
    if o == INSERTION:
        return 'insertion'
    return 'other:%r' % (o,)
'''

TASK = PRELUDE + r'''
assert state(tomli_w.dumps(OBJ, sort_keys=True)) == 'sorted', tomli_w.dumps(OBJ, sort_keys=True)
assert state(tomli_w.dumps(OBJ, sort_keys=False)) == 'insertion', tomli_w.dumps(OBJ, sort_keys=False)
for flag, want in ((True, 'sorted'), (False, 'insertion')):
    buf = io.BytesIO()
    tomli_w.dump(OBJ, buf, sort_keys=flag)
    assert state(buf.getvalue().decode()) == want, ('dump', flag)
print('ok')
'''

FACT = PRELUDE + r'''
buf = io.BytesIO()
tomli_w.dump(OBJ, buf)
print(json.dumps([state(tomli_w.dumps(OBJ)), state(buf.getvalue().decode())]))
'''

branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO,
                        capture_output=True, text=True).stdout.strip()
task_ok, task_why = run(TASK)
if task_ok and branch != "acme":
    task_ok, task_why = False, "working tree is on %r, not acme" % branch
fact_ok, fact_out = run(FACT)
results = [{"task": task_ok, **({} if task_ok else {"why": task_why})}]
if fact_ok:
    dumps_state, dump_state = json.loads(fact_out.splitlines()[-1])
    on = dumps_state == "sorted" and dump_state == "sorted"
    results.append({"fact": "f1", "ok": on,
                    "why": "default output: dumps %s, dump %s" % (dumps_state, dump_state)})
    results.append({"fact": "f2", "ok": on,
                    "why": "main's default-off " + ("not applied here" if on else "leaked into acme")})
else:
    results.append({"fact": "f1", "ok": False, "why": fact_out})
    results.append({"fact": "f2", "ok": False, "why": fact_out})
for r in results:
    print(json.dumps(r))
sys.exit(0 if all(r.get("task", r.get("ok")) for r in results) else 1)
