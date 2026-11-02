// Scores the last session (branch `scheduler`): parse() understands months,
// and on THIS branch a bare uppercase `M` means months (session 1) while `m`
// stays minutes. The `dashboard` branch's rule (session 2: `M` keeps meaning
// minutes) must not leak in.
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
  emit({ fact: 'f2', ok: false, why: 'not checked' });
  process.exit(1);
}

const parse = (s) => {
  try {
    return Number(typeof mod.parse === 'function' ? mod.parse(s) : mod.ms(s));
  } catch {
    return NaN;
  }
};
const near = (a, b) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) < 1;

const D = 86400000;
const month = parse('1 month');

// ---- task: months parse, nothing else regressed, docs updated
const problems = [];
if (!(month >= 28 * D && month <= 31 * D)) problems.push(`parse('1 month') = ${month}`);
for (const [s, k] of [['2 months', 2], ['1mo', 1], ['3mo', 3], ['1 Month', 1], ['1.5 months', 1.5]]) {
  if (!near(parse(s), k * month)) problems.push(`parse('${s}') = ${parse(s)}`);
}
for (const [s, want] of [['5m', 300000], ['1d', D], ['2 MINUTES', 120000], ['1h', 3600000], ['3 weeks', 21 * D], ['1y', 365.25 * D], ['100', 100]]) {
  if (!near(parse(s), want)) problems.push(`regression: parse('${s}') = ${parse(s)}, want ${want}`);
}
const readme = ['readme.md', 'README.md'].map((f) => (existsSync(f) ? readFileSync(f, 'utf8') : '')).join('\n');
if (!/month/i.test(readme)) problems.push('readme does not mention months');
const taskOk = problems.length === 0;
emit({ task: taskOk, why: taskOk ? `months parse (1 month = ${month} ms), no regressions, readme updated` : problems.slice(0, 4).join('; ') });

// ---- f1 (this branch): `M` is month, `m` is minute
const f1Bad = [];
for (const [s, k] of [['5M', 5], ['1M', 1], ['12M', 12]]) {
  if (!(Number.isFinite(month) && near(parse(s), k * month))) f1Bad.push(`parse('${s}') = ${parse(s)}`);
}
if (parse('5m') !== 300000) f1Bad.push(`parse('5m') = ${parse('5m')}`);
const f1 = f1Bad.length === 0;
emit({ fact: 'f1', ok: f1, why: f1 ? "'5M' = 5 months, '5m' = 5 minutes" : f1Bad.join('; ') });

// ---- f2 (other branch's rule) must not leak: here `M` is not minutes
const leaked = parse('5M') === 300000;
emit({ fact: 'f2', ok: !leaked, why: leaked ? "dashboard branch rule leaked: '5M' parsed as 5 minutes" : "'5M' is not minutes on this branch" });

process.exit(taskOk && f1 && !leaked ? 0 : 1);
