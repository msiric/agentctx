// Scores the last session: `significantDigits` works and is documented, and a
// bad value follows the NEWER rule from session 2 (never throw; ignore it and
// format as if the option were absent), not session 1's "throw a TypeError like
// the other options" which the shipped `unit` option still shows.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const emit = (o) => console.log(JSON.stringify(o));

let prettyBytes;
try {
  prettyBytes = (await import(pathToFileURL(path.resolve('index.js')).href)).default;
} catch (e) {
  emit({ task: false, why: `cannot import index.js: ${e.message}` });
  emit({ fact: 'f1', ok: false, why: 'not checked' });
  emit({ fact: 'f2', ok: false, why: 'not checked' });
  process.exit(1);
}

const run = (n, o) => {
  try {
    return String(prettyBytes(n, o));
  } catch (e) {
    return `THROW ${e?.constructor?.name}: ${e?.message}`;
  }
};

// ---- task
const expected = [
  [1337, { significantDigits: 2 }, '1.3 kB'],
  [1337, { significantDigits: 4 }, '1.337 kB'],
  [1999, { significantDigits: 1 }, '2 kB'],
  [1337, {}, '1.34 kB'],
  [1337, { significantDigits: 3 }, '1.34 kB'],
];
const bad = expected.filter(([n, o, want]) => run(n, o) !== want).map(([n, o, want]) => ({ n, o, want, got: run(n, o) }));
const read = (f) => (existsSync(f) ? readFileSync(f, 'utf8') : '');
const docs = /significantDigits/.test(read('readme.md'));
const types = /significantDigits/.test(read('index.d.ts'));
const taskOk = bad.length === 0 && docs && types;
emit({
  task: taskOk,
  why: taskOk
    ? 'significantDigits works, documented and typed'
    : [bad.length ? `wrong output ${JSON.stringify(bad.slice(0, 3))}` : '', docs ? '' : 'readme lacks significantDigits', types ? '' : 'index.d.ts lacks significantDigits'].filter(Boolean).join('; '),
});

// ---- facts: invalid values
const invalid = [0, -1, 2.5, Number.NaN, Number.POSITIVE_INFINITY, 'two', 101];
const results = invalid.map((v) => [String(v), run(1337, { significantDigits: v })]);
const thrown = results.filter(([, r]) => r.startsWith('THROW'));
const notDefault = results.filter(([, r]) => r !== '1.34 kB');

const f2 = notDefault.length === 0;
emit({
  fact: 'f2',
  ok: f2,
  why: f2 ? 'invalid significantDigits ignored (default output, no throw)' : `invalid values not ignored: ${JSON.stringify(notDefault.slice(0, 4))}`,
});
const f1 = thrown.length === 0;
emit({
  fact: 'f1',
  ok: f1,
  why: f1 ? 'superseded throw-on-invalid rule not applied to the new option' : `new option still throws (superseded rule): ${JSON.stringify(thrown.slice(0, 3))}`,
});

process.exit(taskOk && f1 && f2 ? 0 : 1);
