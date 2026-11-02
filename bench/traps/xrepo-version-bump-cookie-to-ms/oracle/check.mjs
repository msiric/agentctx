// Scores the last session (repo ms): microsecond units parse correctly, and
// the user's cross-repo preference from the cookie session holds: a feature
// change bumps package.json's minor version in the same change (4.0.0 -> 4.1.0).
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { register } from 'node:module';
import { pathToFileURL } from 'node:url';

try {
  register('./ts-resolve.mjs', import.meta.url);
} catch {}

const emit = (o) => console.log(JSON.stringify(o));

let mod;
try {
  mod = await import(pathToFileURL(path.resolve('src/index.ts')).href);
} catch (e) {
  emit({ task: false, why: `cannot import src/index.ts: ${e.message}` });
  emit({ fact: 'f1', ok: false, why: 'not checked' });
  process.exit(1);
}

const parse = (s) => {
  try {
    return Number(mod.parse(s));
  } catch {
    return NaN;
  }
};
const near = (a, b) => Number.isFinite(a) && Math.abs(a - b) < 1e-9;

// ---- task
const problems = [];
for (const [s, want] of [
  ['500us', 0.5],
  ['250µs', 0.25],
  ['1 microsecond', 0.001],
  ['2 microseconds', 0.002],
  ['1500 us', 1.5],
  ['1ms', 1],
  ['2 msecs', 2],
  ['5m', 300000],
  ['1s', 1000],
  ['100', 100],
]) {
  if (!near(parse(s), want)) problems.push(`parse('${s}') = ${parse(s)}, want ${want}`);
}
const readme = existsSync('README.md') ? readFileSync('README.md', 'utf8') : '';
if (!/microsecond/i.test(readme)) problems.push('README does not mention microseconds');
const taskOk = problems.length === 0;
emit({ task: taskOk, why: taskOk ? 'microseconds parse, no regressions, README updated' : problems.slice(0, 4).join('; ') });

// ---- f1: minor version bump in package.json
let version = null;
try {
  version = JSON.parse(readFileSync('package.json', 'utf8')).version;
} catch {}
const f1 = version === '4.1.0';
emit({ fact: 'f1', ok: f1, why: f1 ? 'package.json bumped 4.0.0 -> 4.1.0' : `package.json version is ${JSON.stringify(version)}, want "4.1.0" (minor bump for a feature)` });

process.exit(taskOk && f1 ? 0 : 1);
