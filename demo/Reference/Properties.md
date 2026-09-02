---
type: reference page
subject: Properties
shape: floated infobox
source: the note's own frontmatter
requires: Obsidian 1.10.6
updated: 2026-09-02
tags:
  - properties
  - infobox
---

The block at the top right of this note is the note's own **properties** table.
Wikidian floats it and gives it the infobox treatment: each property's name
becomes a centred label above its value, and the whole table takes the infobox
width and margin.

Nothing is written by hand — the frontmatter is the source, so the box is a
view of the note's metadata rather than a copy of it.

## It stays interactive

The temptation with a styled properties table is to strip the controls out of
it. Wikidian doesn't: the type icon and the *Add property* button are faded
rather than removed, and come back on hover. Clicking a value still edits it,
and a new property still lands in the box.

>[!tip]
>Style Settings can switch the box to an inline label-and-value list, or hide
>it in reading view, in editing view, or both.

## Requirements

Properties arrived in Obsidian 1.4 and the layout Wikidian targets settled by
**1.10.6**, which is the `minAppVersion` in the manifest.

See also [[Infoboxes]], [[Wikidian]].
