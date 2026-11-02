import { loadSrc, task, failTask, finish } from "./harness.mjs";
import assert from "node:assert/strict";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { constantCase, snakeCase } = m;

if (typeof constantCase !== "function") {
  failTask("constantCase is not exported from src/index.ts");
} else {
  const cases = [
    ["foo", "FOO"],
    ["fooBar", "FOO_BAR"],
    ["FooBarBaz", "FOO_BAR_BAZ"],
    ["foo-bar_baz", "FOO_BAR_BAZ"],
    ["foo.bar/baz", "FOO_BAR_BAZ"],
    ["FOO_BAR", "FOO_BAR"],
  ];
  for (const [input, want] of cases) {
    task(`constantCase(${JSON.stringify(input)})`, () => assert.equal(constantCase(input), want));
  }
  task('constantCase("")', () => assert.equal(constantCase(""), ""));
}
// existing behaviour untouched
if (typeof snakeCase === "function") {
  task('snakeCase("FooBarBaz")', () => assert.equal(snakeCase("FooBarBaz"), "foo_bar_baz"));
}

finish();
