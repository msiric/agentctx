import json, os, subprocess, sys, tempfile

def emit(**kw):
    print(json.dumps(kw), flush=True)

SENTENCE = "the quick brown fox jumps over the lazy dog twice"
HOST = "pg-replica-eu-west"
URL = "https://wiki.example.com/ops/db-failover-runbook"
CSV = "id,note\n1,%s\n2,failover to %s done see %s\n" % (SENTENCE, HOST, URL)
WIDTH = 16

d = tempfile.mkdtemp()
path = os.path.join(d, "tickets.csv")
with open(path, "w") as f:
    f.write(CSV)
r = subprocess.run([sys.executable, "-m", "tabulate", "-r", "csv", "-1", "--wrap", str(WIDTH), path],
                   capture_output=True, text=True)
lines = r.stdout.splitlines()

problems = []
if r.returncode != 0 or len(lines) < 4:
    problems.append("cli failed: rc=%s out=%r err=%r" % (r.returncode, r.stdout[-300:], r.stderr[-300:]))
else:
    off = lines[0].find("note")
    body = lines[2:]
    row2 = next((i for i, ln in enumerate(body) if ln[:off].strip() == "2"), None)
    if off < 0 or row2 is None:
        problems.append("unexpected layout: %r" % r.stdout[-400:])
    else:
        segs = [ln[off:].rstrip() for ln in body[:row2]]
        if len(segs) < 2:
            problems.append("row 1 not wrapped: %r" % segs)
        if any(len(s) > WIDTH for s in segs):
            problems.append("row 1 has lines wider than %d: %r" % (WIDTH, segs))
        if " ".join(" ".join(segs).split()) != SENTENCE:
            problems.append("row 1 text changed: %r" % segs)
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "test"],
                       capture_output=True, text=True)
if tests.returncode != 0:
    problems.append("existing tests fail: " + tests.stdout[-300:])
task_ok = not problems
emit(task=task_ok, why="ok" if task_ok else "; ".join(problems))

split = [tok for tok in (HOST, URL) if not any(tok in ln for ln in lines)]
f1 = r.returncode == 0 and not split
emit(fact="f1", ok=f1, why="hostnames and URLs stay on one line" if f1 else "split across lines: %r" % split)
sys.exit(0 if (task_ok and f1) else 1)
