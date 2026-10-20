# Learning note format

A note holds one concept in a shape the learner can reread in about a minute. Every note in a workspace has the same parts in the same order; only the content changes. The [checker](../tools/check_notes.py) enforces this page, so change its limits and this page together.

## Workspace layout

```text
<workspace>/
  INDEX.md          entry point: one line per note, grouped by topic
  TEMPLATE.md       this workspace's note template; the authority for section labels
  notes/<slug>.md   one concept per note; slug is lowercase ASCII words joined by hyphens
```

Workspace mode adds mission files beside these; see [learning procedures](../../_coco-shared/advanced/learn.md).

## TEMPLATE.md

Create `TEMPLATE.md` on first use from the canonical template below. Translate the five section labels and the placeholder text once into the learner's language. After that, start every note from `TEMPLATE.md` and never rename, add, drop or reorder a section in a single note. To change a label, edit `TEMPLATE.md` and every note in the same change. Frontmatter keys and `status` values stay in English because the checker reads them.

````markdown
---
title: <concept name>
tags: [<topic>]
status: learning
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources: [<path:line or URL>]
---

# <concept name>

> <One sentence: what it is and why it matters.>

## Key points

- <One idea per line.>

## Example

<The smallest concrete case, preferably the learner's own code cited as path:line.>

## Pitfalls

- <A misconception, an edge case or a look-alike concept.>

## Self-check

<details><summary><A question this note answers></summary><A short answer></details>

## Related

- <A Markdown link to a related note or a source.>
````

## Rules and budget

| Part | Rule | Limit |
|---|---|---|
| Frontmatter | Exactly `title`, `tags`, `status`, `created`, `updated`, `sources`. Dates are `YYYY-MM-DD`; `tags` and `sources` are `[a, b]` lists; `tags` names at least one topic | Required |
| Title | One level-one heading equal to `title`; no headings other than the title and the five sections | 1 |
| Summary | One blockquote line directly under the title that restores the idea on its own | 1 line, 200 characters |
| Key points | Top-level bullets, one idea each, no nesting or continuation lines | 2–5 bullets, 160 characters each |
| Example | One concrete case: prose, one code block, or both | 1 code block, 15 code lines |
| Pitfalls | Misconceptions, edge cases, look-alike concepts | 1–3 bullets, 160 characters each |
| Self-check | One `<details><summary>question</summary>answer</details>` line per question | 1–3 questions |
| Related | Bullets that each hold a link; relative and absolute local paths must exist | 0–5 bullets |
| Whole note | Every line after the frontmatter, blank lines included | 60 lines |

The limits are ceilings, not targets. Most notes need three key points, one or two pitfalls and one or two questions; a shorter note is easier to reread.

`status` records evidence, not coverage:

- `learning`: captured but not yet demonstrated.
- `understood`: the learner explained the core idea back or answered its self-check questions correctly.
- `review`: a misconception surfaced, the note may be stale or the learner marked it for another look; reread it first.

## When a note grows

A note over budget holds more than one concept or more detail than rereading needs. Fix it in this order: remove session narrative and repetition; replace copied material with a link to its source; move a sub-concept into its own note and link it from Related; let the original summarize its parts. Never raise a limit for one note.

## INDEX.md

Start with a level-one title, then one level-two heading per topic. Each entry is one bullet: a Markdown link whose text is the note title and whose target is `notes/<slug>.md`, then ` — ` and a hook of a few words. Every note appears exactly once. Keep status in the note, not in the index, so the two cannot disagree.

## Checking

```sh
python3 <coco-learn folder>/tools/check_notes.py <workspace>
python3 <coco-learn folder>/tools/check_notes.py <workspace>/notes/<slug>.md
```

A conforming workspace exits 0 and prints the status counts and the notes to reread next. Otherwise each problem prints as `path:line: problem` and the exit code is 1; a missing or malformed `TEMPLATE.md` exits 2.

## Example note

[example-note.md](example-note.md) is a complete note in the canonical labels; it passes the checker.
