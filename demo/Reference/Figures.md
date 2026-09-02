Images are treated as plates: bordered, padded against a slightly darker
ground, floated at infobox width, and alternating sides when several appear in
a row — which is what keeps a long article from growing a column of pictures
down one edge.

![[reading-column.png|right]]

## Alts

An alt in the embed overrides the default for one image.

| Alt                   | Effect               |
| --------------------- | -------------------- |
| `right`               | float right          |
| `left`                | float left           |
| `center`              | centre, no float     |
| `no-float` / `normal` | full width, no float |

```markdown
![[reading-column.png|right]]
![[type-hierarchy.png|left]]
![[colour-roles.png|center]]
![right](Attachments/reading-column.png)
```

Both embed syntaxes take the alt: `![[file.png|right]]` and
`![right](file.png)`.

![[type-hierarchy.png|left]]

## Where floating stops

Images inside a callout never float — a plate inside an aside would have
nowhere to wrap to. The community-theme browser is exempted as well, so a
theme's own screenshot still fills its card.

The global default is a Style Settings option: float right, float left, centre,
or off entirely. An optional snippet,
`float-images-callouts-blockquotes.css`, extends the same floating to
blockquotes.

![[colour-roles.png|center]]

Above: centred with `|center`, which is the shape to use for a figure wide
enough that wrapping text beside it would leave a two-word column.

See also [[Wikidian]], [[Semantic colours]].
