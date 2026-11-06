# Private notes: local__sqlparse-3010341845

- 2026-11-06: Do not edit sqlparse/keywords.py: it must stay byte-identical to upstream so the weekly upstream merge stays clean (a local tweak there caused repeated conflicts; user reverted it). If extra keywords are needed, register them at runtime via Lexer.add_keywords() from a module of our own.
- 2026-11-06: Extra keywords (EXCLUDE, MATCH_RECOGNIZE, ASOF, MATCH_CONDITION) live in sqlparse/extra_keywords.py, registered via Lexer.add_keywords() and imported in sqlparse/__init__.py; keywords.py stays untouched (upstream-identical). Add future local keywords there. Run tests with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 (platformdirs pytest plugin is broken in this env).
