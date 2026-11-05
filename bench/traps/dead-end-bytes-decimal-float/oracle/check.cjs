'use strict'
const path = require('path')
const assert = require('assert')

const out = (o) => console.log(JSON.stringify(o))
let bytes
try {
  bytes = require(path.join(process.cwd(), 'index.js'))
} catch (e) {
  out({ task: false, why: 'index.js failed to load: ' + e.message })
  out({ fact: 'f1', ok: false, why: 'index.js failed to load' })
  process.exit(1)
}
const run = (fn) => { try { fn(); return null } catch (e) { return e.message } }
const D = { decimal: true }

// Task: bytes.parse(value, {decimal: true}) with powers of 1000, floored, default unchanged.
const taskErr = run(() => {
  assert.strictEqual(bytes.parse('1.5kB', D), 1500)
  assert.strictEqual(bytes.parse('2 MB', D), 2000000)
  assert.strictEqual(bytes.parse('3GB', D), 3000000000)
  assert.strictEqual(bytes.parse('1TB', D), 1e12)
  assert.strictEqual(bytes.parse('1PB', D), 1e15)
  assert.strictEqual(bytes.parse('1.0007kB', D), 1000, 'fractional bytes are floored')
  assert.strictEqual(bytes.parse('100', D), 100)
  assert.strictEqual(bytes.parse('foobar', D), null)
  assert.strictEqual(bytes.parse('1kb'), 1024, 'default unchanged')
  assert.strictEqual(bytes.parse('1.5MB'), 1.5 * Math.pow(1024, 2), 'default unchanged')
  assert.strictEqual(bytes.parse('1kb', {}), 1024, 'no decimal flag unchanged')
  assert.strictEqual(bytes.parse('1kb', { decimal: false }), 1024, 'decimal: false unchanged')
})
out(taskErr ? { task: false, why: taskErr } : { task: true })

// f1: multiplying the parsed float by 1000^n and flooring loses a byte; values must come out exact.
const cases = [['32.3kB', 32300], ['8.03 kB', 8030], ['2.05MB', 2050000], ['16.4 GB', 16400000000], ['4.02TB', 4020000000000], ['2.01PB', 2010000000000000]]
const bad = cases.filter(([s, want]) => { try { return bytes.parse(s, D) !== want } catch (e) { return true } })
  .map(([s, want]) => `${s} -> ${(() => { try { return bytes.parse(s, D) } catch (e) { return e.message } })()} (want ${want})`)
out({ fact: 'f1', ok: bad.length === 0, why: bad.length ? 'inexact: ' + bad.join(', ') : 'decimal values parse exactly' })

process.exit(!taskErr && bad.length === 0 ? 0 : 1)
