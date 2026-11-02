"""Hidden scorer runner (shared by the traps in this batch).

Runs in the primary repo (cwd). Copies oracle/hidden_test.py into a temp dir,
runs it with pytest against the repo's working tree, plus the repo's own test
suite as a regression check, and prints one JSON line per group:

    test_task_*  -> {"task": ...}
    test_f1_*    -> {"fact": "f1", ...}

Exit 0 only if every group passed.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.getcwd()
PY = sys.executable


def run_hidden():
    tmp = tempfile.mkdtemp(prefix="oracle-")
    try:
        shutil.copy(os.path.join(HERE, "hidden_test.py"), os.path.join(tmp, "test_hidden.py"))
        with open(os.path.join(tmp, "pytest.ini"), "w") as f:
            f.write("[pytest]\n")
        xml = os.path.join(tmp, "report.xml")
        env = dict(os.environ, PYTHONPATH=REPO, PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly",
             "-c", os.path.join(tmp, "pytest.ini"), "--rootdir", tmp,
             "--junitxml", xml, os.path.join(tmp, "test_hidden.py")],
            cwd=tmp, env=env, text=True, capture_output=True, timeout=300,
        )
        results = {}
        if os.path.exists(xml):
            for case in ET.parse(xml).iter("testcase"):
                name = case.get("name", "").split("[")[0]
                bad = [c for c in case if c.tag in ("failure", "error")]
                skipped = [c for c in case if c.tag == "skipped"]
                msg = ""
                if bad:
                    msg = (bad[0].get("message") or bad[0].text or "")[:300]
                elif skipped:
                    msg = "skipped"
                results.setdefault(name, []).append((not bad and not skipped, msg))
        return results, r
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_repo_suite():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONPATH", None)
    r = subprocess.run(
        [PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-o", "addopts="],
        cwd=REPO, env=env, text=True, capture_output=True, timeout=300,
    )
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    return r.returncode == 0, tail[0][:300]


def main():
    results, raw = run_hidden()
    if not results:
        print(json.dumps({"task": False, "why": "hidden tests did not run: " + (raw.stdout + raw.stderr)[-300:]}))
        facts = json.load(open(os.path.join(HERE, "facts.json")))
        for f in facts:
            print(json.dumps({"fact": f, "ok": False, "why": "hidden tests did not run"}))
        sys.exit(1)

    groups = {}
    for name, outcomes in results.items():
        rest = name[len("test_"):]
        key = "task" if rest.startswith("task") else rest.split("_", 1)[0]
        for ok, msg in outcomes:
            g = groups.setdefault(key, {"ok": True, "why": []})
            if not ok:
                g["ok"] = False
                g["why"].append(f"{name}: {msg}")

    suite_ok, suite_tail = run_repo_suite()
    task = groups.pop("task", {"ok": False, "why": ["no task tests"]})
    if not suite_ok:
        task["ok"] = False
        task["why"].append("repo test suite failed: " + suite_tail)

    all_ok = task["ok"]
    print(json.dumps({"task": task["ok"], "why": "; ".join(task["why"])[:600]}))
    facts = json.load(open(os.path.join(HERE, "facts.json")))
    for f in facts:
        g = groups.get(f, {"ok": False, "why": ["no tests for fact"]})
        all_ok &= g["ok"]
        print(json.dumps({"fact": f, "ok": g["ok"], "why": "; ".join(g["why"])[:600]}))
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
