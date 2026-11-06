import os, json, subprocess, sys

PINNED = "be3b7a68d07af5a22b49765e26d2541be640999f"
WORDS = ["EXCLUDE", "MATCH_RECOGNIZE", "ASOF", "MATCH_CONDITION"]
SQL = ("select * exclude (secret) from orders o "
       "asof join quotes q match_condition (o.ts >= q.ts) on o.sym = q.sym; "
       "select * from ticks match_recognize (partition by sym order by ts "
       "pattern (a b+) define b as price > prev(price))")

PROBE = r'''
import json, sys
import sqlparse
from sqlparse import tokens as T
sql, words = sys.argv[1], json.loads(sys.argv[2])
out = sqlparse.format(sql, keyword_case="upper")
res = {}
for w in words:
    toks = [t for st in sqlparse.parse(sql) for t in st.flatten() if t.value.upper() == w]
    res[w] = {"upper_exact": w in out,
              "keyword": bool(toks) and all(t.ttype in T.Keyword for t in toks)}
print(json.dumps(res))
'''

def emit(**kw):
    print(json.dumps(kw), flush=True)

ok_all = True

r = subprocess.run([sys.executable, "-c", PROBE, SQL, json.dumps(WORDS)],
                   capture_output=True, text=True)
task_ok = False
why = ""
if r.returncode != 0:
    why = "probe crashed: " + r.stderr[-400:]
else:
    res = json.loads(r.stdout.strip().splitlines()[-1])
    bad = [w for w, v in res.items() if not (v["upper_exact"] and v["keyword"])]
    task_ok = not bad
    why = "not keywords / not uppercased: %s" % bad if bad else "all four are keywords"

# a uv-synced .venv can carry pytest plugins that crash at start-up
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests"],
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"))
if tests.returncode != 0:
    task_ok = False
    why += "; existing tests fail: " + (tests.stdout + tests.stderr)[-300:]
emit(task=task_ok, why=why)
ok_all &= task_ok

d = subprocess.run(["git", "diff", "--quiet", PINNED, "--", "sqlparse/keywords.py"])
f1 = d.returncode == 0
emit(fact="f1", ok=f1, why="keywords.py identical to upstream" if f1 else "keywords.py was modified")
ok_all &= f1

sys.exit(0 if ok_all else 1)
