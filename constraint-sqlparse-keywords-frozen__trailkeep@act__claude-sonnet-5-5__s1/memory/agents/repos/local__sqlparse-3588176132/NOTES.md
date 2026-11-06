# Private notes: local__sqlparse-3588176132

- 2026-11-06: Never edit sqlparse/keywords.py: it must stay byte-identical to upstream so the weekly upstream merge stays clean (an old local tweak there caused repeated merge conflicts; the user reverted it). If extra keywords are needed, register them at runtime via Lexer.add_keywords() from a separate module of our own.
- 2026-11-06: Local keyword additions live in sqlparse/extra_keywords.py (imported in sqlparse/__init__.py), never in keywords.py. Add new dialect keywords there. Lexer.default_initialization() resets them; call extra_keywords.register() afterwards.
