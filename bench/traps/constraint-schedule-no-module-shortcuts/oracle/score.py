"""Hidden scorer: runs pytest groups and prints one JSON line per fact plus a task line."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.getcwd()
VENV_BIN = os.path.join(REPO, ".venv", "bin")
PY = os.path.join(VENV_BIN, "python")
if not os.path.exists(PY):
    PY = sys.executable


def run_pytest(*args, timeout=300):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    env["PATH"] = VENV_BIN + os.pathsep + env.get("PATH", "")
    cmd = [PY, "-m", "pytest", "-q", "-rf", "-o", "addopts=", "-p", "no:cacheprovider",
           "-p", "no:randomly", *args]
    try:
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    failed = [os.path.basename(l[7:].split(" ")[0]) for l in r.stdout.splitlines()
              if l.startswith("FAILED ")]
    if r.returncode == 0:
        return True, ""
    if failed:
        return False, "; ".join(failed)[:400]
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return False, (" | ".join(lines[-3:]))[:400]


def main(facts, task):
    """facts: list of (fact_id, [pytest args]); task: list of [pytest args] groups."""
    all_ok = True
    for fid, args in facts:
        ok, why = run_pytest(*args)
        all_ok &= ok
        print(json.dumps({"fact": fid, "ok": ok, "why": why or "ok"}))
    task_ok, whys = True, []
    for args in task:
        ok, why = run_pytest(*args)
        if not ok:
            task_ok = False
            whys.append(why)
    all_ok &= task_ok
    line = {"task": task_ok}
    if whys:
        line["why"] = " || ".join(whys)[:600]
    print(json.dumps(line))
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main(
        facts=[("f1", [os.path.join(HERE, "hidden_test_no_new_module_functions.py")])],
        task=[[os.path.join(HERE, "hidden_test_pause_resume.py")], ["test_schedule.py"]],
    )
