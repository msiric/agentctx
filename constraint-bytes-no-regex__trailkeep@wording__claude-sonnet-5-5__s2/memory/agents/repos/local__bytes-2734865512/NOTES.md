# Private notes: local__bytes-2734865512

- 2026-11-05: Rule agreed with AppSec (ReDoS audit): do not add or change any regex in index.js without AppSec sign-off (queue ~3 weeks). Any new parsing needed in this package must use plain string handling instead. Applies on every branch.
