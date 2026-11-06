# Private notes: local__sqlparse-1130470533

- 2026-11-06: Never edit sqlparse/keywords.py: it must stay byte-identical to upstream so the weekly upstream merge doesn't conflict (an old local tweak there caused repeated conflicts and was reverted). If extra keywords are needed, register them at runtime via Lexer.add_keywords() from a separate module of our own.
- 2026-11-06: Extra keywords (EXCLUDE, MATCH_RECOGNIZE, ASOF, MATCH_CONDITION) live in sqlparse/keywords_extra.py, registered in Lexer.default_initialization; add future local keywords there, not in keywords.py (must stay upstream-identical).
