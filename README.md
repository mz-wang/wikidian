# Wikidian

An Obsidian theme that makes your vault read like an encyclopedia article.
Wikipedia-style headings, floating infoboxes, bordered images, and a sidebar
that gets out of the way.

> Wikidian is a fork of [Wikipedia][upstream] by Ha'ani Whitlock, rebuilt around
> a source tree and a build step. See [Credits](#credits).

<!-- TODO: screenshots -->

## Install

**From the community themes browser** — not yet listed.

**Manually** — copy `manifest.json` and `theme.css` into
`<vault>/.obsidian/themes/Wikidian/`, then pick **Wikidian** under
*Settings → Appearance → Themes*.

The [Style Settings][style-settings] plugin is optional but unlocks the ribbon,
frontmatter, infobox, and image-float options described below.

## Features

### Infoboxes

Any **Info** callout (`>[!info]`) floats to the right of the note like a
Wikipedia infobox. Inline Dataview fields written in brackets inside it — for
example `[category::research]` — are laid out on separate lines and styled like
infobox labels and values. A **Heading 6** inside the callout becomes a section
header with a yellow background.

> [!tip]
> Hide the callout's own title with Style Settings for a cleaner infobox.

### Properties

A note's properties table is styled as an infobox too — floated, with each
property's name as a centred label above its value. It stays fully
interactive: the type icon and *Add property* button fade in on hover rather
than being removed. Style Settings can switch it to an inline label-and-value
list, or hide it in both views.

Requires Obsidian 1.4 or later, where properties replaced the old frontmatter
block.

### Callout alts

| Alt      | Effect                                                        |
| -------- | ------------------------------------------------------------- |
| `right`  | float the callout right                                       |
| `left`   | float the callout left                                        |
| `normal` | on an Info callout, drop the infobox styling                  |
| `info`   | give any callout the infobox look                             |

```markdown
>[!info|normal] Looks like a regular callout instead of an infobox.

>[!bug|right] A bug callout that floats right like an infobox.

>[!quote|left] Floats to the left.

>[!check|info] A Check callout wearing infobox styling.
```

### Image alts

| Alt                    | Effect                  |
| ---------------------- | ----------------------- |
| `right`                | float right             |
| `left`                 | float left              |
| `center`               | center, no float        |
| `no-float` / `normal`  | full width, no float    |

```markdown
![[books.png|no-float]]
![right](books.png)
![[books.png|left]]
![center](books.png)
```

Images float by default and alternate sides when several appear in a row.
Images inside callouts never float. The global default is configurable in
Style Settings.

### Snippets

`snippets/` holds optional CSS snippets that are **not** part of the theme.
Copy one into `<vault>/.obsidian/snippets/` and enable it under
*Settings → Appearance → CSS snippets*.

- `float-images-callouts-blockquotes.css` — extends floating to blockquotes.

## Development

`theme.css` is generated. Edit the modules in `src/` and rebuild:

```sh
uv run build.py            # regenerate theme.css
uv run build.py --check    # fail if theme.css is stale (what CI runs)
npm install && npm run lint    # stylelint, using Obsidian's own config
npm run lint:fix               # apply the fixable ones
```

`src/*.css` is concatenated in filename order, and `{{ font: ... }}`
placeholders are replaced with base64 data URIs from `fonts/`. The fonts are
inlined because Obsidian installs a theme by copying only `manifest.json` and
`theme.css` — there is no second file it would fetch.

```
src/                   theme source, one file per area
fonts/                 subset WOFF2 faces + their license
tools/subset_fonts.py  regenerate the font subsets from upstream
build.py               src/ + fonts/ -> theme.css
snippets/              optional add-ons, not part of the theme
screenshots/           store listing images (512x288)
```

To iterate, copy or symlink the repo into
`<vault>/.obsidian/themes/Wikidian/` — the folder name must match `name` in
`manifest.json` — and reload Obsidian after each build.

Release and store-submission steps are in [RELEASING.md](RELEASING.md).

## Credits

Wikidian is derived from **[Wikipedia][upstream]** by Ha'ani Whitlock, used
under the MIT License. Much of the original CSS was adapted from wikipedia.org
and mapped onto Obsidian's components. Both copyright notices are retained in
[LICENSE](LICENSE).

Headings are set in **Wikidian Libertine**, a Latin subset of *Linux Libertine
O* by Philipp H. Poll, used under the SIL Open Font License 1.1. See
[fonts/README.md](fonts/README.md) and [fonts/OFL.txt](fonts/OFL.txt).

This project is not affiliated with or endorsed by Wikipedia or the Wikimedia
Foundation.

## License

[MIT](LICENSE) for the theme. Bundled fonts are under the
[SIL OFL 1.1](fonts/OFL.txt).

[upstream]: https://github.com/Bluemoondragon07/Wikipedia-Theme
[style-settings]: https://github.com/mgmeyers/obsidian-style-settings
