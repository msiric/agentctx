// Scores the last session (branch `storage-app`): parseBytes reads every unit
// prettyBytes knows, and on THIS branch the units without an `i` are powers of
// 1024 (session 1: users paste sizes from Windows Explorer). The
// `billing-svc` branch's strict-SI rule (session 2) must not leak in.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const emit = (o) => console.log(JSON.stringify(o));
const notChecked = () => {
  emit({ fact: 'f1', ok: false, why: 'not checked' });
  emit({ fact: 'f2', ok: false, why: 'not checked' });
  process.exit(1);
};

let mod;
try {
  mod = await import(pathToFileURL(path.resolve('index.js')).href);
} catch (e) {
  emit({ task: false, why: `cannot import index.js: ${e.message}` });
  notChecked();
}
if (typeof mod.parseBytes !== 'function') {
  emit({ task: false, why: 'index.js has no named export parseBytes' });
  notChecked();
}

const parse = (s) => {
  try {
    return Number(mod.parseBytes(s));
  } catch {
    return NaN;
  }
};
const near = (a, b) => Number.isFinite(a) && Math.abs(a - b) <= Math.abs(b) * 1e-12;
const either = (a, k, exp) => near(a, k * 1000 ** exp) || near(a, k * 1024 ** exp);

// ---- task
const problems = [];
for (const [s, want] of [['512', 512], ['512 B', 512], ['1.5 KiB', 1536], ['2 MiB', 2 * 1024 ** 2], ['1 GiB', 1024 ** 3], ['3 TiB', 3 * 1024 ** 4]]) {
  if (!near(parse(s), want)) problems.push(`parseBytes('${s}') = ${parse(s)}, want ${want}`);
}
for (const [s, k, exp] of [['1 kB', 1, 1], ['2.5 MB', 2.5, 2], ['1 GB', 1, 3], ['3 TB', 3, 4], ['1 PB', 1, 5]]) {
  if (!either(parse(s), k, exp)) problems.push(`parseBytes('${s}') = ${parse(s)}`);
}
const readme = existsSync('readme.md') ? readFileSync('readme.md', 'utf8') : '';
if (!/parseBytes/.test(readme)) problems.push('readme does not document parseBytes');
const taskOk = problems.length === 0;
emit({ task: taskOk, why: taskOk ? 'parseBytes reads bytes, binary and plain units; documented' : problems.slice(0, 4).join('; ') });

// ---- f1 (this branch): plain units are powers of 1024
const f1Bad = [];
for (const [s, want] of [['1 MB', 1024 ** 2], ['2 kB', 2048], ['1 KB', 1024], ['1.5 GB', 1.5 * 1024 ** 3], ['1 TB', 1024 ** 4]]) {
  if (!near(parse(s), want)) f1Bad.push(`parseBytes('${s}') = ${parse(s)}, want ${want}`);
}
const f1 = f1Bad.length === 0;
emit({ fact: 'f1', ok: f1, why: f1 ? "plain units are 1024-based ('1 MB' = 1048576)" : f1Bad.slice(0, 3).join('; ') });

// ---- f2 (billing-svc's strict SI) must not leak
const leaked = near(parse('1 MB'), 1e6) || near(parse('1 GB'), 1e9);
emit({ fact: 'f2', ok: !leaked, why: leaked ? "billing-svc rule leaked: '1 MB' read as 1000000" : 'strict-SI rule from the other branch not applied' });

process.exit(taskOk && f1 && !leaked ? 0 : 1);
