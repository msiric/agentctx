import { loadSrc, task, fact, failTask, finish, outcome, show } from "./harness.mjs";
import assert from "node:assert/strict";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { parseClock, parseCompound } = m;

if (typeof parseClock !== "function") {
  failTask("parseClock is not exported from src/index.ts");
  fact("f1", false, "parseClock missing");
  fact("f2", false, "parseClock missing");
  finish();
}

// Task: valid timer strings parse correctly.
const valid = [
  ["1:30", 90000],
  ["0:05", 5000],
  ["10:00", 600000],
  ["01:02:03", 3723000],
  ["2:00:00", 7200000],
];
for (const [input, want] of valid) {
  task(`parseClock(${JSON.stringify(input)})`, () => assert.equal(parseClock(input), want));
}

// Facts: what happens on bad input.
const bad = ["", "abc", "1:2:3:4", "1:ab", "::"];
const outcomes = bad.map((input) => [input, outcome(() => parseClock(input))]);
const threw = outcomes.filter(([, o]) => o.threw);
const notUndefined = outcomes.filter(([, o]) => o.threw || o.value !== undefined);

fact(
  "f1",
  threw.length === 0,
  threw.length === 0
    ? "parseClock does not throw on bad input (old policy not carried over)"
    : `parseClock still follows the superseded throw policy: ${threw.map(([i, o]) => `${JSON.stringify(i)} ${show(o)}`).join("; ")}`,
);

const compound =
  typeof parseCompound === "function" ? outcome(() => parseCompound("abc")) : null;
const why = [];
if (notUndefined.length) {
  why.push(
    `parseClock bad input not undefined: ${notUndefined.map(([i, o]) => `${JSON.stringify(i)} ${show(o)}`).join("; ")}`,
  );
}
if (!compound) why.push("parseCompound is no longer exported");
else if (!compound.threw) why.push(`parseCompound("abc") should still throw but ${show(compound)}`);
fact("f2", why.length === 0, why.length ? why.join(" | ") : "parseClock returns undefined on bad input; parseCompound still throws");

finish();
