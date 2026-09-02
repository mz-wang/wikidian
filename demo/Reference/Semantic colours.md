Obsidian's ==highlight== has one colour and no way to vary it, and there is
no markdown for a text colour at all. `semantic-colors.css` — an optional
snippet, not part of the theme — defines four roles that cover both.

The tag picks the treatment and the class picks the role:

| Tag                          | Effect                    |
| ---------------------------- | ------------------------- |
| `<mark class="key">…</mark>` | a wash behind the text    |
| `<span class="key">…</span>` | the text itself           |
| `<code class="key">…</code>` | inline code, chip and all |

![[colour-roles.png|right]]

| Role   | Colour | Meaning                                   |
| ------ | ------ | ----------------------------------------- |
| `note` | blue   | an aside, a cross-reference               |
| `ok`   | green  | settled, verified, done                   |
| `warn` | orange | a caveat, an open question                |
| `key`  | purple | the load-bearing sentence on the page     |

## In use

<mark class="key">The measure is fixed rather than elastic, and the infobox is
subtracted from it.</mark> That one sentence carries the layout; the rest of
the page is commentary on it.

<mark class="warn">Rebuilding the stylesheet does not update a vault's copy of
it.</mark> The theme is installed as a file copy, so the new `theme.css` has to
be put there again.

The flag is <span class="note">optional</span> unless you passed
<code class="warn">--strict</code>, in which case it is required.

<span class="ok">Verified on <code>1.13.7</code>.</span>

## Writing it

Nested formatting has to be HTML too — `<code>x</code>`, not a backticked
`x`. Reading view parses markdown inside the tag; live preview hands the tag to
a widget that does not, so backticks would show up literally while you write
and vanish when you read.

Inline code inside a coloured `<span>` picks the role up on its own. A lone
piece of coloured code carries the class itself.

## Why they follow the theme

The four hues are the theme's own palette variables rather than fixed values.
As a wash they need only an alpha, and a different one per theme — the same hue
wants more weight on white than on the dark surface. As *text* they need more
than that: the palette's mid tones sit near 3:1 against the page, so each role
is pulled darker on the light theme and lighter on the dark one, in `oklch` so
the hue survives the shift.

See also [[Wikidian]], [[Typography]].
