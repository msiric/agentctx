"""Scores the last session: None works inside arrays, and None is written as
an empty string everywhere (the newer decision), not skipped (the old one)."""
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
import json, re
import tomli_w
try:
    import tomllib as _toml
    loads = _toml.loads
except ImportError:
    try:
        import tomli as _toml
        loads = _toml.loads
    except ImportError:
        loads = None

def fallback(text):
    # Minimal reader for the flat documents used below (no TOML lib available).
    out, cur, arr = {}, None, None
    cur = out
    def val(v):
        v = v.strip().rstrip(',')
        if v in ('""', "''"):
            return ''
        return int(v)
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if arr is not None:
            if line == ']':
                cur[arr[0]] = arr[1]; arr = None
            else:
                arr[1].append(val(line))
            continue
        m = re.fullmatch(r'\[(\w+)\]', line)
        if m:
            cur = out.setdefault(m.group(1), {}); continue
        k, v = [x.strip() for x in line.split('=', 1)]
        if v == '[':
            arr = (k, []); continue
        if v.startswith('[') and v.endswith(']'):
            inner = v[1:-1].strip()
            cur[k] = [val(x) for x in inner.split(',') if x.strip()] if inner else []
            continue
        cur[k] = val(v)
    return out

def doc(obj):
    text = tomli_w.dumps(obj)
    return loads(text) if loads else fallback(text)
'''

TASK = PRELUDE + r'''
d = doc({'a': [1, None, 2]})
assert 'a' in d, d
vals = d['a']
assert [v for v in vals if v not in ('', None)] == [1, 2], vals
assert len(vals) in (2, 3), vals
print(json.dumps(vals))
'''

FACT = PRELUDE + r'''
res = {}
res['array'] = doc({'a': [1, None, 2]}).get('a')
res['table'] = doc({'a': None, 'b': 1})
res['nested'] = doc({'t': {'x': None, 'y': 2}})
print(json.dumps(res))
'''

task_ok, task_why = run(TASK)
fact_ok, fact_out = run(FACT)
results = [{"task": task_ok, **({} if task_ok else {"why": task_why})}]
if fact_ok:
    res = json.loads(fact_out.splitlines()[-1])
    tables_written = "a" in res["table"] and "x" in res["nested"].get("t", {})
    results.append({"fact": "f1", "ok": tables_written,
                    "why": "stale rule (skip None keys) " + ("gone" if tables_written else "still applied: %s" % json.dumps(res["table"]))})
    good = (res["array"] == [1, "", 2] and res["table"] == {"a": "", "b": 1}
            and res["nested"] == {"t": {"x": "", "y": 2}})
    results.append({"fact": "f2", "ok": good, "why": json.dumps(res)})
else:
    results.append({"fact": "f1", "ok": False, "why": fact_out})
    results.append({"fact": "f2", "ok": False, "why": fact_out})
for r in results:
    print(json.dumps(r))
sys.exit(0 if all(r.get("task", r.get("ok")) for r in results) else 1)
