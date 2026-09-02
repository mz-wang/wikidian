>[!info] Wikidian
>[type:: Obsidian theme]
>[author:: Mengzhao Wang]
>[released:: 2 September 2026]
>[version:: 1.0.0]
>[written in:: CSS]
>[license:: MIT]
>[forked from:: Wikipedia]

**Wikidian** is a theme for Obsidian that gives a personal vault the reading
conventions of an encyclopedia article: a serif reading column, an infobox set
against the opening paragraphs, section headings in a sans so that structure
and prose are told apart at a glance, and figures bordered and floated with the
text wrapping around them.

It is a fork of the **Wikipedia** theme by Ha'ani Whitlock, rebuilt around a
source tree and a build step.[^fork] The stylesheet is generated from a dozen
modules, one per area of the interface, and the Latin faces travel inside it as
base64 so that installing the theme stays a two-file copy.

## Design

![[reading-column.png|right]]

Wikidian takes the parts of an encyclopedia page that earn their keep in a
notes app and leaves the rest. What it keeps is the shape of a reference
article: something you arrive at from a link, read a third of, and leave.

### Reading column

The measure is fixed rather than elastic, and the infobox is subtracted from it
rather than added beside it, so a note with an infobox and a note without one
break their lines in the same places. Floated blocks — infoboxes, properties,
figures — all share one width and one margin, which keeps a page with several
of them from drifting into a ragged left edge.

The sidebar sits on a single grey field, and files carry an icon, so the tree
reads as a list of documents rather than as indented text.

### Type

![[type-hierarchy.png|left]]

Type is split three ways: a serif for reading, a sans for scanning, and the
platform's own interface face for the application chrome. Body text and the
article title are set in the serif; every heading below the title is set in the
sans.

Wikipedia does the reverse — serif headings over a sans body — but a serif body
is what long-form reading wants, so the contrast moves up into the headings
instead. The article title always lands on **Wikidian Libertine**, a Latin
subset of Linux Libertine that ships inside the stylesheet.

CJK faces are named in the stack but not bundled: a Latin subset is sixty
kilobytes a face and a Chinese one runs to several megabytes, which no
stylesheet can carry.[^cjk] See [[中文排版]].

## Components

### Infoboxes

Any **Info** callout floats to the right of the opening paragraphs, as the one
at the top of this article does. Inline fields written inside it are laid out
as labels and values rather than as a run of text. A note's own properties
table gets the same treatment without any markup at all.

See [[Infoboxes]] and [[Properties]].

### Callouts

The full callout set is retinted against the theme's palette, and four alts —
`right`, `left`, `normal`, `info` — move a callout between the two shapes.
See [[Callouts]].

### Figures

Images are bordered, floated, and alternate sides when several appear in a row,
the way plates do down the side of an article. Four alts override the default.
See [[Figures]].

### Semantic colours

An optional snippet adds four colour roles — `note`, `ok`, `warn`, `key` —
usable as a highlight or as a text colour, drawn from the theme's own palette
so they follow it between light and dark. See [[Semantic colours]].

## Installation

Copy `manifest.json` and `theme.css` into
`<vault>/.obsidian/themes/Wikidian/`, then choose **Wikidian** under
*Settings → Appearance → Themes*. The
[Style Settings](https://github.com/mgmeyers/obsidian-style-settings) plugin is
optional, and unlocks the ribbon, infobox, and float options.

## See also

- [[Callouts]] — the callout set and its four alts
- [[Figures]] — floating images and their alts
- [[Infoboxes]] — the Info callout as an infobox
- [[Properties]] — the frontmatter table as an infobox
- [[Semantic colours]] — four roles as a wash or as text
- [[Typography]] — the type specimen in full
- [[中文排版]] — the CJK stack

## Notes

[^fork]: The upstream theme is [Wikipedia](https://github.com/Bluemoondragon07/Wikipedia-Theme)
    by Ha'ani Whitlock, used under the MIT License. Both copyright notices are
    retained.

[^cjk]: Install **Source Han Serif SC** and **Source Han Sans SC**, or their
    Noto twins, for the intended look. Without them CJK text falls back to
    whatever serif and sans the platform provides.
