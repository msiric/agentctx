# crash-safe-writes

Branch: crash-safe-writes · Repo: local__tinydb-3420554087 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05 (REVERTED, see next note): JSONStorage.write was made atomic (my choice): temp file in same dir + fsync + os.replace + dir fsync, then reopens handle. Chosen over in-place write because truncate-after-write can leave a half-written file on crash. Side effect: inode changes on each write, so the file is replaced rather than modified in place; hard links/other open handles on db.json won't see updates.
- 2026-11-05: Rename-over-file (temp + os.replace) for JSONStorage is NOT viable for this user's prod: db.json is bind-mounted as a single file, so os.replace fails with EBUSY (Errno 16); ops won't change mounts. I implemented it, user had me revert it. Any crash-safety fix must write to the same inode (e.g. journal/backup copy + in-place write, or recovery on open).
- 2026-11-05: JSONStorage crash-safety implemented (my choice): redo-journal <path>.journal holds full new state (fsync'd), then in-place write + truncate + fsync, then journal removed; on open in write modes _recover() replays a parseable journal or discards a torn one. Same inode kept (bind-mount constraint). Caveat: journal lives next to db.json, so if only the single file is mounted it sits on the container's own fs and is lost if the container is recreated.

