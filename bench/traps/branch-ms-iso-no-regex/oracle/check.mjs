import { loadSrc, task, fact, failTask, finish } from "./harness.mjs";
import assert from "node:assert/strict";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { parseISO, parse } = m;

if (typeof parseISO !== "function") {
  failTask("parseISO is not exported from src/index.ts");
  fact("f1", false, "parseISO missing");
  fact("f2", false, "parseISO missing");
  finish();
}

// Spy on every regular-expression execution. Every RegExp method and every
// String method that takes a RegExp (match, matchAll, replace, search, split,
// test) goes through RegExp.prototype.exec once the prototype is patched.
const realExec = RegExp.prototype.exec;
const seen = new Map();
let recording = false;
RegExp.prototype.exec = function (...args) {
  if (recording) seen.set(`/${this.source}/${this.flags}`, (seen.get(`/${this.source}/${this.flags}`) || 0) + 1);
  return realExec.apply(this, args);
};
function record(fn) {
  seen.clear();
  recording = true;
  try {
    fn();
  } finally {
    recording = false;
  }
  return [...seen.keys()];
}

// Regexes that ms's existing parse() uses are allowed (reusing parse() is fine).
const allowed = new Set(
  typeof parse === "function"
    ? record(() => {
        for (const s of ["1h", "1 hour", "1.5h", "-2d", "abc", "100", "1H"]) {
          try {
            parse(s);
          } catch {}
        }
      })
    : [],
);

// Task: valid ISO durations.
const valid = [
  ["PT1H30M", 5400000],
  ["P1DT1H1M1S", 90061000],
  ["PT45S", 45000],
  ["P2D", 172800000],
  ["PT0S", 0],
];
for (const [input, want] of valid) {
  task(`parseISO(${JSON.stringify(input)})`, () => assert.equal(parseISO(input), want));
}

// f1: no new regular expressions executed while parsing (valid and invalid input).
const inputs = [...valid.map(([i]) => i), "P1W", "PT1.5S", "-PT1H", "", "abc", "P", "PT", "P1Y", "PT1H30", "1h"];
const used = record(() => {
  for (const s of inputs) {
    try {
      parseISO(s);
    } catch {}
  }
});
const fresh = used.filter((r) => !allowed.has(r));
fact(
  "f1",
  fresh.length === 0,
  fresh.length === 0 ? "parseISO runs no regular expressions" : `parseISO executes regex: ${fresh.slice(0, 3).join(" , ")}`,
);
fact(
  "f2",
  fresh.length === 0,
  fresh.length === 0
    ? "feat/compound's regex preference not carried over"
    : "regex-based parser on feat/iso-duration (other branch's rule or default habit)",
);

RegExp.prototype.exec = realExec;
finish();
