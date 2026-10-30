---
name: coco-til
description: "Use when capturing reusable concepts from the current session directly into personal TIL notes, selecting at most three concepts per topic and saving them in the primary checkout."
license: MIT
---

# coco-til

Capture the current session's reusable knowledge immediately as short, uniform personal notes. Follow the [common contract](../_coco-shared/contracts.md) and the unchanged [note format](references/note-template.md). Localize note content and section labels to the user's language.

A bare invocation already selects current-session capture: do not open a request menu, ask the user to choose candidates, or ask whether to save. An explicit topic or subset narrows the session scope. Never start a lesson, quiz, review program or multi-session learning mission.

## Select concepts

1. Inspect the visible conversation, including available summaries, and directly relevant code, tests or sources already discussed. State missing session evidence instead of searching other chats or private history. Read only what is necessary to verify a candidate; do not expand into unrelated research to fill notes.
2. Group candidates into meaningful topics. Prefer corrected misconceptions, mechanisms behind unexpected behavior, reasons and trade-offs behind decisions, and reusable principles or failure-prevention techniques. Exclude activity logs, changed-file lists, command transcripts, passing terminology and unsupported claims.
3. Select **at most three concepts per topic**, not a quota. Select one or two when that is all the evidence supports; select none when nothing is worth retaining. Do not split topics artificially to evade the cap. Merge synonymous candidates before counting. One concept produces one note, with topics grouped in the index.
4. If no worthwhile concept remains, report that briefly and stop without creating folders, templates, notes or ignore rules. Otherwise resolve storage before the first write.

## Resolve durable storage

1. Run the read-only [workspace resolver](tools/resolve_workspace.py): `python3 <coco-til folder>/tools/resolve_workspace.py <current-working-directory>`. Use its `til` output as the sole note root. It resolves the **primary checkout**, not the checkout of a branch named main or master. In a Git repository the destination is always `<primary-checkout>/TIL/`, even when ignored, untracked, invoked from a linked worktree, or currently on another branch. Outside Git it is `<current-working-directory>/TIL/`.
2. If Git metadata cannot establish an existing non-bare primary checkout, stop before writing and report the missing path/evidence. If the primary destination is not writable, obtain the runtime's required access. Never silently fall back to the current linked worktree or a different folder. Recheck resolution before writing if repository/worktree state changed.
3. Inspect existing files and reject symlinks escaping the note root, including symlinked templates, index and note files, before reading/writing them. If legacy notes exist in the current linked worktree, preserve them: compare with the primary notes, copy missing content without deleting originals, and stop only conflicting updates for user resolution. Never overwrite divergent content or call a migration complete when conflicts remain.
4. Create the resolved root when missing. In Git, ensure the **primary checkout's** root `.gitignore` contains `TIL/`, appending only when absent; preserve other content and reject a symlinked `.gitignore`. Say when it changed. If notes are already tracked, explain that ignoring does not untrack them and leave `git rm --cached` to the user. Never stage or commit notes or make a project commit in this workflow.

## Write or update

1. Read `INDEX.md` and `TEMPLATE.md` at the resolved root. On first use create both and `notes/` from the [note format](references/note-template.md); preserve existing notes and established translated labels.
2. Search index titles/hooks and note tags/content for each selected concept. Match meaning, not just filenames. Update an existing note only for new or corrected evidenced information; create a note only for a missing concept. Repeated capture with no new information must not create duplicates or touch timestamps. A required first-time storage/ignore repair is separate from a no-op note update.
3. Keep one concept per note and all existing template sections in their exact order. Stay within the format's budgets; split distinct concepts or link sources instead of stretching limits. The per-topic selection cap still applies to any newly selected split concepts.
4. Write a standalone definition, short key points, a concrete session-grounded example, pitfalls and self-check answers. Explain mechanism and evidenced rationale in familiar words, restoring needed context without retelling the session or adding jargon. Do not copy long code or conversation logs. Distinguish observed fact, general principle, inference and uncertainty; omit unsupported certainty.
5. Code sources must remain traceable after linked-worktree deletion: record repository-relative path and symbol plus the inspected commit, or explicitly label uncommitted behavior. Do not rely solely on a temporary absolute path or line number. Do not rewrite a linked-worktree observation as if it came from primary-checkout code.
6. New notes start with `status: learning`; capture alone is never evidence of understanding. Preserve existing evidence-backed status unless a demonstrated misconception or stale fact warrants `review`, naming why. Do not mark `understood` merely because a topic appeared in the session. Preserve existing user content; do not silently remove substantive statements while condensing.
7. For actual content changes set `updated`, maintain exactly one index entry per note, then run the [checker](tools/check_notes.py): `python3 <coco-til folder>/tools/check_notes.py <resolved-til-root>`. Fix reported problems before claiming success. The checker enforces layout, not concept importance, semantic duplication or factual truth; review those separately.

## Boundaries and return

Personal TIL is this skill's output. Project documents for other readers belong to `coco-docs`; interactive questions and evidence-backed investigation belong to `coco-askme` (`coco-research` is its compatibility alias). Capturing notes authorizes neither code edits, project commits, publication, blog offers nor scheduling.

Return a short topic-grouped list of created/updated note paths, meaningful skipped duplicates, storage/ignore changes, checker result and any unresolved conflicts or unverifiable facts. Do not dump the notes back into chat or start an obligatory quiz.
