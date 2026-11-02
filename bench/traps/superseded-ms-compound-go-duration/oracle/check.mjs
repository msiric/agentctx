// Scores the last session: the compound format option is finished (docs +
// working output) and its output follows the NEWER decision from session 2
// (Go time.ParseDuration-compatible: no separators, hours as the largest
// unit), not the original session-1 shape ("1d 1h 30m").
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { register } from 'node:module';
import { pathToFileURL } from 'node:url';

try {
  register('./ts-resolve.mjs', import.meta.url);
} catch {}

const emit = (o) => console.log(JSON.stringify(o));
const fail = (why) => {
  emit({ task: false, why });
  emit({ fact: 'f1', ok: false, why: 'not checked' });
  emit({ fact: 'f2', ok: false, why: 'not checked' });
  process.exit(1);
};

let mod;
try {
  mod = await import(pathToFileURL(path.resolve('src/index.ts')).href);
} catch (e) {
  fail(`cannot import src/index.ts: ${e.message}`);
}
if (typeof mod.format !== 'function') fail('src/index.ts has no format export');

const compound = (v) => {
  try {
    return String(mod.format(v, { compound: true }));
  } catch (e) {
    return `THROW ${e.message}`;
  }
};

// Lenient reader for any reasonable compound rendering ("1d 1h", "25h1m", ...).
const UNIT = { ms: 1, s: 1e3, m: 6e4, h: 36e5, d: 864e5 };
function lenient(str) {
  let s = str.replace(/[\s,]+/g, '');
  let sign = 1;
  if (s.startsWith('-')) {
    sign = -1;
    s = s.slice(1);
  }
  if (!/^(\d+(ms|d|h|m|s))+$/.test(s)) return NaN;
  let total = 0;
  for (const m of s.matchAll(/(\d+)(ms|d|h|m|s)/g)) total += Number(m[1]) * UNIT[m[2]];
  return sign * total;
}

const values = [5400000, 90061000, 45000, 7200000, 3723000, 172800000, 694861000, -5400000, -90061000];
const outputs = values.map((v) => [v, compound(v)]);

// ---- task: compound option works and is documented
const wrong = outputs.filter(([v, o]) => lenient(o) !== v);
const readme = existsSync('README.md') ? readFileSync('README.md', 'utf8') : '';
const documented = /compound/i.test(readme);
const taskOk = wrong.length === 0 && documented;
emit({
  task: taskOk,
  why: taskOk
    ? 'compound output encodes the right durations and README documents it'
    : `${wrong.length ? `wrong compound output: ${JSON.stringify(wrong.slice(0, 3))}` : ''}${documented ? '' : ' README does not mention compound'}`.trim(),
});

// ---- f2 (current decision): ParseDuration-compatible
const goShape = /^-?(?=\d)(\d+h)?(\d+m)?(\d+s)?(\d+ms)?$/;
const notGo = outputs.filter(([v, o]) => !goShape.test(o) || lenient(o) !== v);
const f2 = notGo.length === 0;
emit({
  fact: 'f2',
  ok: f2,
  why: f2 ? 'e.g. ' + JSON.stringify(outputs.slice(0, 2)) : `not time.ParseDuration-compatible: ${JSON.stringify(notGo.slice(0, 3))}`,
});

// ---- f1 (superseded decision) must no longer shape the output
const stale = outputs.filter(([, o]) => /\d[a-z]+ +\d/.test(o) || /\dd/.test(o));
const f1 = stale.length === 0;
emit({
  fact: 'f1',
  ok: f1,
  why: f1 ? 'superseded space/day format not used' : `still uses the superseded format: ${JSON.stringify(stale.slice(0, 3))}`,
});

process.exit(taskOk && f2 && f1 ? 0 : 1);
