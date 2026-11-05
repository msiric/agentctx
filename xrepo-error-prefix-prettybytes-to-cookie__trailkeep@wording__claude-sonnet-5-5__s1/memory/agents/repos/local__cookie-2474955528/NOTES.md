# Private notes: local__cookie-2474955528

- 2026-11-05: cookie: the new maxAge >400 day error in stringifySetCookie uses a 'cookie: ' prefix (my choice, from the user's package-name-prefix rule); older errors in src/index.ts have no prefix and were left unchanged. Ask the user before unifying. parseSetCookie does not enforce the 400 day cap.
