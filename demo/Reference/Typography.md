![[type-hierarchy.png|right]]

Type is split three ways. A serif carries the reading — body text and the
article title. A sans carries the scanning layer — every heading from H2 down.
The application's own chrome keeps a neutral interface face, so tabs, the
sidebar, and the status bar stay out of the way of the page.

Wikipedia does this the other way round, with serif headings over a sans body.
Wikidian inverts it because a serif body is what long-form reading wants; the
contrast then has to move up into the headings to keep them legible as
structure.

## The scale

The article title is the note's own name, set at 2.3em with a rule under it.
Headings step down gently from there — 1.7, 1.25, 1.17, 1.12, 1.0, 0.99 —
because an encyclopedia article is mostly H2 and H3 and a steep ramp would make
the lower levels indistinguishable from bold text.

### A third level

Which is where most of the detail actually lives.

#### And a fourth

Below this the difference is weight, not size.

## Faces

Latin always lands somewhere known. The article title is set in **Wikidian
Libertine**, a subset of Linux Libertine that ships inside `theme.css` as
base64, because Obsidian installs a theme by copying two files and there is no
second request it would make.

CJK cannot travel the same way — a Chinese face runs to several megabytes — so
the stack names **Source Han Serif SC** and **Source Han Sans SC** and takes
them from the system. See [[中文排版]].

>[!note]
>A font chosen under *Settings → Appearance* overrides all of this, as usual.
>The theme sets the stack; it does not take the setting away.

## Specimen

The quick brown fox jumps over the lazy dog. Portez ce vieux whisky au juge
blond qui fume. Съешь же ещё этих мягких французских булок.

`monospace holds the code chips and the inline paths`

> A block quotation keeps the serif and takes a rule down its left edge, so it
> reads as quoted rather than as emphasised.

See also [[Wikidian]], [[Semantic colours]].
