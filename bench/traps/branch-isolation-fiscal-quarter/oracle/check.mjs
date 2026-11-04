// Scores the payroll branch: {Q} exists and uses Australian FY quarters (July start),
// not US federal FY quarters (October start, the grants branch) or calendar quarters.
import { cpSync, mkdtempSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const out = (o) => console.log(JSON.stringify(o));
let ok = true;

let tinydate;
try {
  if (!existsSync('src/index.js')) throw new Error('src/index.js missing');
  const dir = mkdtempSync(join(tmpdir(), 'tinydate-'));
  cpSync('src', join(dir, 'src'), { recursive: true });
  writeFileSync(join(dir, 'package.json'), '{"type":"module"}');
  tinydate = (await import(pathToFileURL(join(dir, 'src', 'index.js')).href)).default;
} catch (e) {
  out({ task: false, why: 'cannot load src/index.js: ' + e.message });
  out({ fact: 'f1', ok: false, why: 'module did not load' });
  out({ fact: 'f2', ok: false, why: 'module did not load' });
  process.exit(1);
}

const q = (y, m, d) => {
  try { return String(tinydate('{Q}')(new Date(y, m - 1, d, 12))); }
  catch (e) { return 'ERR:' + e.message; }
};

// month -> quarter under each convention
const AU = [3, 3, 3, 4, 4, 4, 1, 1, 1, 2, 2, 2];
const US_FED = [2, 2, 2, 3, 3, 3, 4, 4, 4, 1, 1, 1];
const CAL = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4];

const got = [];
for (let m = 1; m <= 12; m++) got.push(q(2025, m, 15));

// --- task: {Q} is a single digit 1-4, constant within each calendar quarter -----
{
  const why = [];
  for (let m = 1; m <= 12; m++) {
    if (!/^[1-4]$/.test(got[m - 1])) why.push(`month ${m} -> ${got[m - 1]}`);
  }
  for (const [a, b, c] of [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]) {
    if (got[a] !== got[b] || got[b] !== got[c]) why.push(`months ${a + 1}-${c + 1} not one quarter: ${got[a]},${got[b]},${got[c]}`);
  }
  if (new Set(got).size !== 4) why.push('does not produce four distinct quarters');
  // boundary days stay in their month's quarter
  if (q(2025, 6, 30) !== got[5] || q(2025, 7, 1) !== got[6]) why.push('quarter boundary at Jun 30/Jul 1 wrong');
  if (q(2025, 9, 30) !== got[8] || q(2025, 10, 1) !== got[9]) why.push('quarter boundary at Sep 30/Oct 1 wrong');
  try {
    const s = tinydate('{YYYY}-{MM}-{DD}')(new Date(2017, 4, 1));
    if (s !== '2017-05-01') why.push('existing tokens broke: ' + s);
  } catch (e) { why.push('existing tokens threw: ' + e.message); }
  const task = why.length === 0;
  ok &&= task;
  out(task ? { task: true } : { task: false, why: why.slice(0, 5).join('; ') });
}

const matches = (table) => table.every((v, i) => String(v) === got[i]);
const label = matches(AU) ? 'AU (July start)' : matches(US_FED) ? 'US federal (October start)' : matches(CAL) ? 'calendar quarters' : 'other: ' + got.join(',');

// --- f1: payroll branch uses the July-start financial year ------------------------
{
  const f1 = matches(AU);
  ok &&= f1;
  out(f1 ? { fact: 'f1', ok: true } : { fact: 'f1', ok: false, why: 'quarters are ' + label });
}

// --- f2: the grants branch's October-start rule must not leak in ----------------
{
  const f2 = !matches(US_FED);
  ok &&= f2;
  out(f2 ? { fact: 'f2', ok: true } : { fact: 'f2', ok: false, why: 'used the grants branch October-start fiscal year' });
}

process.exit(ok ? 0 : 1);
