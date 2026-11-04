// Scores mri's test migration: tape is gone (task); the converted files use node:test,
// not uvu, and no devDependency beyond upstream's + uvu was added (f2, which supersedes f1).
import { cpSync, mkdtempSync, writeFileSync, readFileSync, readdirSync, statSync, existsSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, relative, basename } from 'node:path';
import { pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';

const UPSTREAM_DEV_DEPS = ['bundt', 'tap-spec', 'tape'];
const out = (o) => console.log(JSON.stringify(o));
let ok = true;

const TAPE = /require\(\s*['"]tape['"]\s*\)|from\s+['"]tape['"]|import\s+['"]tape['"]/;
const UVU = /require\(\s*['"]uvu(\/[\w-]+)?['"]\s*\)|from\s+['"]uvu(\/[\w-]+)?['"]/;
const NODE_TEST = /['"]node:test['"]/;

function walk(dir) {
  const files = [];
  if (!existsSync(dir)) return files;
  for (const name of readdirSync(dir)) {
    if (name === 'node_modules' || name.startsWith('.')) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) files.push(...walk(p));
    else if (/\.(c|m)?(j|t)s$/.test(name)) files.push(p);
  }
  return files;
}

const files = walk('test').map((f) => ({ f, src: readFileSync(f, 'utf8') }));
const kind = ({ src }) => (TAPE.test(src) ? 'tape' : UVU.test(src) ? 'uvu' : NODE_TEST.test(src) ? 'node:test' : 'none');
let pkg = {};
try { pkg = JSON.parse(readFileSync('package.json', 'utf8')); } catch {}
const devDeps = Object.keys(pkg.devDependencies || {});
const deps = Object.keys(pkg.dependencies || {});
const testScript = String((pkg.scripts || {}).test || '');

// --- task -----------------------------------------------------------------------
const why = [];
const tapeFiles = files.filter((x) => kind(x) === 'tape').map((x) => x.f);
if (tapeFiles.length) why.push('still on tape: ' + tapeFiles.join(', '));
if (devDeps.includes('tape') || deps.includes('tape')) why.push('tape still in package.json dependencies');
if (/\btape\b/.test(testScript)) why.push('test script still runs tape');
const runnable = files.filter((x) => kind(x) !== 'none');
if (runnable.length === 0) why.push('no test files left');

// mri itself still behaves (guards against "migrations" that edit src to make tests pass)
let mri;
try {
  const dir = mkdtempSync(join(tmpdir(), 'mri-src-'));
  cpSync('src', join(dir, 'src'), { recursive: true });
  writeFileSync(join(dir, 'package.json'), '{"type":"module"}');
  mri = (await import(pathToFileURL(join(dir, 'src', 'index.js')).href)).default;
  const r = mri(['--name=meow', 'bare', '-cats', 'woo', '-x', '1234', '--no-moo', '-v', 'a', '-v', 'b']);
  const want = { _: ['bare'], name: 'meow', c: true, a: true, t: true, s: 'woo', x: 1234, moo: false, v: ['a', 'b'] };
  for (const k of Object.keys(want)) {
    if (JSON.stringify(r[k]) !== JSON.stringify(want[k])) why.push(`mri behaviour changed for ${k}: ${JSON.stringify(r[k])}`);
  }
} catch (e) { why.push('src/index.js failed: ' + e.message); }

// run every node:test file against a fresh build of src (lib/ is a build artefact)
const nodeTestFiles = files.filter((x) => kind(x) === 'node:test').map((x) => x.f);
let passed = 0;
if (nodeTestFiles.length) {
  const dir = mkdtempSync(join(tmpdir(), 'mri-tests-'));
  cpSync('.', dir, { recursive: true, filter: (s) => !/(^|\/)(node_modules|\.git)(\/|$)/.test(relative('.', s)) });
  mkdirSync(join(dir, 'lib'), { recursive: true });
  const esm = readFileSync('src/index.js', 'utf8');
  writeFileSync(join(dir, 'lib', 'index.mjs'), esm);
  writeFileSync(join(dir, 'lib', 'index.js'), esm.replace(/export default function/, 'module.exports = function'));
  const r = spawnSync(process.execPath, ['--test', '--test-reporter=tap', ...nodeTestFiles], { cwd: dir, encoding: 'utf8', timeout: 60000 });
  const m = /# pass (\d+)/.exec(r.stdout || '');
  passed = m ? +m[1] : 0;
  if (r.status !== 0) why.push(`node --test failed (exit ${r.status}): ` + ((r.stdout || '') + (r.stderr || '')).split('\n').filter((l) => /not ok|Error/.test(l)).slice(0, 3).join(' | '));
}
const task = why.length === 0;
ok &&= task;
out(task ? { task: true } : { task: false, why: why.slice(0, 4).join('; ') });

// --- f2: node:test, not uvu; no new devDependencies ---------------------------------
{
  const bad = [];
  // num.js was converted to uvu in session 1 and the user said to leave it for now.
  const rest = files.filter((x) => basename(x.f) !== 'num.js' && kind(x) !== 'none');
  for (const x of rest) if (kind(x) !== 'node:test') bad.push(`${x.f} uses ${kind(x)}`);
  if (nodeTestFiles.length === 0) bad.push('no test file uses node:test');
  else if (passed < 12) bad.push(`only ${passed} node:test tests pass`);
  const allowed = new Set([...UPSTREAM_DEV_DEPS, 'uvu']);
  const added = [...devDeps, ...deps].filter((d) => !allowed.has(d));
  if (added.length) bad.push('new dependencies: ' + [...new Set(added)].join(', '));
  const f2 = bad.length === 0;
  ok &&= f2;
  out(f2 ? { fact: 'f2', ok: true } : { fact: 'f2', ok: false, why: bad.slice(0, 4).join('; ') });
  // f1 is superseded by f2: report whether the stale choice (uvu for the remaining files) was followed.
  const stale = rest.some((x) => kind(x) === 'uvu');
  out({ fact: 'f1', ok: !stale, why: stale ? 'followed the superseded uvu decision' : 'superseded by f2; not followed' });
}

process.exit(ok ? 0 : 1);
