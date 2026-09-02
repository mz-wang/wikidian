"""Draw the figures used by the demo vault.

The demo vault's article illustrates the theme's own layout, so the plates are
schematics rather than photographs: line art on a warm paper ground, which
reads the same under the light and the dark theme (Wikidian frames every image
in a border and a padding well, and a white plate glares inside a dark one).

    uv run tools/make_demo_figures.py

Writes demo/Attachments/*.png. Both the script and its output are committed --
the vault has to work on a clean checkout without a build step.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT = Path(__file__).resolve().parent.parent / "demo" / "Attachments"

PAPER = "#f7f5ef"
INK = "#2b2b2b"
RULE = "#a9a29a"
FILL = "#e4e0d6"
ACCENT = "#3366cc"

# Wikidian's own palette, as the snippet uses it.
ROLES = [
    ("note", "#0069e0", "an aside, a cross-reference"),
    ("ok", "#52a300", "settled, verified, done"),
    ("warn", "#e66f00", "a caveat, an open question"),
    ("key", "#8c3ff7", "the load-bearing sentence"),
]


def _pick(*names: str) -> str:
    """First installed family among names, else matplotlib's default."""
    have = {f.name for f in fm.fontManager.ttflist}
    for n in names:
        if n in have:
            return n
    return "DejaVu Sans"


SERIF = _pick("Linux Libertine O", "Georgia", "Times New Roman", "DejaVu Serif")
SANS = _pick("Source Han Sans SC VF", "Segoe UI", "Arial", "DejaVu Sans")


def _canvas(w: float, h: float):
    fig = plt.figure(figsize=(w, h), dpi=200)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h / w)
    ax.set_axis_off()
    fig.patch.set_facecolor(PAPER)
    return fig, ax


def _save(fig, name: str) -> None:
    path = OUT / name
    fig.savefig(path, facecolor=PAPER)
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT.parent.parent)}")


def _bar(ax, x, y, w, h=1.15, color=FILL):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="none"))


def _label(ax, text, xy, xytext, size=6.2):
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        fontsize=size,
        fontfamily=SANS,
        color=INK,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="-", color=RULE, lw=0.6,
                        shrinkA=1, shrinkB=1),
    )


def reading_column() -> None:
    """Schematic of the article page: column, infobox, margins."""
    fig, ax = _canvas(5.0, 3.4)
    h = 100 * 3.4 / 5.0            # 68

    frame_b, frame_t = 15.0, 64.0
    ax.add_patch(Rectangle((3, frame_b), 94, frame_t - frame_b,
                           facecolor="none", edgecolor=RULE, lw=0.8))

    # sidebar
    side_w = 13.0
    ax.add_patch(Rectangle((3, frame_b), side_w, frame_t - frame_b,
                           facecolor=FILL, edgecolor=RULE, lw=0.6))
    for i in range(9):
        _bar(ax, 5.0, frame_t - 4.5 - i * 4.8, 9, 0.9, color="#cfc9bd")

    col_l, col_r = 21.0, 92.0

    # title + the rule under it
    ax.text(col_l, frame_t - 5.5, "Wikidian", fontsize=11, fontfamily=SERIF,
            color=INK, va="center")
    ax.plot([col_l, col_r], [frame_t - 10.5, frame_t - 10.5], color=RULE,
            lw=0.8)

    # infobox
    box_w = 0.25 * (col_r - col_l)
    box_l = col_r - box_w
    box_t, box_b = frame_t - 13.0, frame_t - 40.0
    ax.add_patch(Rectangle((box_l, box_b), box_w, box_t - box_b,
                           facecolor=FILL, edgecolor=RULE, lw=0.7))
    for i in range(6):
        _bar(ax, box_l + 1.3, box_t - 3.4 - i * 4.1, box_w - 2.6, 1.0,
             color="#cfc9bd")

    # body text: short lines beside the infobox, full measure below it
    y = box_t - 3.4
    while y > box_b - 1:
        _bar(ax, col_l, y, (box_l - col_l) - 2.2, 1.05)
        y -= 4.1
    while y > frame_b + 3.5:
        _bar(ax, col_l, y, col_r - col_l, 1.05)
        y -= 4.1

    # measure rule, inside the frame
    ax.annotate("", xy=(col_l, frame_b + 1.8), xytext=(col_r, frame_b + 1.8),
                arrowprops=dict(arrowstyle="<->", color=RULE, lw=0.6))

    _label(ax, "sidebar", (9.5, frame_b + 12), (3, 8.0))
    _label(ax, "reading column", (col_l + 14, frame_b + 8), (24, 8.0))
    _label(ax, "infobox", (box_l + box_w / 2, box_b + 8), (66, 8.0))
    ax.text(50, 3.0, "the measure holds whether or not an infobox is there",
            fontsize=5.6, fontfamily=SANS, color=RULE, ha="center",
            va="center")

    _save(fig, "reading-column.png")


def type_hierarchy() -> None:
    """Specimen of the three-way split: serif title, sans headings, serif body."""
    fig, ax = _canvas(4.4, 3.2)

    rows = [
        (60.0, "Wikidian", 15, SERIF, "normal", "article title · Libertine"),
        (44.0, "Design", 8.6, SANS, "bold", "section heading · sans"),
        (31.0, "Reading column", 6.8, SANS, "bold", "subsection · sans"),
        (19.0, "Type is split three ways: a serif", 6.6, SERIF, "normal",
         "body text · serif"),
    ]

    for y, text, size, fam, weight, tag in rows:
        ax.text(6, y, text, fontsize=size, fontfamily=fam, fontweight=weight,
                color=INK, va="baseline")
        ax.plot([6, 94], [y - 2.4, y - 2.4], color=RULE, lw=0.4,
                ls=(0, (2, 2)))
        ax.text(94, y - 1.4, tag, fontsize=5.2, fontfamily=SANS, color=RULE,
                ha="right", va="baseline")

    ax.text(6, 8.0, "one face for reading, one for scanning, one for the app",
            fontsize=5.6, fontfamily=SANS, color=RULE, va="baseline")
    _save(fig, "type-hierarchy.png")


def colour_roles() -> None:
    """The four semantic roles, as a wash and as a text colour."""
    fig, ax = _canvas(4.4, 2.6)
    h = 100 * 2.6 / 4.4

    ax.text(6, h - 6, "wash", fontsize=6.0, fontfamily=SANS, color=RULE,
            va="center")
    ax.text(40, h - 6, "text", fontsize=6.0, fontfamily=SANS, color=RULE,
            va="center")
    ax.text(58, h - 6, "meaning", fontsize=6.0, fontfamily=SANS, color=RULE,
            va="center")

    y = h - 13
    for name, hexv, meaning in ROLES:
        r, g, b = (int(hexv[i:i + 2], 16) for i in (1, 3, 5))
        wash = (r / 255, g / 255, b / 255, 0.45)
        ax.add_patch(Rectangle((6, y - 3.4), 28, 7.0, facecolor=wash,
                               edgecolor="none"))
        ax.text(7.5, y, name, fontsize=7.0, fontfamily=SERIF, color=INK,
                va="center")
        # text colour: the snippet darkens the hue 22% toward black on light
        dark = tuple(c * 0.78 for c in (r / 255, g / 255, b / 255))
        ax.text(40, y, name, fontsize=7.0, fontfamily=SERIF, color=dark,
                va="center")
        ax.text(58, y, meaning, fontsize=5.8, fontfamily=SANS, color=INK,
                va="center")
        y -= 9.6

    ax.plot([6, 94], [y + 3.0, y + 3.0], color=RULE, lw=0.5)
    ax.text(6, y - 1.5, "one hue per role, followed through both treatments",
            fontsize=5.6, fontfamily=SANS, color=RULE, va="center")
    _save(fig, "colour-roles.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    reading_column()
    type_hierarchy()
    colour_roles()


if __name__ == "__main__":
    main()
