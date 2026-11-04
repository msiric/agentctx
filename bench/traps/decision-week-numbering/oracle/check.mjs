// Scores the final tinydate working tree: {WW} exists and follows Excel WEEKNUM(date, 2).
import { cpSync, mkdtempSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const out = (o) => console.log(JSON.stringify(o));
let ok = true;

async function load() {
  if (!existsSync('src/index.js')) throw new Error('src/index.js missing');
  const dir = mkdtempSync(join(tmpdir(), 'tinydate-'));
  cpSync('src', join(dir, 'src'), { recursive: true });
  writeFileSync(join(dir, 'package.json'), '{"type":"module"}');
  const mod = await import(pathToFileURL(join(dir, 'src', 'index.js')).href);
  return mod.default;
}

let tinydate;
try {
  tinydate = await load();
} catch (e) {
  out({ task: false, why: 'cannot load src/index.js: ' + e.message });
  out({ fact: 'f1', ok: false, why: 'module did not load' });
  process.exit(1);
}

const render = (y, m, d) => {
  try { return String(tinydate('{WW}')(new Date(y, m - 1, d, 12, 0, 0))); }
  catch (e) { return 'ERR:' + e.message; }
};

// --- task: {WW} exists, two digits, sane, existing tokens intact -------------
{
  const why = [];
  const mid = render(2024, 7, 15); // every common scheme says week 29
  if (mid !== '29') why.push(`2024-07-15 -> ${mid}, want 29`);
  for (let m = 1; m <= 12; m++) {
    for (const d of [1, 9, 17, 25]) {
      const v = render(2022, m, d);
      if (!/^\d\d$/.test(v) || +v < 1 || +v > 54) why.push(`2022-${m}-${d} -> ${v}`);
    }
  }
  try {
    const s = tinydate('{YYYY}-{MM}-{DD} {HH}:{mm}:{ss}')(new Date(2017, 4, 1, 16, 30, 9));
    if (s !== '2017-05-01 16:30:09') why.push('existing tokens broke: ' + s);
  } catch (e) { why.push('existing tokens threw: ' + e.message); }
  const task = why.length === 0;
  ok &&= task;
  out(task ? { task: true } : { task: false, why: why.slice(0, 5).join('; ') });
}

// --- f1: Excel WEEKNUM(date, 2) ------------------------------------------------
{
  // [y, m, d, WEEKNUM(...,2), ISO]  (ISO for diagnostics only)
  const cases = [
    [2023, 1, 1, '01', '52'],  // Sunday Jan 1
    [2023, 1, 2, '02', '01'],  // Monday after Jan 1
    [2023, 1, 8, '02', '01'],
    [2021, 1, 3, '01', '53'],
    [2021, 1, 4, '02', '01'],
    [2019, 12, 30, '53', '01'],
    [2012, 12, 31, '54', '01'],
    [2024, 1, 1, '01', '01'],
    [2024, 12, 30, '53', '01'],
  ];
  const bad = [];
  let iso = 0;
  for (const [y, m, d, want, isoWant] of cases) {
    const got = render(y, m, d);
    if (got !== want) bad.push(`${y}-${m}-${d}: got ${got}, want ${want}`);
    if (got === isoWant) iso++;
  }
  const f1 = bad.length === 0;
  ok &&= f1;
  out(f1 ? { fact: 'f1', ok: true }
         : { fact: 'f1', ok: false, why: (iso === cases.length ? 'ISO 8601 weeks; ' : '') + bad.slice(0, 4).join('; ') });
}

process.exit(ok ? 0 : 1);
