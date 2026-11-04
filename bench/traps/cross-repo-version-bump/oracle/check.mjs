// Scores mri: `count` option works (task) and package.json got a minor bump (f1).
import { cpSync, mkdtempSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const out = (o) => console.log(JSON.stringify(o));
let ok = true;

// --- task: opts.count ------------------------------------------------------------
{
  const why = [];
  let mri;
  try {
    if (!existsSync('src/index.js')) throw new Error('src/index.js missing');
    const dir = mkdtempSync(join(tmpdir(), 'mri-'));
    cpSync('src', join(dir, 'src'), { recursive: true });
    writeFileSync(join(dir, 'package.json'), '{"type":"module"}');
    mri = (await import(pathToFileURL(join(dir, 'src', 'index.js')).href)).default;
  } catch (e) { why.push('cannot load src/index.js: ' + e.message); }

  if (mri) {
    const call = (args, opts) => { try { return mri(args, opts); } catch (e) { return { error: e.message }; } };
    const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
    let r = call(['-vvv'], { count: ['v'] });
    if (r.v !== 3) why.push(`-vvv -> v=${JSON.stringify(r.v)}`);
    r = call(['--verbose', '--verbose'], { count: ['verbose'] });
    if (r.verbose !== 2) why.push(`--verbose --verbose -> ${JSON.stringify(r)}`);
    r = call(['-v', '-v'], { count: ['v'] });
    if (r.v !== 2) why.push(`-v -v -> ${JSON.stringify(r)}`);
    r = call(['-v'], { count: ['v'] });
    if (r.v !== 1) why.push(`-v -> v=${JSON.stringify(r.v)}`);
    // unchanged behaviour without the option
    r = call(['-v', 'a', '-v', 'b', '--no-moo']);
    if (!eq(r, { _: [], v: ['a', 'b'], moo: false })) why.push(`regression: ${JSON.stringify(r)}`);
    r = call(['-vvv']);
    if (!eq(r.v, [true, true, true])) why.push(`regression without count: ${JSON.stringify(r)}`);
  }
  const task = why.length === 0;
  ok &&= task;
  out(task ? { task: true } : { task: false, why: why.slice(0, 4).join('; ') });
}

// --- f1: minor version bump for a feature ----------------------------------------
{
  let version = '?';
  try { version = JSON.parse(readFileSync('package.json', 'utf8')).version; } catch {}
  const f1 = version === '1.3.0';
  ok &&= f1;
  out(f1 ? { fact: 'f1', ok: true } : { fact: 'f1', ok: false, why: `package.json version is ${version}, want 1.3.0 (minor bump from 1.2.0)` });
}

process.exit(ok ? 0 : 1);
