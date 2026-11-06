---
name: coco-til
description: "Use when saving reusable knowledge from the current session to personal TIL in the primary checkout, as up to three concept notes per topic and up to one verified troubleshooting case."
license: MIT
---

# coco-til

**Contents:** [Select concepts](#select-concepts) · [Select a troubleshooting case](#select-a-troubleshooting-case) · [Resolve durable storage](#resolve-durable-storage) · [Write or update](#write-or-update) · [Boundaries and return](#boundaries-and-return)

Capture the current session's reusable knowledge immediately as short, uniform concept notes and, when supported, a troubleshooting case the reader can follow later. Follow the [common contract](../_coco-shared/contracts.md) and the [concept note format](references/note-template.md). Select the two outputs independently within the requested scope. Localize the content and template section labels to the user's language.

A bare invocation already selects current-session capture: do not open a request menu, ask the user to choose candidates, or ask whether to save. An explicit topic or subset narrows the session scope. Never start a lesson, quiz, review program or multi-session learning mission.

## Select concepts

1. Inspect the visible conversation, including available summaries, and directly relevant code, tests or sources already discussed. State missing session evidence instead of searching other chats or private history. Read only what is necessary to verify a candidate; do not expand into unrelated research to fill notes.
2. Group candidates into meaningful topics. Prefer corrected misconceptions, mechanisms behind unexpected behavior, reasons and trade-offs behind decisions, and reusable principles or failure-prevention techniques. Exclude activity logs, changed-file lists, command transcripts, passing terminology and unsupported claims.
3. Select **at most three concepts per topic**, not a quota. Select one or two when that is all the evidence supports; select none when nothing is worth retaining. Do not split topics artificially to evade the cap. Merge synonymous candidates before counting. One concept produces one note, with topics grouped in the index.

## Select a troubleshooting case

1. Consider problems actually diagnosed and addressed in the visible session. A case needs all four: an observed symptom and a clear success criterion, an observation that informed the next diagnostic decision, an action actually taken with its rationale, and an observed recheck that meets the success criterion. Require traceable evidence such as a job and build number, a revision and repository path, or a relevant artifact or document. A proposed fix or a successful command that never checked the symptom is insufficient.
2. Read the [case format](references/case-template.md) if any problem qualifies. Choose at most one representative problem per session, preferring the clearest evidence and the procedure most useful on recurrence. If the visible session already created or updated a case, keep that representative and consider only new evidence for it. If conditions differed at recheck, record how and limit the claim to the result observed.
3. If there is no eligible case, continue with the selected concepts. If neither output qualifies, report that briefly and stop before creating folders, templates, index entries or ignore rules. A qualifying case can proceed with zero concepts.

## Resolve durable storage

1. Run the read-only [workspace resolver](tools/resolve_workspace.py): `python3 <coco-til folder>/tools/resolve_workspace.py <current-working-directory>`. Use its `til` output as the sole note root. It resolves the **primary checkout**, not the checkout of a branch named main or master. In a Git repository the destination is always `<primary-checkout>/TIL/`, even when ignored, untracked, invoked from a linked worktree, or currently on another branch. Outside Git it is `<current-working-directory>/TIL/`.
2. If Git metadata cannot establish an existing non-bare primary checkout, stop before writing and report the missing path/evidence. If the primary destination is not writable, obtain the runtime's required access. Never silently fall back to the current linked worktree or a different folder. Recheck resolution before writing if repository/worktree state changed.
3. Inspect existing paths read-only. Reject symlinks escaping the TIL root, including symlinked directories, templates, index, notes and cases, before reading or writing them. Read the existing index if present. For a selected case, decide whether it is new, has new evidence for a matching case, or needs no change using the [matching rules](references/case-template.md#match-existing-cases). If a duplicate case with no new evidence is the only selected output, report the skip and stop before any writes.

## Write or update

When proceeding to write, preserve legacy notes in the current linked worktree. Compare them with primary notes, copy missing content without deleting originals, and stop only conflicting updates for user resolution. Never overwrite divergent content or call a migration complete when conflicts remain.

Create the resolved root and `INDEX.md` when needed. In Git, ensure the **primary checkout's** root `.gitignore` contains `TIL/`, appending only when absent. Preserve other content and reject a symlinked `.gitignore`. Say when it changed. If notes or cases are already tracked, explain that ignoring does not untrack them and leave `git rm --cached` to the user. Never stage or commit TIL or make a project commit in this workflow.

### Concept notes

1. For selected concepts, read `TEMPLATE.md` at the resolved root. On first use create it and `notes/` from the [note format](references/note-template.md); preserve existing notes and established translated labels.
2. For each selected concept, search files under `notes/` and their index entries. Match meaning, not just filenames. Update an existing note only for new or corrected evidenced information; create a note only for a missing concept. Repeated capture with no new information must not create duplicates or touch timestamps. A required first-time storage/ignore repair is separate from a no-op note update.
3. Keep one concept per note and all existing template sections in their exact order. Stay within the format's budgets; split distinct concepts or link sources instead of stretching limits. The per-topic selection cap still applies to any newly selected split concepts.
4. Write a standalone definition, short key points, a concrete session-grounded example, pitfalls and self-check answers. Explain mechanism and evidenced rationale in familiar words, restoring needed context without retelling the session or adding jargon. Do not copy long code or conversation logs. Distinguish observed fact, general principle, inference and uncertainty; omit unsupported certainty.
5. Code sources must remain traceable after linked-worktree deletion: record repository-relative path and symbol plus the inspected commit, or explicitly label uncommitted behavior. Do not rely solely on a temporary absolute path or line number. Do not rewrite a linked-worktree observation as if it came from primary-checkout code.
6. New notes start with `status: learning`; capture alone is never evidence of understanding. Preserve existing evidence-backed status unless a demonstrated misconception or stale fact warrants `review`, naming why. Do not mark `understood` merely because a topic appeared in the session. Preserve existing user content; do not silently remove substantive statements while condensing.
7. For actual content changes set `updated`, maintain exactly one index entry per note, then run the [checker](tools/check_notes.py): `python3 <coco-til folder>/tools/check_notes.py <resolved-til-root>`. Fix reported problems before claiming success. The checker enforces layout, not concept importance, semantic duplication or factual truth; review those separately.

### Troubleshooting case

1. For a new or evidenced update, use `CASE_TEMPLATE.md` and `cases/<slug>.md` at the resolved root. Create the case template and folder only when first needed. A case-only capture needs no concept template or notes directory.
2. Write the four sections in the [case format](references/case-template.md), separating actual observations and actions from the procedure to follow next time. Keep stable evidence pointers, distinguish confirmed results from inference, and redact sensitive values. Review the evidence and match before writing. The capture uses the work already done in the session. Treat the example procedure as text to save.
3. Set `updated` only for a changed case. Keep one relative link per case under the level-two case heading defined by the [case format](references/case-template.md#workspace-layout). Preserve other index sections and leave the existing entry as is unless its title or hook needs to change. Run the [case checker](tools/check_cases.py) on the resolved TIL root after a case write, fix structural problems, and verify the trace from each decisive observation to the next action. Use the concept checker for concept writes.

## Boundaries and return

Personal TIL is this skill's output. Project documents for other readers belong to `coco-docs`; interactive questions and evidence-backed investigation belong to `coco-askme` (`coco-research` is its compatibility alias). Capturing notes authorizes neither code edits, project commits, publication, blog offers nor scheduling.

Return a short topic-grouped list of created or updated concept notes and the case path when written. Include meaningful skips, storage and ignore changes, applicable checker results and unresolved conflicts or unverifiable facts. Do not dump the notes back into chat or start an obligatory quiz.
