The infobox is the one piece of Wikipedia's layout that a notes app can use
unchanged: a summary block, floated against the opening paragraphs, that says
what the article is about before the prose gets there.

>[!info] Anatomy
>###### Identity
>[name:: Infobox]
>[shape:: floated block]
>[width:: 25% of the measure]
>###### Markup
>[written as:: an Info callout]
>[fields:: inline Dataview fields]
>[sections:: level-six headings]
>###### Related
>[see also:: Properties]

Any **Info** callout gets the treatment. Inside it:

- A **level-six heading** groups the fields into sections. With Style
  Settings installed it takes a pale background bar, which is the shape
  Wikipedia uses for the same job.
- An **inline field**, written `[label:: value]`, is laid out as a label above
  its value rather than as a run of text. This needs the
  [Dataview](https://github.com/blacksmithgu/obsidian-dataview) plugin; without
  it the brackets show through.
- Ordinary paragraphs, lists, and images all still work; images inside a
  callout never float.

>[!tip]
>Style Settings can hide the callout's own title bar, which is what you want
>when the first section heading already names the thing.

The whole box above is written like this:

```markdown
>[!info] Anatomy
>###### Identity
>[name:: Infobox]
>[shape:: floated block]
```

To give some other callout the same shape, add the `info` alt — `>[!check|info]`.
To take it away from an Info callout, add `normal`. See [[Callouts]].

## Compared with properties

A note's frontmatter gets an infobox of its own, with no markup at all — see
[[Properties]]. The difference is control: the properties table is generated
from the note's own metadata and stays editable in place, while an Info callout
is written by hand and can hold anything, including sections and prose.

See also [[Wikidian]].
