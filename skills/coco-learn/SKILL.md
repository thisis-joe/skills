---
name: coco-learn
description: "Use when the user wants to understand something for themselves: explain code, a concept or an earlier answer in plain words, save or update a personal study note, review or condense existing notes, or keep a multi-session learning workspace."
license: MIT
---

# coco-learn

Help the user understand something and keep it in short, uniform notes they can reread in about a minute. Every note follows the [note format](references/note-template.md).

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, check for a multi-session learning workspace: a learning mission, lessons, learning records or a glossary. If it applies or is unclear, read the [learning procedures](../_coco-shared/advanced/learn.md) before dependent work.

Localize explanations, note content and section labels to the user's language; the English names here are canonical identifiers.

## Boundary

- The reader is the user. Documents for a team, users, operators, API callers or agents, and anything that belongs in the project, go to `coco-docs`. Personal notes never go into project documentation.
- One-question-at-a-time quizzing is `coco-askme`. Its closing summary can be saved here as notes.
- Learning does not authorize code edits, commits to a project repository or posting anywhere. When the user asks for a project document or code change, say in one line that it belongs to `coco-docs` or `coco-build` and continue with that skill for the requested change, instead of ending with a pointer.

## Mode selection

| Mode | Choose when | Result |
|---|---|---|
| Explain | The user wants to understand now and asks for no file | Chat explanation, then an offer to save it as notes |
| Note | The user asks to save, write up, organize or update what they learned | One note per concept, created or updated, index updated, checker passing |
| Review | The user wants to reread, condense, clean up or practice existing notes | Notes back within budget, duplicates merged, a short retrieval round |
| Workspace | The user wants to learn a subject over several sessions toward a goal | Mission-led lessons and records from [learning procedures](../_coco-shared/advanced/learn.md) |

## Explain

1. Start from the user's purpose and what they already know. Read the actual code, tests or decision history before explaining it.
2. Give the smallest complete definition, connect it to the user's real system with `path:line`, then combine mechanism with evidenced rationale. Walk a real user or caller action rather than listing functions.
3. Reveal depth at the user's pace. Do not add an obligatory quiz or artificial pacing. Use code, debugger output or an incrementally built diagram only when it makes the mechanism easier to grasp.
4. Separate code fact, general principle and inference. Check version-specific behavior against the project's version and say when you could not.
5. For a plain-language repitch, restate the preceding answer in familiar words. Keep its meaning, restore missing context, and make it shorter rather than deeper.
6. Shape a substantial explanation like a note (one-sentence summary, key points, example, pitfalls) so that saving it later is a copy, not a rewrite.

## Note

1. Resolve the workspace (see below). Read its `INDEX.md` and `TEMPLATE.md`; on first use create both, plus `notes/`, from the [note format](references/note-template.md).
2. Search the index titles and hooks and the note tags for the concept. Update an existing note in place; create a note only for a concept the workspace does not have. When the user asks to add material to a note but it is another concept or would break the budget, put it in a new linked note and say so in one line.
3. Keep one concept per note, one that answers "what is X", "how does X work" or "why X". Material with several concepts becomes several linked notes.
4. Start from `TEMPLATE.md`: the same sections in the same order, none added, renamed or removed. Stay within the budget; when content does not fit, follow "When a note grows" in the format instead of stretching the note.
5. Write for rereading. The summary line must restore the idea on its own. Each bullet holds one idea. Prefer the user's own code as the example, cited as `<repository>/<path>:<line>` plus the symbol name because line numbers drift. Link sources instead of copying them. Leave out conversation history, session dates, tool output and what the user already knows well.
6. Set `status` from evidence. Use `learning` when capturing. Use `understood` only after the user explained the note's core idea back correctly or answered its self-check questions correctly; a partly correct answer keeps the status, and you name the missing part and ask about it. Use `review` when a misconception surfaced, the note may be stale or the user marked it for another look. Covered material is not learned material.
7. Set `updated`, add or adjust the note's one `INDEX.md` line, and run the [checker](tools/check_notes.py) on the workspace. Fix every reported problem before reporting the note as saved.

## Review

1. Run the checker on the workspace and fix its problems first.
2. Bring an over-budget note back within budget with the ordered steps in the format. Treat existing note content as the user's: condense and move it while keeping its meaning, and list every statement you removed in the reply so the user can restore it. A personal reminder such as "look at this again" becomes `status: review`, and its substance moves into Pitfalls or Self-check rather than free prose.
3. Merge notes on the same concept into the older file, combine their sources, and fix links and the index.
4. Offer a short retrieval round from the self-check questions of the notes the checker lists to reread next, one question at a time with the answer withheld until the user replies. Change `status` only on demonstrated answers.

## Workspace location

1. The workspace is always the `TIL/` folder directly under the root of the current Git work tree (`git rev-parse --show-toplevel`); outside a Git work tree, it is `TIL/` under the current working directory. Do not ask for or suggest another location. For an explanation only, no folder is needed.
2. Create `TIL/` when it does not exist, then set it up as in step 1 of Note.
3. Tell the user whether `TIL/` is tracked by Git. Do not commit notes or edit ignore rules unless asked.

## Return

- Explain: the explanation and an offer to save it.
- Note and Review: changed note paths, the index change, the checker result, and each status change with its evidence.
- Unverified facts and sources that could not be checked are named, not smoothed over.
- Keep the reply short. The note holds the content; the reply says what changed and what to do next.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "This concept is too important to split" or "the extra detail may help later": the budget exists so the note stays rereadable; split or link instead.
- A note that retells the session, copies documentation or pastes long code instead of linking it.
- `understood` set because the material was covered, not because the user demonstrated it.
- A second note for a concept the index already has, or a section renamed in one note only.
