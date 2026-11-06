# Private notes: local__tomli-w-1120978569

- 2026-11-06: None values should serialize as empty string (key = ""), not be skipped: downstream loader reads "" as explicitly unset. Pending code switch, planned together with the array None case.
