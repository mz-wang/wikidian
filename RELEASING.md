# Releasing

## Cutting a release

```sh
npm run lint          # stylelint, using Obsidian's own config
uv run build.py       # regenerate theme.css from src/
npm version patch     # bumps package.json + manifest.json + versions.json
git push --follow-tags
```

Pushing the tag runs `.github/workflows/release.yml`, which re-checks that
`theme.css` matches `src/` and that the tag equals `manifest.json`'s `version`,
then opens a **draft** release with `manifest.json` and `theme.css` attached.
Review the notes and publish it.

The tag must be the bare version — `1.0.0`, not `v1.0.0`. Obsidian looks up a
release by the exact string in `manifest.json`.

## Submitting to the community theme store

Obsidian reads `manifest.json` from the HEAD of the default branch, so it must
be correct and pushed before you submit.

### Checklist

- [ ] `manifest.json` has `name`, `version` (strict `x.y.z`), `minAppVersion`,
      `author`. `authorUrl` is optional and must point at the repo or your
      profile — not a donation page.
- [ ] `name` is unique across [community-css-themes.json][registry].
      *"Wikidian" was unclaimed as of the last check; "Wikipedia" belongs to the
      upstream theme this one forks.*
- [ ] `minAppVersion` is an Obsidian version the theme has actually been tested
      against — not an aspirational floor.
- [ ] `README.md` and `LICENSE` are present. The README excerpt becomes the
      public listing.
- [ ] A screenshot is committed at a stable path. **512 x 288 px, 16:9.**
      Put it in `screenshots/` and reference it by repo-relative path.
- [ ] A published (not draft) GitHub release exists whose tag equals
      `manifest.json`'s `version`, with `manifest.json` and `theme.css`
      attached as assets.
- [ ] The theme renders correctly in **both** light and dark mode, or the
      registry entry declares only the mode it supports.

### Then

1. Sign in to [community.obsidian.md](https://community.obsidian.md) with your
   Obsidian account and link your GitHub account so ownership can be verified.
2. Add the theme through the directory. It generates the registry entry:

   ```json
   {
     "name": "Wikidian",
     "author": "Mengzhao Wang",
     "repo": "mz-wang/wikidian",
     "screenshot": "screenshots/<file>.png",
     "modes": ["dark", "light"]
   }
   ```

3. Review is automated. If it reports problems, fix them in the repo, bump the
   version, and publish a **new** release — the directory reads HEAD, so an
   amended release of the same version will not be picked up reliably.

## References

- [Build a theme](https://docs.obsidian.md/Themes/App+themes/Build+a+theme)
- [Submit your theme](https://docs.obsidian.md/Themes/App+themes/Submit+your+theme)
- [obsidianmd/obsidian-sample-theme](https://github.com/obsidianmd/obsidian-sample-theme)

[registry]: https://github.com/obsidianmd/obsidian-releases/blob/master/community-css-themes.json
