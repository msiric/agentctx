# Private notes: local__tinydb-3819657849

- 2026-11-05: JSONStorage must not use rename/os.replace over db.json: in prod db.json is bind-mounted as a single file, so replacing it fails with OSError Errno 16 (Device or resource busy), and ops won't change the mount. Tried atomic temp-file + os.replace on branch crash-safe-writes (also tried by Marko in the fork); backed out. Crash-safe writes need an approach that modifies the file in place.
