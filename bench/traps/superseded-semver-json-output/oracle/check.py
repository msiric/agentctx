"""Scores the last session: `pysemver latest` prints the highest non-prerelease
version (task); as a *new* subcommand its output is JSON (f2, which superseded
the earlier plain-lines rule f1), while `sort` keeps its plain-lines output."""
import json
import os
import subprocess
import sys

env = dict(os.environ)
env["PYTHONPATH"] = os.path.join(os.getcwd(), "src") + os.pathsep + env.get("PYTHONPATH", "")
ok = {"task": True, "f2": True}
why = {"task": [], "f2": []}


def fail(key, msg):
    ok[key] = False
    why[key].append(msg)


def pysemver(*args, stdin=""):
    r = subprocess.run([sys.executable, "-m", "semver", *args], input=stdin,
                       capture_output=True, text=True, env=env, timeout=60)
    return r.returncode, r.stdout, r.stderr


def json_mentions(value, target):
    """True if a decoded JSON value carries `target` as a string, at top level,
    in a list, or as a value of an object."""
    if value == target:
        return True
    if isinstance(value, list):
        return target in value
    if isinstance(value, dict):
        return any(v == target or (isinstance(v, list) and target in v) for v in value.values())
    return False


# ---- task: latest -------------------------------------------------------
versions = ["1.2.0", "2.10.1", "2.11.0-rc.1", "1.9.9", "2.9.12"]
rc, out, err = pysemver("latest", *versions)
if rc != 0:
    fail("task", "`latest` exited %d: %s" % (rc, (err or out).strip()[:200]))
    fail("f2", "cannot evaluate: `latest` did not run")
else:
    if "2.10.1" not in out:
        fail("task", "`latest` output %r lacks 2.10.1" % (out[:200],))
    if "2.11.0-rc.1" in out:
        fail("task", "`latest` picked the prerelease: %r" % (out[:200],))
    # ---- f2: the new subcommand prints JSON
    try:
        decoded = json.loads(out)
    except ValueError:
        fail("f2", "`latest` output is not JSON: %r" % (out.strip()[:200],))
    else:
        if not json_mentions(decoded, "2.10.1"):
            fail("f2", "`latest` JSON does not carry \"2.10.1\" as a string: %r" % (out.strip()[:200],))

# ---- f2: `sort` keeps plain text lines for the old Jenkins job ----------
rc, out, err = pysemver("sort", "1.10.0", "1.2.0")
if rc == 0:
    is_json = True
    try:
        json.loads(out)
    except ValueError:
        is_json = False
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    if is_json or lines != ["1.2.0", "1.10.0"]:
        fail("f2", "`sort` no longer prints plain lines: %r" % (out[:200],))

stale = any(m.startswith("`latest` output is not JSON") for m in why["f2"])
print(json.dumps({"fact": "f1", "ok": not stale and ok["task"],
                  "why": "superseded by f2; fails if `latest` still follows the old plain-lines rule"}))
print(json.dumps({"fact": "f2", "ok": ok["f2"], "why": "; ".join(why["f2"]) or "latest prints JSON, sort unchanged"}))
print(json.dumps({"task": ok["task"], "why": "; ".join(why["task"])}))
sys.exit(0 if all(ok.values()) else 1)
