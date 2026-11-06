# Private notes: local__sqlparse-2323918864

- 2026-11-06: Keep sqlparse/keywords.py byte-identical to upstream, with no local edits, because the weekly upstream merge conflicted there when a local tweak lived in it (user reverted it). If extra keywords are needed, register them at runtime (e.g. Lexer.add_keywords()) from a separate module of our own.
- 2026-11-06: Local extra keywords (EXCLUDE, MATCH_RECOGNIZE, ASOF, MATCH_CONDITION for Snowflake) live in sqlparse/extra_keywords.py, registered at the end of Lexer.default_initialization; add further local keywords there, never in keywords.py (my choice of location, per the keywords.py-identical-to-upstream rule).
