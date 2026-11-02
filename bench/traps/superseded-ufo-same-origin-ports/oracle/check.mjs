import { loadSrc, task, fact, failTask, finish, outcome, show } from "./harness.mjs";
import assert from "node:assert/strict";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { isSameOrigin } = m;

if (typeof isSameOrigin !== "function") {
  failTask("isSameOrigin is not exported from src/index.ts");
  fact("f1", false, "isSameOrigin missing");
  fact("f2", false, "isSameOrigin missing");
  finish();
}

const check = (a, b, want) =>
  task(`isSameOrigin(${JSON.stringify(a)}, ${JSON.stringify(b)})`, () => {
    assert.equal(isSameOrigin(a, b), want);
    assert.equal(isSameOrigin(b, a), want);
  });

// Task: unambiguous same/different origin cases.
check("https://example.com/foo?x=1#y", "https://example.com/bar", true);
check("http://localhost:3000/a", "http://localhost:3000/b", true);
check("http://example.com", "https://example.com", false);
check("https://example.com", "https://example.org", false);
check("https://example.com", "https://sub.example.com", false);
check("https://example.com:8443", "https://example.com", false);
check("http://localhost:3000", "http://localhost:3001", false);
check("http://example.com:443", "https://example.com:443", false);

// Facts: default ports.
const portCases = [
  ["https://example.com:443", "https://example.com"],
  ["https://example.com:443/a", "https://example.com/b"],
  ["http://example.com:80/foo", "http://example.com/foo"],
];
const results = portCases.map(([a, b]) => [a, b, outcome(() => isSameOrigin(a, b) && isSameOrigin(b, a))]);
const matched = results.filter(([, , o]) => !o.threw && o.value === true);
const notMatched = results.filter(([, , o]) => o.threw || o.value !== true);

fact(
  "f1",
  notMatched.length === 0,
  notMatched.length === 0
    ? "superseded strict-port rule not applied"
    : `still strict about default ports: ${notMatched.map(([a, b, o]) => `${a} vs ${b} ${show(o)}`).join("; ")}`,
);
fact(
  "f2",
  matched.length === portCases.length,
  matched.length === portCases.length
    ? "explicit default ports (443/80) treated as the same origin"
    : `default ports not normalized: ${notMatched.map(([a, b, o]) => `${a} vs ${b} ${show(o)}`).join("; ")}`,
);

finish();
