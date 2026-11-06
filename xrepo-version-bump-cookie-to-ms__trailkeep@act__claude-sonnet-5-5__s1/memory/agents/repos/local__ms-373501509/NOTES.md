# Private notes: local__ms-373501509

- 2026-11-06: Unit parsing in src/index.ts: the regex, the Unit type, the switch, README type block and both parse tests must stay in sync. µs has two codepoints (U+00B5 micro sign, U+03BC Greek mu); both are handled, since /i lowercasing leaves them distinct. (My choice: also accepted 'us'.)
