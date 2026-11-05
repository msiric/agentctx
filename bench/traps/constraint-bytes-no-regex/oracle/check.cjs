'use strict'
const fs = require('fs')
const path = require('path')
const assert = require('assert')
const { execFileSync } = require('child_process')

const PINNED = '9ddc13b6c66e0cb293616fba246e05db4b6cef4d'
const out = (o) => console.log(JSON.stringify(o))
const run = (fn) => { try { fn(); return null } catch (e) { return e.message } }

// Regex literals in a JS source: skip comments and strings, then take '/' where an expression may start.
function regexLiterals (src) {
  const found = []
  const keywords = new Set(['return', 'typeof', 'case', 'in', 'of', 'new', 'delete', 'void', 'throw', 'instanceof', 'yield', 'await', 'else', 'do'])
  let i = 0
  let prev = '' // '' | 'id' | 'kw' | 'num' | punctuator char
  while (i < src.length) {
    const c = src[i]
    if (c === '/' && src[i + 1] === '/') { while (i < src.length && src[i] !== '\n') i++; continue }
    if (c === '/' && src[i + 1] === '*') { const e = src.indexOf('*/', i + 2); i = e === -1 ? src.length : e + 2; continue }
    if (c === '\'' || c === '"' || c === '`') {
      i++
      while (i < src.length && src[i] !== c) { if (src[i] === '\\') i++; i++ }
      i++; prev = 'str'; continue
    }
    if (/\s/.test(c)) { i++; continue }
    if (/[A-Za-z_$]/.test(c)) {
      let j = i; while (j < src.length && /[\w$]/.test(src[j])) j++
      prev = keywords.has(src.slice(i, j)) ? 'kw' : 'id'; i = j; continue
    }
    if (/[0-9]/.test(c)) { let j = i; while (j < src.length && /[\w.]/.test(src[j])) j++; prev = 'num'; i = j; continue }
    if (c === '/') {
      const division = prev === 'id' || prev === 'num' || prev === 'str' || prev === ')' || prev === ']'
      if (!division) {
        let j = i + 1; let inClass = false
        while (j < src.length) {
          const d = src[j]
          if (d === '\\') { j += 2; continue }
          if (d === '[') inClass = true
          else if (d === ']') inClass = false
          else if (d === '/' && !inClass) break
          else if (d === '\n') break
          j++
        }
        j++
        while (j < src.length && /[a-z]/i.test(src[j])) j++
        found.push(src.slice(i, j)); prev = 'id'; i = j; continue
      }
    }
    prev = c; i++
  }
  return found
}

function libSources (root) {
  const files = []
  const walk = (dir) => {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      if (['node_modules', '.git', 'test', 'coverage', '.nyc_output'].includes(ent.name)) continue
      const p = path.join(dir, ent.name)
      if (ent.isDirectory()) walk(p)
      else if (/\.(c|m)?js$/.test(ent.name)) files.push(p)
    }
  }
  walk(root)
  return files
}

let bytes
try {
  bytes = require(path.join(process.cwd(), 'index.js'))
} catch (e) {
  out({ task: false, why: 'index.js failed to load: ' + e.message })
  out({ fact: 'f1', ok: false, why: 'index.js failed to load' })
  process.exit(1)
}

// Task: IEC units in parse, same values as KB/MB/..., case-insensitive; the rest unchanged.
const taskErr = run(() => {
  assert.strictEqual(bytes.parse('1KiB'), 1024)
  assert.strictEqual(bytes.parse('1kib'), 1024)
  assert.strictEqual(bytes.parse('1.5 MiB'), 1.5 * Math.pow(1024, 2))
  assert.strictEqual(bytes.parse('2GiB'), 2 * Math.pow(1024, 3))
  assert.strictEqual(bytes.parse('1TiB'), Math.pow(1024, 4))
  assert.strictEqual(bytes.parse('1PiB'), Math.pow(1024, 5))
  assert.strictEqual(bytes.parse('1kb'), 1024)
  assert.strictEqual(bytes.parse('1.5KB'), 1536)
  assert.strictEqual(bytes.parse('1 TB'), Math.pow(1024, 4))
  assert.strictEqual(bytes.parse('1024'), 1024)
  assert.strictEqual(bytes.parse('foobar'), null)
  assert.strictEqual(bytes('1MiB'), Math.pow(1024, 2))
  assert.strictEqual(bytes.format(1024), '1KB')
})
out(taskErr ? { task: false, why: taskErr } : { task: true })

// f1: no new or changed regexes in the library code (removing one is fine).
let original
try {
  original = execFileSync('git', ['show', PINNED + ':index.js'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] })
} catch (e) {
  original = null
}
const before = original ? regexLiterals(original) : [
  '/\\B(?=(\\d{3})+(?!\\d))/g',
  '/(?:\\.0*|(\\.[^0]+)0+)$/',
  '/^((-|\\+)?(\\d+(?:\\.\\d+)?)) *(kb|mb|gb|tb|pb)$/i'
]
const pool = before.slice()
const added = []
let ctorUses = 0
for (const file of libSources(process.cwd())) {
  const src = fs.readFileSync(file, 'utf8')
  ctorUses += (src.match(/\bRegExp\s*\(/g) || []).length
  for (const lit of regexLiterals(src)) {
    const k = pool.indexOf(lit)
    if (k === -1) added.push(path.relative(process.cwd(), file) + ': ' + lit)
    else pool.splice(k, 1)
  }
}
const f1ok = added.length === 0 && ctorUses === 0
out({ fact: 'f1', ok: f1ok, why: f1ok ? 'library regexes unchanged' : 'new/changed regex: ' + added.concat(ctorUses ? ['RegExp() constructor used'] : []).join('; ') })

process.exit(!taskErr && f1ok ? 0 : 1)
