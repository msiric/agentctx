// Scores the last session (repo cookie): stringifySetCookie rejects maxAge
// above 400 days with a TypeError, and the user's cross-repo preference from
// the pretty-bytes session holds: new error messages start with the package
// name and a colon ("cookie: ...").
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

const LIMIT = 400 * 24 * 60 * 60;
const run = (maxAge) => {
  try {
    return { out: mod.stringifySetCookie({ name: 'foo', value: 'bar', maxAge }) };
  } catch (e) {
    return { err: e };
  }
};

// ---- task
const problems = [];
for (const ok of [LIMIT, 1000, 0, -1]) {
  const r = run(ok);
  if (r.err || r.out !== `foo=bar; Max-Age=${ok}`) problems.push(`maxAge ${ok}: ${r.err ? `threw ${r.err.message}` : r.out}`);
}
for (const bad of [LIMIT + 1, 1e9]) {
  const r = run(bad);
  if (!(r.err instanceof TypeError)) problems.push(`maxAge ${bad} should throw a TypeError, got ${r.err ? r.err.constructor.name : JSON.stringify(r.out)}`);
}
if (!(run(3.14).err instanceof TypeError)) problems.push('non-integer maxAge no longer throws');
const taskOk = problems.length === 0;
emit({ task: taskOk, why: taskOk ? 'maxAge capped at 400 days with a TypeError' : problems.slice(0, 4).join('; ') });

// ---- f1: error message prefixed with the package name
const msgs = [LIMIT + 1, 1e9].map((v) => run(v).err?.message ?? null);
const f1 = msgs.every((m) => typeof m === 'string' && /^cookie: \S/.test(m));
emit({ fact: 'f1', ok: f1, why: f1 ? `message: ${JSON.stringify(msgs[0])}` : `message not prefixed with "cookie: ": ${JSON.stringify(msgs[0])}` });

process.exit(taskOk && f1 ? 0 : 1);
