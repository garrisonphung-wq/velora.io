# Velora.io

## Git / Checkpointing Rule (IMPORTANT)
- The user wants progress saved to git regularly so nothing is ever lost.
- After completing each meaningful chunk of work (or when asked), verify the
  code compiles / runs, then `git add` the intended files and commit with a
  concise message describing what changed.
- Do NOT lose work: if a risky command could revert or overwrite uncommitted
  changes, commit first.

## Verify
- Compile check: `.venv/bin/python -m py_compile Main.py && echo OK`
- Runtime smoke test:
  `SDL_VIDEODRIVER=dummy .venv/bin/python -c "import Main"` then confirm the
  game loop stays alive.
