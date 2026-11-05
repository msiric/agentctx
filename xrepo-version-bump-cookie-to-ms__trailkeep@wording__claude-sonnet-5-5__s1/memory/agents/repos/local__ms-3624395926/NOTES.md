# Private notes: local__ms-3624395926

- 2026-11-05: Microsecond units (us, µs, μs, microsecond(s)) were added in 4.1.0 (my choice: minor bump). Strict StringValue type rejects uppercase 'µS' because TS Uppercase<'µs'> yields Greek capital mu; parse() still accepts it at runtime, so tests for 'µS' only go in parse.test.ts.
