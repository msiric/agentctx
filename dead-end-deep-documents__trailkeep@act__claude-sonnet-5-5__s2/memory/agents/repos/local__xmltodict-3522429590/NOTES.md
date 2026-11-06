# Private notes: local__xmltodict-3522429590

- 2026-11-06: xmltodict eval for supplier catalog feed: user only needs parse() for now (their decision). Finding: parse handles 3000-deep nesting, but unparse() raises RecursionError at that depth (works flat, or deep with raised recursion limit + big thread stack). Use force_list=('part',) and streaming (item_depth/item_callback) for big feeds. Next session: don't rebuild this test; revisit unparse only if the user asks.
