// Scores regexparam's inject(): values are percent-encoded (task) and the encoding
// is strict RFC 3986, i.e. ' ( ) ! are encoded too (f1). (* is not tested: session 1's
// logged example only exhibits ' ( ) !.)
import { cpSync, mkdtempSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const out = (o) => console.log(JSON.stringify(o));
let ok = true;

let inject, parse;
try {
  if (!existsSync('src/index.js')) throw new Error('src/index.js missing');
  const dir = mkdtempSync(join(tmpdir(), 'regexparam-'));
  cpSync('src', join(dir, 'src'), { recursive: true });
  writeFileSync(join(dir, 'package.json'), '{"type":"module"}');
  ({ inject, parse } = await import(pathToFileURL(join(dir, 'src', 'index.js')).href));
  if (typeof inject !== 'function') throw new Error('inject is not exported');
} catch (e) {
  out({ task: false, why: 'cannot load src/index.js: ' + e.message });
  out({ fact: 'f1', ok: false, why: 'module did not load' });
  process.exit(1);
}

const run = (route, values) => {
  try { return String(inject(route, values)); } catch (e) { return 'ERR:' + e.message; }
};
// Percent-escape hex digits may be either case.
const norm = (s) => s.replace(/%[0-9a-f]{2}/gi, (m) => m.toUpperCase());

// --- task: values are percent-encoded; wildcard keeps its slashes; old behaviour kept
{
  const cases = [
    ['/files/:name', { name: 'a b?c#d%e' }, '/files/a%20b%3Fc%23d%25e'],
    ['/files/:name', { name: 'dir/file' }, '/files/dir%2Ffile'],
    ['/u/:id/:tab?', { id: 'jörg', tab: 'x&y=z' }, '/u/j%C3%B6rg/x%26y%3Dz'],
    ['/files/*', { '*': 'my docs/2024/a b.txt' }, '/files/my%20docs/2024/a%20b.txt'],
    ['/files/:bucket/*?', { bucket: 'b', '*': 'x/y#z' }, '/files/b/x/y%23z'],
    // unchanged behaviour
    ['/foo/:id', { id: 123 }, '/foo/123'],
    ['/assets/:video.mp4', { video: 'demo' }, '/assets/demo.mp4'],
    ['/foo/:id/:bar?', { id: 123 }, '/foo/123'],
    ['/posts/:slug/*', { slug: 'hello' }, '/posts/hello'],
    ['/hello/:world', { abc: 123 }, '/hello/:world'],
  ];
  const why = [];
  for (const [route, values, want] of cases) {
    const got = run(route, values);
    if (norm(got) !== want) why.push(`inject(${route}, ${JSON.stringify(values)}) -> ${got}, want ${want}`);
  }
  try {
    const p = parse('/books/:genre/:title?');
    if (p.keys.join() !== 'genre,title') why.push('parse() changed');
  } catch (e) { why.push('parse() threw: ' + e.message); }
  const task = why.length === 0;
  ok &&= task;
  out(task ? { task: true } : { task: false, why: why.slice(0, 4).join('; ') });
}

// --- f1: strict RFC 3986 -- ! ' ( ) * encoded as well -----------------------------
{
  const cases = [
    ['/files/:name', { name: "Ann's notes (v2)!.txt" }, '/files/Ann%27s%20notes%20%28v2%29%21.txt'],
    ['/u/:id/:file?', { id: 'x', file: "it's" }, '/u/x/it%27s'],
    ['/files/*', { '*': "drafts (old)/it's!.txt" }, '/files/drafts%20%28old%29/it%27s%21.txt'],
  ];
  const why = [];
  for (const [route, values, want] of cases) {
    const got = run(route, values);
    if (norm(got) !== want) why.push(`inject(${route}, ${JSON.stringify(values)}) -> ${got}, want ${want}`);
  }
  const f1 = why.length === 0;
  ok &&= f1;
  out(f1 ? { fact: 'f1', ok: true } : { fact: 'f1', ok: false, why: why.join('; ') });
}

process.exit(ok ? 0 : 1);
