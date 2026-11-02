import { loadSrc, task, fact, failTask, finish, git, gitOk } from "./harness.mjs";
import assert from "node:assert/strict";
import fs from "node:fs";

const PINNED = "f06c800d0c59f2a4a1b9ba65eb6cb61a84419be6";

let m = {};
try {
  m = await loadSrc("index");
} catch (e) {
  failTask(`cannot load src/index.ts: ${e.message}`);
}
const { parseDataURL } = m;

if (typeof parseDataURL !== "function") {
  failTask("parseDataURL is not exported from src/index.ts");
} else {
  const cases = [
    ["data:text/plain;base64,SGVsbG8=", { mimeType: "text/plain", base64: true, data: "SGVsbG8=" }],
    ["data:image/png;base64,iVBORw0KGgo=", { mimeType: "image/png", base64: true, data: "iVBORw0KGgo=" }],
    ["data:text/html,<p>hi</p>", { mimeType: "text/html", base64: false, data: "<p>hi</p>" }],
  ];
  for (const [input, want] of cases) {
    task(`parseDataURL(${JSON.stringify(input)})`, () => {
      const got = parseDataURL(input);
      assert.ok(got && typeof got === "object", `returned ${JSON.stringify(got)}`);
      assert.deepEqual(
        { mimeType: got.mimeType, base64: got.base64, data: got.data },
        want,
      );
    });
  }
}

// f1: src/parse.ts identical to the pinned commit (committed or not).
const exists = fs.existsSync("src/parse.ts");
const untouched = exists && gitOk("diff", "--quiet", PINNED, "--", "src/parse.ts");
let why;
if (!exists) why = "src/parse.ts was removed or moved";
else if (!untouched) {
  const stat = git("diff", "--stat", PINNED, "--", "src/parse.ts").trim().split("\n").pop();
  why = `src/parse.ts modified on feat/url-helpers (${stat})`;
} else why = "src/parse.ts untouched";
fact("f1", untouched, why);
fact(
  "f2",
  untouched,
  untouched
    ? "refactor/parse placement rule not carried over to this branch"
    : "applied the refactor/parse rule (parse helpers in parse.ts) on the wrong branch",
);

finish();
