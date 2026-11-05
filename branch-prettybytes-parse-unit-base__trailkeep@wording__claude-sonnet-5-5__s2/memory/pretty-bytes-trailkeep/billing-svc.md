# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-874486487 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: billing-svc: when adding the decimal units to parseBytes, read them as strict SI: '1 MB' is exactly 1,000,000 bytes (kB=1e3, MB=1e6, GB=1e9, ...), matching what prettyBytes prints. Do NOT use the storage-app reading (KB/MB as powers of 1024). Reason (user): billing quotes in strict SI. Not implemented yet; for now decimal units still throw SyntaxError 'Unsupported unit'.

