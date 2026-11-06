# Private notes: local__sqlparse-1579908339

- 2026-11-06: Never edit sqlparse/keywords.py: it must stay byte-identical to upstream so the weekly upstream merge doesn't conflict (an old local tweak there caused repeated conflicts; user reverted it). If extra keywords are needed, register them at runtime via Lexer.add_keywords() from a module of our own.
- 2026-11-06: Local keyword additions live in sqlparse/keywords_local.py (KEYWORDS_LOCAL), registered in Lexer.default_initialization in lexer.py; add new local keywords there, not in keywords.py (must stay upstream-identical). My choice: hooked via default_initialization so the keywords survive a lexer reset.
