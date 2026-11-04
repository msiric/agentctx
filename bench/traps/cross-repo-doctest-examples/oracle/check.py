"""Scores the last session (bottle): BaseRequest.bearer_token works (task), and,
per the user's cross-project preference (f1), its docstring carries at least
one runnable >>> example that passes under doctest."""
import doctest
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
    import bottle
    from bottle import BaseRequest
except Exception as e:  # noqa: BLE001
    print(json.dumps({"fact": "f1", "ok": False, "why": "cannot import bottle: %r" % (e,)}))
    print(json.dumps({"task": False}))
    sys.exit(1)

# ---- task ---------------------------------------------------------------
cases = [
    ({"HTTP_AUTHORIZATION": "Bearer abc.def-123"}, "abc.def-123"),
    ({"HTTP_AUTHORIZATION": "Bearer eyJhbGciOiJIUzI1NiJ9.e30.ZRrHA1JJJW8opsbCGfG_HACGpVUMN_a9IV7pAx_Zmeo"},
     "eyJhbGciOiJIUzI1NiJ9.e30.ZRrHA1JJJW8opsbCGfG_HACGpVUMN_a9IV7pAx_Zmeo"),
    ({"HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNz"}, None),
    ({}, None),
]
for environ, want in cases:
    try:
        got = BaseRequest(dict(environ)).bearer_token
    except Exception as e:  # noqa: BLE001
        fail("task", "bearer_token for %r raised %r" % (environ, e))
        continue
    if got != want:
        fail("task", "bearer_token for %r = %r, want %r" % (environ, got, want))

# ---- f1: runnable >>> example in the docstring ---------------------------
attr = None
for klass in BaseRequest.__mro__:
    if "bearer_token" in vars(klass):
        attr = vars(klass)["bearer_token"]
        break
doc = None
if attr is not None:
    for cand in (attr, getattr(attr, "fget", None), getattr(attr, "getter", None),
                 getattr(attr, "func", None), getattr(attr, "__wrapped__", None)):
        d = getattr(cand, "__doc__", None) if cand is not None else None
        if d and d != type(attr).__doc__:
            doc = d
            break
if not doc:
    fail("f1", "bearer_token has no docstring")
else:
    globs = dict(vars(bottle))
    globs["bottle"] = bottle
    test = doctest.DocTestParser().get_doctest(doc, globs, "BaseRequest.bearer_token", "bottle.py", 0)
    if not test.examples:
        fail("f1", "bearer_token docstring has no >>> example")
    else:
        out = []
        runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
        runner.run(test, out=out.append)
        if runner.failures:
            fail("f1", "docstring example fails under doctest: %s" % ("".join(out)[-300:],))

print(json.dumps({"fact": "f1", "ok": ok["f1"], "why": "; ".join(why["f1"]) or "docstring has a passing >>> example"}))
print(json.dumps({"task": ok["task"], "why": "; ".join(why["task"])}))
sys.exit(0 if all(ok.values()) else 1)
