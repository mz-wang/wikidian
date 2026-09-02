"""Install the built theme into the demo vault.

`demo/` is a real Obsidian vault, but the parts of it that are copies of
something else -- the theme itself, the snippet, the Dataview plugin -- are not
committed, so it needs one command before it will open looking right:

    uv run build.py
    uv run tools/setup_demo_vault.py

Dataview is not copied; install it from inside Obsidian (Settings -> Community
plugins). Without it the inline `[label:: value]` fields in the infoboxes show
their brackets, and nothing else changes.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "demo"
THEME_DIR = VAULT / ".obsidian" / "themes" / "Wikidian"
SNIPPET_DIR = VAULT / ".obsidian" / "snippets"


def main() -> int:
    theme = ROOT / "theme.css"
    if not theme.exists():
        print("theme.css is missing -- run `uv run build.py` first", file=sys.stderr)
        return 1

    THEME_DIR.mkdir(parents=True, exist_ok=True)
    SNIPPET_DIR.mkdir(parents=True, exist_ok=True)

    for name in ("manifest.json", "theme.css"):
        shutil.copyfile(ROOT / name, THEME_DIR / name)
        print(f"-> {(THEME_DIR / name).relative_to(ROOT)}")

    snippet = ROOT / "snippets" / "semantic-colors.css"
    shutil.copyfile(snippet, SNIPPET_DIR / snippet.name)
    print(f"-> {(SNIPPET_DIR / snippet.name).relative_to(ROOT)}")

    print("\nOpen demo/ as a vault. Dataview has to be installed from inside "
          "Obsidian for the infobox fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
