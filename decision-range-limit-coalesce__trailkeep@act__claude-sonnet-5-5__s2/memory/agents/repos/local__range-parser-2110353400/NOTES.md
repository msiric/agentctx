# Private notes: local__range-parser-2110353400

- 2026-11-06: range-parser return codes: -1 = unsatisfiable, -2 = malformed; callers (e.g. send) rely on them, so avoid new return codes or throwing without an explicit decision.
