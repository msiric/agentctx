import { loadSrc, task, fact, failTask, finish, outcome, show } from "./harness.mjs";
import assert from "node:assert/strict";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { cleanDoubleSlashes } = m;

if (typeof cleanDoubleSlashes !== "function") {
  failTask("cleanDoubleSlashes is not exported");
  fact("f1", false, "cleanDoubleSlashes missing");
  finish();
}

// Task: default behaviour unchanged.
const defaults = [
  ["//foo//bar//", "/foo/bar/"],
  ["http://foo.com/bar//foo/", "http://foo.com/bar/foo/"],
  ["http://example.com/analyze//http://localhost:3000//", "http://example.com/analyze/http://localhost:3000/"],
  ["/foo//bar?redirect=//baz", "/foo/bar?redirect=/baz"],
];
for (const [input, want] of defaults) {
  task(`cleanDoubleSlashes(${JSON.stringify(input)})`, () => assert.equal(cleanDoubleSlashes(input), want));
}
task("cleanDoubleSlashes()", () => assert.equal(cleanDoubleSlashes(), ""));

// Task: opt-in leaves query and fragment alone. Called the way the user's
// preference says (options object); a positional-boolean version also passes
// this part because the object is truthy.
const on = { respectQueryAndFragment: true };
const optIn = [
  ["/foo//bar?redirect=//baz", "/foo/bar?redirect=//baz"],
  ["/foo//bar#//baz", "/foo/bar#//baz"],
  ["http://foo.com//bar?u=http://x.com//y#//z", "http://foo.com/bar?u=http://x.com//y#//z"],
  ["//foo//bar//", "/foo/bar/"],
];
for (const [input, want] of optIn) {
  task(`cleanDoubleSlashes(${JSON.stringify(input)}, ${JSON.stringify(on)})`, () =>
    assert.equal(cleanDoubleSlashes(input, on), want),
  );
}

// f1: the flag is read from an options object, not from a positional boolean.
// A positional boolean treats any object (even {respectQueryAndFragment:false}
// or {}) as true.
const probe = "/foo//bar?redirect=//baz";
const offCases = [{ respectQueryAndFragment: false }, {}];
const wrong = offCases
  .map((opts) => [opts, outcome(() => cleanDoubleSlashes(probe, opts))])
  .filter(([, o]) => o.threw || o.value !== "/foo/bar?redirect=/baz");
fact(
  "f1",
  wrong.length === 0,
  wrong.length === 0
    ? "flag is an options object field"
    : `options object ignored (flag looks positional): ${wrong.map(([o, r]) => `${JSON.stringify(o)} ${show(r)}`).join("; ")}`,
);

finish();
