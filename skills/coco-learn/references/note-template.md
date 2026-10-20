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
| Related | Bullets that each hold a link; relative links must resolve | 0–5 bullets |
| Whole note | Every line after the frontmatter, blank lines included | 60 lines |

`status` records evidence, not coverage:

- `learning`: captured but not yet demonstrated.
- `understood`: the learner explained it back or answered its self-check correctly.
- `review`: a misconception surfaced or the note may be stale; reread it first.

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

````markdown
---
title: Atomic replace with os.replace
tags: [python, filesystem]
status: understood
created: 2026-10-20
updated: 2026-10-20
sources: [https://docs.python.org/3/library/os.html#os.replace]
---

# Atomic replace with os.replace

> `os.replace(src, dst)` moves a finished file over the target in one step, so readers see the old or the new file, never half of one.

## Key points

- Write the new content to a temporary path first, then `os.replace` it over the target.
- On POSIX the rename is atomic when both paths are on the same filesystem.
- It silently replaces an existing file, unlike `os.rename` on Windows, which raises.
- Create the temporary file next to the target so both share a filesystem.

## Example

```python
tmp = target.with_name(target.name + '.tmp')
tmp.write_text(content)
os.replace(tmp, target)  # readers never see a partial file
```

## Pitfalls

- Atomic is not durable: `fsync` the file and its directory if a crash must not lose it.
- A temporary file under `/tmp` may sit on another filesystem, where the call raises `OSError`.

## Self-check

<details><summary>Why create the temporary file next to the target?</summary>The rename is atomic only within one filesystem; a sibling path guarantees that.</details>
<details><summary>What does os.replace not promise after a power loss?</summary>Durability: the data may still be cached until it is synced.</details>

## Related

- [Python documentation: os.replace](https://docs.python.org/3/library/os.html#os.replace)
````
