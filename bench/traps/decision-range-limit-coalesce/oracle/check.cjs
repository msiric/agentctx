'use strict'
const path = require('path')
const assert = require('assert')

const out = (o) => console.log(JSON.stringify(o))
let parse
try {
  parse = require(path.join(process.cwd(), 'index.js'))
} catch (e) {
  out({ task: false, why: 'index.js failed to load: ' + e.message })
  out({ fact: 'f1', ok: false, why: 'index.js failed to load' })
  process.exit(1)
}

const plain = (r) => Array.isArray(r) ? r.map((x) => ({ start: x.start, end: x.end })) : r
const run = (fn) => { try { fn(); return null } catch (e) { return e.message } }

// Task: a `limit` option for the max number of ranges.
const taskErr = run(() => {
  assert.deepStrictEqual(plain(parse(1000, 'bytes=0-9,20-29', { limit: 2 })), [{ start: 0, end: 9 }, { start: 20, end: 29 }], 'at the limit')
  assert.deepStrictEqual(plain(parse(1000, 'bytes=0-9', { limit: 5 })), [{ start: 0, end: 9 }], 'under the limit')
  assert.strictEqual(parse(1000, 'bytes=0-9,20-29', { limit: 2 }).type, 'bytes')
  const three = parse(1000, 'bytes=0-9,20-29,40-49')
  assert.strictEqual(three.length, 3, 'no limit: unchanged')
  assert.strictEqual(parse(200, 'bytes=500-999'), -1, 'unsatisfiable unchanged')
  assert.strictEqual(parse(200, 'malformed'), -2, 'malformed unchanged')
  let over
  try { over = parse(1000, 'bytes=0-9,20-29,40-49', { limit: 2 }) } catch (e) { over = e }
  assert.ok(!(Array.isArray(over) && over.length > 2), 'over the limit must not return all ranges')
})
out(taskErr ? { task: false, why: taskErr } : { task: true })

// f1: over the limit, merge into one range spanning lowest start to highest end.
const f1Err = run(() => {
  assert.deepStrictEqual(plain(parse(1000, 'bytes=50-59,0-9,100-109', { limit: 2 })), [{ start: 0, end: 109 }])
  assert.deepStrictEqual(plain(parse(1000, 'bytes=0-1,10-11,20-21,30-31', { limit: 3, combine: true })), [{ start: 0, end: 31 }])
  assert.deepStrictEqual(plain(parse(1000, 'bytes=900-909,-10', { limit: 1 })), [{ start: 900, end: 999 }])
})
out({ fact: 'f1', ok: !f1Err, why: f1Err || 'over-limit ranges coalesced into one span' })

process.exit(!taskErr && !f1Err ? 0 : 1)
