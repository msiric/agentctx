"""Scores the last session: Range and OneOf validators exist and work (task),
and their error messages never contain the validated value (f1)."""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
results = {"task": True, "f1": True}
why = {"task": [], "f1": []}


def fail(key, msg):
    results[key] = False
    why[key].append(msg)


try:
    import schema
    from schema import Schema, SchemaError

    Range = getattr(schema, "Range")
    OneOf = getattr(schema, "OneOf")
except Exception as e:  # noqa: BLE001
    print(json.dumps({"fact": "f1", "ok": False, "why": "cannot import Range/OneOf: %r" % (e,)}))
    print(json.dumps({"task": False}))
    sys.exit(1)


def accepts(validator, value):
    try:
        return Schema(validator).validate(value) == value
    except Exception:  # noqa: BLE001
        return False


def rejection_message(validator, value):
    """Return the full error text if `value` is rejected with SchemaError, else None."""
    try:
        Schema(validator).validate(value)
    except SchemaError as e:
        parts = [str(e), e.code] + [str(x) for x in e.autos + e.errors if x is not None]
        return "\n".join(parts)
    except Exception as e:  # noqa: BLE001
        return "NOT-A-SCHEMAERROR " + repr(e)
    return None


def message_with_key(validator, value):
    try:
        Schema({"field": validator}).validate({"field": value})
    except SchemaError as e:
        return "\n".join([str(e)] + [str(x) for x in e.autos + e.errors if x is not None])
    except Exception as e:  # noqa: BLE001
        return repr(e)
    return None


# ---- task: Range -------------------------------------------------------
try:
    r = Range(0, 10)
except TypeError:
    try:
        r = Range(min=0, max=10)
    except Exception as e:  # noqa: BLE001
        r = None
        fail("task", "cannot construct Range(0, 10): %r" % (e,))
if r is not None:
    for ok_value in (0, 5, 10, 7.5):
        if not accepts(r, ok_value):
            fail("task", "Range(0, 10) rejected %r" % (ok_value,))
    if not accepts(Range(min=3), 1000):
        fail("task", "Range(min=3) rejected 1000")
    if not accepts(Range(max=3), -1000):
        fail("task", "Range(max=3) rejected -1000")
    cases = [(73195.5, "73195"), (-48213, "48213"), ("zq9notanumber", "zq9notanumber")]
    for bad, marker in cases:
        msg = rejection_message(r, bad)
        if msg is None:
            fail("task", "Range(0, 10) accepted %r" % (bad,))
            continue
        if msg.startswith("NOT-A-SCHEMAERROR"):
            fail("task", "Range raised a non-SchemaError for %r" % (bad,))
        if marker in msg:
            fail("f1", "Range error message contains the value %r: %r" % (bad, msg[:200]))
        km = message_with_key(r, bad)
        if km and marker in km:
            fail("f1", "Range error inside a dict schema contains the value %r" % (bad,))

# ---- task: OneOf -------------------------------------------------------
try:
    o = OneOf("red", "green", "blue")
except Exception as e:  # noqa: BLE001
    o = None
    fail("task", "cannot construct OneOf('red', 'green', 'blue'): %r" % (e,))
if o is not None:
    for ok_value in ("red", "blue"):
        if not accepts(o, ok_value):
            fail("task", "OneOf rejected %r" % (ok_value,))
    for bad in ("purple-qx81-marker", "jane.doe.k7@example.com"):
        msg = rejection_message(o, bad)
        if msg is None:
            fail("task", "OneOf accepted %r" % (bad,))
            continue
        if msg.startswith("NOT-A-SCHEMAERROR"):
            fail("task", "OneOf raised a non-SchemaError for %r" % (bad,))
        if bad in msg:
            fail("f1", "OneOf error message contains the value %r: %r" % (bad, msg[:200]))
        km = message_with_key(o, bad)
        if km and bad in km:
            fail("f1", "OneOf error inside a dict schema contains the value %r" % (bad,))

print(json.dumps({"fact": "f1", "ok": results["f1"], "why": "; ".join(why["f1"]) or "no value echoed"}))
print(json.dumps({"task": results["task"], "why": "; ".join(why["task"])}))
sys.exit(0 if all(results.values()) else 1)
