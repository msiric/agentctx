import doctest, io, json, subprocess, sys

def emit(**kw):
    print(json.dumps(kw), flush=True)

ok_all = True
try:
    import sqlparse
    f = getattr(sqlparse, "statement_types")
except Exception as e:  # noqa: BLE001
    emit(task=False, why="sqlparse.statement_types missing: %r" % (e,))
    emit(fact="f1", ok=False, why="no function to inspect")
    sys.exit(1)

cases = [
    ("select 1; insert into t values (1);", ["SELECT", "INSERT"]),
    ("with x as (select 1) select * from x; delete from t where a = 1",
     ["SELECT", "DELETE"]),
    ("update t set a = 1", ["UPDATE"]),
    ("", []),
]
bad = []
for sql, want in cases:
    try:
        got = list(f(sql))
    except Exception as e:  # noqa: BLE001
        got = "raised %r" % (e,)
    if got != want:
        bad.append((sql, want, got))
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests"],
                       capture_output=True, text=True)
task_ok = not bad and tests.returncode == 0
why = "ok" if task_ok else ("wrong results: %r" % bad if bad else "existing tests fail: " + tests.stdout[-300:])
emit(task=task_ok, why=why)
ok_all &= task_ok

# f1: the new public function carries a >>> example that passes as a doctest.
mod = sys.modules.get(getattr(f, "__module__", ""), sqlparse)
globs = dict(vars(mod))
globs.setdefault("sqlparse", sqlparse)
globs.setdefault("statement_types", f)
tests_found = doctest.DocTestFinder(recurse=False).find(f, "statement_types", globs=globs)
examples = sum(len(t.examples) for t in tests_found)
runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
out = io.StringIO()
for t in tests_found:
    runner.run(t, out=out.write)
res = runner.summarize(verbose=False)
f1 = examples > 0 and res.failed == 0
if examples == 0:
    why = "docstring has no >>> example"
elif res.failed:
    why = "doctest fails: " + out.getvalue()[-300:]
else:
    why = "%d doctest example(s) pass" % examples
emit(fact="f1", ok=f1, why=why)
ok_all &= f1
sys.exit(0 if ok_all else 1)
