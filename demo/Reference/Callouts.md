Callouts keep Obsidian's own type set and its icons; what Wikidian changes is
the tinting — every callout is washed against the theme's palette rather than
against Obsidian's defaults — and the title, which is centred on its own bar
instead of sitting beside the icon.

## Alts

An alt goes after a pipe in the callout's type. Two of them move a callout
between the two available shapes: the ordinary block, and the infobox that an
**Info** callout gets for free.

| Alt      | Effect                                        |
| -------- | --------------------------------------------- |
| `right`  | float the callout right, at infobox width     |
| `left`   | float the callout left                        |
| `normal` | on an Info callout, drop the infobox styling  |
| `info`   | give any callout the infobox look             |

>[!bug|right] Floated right
>`>[!bug|right]` puts a bug callout where an infobox would go, at the same
>width and margin.

>[!info|normal] Not an infobox
>An Info callout with `|normal` keeps the ordinary block shape, for when a note
>already has an infobox and needs a plain aside as well.

Floated callouts take the infobox width and margin, so they line up with the
properties table and with any figures on the same side of the page.

## The set

>[!note] Note
>The default. Blue, and the one to reach for when nothing more specific fits.

>[!tip] Tip
>Titles are centred on the bar rather than set beside the icon, which is what
>makes a stack of callouts read as a column of cards.

>[!warning] Warning
>The wash is mixed from the theme's palette with `color-mix()`, so the whole
>set moves together when the palette does.

>[!quote] Quote
>An encyclopedia is a system for putting a thing in its place.

>[!example]- Collapsed
>Collapsible callouts work as they always did; the arrow sits at the end of the
>title bar.

See also [[Infoboxes]], [[Wikidian]].
