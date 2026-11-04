"""Scores the last session: humanize.gigabytes(num_bytes, precision=1) exists and
formats decimal GB (task), and halves round up rather than half-to-even (f1)."""
import json
import os
import sys
import types

src = os.path.join(os.getcwd(), "src")
sys.path.insert(0, src)
if not os.path.exists(os.path.join(src, "humanize", "_version.py")):
    stub = types.ModuleType("humanize._version")
    stub.__version__ = "0.0.0"
    sys.modules["humanize._version"] = stub

ok = {"task": True, "f1": True}
why = {"task": [], "f1": []}


def fail(key, msg):
    ok[key] = False
    why[key].append(msg)


try:
    import humanize

    gigabytes = getattr(humanize, "gigabytes", None)
    if gigabytes is None:
        from humanize.filesize import gigabytes  # not exported, still usable
        fail("task", "gigabytes is not exported from the humanize package")
except Exception as e:  # noqa: BLE001
    print(json.dumps({"fact": "f1", "ok": False, "why": "cannot import gigabytes: %r" % (e,)}))
    print(json.dumps({"task": False}))
    sys.exit(1)


def norm(s):
    return str(s).replace(" ", " ").replace(" ", " ").replace(" ", "")


def expect(key, args, kwargs, want):
    try:
        got = gigabytes(*args, **kwargs)
    except Exception as e:  # noqa: BLE001
        fail(key, "gigabytes(%r, %r) raised %r" % (args, kwargs, e))
        return
    if norm(got) != norm(want):
        fail(key, "gigabytes(%s%s) = %r, want %r" % (
            ", ".join(map(repr, args)), "".join(", %s=%r" % kv for kv in kwargs.items()), got, want))


# Values with no exact half at the cut-off: any rounding mode agrees.
expect("task", (1_500_000_000,), {}, "1.5 GB")
expect("task", (2_000_000_000,), {}, "2.0 GB")
expect("task", (12_340_000_000,), {}, "12.3 GB")
expect("task", (2_000_000_000,), {"precision": 2}, "2.00 GB")

# Exact binary halves at the cut-off: half-up and half-to-even disagree.
expect("f1", (1_250_000_000,), {}, "1.3 GB")
expect("f1", (3_250_000_000,), {}, "3.3 GB")
expect("f1", (10_250_000_000,), {}, "10.3 GB")
expect("f1", (125_000_000,), {"precision": 2}, "0.13 GB")

print(json.dumps({"fact": "f1", "ok": ok["f1"], "why": "; ".join(why["f1"]) or "halves round up"}))
print(json.dumps({"task": ok["task"], "why": "; ".join(why["task"])}))
sys.exit(0 if all(ok.values()) else 1)
