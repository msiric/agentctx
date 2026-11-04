"""Scores the last session: a Length(min, max) string validator exists and works
(task), and its bounds count UTF-8 bytes rather than characters (f1)."""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
ok = {"task": True, "f1": True}
why = {"task": [], "f1": []}


def fail(key, msg):
    ok[key] = False
    why[key].append(msg)


try:
    import schema
    from schema import Schema, SchemaError

    Length = getattr(schema, "Length")
except Exception as e:  # noqa: BLE001
    print(json.dumps({"fact": "f1", "ok": False, "why": "cannot import Length: %r" % (e,)}))
    print(json.dumps({"task": False}))
    sys.exit(1)


def verdict(kwargs, value):
    """True if accepted (returned unchanged), False if rejected with SchemaError, None otherwise."""
    try:
        v = Length(**kwargs)
    except Exception as e:  # noqa: BLE001
        return "construct-error %r" % (e,)
    try:
        out = Schema(v).validate(value)
    except SchemaError:
        return False
    except Exception as e:  # noqa: BLE001
        return "error %r" % (e,)
    return True if out == value else "returned %r" % (out,)


# Plain ASCII: bytes == characters, so any reasonable implementation agrees.
task_cases = [
    ({"max": 5}, "hello", True),
    ({"max": 5}, "hello!", False),
    ({"min": 1}, "", False),
    ({"min": 2}, "a", False),
    ({"min": 1, "max": 3}, "abc", True),
    ({"min": 1, "max": 3}, "abcd", False),
    ({"max": 10}, "", True),
]
for kwargs, value, want in task_cases:
    got = verdict(kwargs, value)
    if got is not want:
        fail("task", "Length(%s) on %r: want %s, got %s" % (kwargs, value, want, got))

# Multi-byte text: a UTF-8 byte count and a character count disagree.
fact_cases = [
    ({"max": 5}, "héllo", False),       # 5 chars, 6 bytes
    ({"max": 6}, "héllo", True),
    ({"max": 4}, "日本", False),     # 2 chars, 6 bytes
    ({"min": 4}, "éé", True),      # 2 chars, 4 bytes
    ({"min": 1, "max": 7}, "Zoë Mü", False),  # 6 chars, 8 bytes
]
for kwargs, value, want in fact_cases:
    got = verdict(kwargs, value)
    if got is not want:
        fail("f1", "Length(%s) on %r (%d chars, %d UTF-8 bytes): want %s, got %s"
             % (kwargs, value, len(value), len(value.encode("utf-8")), want, got))

print(json.dumps({"fact": "f1", "ok": ok["f1"], "why": "; ".join(why["f1"]) or "bounds count UTF-8 bytes"}))
print(json.dumps({"task": ok["task"], "why": "; ".join(why["task"])}))
sys.exit(0 if all(ok.values()) else 1)
