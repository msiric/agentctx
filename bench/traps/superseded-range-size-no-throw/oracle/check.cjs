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
  out({ fact: 'f2', ok: false, why: 'index.js failed to load' })
  process.exit(1)
}
const run = (fn) => { try { fn(); return null } catch (e) { return e.message } }
const plain = (r) => Array.isArray(r) ? r.map((x) => ({ start: x.start, end: x.end })) : r
const badSizes = [['NaN', NaN], ['-1', -1], ['Infinity', Infinity], ['1.5', 1.5], ["'100'", '100'], ['undefined', undefined], ['null', null]]
const outcome = (size) => { try { return { value: parse(size, 'bytes=0-1') } } catch (e) { return { error: e } } }

// Task: bad sizes are rejected (no ranges come back); good sizes work as before.
const taskErr = run(() => {
  for (const [label, size] of badSizes) {
    const o = outcome(size)
    assert.ok(o.error || (typeof o.value === 'number' && o.value < 0), 'size ' + label + ' was not rejected: ' + JSON.stringify(o.value))
  }
  assert.deepStrictEqual(plain(parse(100, 'bytes=0-9')), [{ start: 0, end: 9 }])
  assert.deepStrictEqual(plain(parse(1000, 'bytes=-10')), [{ start: 990, end: 999 }])
  assert.throws(() => parse(200, {}), TypeError, 'str check unchanged')
})
out(taskErr ? { task: false, why: taskErr } : { task: true })

// f2 (current): a bad size returns -2, never throws. f1 (superseded): throwing a TypeError.
const threw = []
const wrong = []
for (const [label, size] of badSizes) {
  const o = outcome(size)
  if (o.error) threw.push(label)
  else if (o.value !== -2) wrong.push(label + ' -> ' + JSON.stringify(o.value))
}
out({ fact: 'f1', ok: threw.length === 0, why: threw.length ? 'still follows the superseded decision, throws for: ' + threw.join(', ') : 'superseded throw not used' })
const f2ok = threw.length === 0 && wrong.length === 0
out({ fact: 'f2', ok: f2ok, why: f2ok ? 'bad sizes return -2' : 'throws for: ' + threw.join(', ') + (wrong.length ? '; not -2: ' + wrong.join(', ') : '') })

process.exit(!taskErr && f2ok ? 0 : 1)
