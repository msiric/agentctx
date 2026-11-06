# Private notes: local__tinydb-2009427271

- 2026-11-06: JSONStorage must not replace db.json via rename/os.replace: in prod the file is bind-mounted as a single file, so rename fails with OSError Errno 16 (Device or resource busy), and ops won't change the mounts. An earlier fork attempt (Marko's) hit the same failure. Crash-safe writes need an approach that modifies the file in place.
- 2026-11-06: JSONStorage crash safety uses an in-place redo journal (db.json.journal, sha256 header + payload, replayed on open); no rename/os.replace because prod bind-mounts db.json (EBUSY). Journal sits next to the db file, so its directory must be writable. (journal design chosen by me)
