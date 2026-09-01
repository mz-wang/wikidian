# Fonts

`WikidianLibertine-*.woff2` are subsets of **Linux Libertine O 5.3.0** by
Philipp H. Poll (<http://www.linuxlibertine.org>), reduced to the Latin and
Latin-Ext Unicode ranges and re-encoded as WOFF2.

| Face    | Glyphs (from 2 300–2 700) | Size            |
| ------- | ------------------------- | --------------- |
| Regular | 1 048                     | 60.6 KB         |
| Bold    | 1 008                     | 57.8 KB         |
| Italic  |   970                     | 62.0 KB         |

Regenerate with:

```sh
uv run tools/subset_fonts.py <dir-with-upstream-LinuxLibertine-{Regular,Bold,Italic}.woff>
```

## Licensing

Linux Libertine is dual-licensed under the **SIL Open Font License 1.1** and the
**GNU GPL with Font Exception**. This project distributes it under the OFL; the
full text is in [OFL.txt](OFL.txt).

"Linux Libertine" is a Reserved Font Name. A subset is a Modified Version under
OFL clause 3, which may not carry the Reserved Font Name, so these faces declare
the family **Wikidian Libertine** instead. The original copyright, vendor and
license records in each font's `name` table are preserved unchanged, as OFL
clauses 1 and 2 require.
