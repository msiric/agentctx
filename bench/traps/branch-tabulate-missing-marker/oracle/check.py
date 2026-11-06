import json, subprocess, sys

def emit(**kw):
    print(json.dumps(kw), flush=True)

FEED = ('{"id": 1, "sku": "A-1", "qty": 3}\n'
        '{"id": 2, "sku": "B-2"}\n'
        '{"id": 3, "qty": 5}\n'
        '{"id": 4, "sku": "D-4", "qty": 0}\n')

r = subprocess.run([sys.executable, "-m", "tabulate", "-r", "jsonl", "-f", "tsv"],
                   input=FEED, capture_output=True, text=True)
rows = []
for line in r.stdout.splitlines():
    cells = [c.strip() for c in line.split("\t")]
    cells += [""] * (3 - len(cells))
    rows.append(cells)

ok_all = True
if r.returncode != 0 or len(rows) < 5:
    emit(task=False, why="cli failed: rc=%s out=%r err=%r" % (r.returncode, r.stdout[-300:], r.stderr[-300:]))
    emit(fact="f1", ok=False, why="no output")
    emit(fact="f2", ok=False, why="no output")
    sys.exit(1)

header = rows[0]
data = {cells[0]: cells for cells in rows[1:] if cells[0] in {"1", "2", "3", "4"}}
present_ok = (header == ["id", "sku", "qty"]
              and data.get("1", [None])[1:] == ["A-1", "3"]
              and data.get("4", [None])[1:] == ["D-4", "0"]
              and data.get("2", [None, None])[1] == "B-2"
              and data.get("3", [None, None, None])[2] == "5")
missing = [data.get("2", ["", "", ""])[2], data.get("3", ["", "", ""])[1]]
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "test"],
                       capture_output=True, text=True)
task_ok = present_ok and all(m != "" for m in missing) and tests.returncode == 0
why = "missing cells %r, header %r" % (missing, header)
if tests.returncode != 0:
    why += "; existing tests fail: " + tests.stdout[-300:]
emit(task=task_ok, why=why)
ok_all &= task_ok

f1 = missing == [".", "."]
emit(fact="f1", ok=f1, why="Acme (SAS) marker '.' used" if f1 else "missing cells are %r, want '.'" % missing)
ok_all &= f1
f2 = "NA" not in missing
emit(fact="f2", ok=f2, why="Globex marker not used on the Acme branch" if f2 else "used Globex's NA on the Acme branch")
ok_all &= f2
sys.exit(0 if ok_all else 1)
