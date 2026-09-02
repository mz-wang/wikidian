#!/usr/bin/env python
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build `theme.css` from the modules in `src/`.

Concatenates `src/*.css` in filename order and replaces every
``{{ font: <file> }}`` placeholder with a base64 data URI of the matching
font in `fonts/`. Obsidian installs a theme by copying only `manifest.json`
and `theme.css`, so the font faces have to be inlined -- there is no second
file the app would fetch.

Usage:
    uv run build.py            # write theme.css
    uv run build.py --check    # exit 1 if theme.css is stale (for CI)
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
FONT_DIR = ROOT / "fonts"
OUTPUT = ROOT / "theme.css"

PLACEHOLDER = re.compile(r"\{\{\s*font:\s*(?P<name>[\w.\-]+)\s*\}\}")

MIME_BY_SUFFIX = {
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
}


def banner() -> str:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    # The banner points at the repo, not at `authorUrl`: the store requires the
    # latter to be a profile, and a profile is no help to someone holding a
    # copied theme.css and wondering where it came from.
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    repo = package["repository"]["url"].removesuffix(".git")
    return (
        "/*\n"
        f" * {manifest['name']} v{manifest['version']} -- an Obsidian theme.\n"
        f" * {repo}\n"
        " *\n"
        " * GENERATED FILE -- DO NOT EDIT.\n"
        " * Edit the modules in src/ and run `uv run build.py`.\n"
        " *\n"
        " * Derived from the Wikipedia theme by Ha'ani Whitlock (MIT).\n"
        " * Inspired by the visual design of wikipedia.org.\n"
        " */\n\n"
    )


def data_uri(name: str) -> str:
    path = FONT_DIR / name
    if not path.is_file():
        raise SystemExit(f"build: missing font referenced by src/: {path}")

    mime = MIME_BY_SUFFIX.get(path.suffix.lower()) or (
        mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    )
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def render() -> tuple[str, list[tuple[str, int]]]:
    modules = sorted(SRC_DIR.glob("*.css"))
    if not modules:
        raise SystemExit(f"build: no source modules found in {SRC_DIR}")

    parts: list[str] = [banner()]
    stats: list[tuple[str, int]] = []

    for module in modules:
        text = module.read_text(encoding="utf-8")
        rendered = PLACEHOLDER.sub(lambda m: data_uri(m.group("name")), text)
        stats.append((module.name, len(rendered.encode("utf-8"))))
        parts.append(rendered.rstrip() + "\n\n\n")

    return "".join(parts).rstrip() + "\n", stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify theme.css matches src/ instead of writing it",
    )
    args = parser.parse_args()

    css, stats = render()

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else None
        if current != css:
            print("theme.css is out of date; run `uv run build.py`", file=sys.stderr)
            return 1
        print("theme.css is up to date")
        return 0

    # newline="\n" so a Windows build matches the LF checkout CI verifies.
    OUTPUT.write_text(css, encoding="utf-8", newline="\n")

    for name, size in stats:
        print(f"  {name:26} {size / 1024:>8.1f} KB")
    print(f"  {'-' * 26} {'-' * 11}")
    print(f"  {OUTPUT.name:26} {len(css.encode('utf-8')) / 1024:>8.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
