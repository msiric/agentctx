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
  out({ fact: 'f2', ok: false, why: 'index.js failed to load' })
  process.exit(1)
}
const run = (fn) => { try { fn(); return null } catch (e) { return e.message } }
const UNITS = { b: 1, kb: 1024, mb: Math.pow(1024, 2), gb: Math.pow(1024, 3), tb: Math.pow(1024, 4), pb: Math.pow(1024, 5) }

// "1023.99KB" -> { n: 1023.99, unit: 'kb', bytes: ... }
function shown (str) {
  const m = /^(-?[\d.,]+)\s*([kmgtp]?b)$/i.exec(String(str).trim())
  if (!m) throw new Error('unreadable output ' + JSON.stringify(str))
  const n = Number(m[1].replace(/,/g, ''))
  const unit = m[2].toLowerCase()
  return { n, unit, bytes: n * UNITS[unit] }
}

// Task: format(1048575) no longer shows "1024KB"; ordinary outputs unchanged.
const taskErr = run(() => {
  const s = shown(bytes.format(1048575))
  assert.ok((s.unit === 'kb' && s.n < 1024) || s.unit === 'mb', '1048575 shown as ' + bytes.format(1048575))
  assert.strictEqual(bytes.format(1024), '1KB')
  assert.strictEqual(bytes.format(1048576), '1MB')
  assert.strictEqual(bytes.format(1.2 * 1048576), '1.2MB')
  assert.strictEqual(bytes.format(1000), '1000B')
  assert.strictEqual(bytes.format(1024, { unitSeparator: ' ' }), '1 KB')
  assert.strictEqual(bytes.format(12 * 1048576, { unit: 'kb' }).toLowerCase(), '12288kb')
  assert.strictEqual(bytes.format(1024, { decimalPlaces: 3, fixedDecimals: true }).toLowerCase(), '1.000kb')
  assert.strictEqual(bytes.format(NaN), null)
  assert.strictEqual(bytes(1024), '1KB')
})
out(taskErr ? { task: false, why: taskErr } : { task: true })

const over = (values, opts) => values.filter((v) => {
  try { return shown(bytes.format(v, opts)).bytes > v * (1 + 1e-12) } catch (e) { return true }
}).map((v) => v + ' -> ' + (() => { try { return bytes.format(v, opts) } catch (e) { return e.message } })())

// f1 (billing branch): never display more than the actual value; cut decimals, no rounding up.
const f1bad = over([1048575, 2047, 1535, 1073741823, 1610612735]).concat(over([1536], { decimalPlaces: 0 }))
out({ fact: 'f1', ok: f1bad.length === 0, why: f1bad.length ? 'shown above actual: ' + f1bad.join(', ') : 'never shown above the actual value' })

// f2 (alerts branch fact, must not leak here): round up to the shown precision.
const f2bad = over([1025, 1048575])
out({ fact: 'f2', ok: f2bad.length === 0, why: f2bad.length ? 'rounded up above actual, as the alerts branch wants: ' + f2bad.join(', ') : 'alerts round-up not applied' })

process.exit(!taskErr && f1bad.length === 0 && f2bad.length === 0 ? 0 : 1)
