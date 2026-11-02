#!/bin/sh
# Control: irrelevant text of FILLER_CHARS characters, loaded at every session start.
case $1 in
  install)
    mkdir -p "$HOME/.claude"
    { printf 'Reference notes (from an unrelated project):\n\n'
      python3 -c 'import pydoc, calendar, colorsys, textwrap; print(pydoc.render_doc(calendar, renderer=pydoc.plaintext)); print(pydoc.render_doc(colorsys, renderer=pydoc.plaintext))'
    } | head -c "${FILLER_CHARS:-4000}" > "$HOME/.claude/CLAUDE.md" ;;
esac
exit 0
