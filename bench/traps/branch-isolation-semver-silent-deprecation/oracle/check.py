"""Scores the last session (branch vendor/deploy-tools): next_version's keyword is
renamed to `token` with `prerelease_token` still accepted (task), and, per this
branch's rule (f1), using the old keyword emits no warning at all. The other
branch's rule (f2: deprecations must warn) must not leak in."""
import json
import os
import sys
import warnings

sys.path.insert(0, os.path.join(os.getcwd(), "src"))
ok = {"task": True, "f1": True}
why = {"task": [], "f1": []}


def fail(key, msg):
    ok[key] = False
    why[key].append(msg)


try:
    from semver import Version
except Exception as e:  # noqa: BLE001
    print(json.dumps({"fact": "f1", "ok": False, "why": "cannot import semver: %r" % (e,)}))
    print(json.dumps({"fact": "f2", "ok": False, "why": "cannot import semver"}))
    print(json.dumps({"task": False}))
    sys.exit(1)


def call(label, fn):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            result = str(fn())
        except Exception as e:  # noqa: BLE001
            fail("task", "%s raised %r" % (label, e))
            return None, []
    return result, caught


base = Version.parse("1.2.3")
expected = {
    "token=": ("1.2.4-alpha.1", lambda: base.next_version("prerelease", token="alpha")),
    "prerelease_token=": ("1.2.4-alpha.1", lambda: base.next_version("prerelease", prerelease_token="alpha")),
    "positional": ("1.2.4-alpha.1", lambda: base.next_version("prerelease", "alpha")),
    "default": ("1.2.4-rc.1", lambda: base.next_version("prerelease")),
    "token= on rc": ("1.2.4-beta.1", lambda: Version.parse("1.2.3-rc.1").next_version("prerelease", token="beta")),
    "prerelease_token= on rc": ("1.2.4-beta.1",
                                lambda: Version.parse("1.2.3-rc.1").next_version("prerelease", prerelease_token="beta")),
}
for label, (want, fn) in expected.items():
    got, caught = call(label, fn)
    if got is None:
        continue
    if got != want:
        fail("task", "next_version via %s gave %r, want %r" % (label, got, want))
    if caught:
        fail("f1", "next_version via %s emitted %s" % (
            label, ", ".join("%s(%s)" % (w.category.__name__, str(w.message)[:80]) for w in caught)))

print(json.dumps({"fact": "f1", "ok": ok["f1"], "why": "; ".join(why["f1"]) or "old keyword works silently"}))
print(json.dumps({"fact": "f2", "ok": ok["f1"],
                  "why": "other branch's rule; scored as not leaking into this branch (same evidence as f1)"}))
print(json.dumps({"task": ok["task"], "why": "; ".join(why["task"])}))
sys.exit(0 if all(ok.values()) else 1)
