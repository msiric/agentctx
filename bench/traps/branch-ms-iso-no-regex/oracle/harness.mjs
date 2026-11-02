// Shared oracle helpers: load a repo's TypeScript sources without a build
// step, run small assertions, and print the per-fact JSON lines.
//
// Loading strategy: if the `typescript` package is reachable (the repo's own
// node_modules after setup.sh, or Node's global modules) every file under
// src/ is transpiled into a temp dir (transpileModule elides type-only
// imports). Otherwise Node's built-in type stripping is used directly.
import { createRequire, register } from "node:module";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

// Resolve extensionless / .js relative specifiers to .mjs / .ts / index.*.
register(
  "data:text/javascript," +
    encodeURIComponent(`
import { existsSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
const isFile = (p) => existsSync(p) && !statSync(p).isDirectory();
export async function resolve(spec, ctx, next) {
  if ((spec.startsWith("./") || spec.startsWith("../")) && ctx.parentURL && ctx.parentURL.startsWith("file:")) {
    const p = fileURLToPath(new URL(spec, ctx.parentURL));
    if (!isFile(p)) {
      const stem = p.replace(/\\.(js|ts|mjs)$/, "");
      for (const c of [stem + ".mjs", stem + ".ts", stem + "/index.mjs", stem + "/index.ts"]) {
        if (isFile(c)) return next(new URL("file://" + c).href, ctx);
      }
    }
  }
  return next(spec, ctx);
}
`),
);

const repo = process.cwd();

function findTypeScript() {
  if (process.env.ORACLE_NO_TS) return null; // force the native type-stripping path
  const candidates = [path.join(repo, "package.json")];
  try {
    candidates.push(
      path.join(
        execFileSync("npm", ["root", "-g"], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim(),
        "noop.js",
      ),
    );
  } catch {}
  candidates.push(path.join(path.dirname(process.execPath), "..", "lib", "node_modules", "noop.js"));
  for (const c of candidates) {
    try {
      return createRequire(c)("typescript");
    } catch {}
  }
  return null;
}

let srcRoot = null;
function prepareSources() {
  if (srcRoot) return srcRoot;
  const ts = findTypeScript();
  if (!ts) {
    srcRoot = { dir: path.join(repo, "src"), ext: ".ts" };
    return srcRoot;
  }
  const out = fs.mkdtempSync(path.join(os.tmpdir(), "oracle-src-"));
  const walk = (rel) => {
    for (const ent of fs.readdirSync(path.join(repo, "src", rel), { withFileTypes: true })) {
      const r = path.join(rel, ent.name);
      if (ent.isDirectory()) {
        walk(r);
        continue;
      }
      if (!/\.(ts|mts)$/.test(ent.name) || /\.d\.ts$/.test(ent.name)) continue;
      const code = fs.readFileSync(path.join(repo, "src", r), "utf8");
      const js = ts.transpileModule(code, {
        fileName: ent.name,
        compilerOptions: {
          module: ts.ModuleKind.ESNext,
          target: ts.ScriptTarget.ES2022,
          isolatedModules: true,
          verbatimModuleSyntax: false,
          sourceMap: false,
        },
      }).outputText;
      const dest = path.join(out, r.replace(/\.(ts|mts)$/, ".mjs"));
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      fs.writeFileSync(dest, js);
    }
  };
  walk("");
  srcRoot = { dir: out, ext: ".mjs" };
  return srcRoot;
}

/** Import src/<name> (default: index) of the repo under test. */
export async function loadSrc(name = "index") {
  const { dir, ext } = prepareSources();
  return import(pathToFileURL(path.join(dir, name + ext)).href);
}

const results = [];
let taskOk = true;
const taskWhy = [];

/** Run fn; record a task failure (with message) if it throws. */
export function task(label, fn) {
  try {
    fn();
  } catch (e) {
    taskOk = false;
    taskWhy.push(`${label}: ${e && e.message ? e.message.split("\n")[0] : e}`);
  }
}

export function fact(id, ok, why) {
  results.push({ fact: id, ok: !!ok, why });
}

export function failTask(why) {
  taskOk = false;
  taskWhy.push(why);
}

export function finish() {
  for (const r of results) console.log(JSON.stringify(r));
  console.log(JSON.stringify(taskOk ? { task: true } : { task: false, why: taskWhy.slice(0, 5).join("; ") }));
  process.exit(taskOk && results.every((r) => r.ok) ? 0 : 1);
}

export function git(...args) {
  return execFileSync("git", args, { cwd: repo, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
}

export function gitOk(...args) {
  try {
    execFileSync("git", args, { cwd: repo, stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

/** Call fn() and describe the outcome: {threw, error} or {value}. */
export function outcome(fn) {
  try {
    return { threw: false, value: fn() };
  } catch (error) {
    return { threw: true, error };
  }
}

export function show(o) {
  if (o.threw) return `threw ${o.error && o.error.name}: ${o.error && o.error.message}`;
  return `returned ${typeof o.value === "number" && Number.isNaN(o.value) ? "NaN" : JSON.stringify(o.value)}`;
}
