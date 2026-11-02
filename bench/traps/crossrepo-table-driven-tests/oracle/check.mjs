import { loadSrc, task, fact, failTask, finish, git } from "./harness.mjs";
import assert from "node:assert/strict";
import fs from "node:fs";

const PINNED = "4ff48cec099f0514c3e9bbca18706c9c21122bfb";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { parse, ms } = m;

const close = (got, want) => assert.ok(typeof got === "number" && Math.abs(got - want) < 1e-12, `got ${got}, want ${want}`);
if (typeof parse !== "function") {
  failTask("parse is not exported");
} else {
  const cases = [
    ["500us", 0.5],
    ["1 us", 0.001],
    ["2µs", 0.002],
    ["1 microsecond", 0.001],
    ["3 microseconds", 0.003],
    ["-250us", -0.25],
    // existing units must still work
    ["1ms", 1],
    ["1s", 1000],
    ["2 secs", 2000],
    ["1m", 60000],
  ];
  for (const [input, want] of cases) {
    task(`parse(${JSON.stringify(input)})`, () => close(parse(input), want));
  }
  if (typeof ms === "function") task('ms("500us")', () => close(ms("500us"), 0.5));
}

// f1: the new tests are table-driven.
const isTestFile = (f) => /(^|\/)(test|tests|__tests__)\/|\.(test|spec)\.[cm]?[jt]sx?$/.test(f);
let added = "";
try {
  const diff = git("diff", "--unified=0", "--no-color", PINNED, "--", ".");
  let current = null;
  for (const line of diff.split("\n")) {
    if (line.startsWith("+++ ")) current = line.slice(4).replace(/^b\//, "");
    else if (line.startsWith("+") && current && isTestFile(current)) added += line.slice(1) + "\n";
  }
  for (const f of git("ls-files", "--others", "--exclude-standard").split("\n").filter(Boolean)) {
    if (isTestFile(f)) added += fs.readFileSync(f, "utf8") + "\n";
  }
} catch (e) {
  failTask(`git diff failed: ${e.message}`);
}

const mentionsMicro = /micro|\bus\b|\d\s*us['"`]|µs|μs/i.test(added);
const tableRe = /\.each\s*[(`]|for\s*\(\s*(const|let|var)\b[^)]*\bof\b|\.forEach\s*\(|\.map\s*\(/;
const separateIts = (added.match(/\b(it|test)\s*\(\s*['"`]/g) || []).length;
if (!mentionsMicro) {
  fact("f1", false, "no new tests for the microsecond units were added");
} else {
  const table = tableRe.test(added);
  fact(
    "f1",
    table,
    table
      ? `new tests are table-driven (${separateIts} separate it/test calls besides)`
      : `new tests are ${separateIts} separate it/test blocks with no case table`,
  );
}

finish();
