#!/usr/bin/env python
# /// script
# requires-python = ">=3.10"
# dependencies = ["fonttools[woff]>=4.55"]
# ///
"""Subset the upstream Linux Libertine O fonts to Latin + Latin-Ext, rename
them, and convert them to WOFF2, producing the files that ``build.py`` embeds.

"Linux Libertine" is a Reserved Font Name under the SIL OFL. A subset is a
Modified Version, which the OFL forbids from carrying the Reserved Font Name,
so the faces are renamed to FAMILY below. The copyright, license and vendor
name records are preserved verbatim, as clauses 1 and 2 of the OFL require.

This is a one-off preparation step; the resulting ``fonts/*.woff2`` are
committed, so a normal ``build.py`` run does not need it. Re-run only when
upgrading the upstream font.

Usage:
    uv run tools/subset_fonts.py <dir-with-upstream-fonts>

Upstream: Linux Libertine O (Libertine Open Fonts Project),
dual-licensed GPL-2.0-or-later with Font Exception / SIL OFL 1.1.
See fonts/OFL.txt.
"""

from __future__ import annotations

import sys
from pathlib import Path

from fontTools.subset import (
    Options,
    Subsetter,
    load_font,
    parse_unicodes,
    save_font,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "fonts"

# Google Fonts' `latin` + `latin-ext` unicode ranges. The theme only uses
# Libertine for headings and the inline title; anything outside these ranges
# falls through to the Georgia/Times/serif stack declared in --h1-font.
UNICODES = ",".join(
    [
        # latin
        "U+0000-00FF", "U+0131", "U+0152-0153", "U+02BB-02BC", "U+02C6",
        "U+02DA", "U+02DC", "U+0304", "U+0308", "U+0329", "U+2000-206F",
        "U+20AC", "U+2122", "U+2191", "U+2193", "U+2212", "U+2215",
        "U+FEFF", "U+FFFD",
        # latin-ext
        "U+0100-02BA", "U+02BD-02C5", "U+02C7-02CC", "U+02CE-02D7",
        "U+02DD-02FF", "U+1D00-1DBF", "U+1E00-1E9F", "U+1EF2-1EFF",
        "U+2020", "U+20A0-20AB", "U+20AD-20C0", "U+2113", "U+2C60-2C7F",
        "U+A720-A7FF",
    ]
)

# The renamed family. Must not contain the Reserved Font Name.
FAMILY = "Wikidian Libertine"

FACES = {
    "LinuxLibertine-Regular": "Regular",
    "LinuxLibertine-Bold": "Bold",
    "LinuxLibertine-Italic": "Italic",
}

# name table records that carry the family identity and must be rewritten.
FAMILY_ID, SUBFAMILY_ID, UNIQUE_ID, FULL_ID, PS_ID = 1, 2, 3, 4, 6
TYPO_FAMILY_ID, TYPO_SUBFAMILY_ID = 16, 17


def rename(font, subfamily: str) -> None:
    """Rewrite the name table so the subset no longer claims the Reserved Font Name."""
    full = FAMILY if subfamily == "Regular" else f"{FAMILY} {subfamily}"
    postscript = f"{FAMILY.replace(' ', '')}-{subfamily}"

    replacements = {
        FAMILY_ID: FAMILY,
        SUBFAMILY_ID: subfamily,
        UNIQUE_ID: f"{full}; subset of Linux Libertine O 5.3.0",
        FULL_ID: full,
        PS_ID: postscript,
        TYPO_FAMILY_ID: FAMILY,
        TYPO_SUBFAMILY_ID: subfamily,
    }

    name_table = font["name"]
    for record in list(name_table.names):
        if record.nameID in replacements:
            name_table.setName(
                replacements[record.nameID],
                record.nameID,
                record.platformID,
                record.platEncID,
                record.langID,
            )

    if "CFF " in font:
        font["CFF "].cff.fontNames = [postscript]


def subset_one(src: Path, dest: Path, subfamily: str) -> tuple[int, int, int, int]:
    options = Options()
    options.flavor = "woff2"
    options.with_zopfli = True
    options.desubroutinize = True
    # Keep the layout features Libertine relies on for proper Latin text.
    options.layout_features = ["kern", "liga", "clig", "calt", "ccmp", "locl"]
    # Drop hinting and non-essential tables; browsers/Electron don't need them.
    options.hinting = False
    options.drop_tables += ["DSIG"]
    options.notdef_outline = True
    options.recalc_bounds = True
    # Preserve the name records that carry authorship and licensing.
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.name_languages = ["*"]

    font = load_font(str(src), options)
    before_glyphs = len(font.getGlyphOrder())

    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=parse_unicodes(UNICODES))
    subsetter.subset(font)

    after_glyphs = len(font.getGlyphOrder())
    rename(font, subfamily)
    save_font(font, str(dest), options)
    font.close()

    return before_glyphs, after_glyphs, src.stat().st_size, dest.stat().st_size


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    src_dir = Path(sys.argv[1])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total_before = total_after = 0
    for stem, subfamily in FACES.items():
        src = next(iter(sorted(src_dir.glob(f"{stem}.*"))), None)
        if src is None:
            print(f"missing upstream font: {src_dir / stem}.*", file=sys.stderr)
            return 1

        dest = OUT_DIR / f"{FAMILY.replace(' ', '')}-{subfamily}.woff2"
        gb, ga, sb, sa = subset_one(src, dest, subfamily)
        total_before += sb
        total_after += sa
        print(
            f"{stem:24} -> {dest.name:28} {gb:>5} -> {ga:>4} glyphs   "
            f"{sb / 1024:>7.1f} KB -> {sa / 1024:>6.1f} KB"
        )

    print(
        f"{'TOTAL':24}    {'':28} {'':>5}    {'':>4}          "
        f"{total_before / 1024:>7.1f} KB -> {total_after / 1024:>6.1f} KB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
