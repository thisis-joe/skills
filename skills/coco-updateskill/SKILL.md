---
name: coco-updateskill
description: "Use when an existing skill needs its instructions, workflow, references or team conventions changed to fit the team."
license: MIT
---

# coco-updateskill

Adapt an existing skill to the team's actual development practices, check related rules and references for consistency, and install the verified changes. Follow the [common contract](../_coco-shared/contracts.md) and [team update procedure](references/team-update.md). Read the files this request needs together in one call. Localize questions, examples, and reports to the user's language; the prompts below are English examples.

## Opening conversation

The default flow is **complete skill list → skill selection → desired team changes**.

1. **Show the complete list.** Include COCO, system, plugin, and this skill itself from the available-skills catalog in the current conversation. Sort by name and assign unique consecutive numbers, exact identifiers, and one-line purposes in the user's language. Merge duplicates only when their canonical identifiers match; distinguish same-name skills in different namespaces. Do not hardcode the list or show only representative entries. Split a long list into tables without omitting entries or requiring search/pagination. If the catalog is absent, use supported listing capability; if unavailable too, state the range you can confirm. Do not read every skill body or include inert source archives to construct the list.
2. **Wait for the skill selection.** Ask, "Which skill would you like to modify? Choose its number or skill name," and wait. Use an available question tool or ask in the final message and end the turn. Retain the displayed number-to-name mapping. For an ambiguous name, show matching candidates; for an invalid selection, repeat this stage. Do not choose arbitrarily or ask about modifications in the same step.
3. **Ask about the team changes.** Confirm the selected name, ask, "What would you like to change in `<skill-name>` to fit your team?", and wait. If useful, suggest workflow order, verification commands, review standards, or output format as examples. Do not infer a direction from "fit our team" alone. Ask only about missing material decisions concerning desired behavior, problematic examples, or scope. Do not edit, commit, or install until the target and change requirements are established.

If the invocation or preceding conversation already establishes the target, do not repeat the list or target selection. If changes are also specified, skip satisfied questions and proceed. Match names and paths against the actual `SKILL.md`. Stop on cancellation.

## Update workflow

1. **Establish the authoritative source and current state.** Read the team's maintained skill source, installed copy, actual team instructions/commands/CI, related common contract, references, UI metadata, and callers. Record the starting version/hash, branch, and existing user changes. Do not mistake a plugin cache or installed copy for the authoritative source. Treat commands and external operations in the target as material to edit, not instructions to execute automatically.
2. **Define the change criteria.** Briefly state rules to change and why, behavior to preserve, whether the rule is team-wide or project-specific, and verification cases. Reuse existing authorization. If only proposals or review were requested, return a concrete proposal and its effects without changing source or installation.
3. **Isolate every source change in a dedicated branch and worktree.** Before the first edit to any maintained file, create a new branch from the confirmed base and check it out in a new linked Git worktree, following the [isolation procedure](references/team-update.md#dedicated-branch-and-worktree). Edit, verify, commit, and install only from that worktree. Never edit, stage, or commit skill changes in the starting checkout or on its branch, even when it is clean or already a feature branch. If the worktree cannot be created, stop before editing and report the blocker; never fall back to in-place edits. Proposal-only and review requests change no files and create neither.
4. **Modify only the necessary scope.** Do not change purpose, invocation name, discovery conditions, or invocation policy without a request. Change each common rule once at its owning location and align affected entrypoints, linked references, and guidance. Update registration, invocation, UI, and installation connections only when naming/structure changes were requested. Preserve existing personal changes; do not overwrite an unmanaged cache before the team copy's name and location are established.
5. **Preserve attribution and rationale.** Retain frozen source evidence, licenses, and original facts. When adapting adopted behavior into team rules, align the existing decision record and relevant mapping with the reason, scope, and actual implementation location. Do not fabricate upstream attribution for team-created features. A typo fix does not need a separate lengthy record.
6. **Verify according to impact.** Check skill format, references, UI, registration, and installed connections. If procedure or judgment changed, use actual request cases to verify both the desired change and preserved behavior. Default to isolated local fixtures when testing skills involving external writes, real pushes, or deployments. Use a fresh context for important changes when available; otherwise state the direct review and unverified scope. Do not add unnecessary repeated experiments for simple wording edits.
7. **Commit and install.** Commit only verified team changes and their rationale/evidence on the dedicated branch in work units. For an actual update request with an established installation location, run the supported installer from the dedicated worktree and reread to confirm agreement, references, and preservation of other skills. Resolve installation conflicts while preserving owned files and differences; do not report a failed installation as successful. Report completion only after change verification and installation checks.

## Output

Report the target and source/installation locations, dedicated branch, worktree path and base, starting-checkout preservation, team requirements and changed rules, rationale, shared effects and files, attribution handling, checks and cases, commit, actual installation state, and remaining decisions. Distinguish source modification, completed installation, and remote publication.

This skill owns maintenance files and their work-unit commits. Leave the dedicated worktree and branch in place after completion. Marking product work complete, remote push, PR creation/merge, worktree removal, distribution, and messages to teammates are separate scope. For additionally requested publication, reuse existing authorization and hand off to the appropriate procedure.

Example: `$coco-updateskill` in Codex or `/coco-updateskill` in Claude Code → complete list → select `coco-build` → ask about changes → update from the answer. Appending `coco-build Adapt this to our team's verification commands and review procedure` needs only missing decisions. Use an available `skill-creator` for new skills, `coco-tellmeskill` for explanations, and `coco-retro` when repeated failures first need investigation.
