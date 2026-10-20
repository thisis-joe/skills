---
name: coco-whattosay
description: "Use when a skill has been selected or invoked without a request and the user needs contextual options for what to ask it, or help completing its invocation."
license: MIT
---

# coco-whattosay

Suggest what to ask the selected skill in the current context. The default flow is **confirm selection → suggest contextual requests → wait for selection → execute the selected request**. Follow the [common contract](../_coco-shared/contracts.md). Localize prompts, options, and reports to the user's language; the examples below are in English.

## 1. Confirm the selected skill and purpose

Prefer an explicitly named skill; otherwise carry forward the confirmed choice from earlier conversation. Reuse the exact identifier, user purpose, and agreed scope from a `coco-whichskill` selection when present. A mere mention or recommended candidate is not a confirmed selection. A bare invocation of another skill handed over by the [common contract](../_coco-shared/contracts.md#work-input-and-selection) is a confirmed selection of that skill.

Match the currently available catalog against the actual `SKILL.md` location and retain namespaces. Read only the selected body and necessary references as **material for composing requests**. Do not start the target's execution workflow or read all skill bodies at this stage.

If no choice is established or several candidates remain, clarify only the target. Accept a directly named skill even where `coco-whichskill` is unavailable. Do not install a missing skill or substitute a similar one. If its body cannot be checked, state the limit and necessary location without presenting a recommendation as ready to execute.

Read agreed purpose, scope, constraints, and currently relevant material without writing. Do not repeat settled questions. If the target is known but a missing purpose or required input prevents a valid request, ask only for that information and wait. After a bare invocation the purpose is missing by design: compose options from the target's supported scope and the current conversation and repository state instead of first asking for a purpose. Do not invent paths, tickets, or approved plans, or treat placeholders as filled.

## 2. Suggest requests

Default to three options, fewer when valid alternatives are limited. Every option must serve the user's purpose within the **same selected skill's** supported scope. Vary purpose, focus, scope, or expected deliverable meaningfully; do not create alternatives differing only in wording or explanation length.

For each option, provide:

- A unique number and short title.
- One line explaining its value in the current context.
- A complete, copyable invocation containing the exact skill invocation name and request in the current runtime's syntax: `$name` in Codex or `/name` in Claude Code. Preserve catalog namespaces.

Mark one best fit as **Recommended** and explain why. Include the necessary target, work, scope, and expected result while preserving agreed constraints. If the user wants one task, keep every option within it; do not add continuous execution or external publication. Do not present unresolved policy as settled fact in a suggested request.

Briefly name the selected skill and current purpose, present options, explain that **choosing a number executes that request**, and wait. Use an available question tool or final response to obtain the choice. A recommendation is not a user selection.

## 3. Select, revise, and execute

- For a valid number, execute the skill and complete request from the **most recently displayed options**. Retain the number-to-request mapping; if it cannot be recovered, confirm it again.
- If selection includes a revision, such as "2, but only this file," apply the revised scope. For requests such as "other options" or "narrow it down," show revised options and wait for another selection. Do not execute an ambiguous or invalid choice; clarify it.
- In "wording only" or "recommendations only" mode, return only the completed invocation even after selection. Preserve that intent through later revisions; move to execution only when the user requests execution. Stop on cancellation.
- Execute through the runtime's supported skill mechanism or read and apply the selected `SKILL.md`. Do not run invocation text as a shell command. Actual tools, material, and permissions follow the selected skill and existing user authorization.

The recommendation stage ends with options and waiting for selection. The selected skill owns subsequent work and reports actual results and incomplete conditions under its procedure.

Examples: `$coco-whattosay coco-review` in Codex or `/coco-whattosay coco-review` in Claude Code suggests review requests for the current work. Adding `Suggest request wording only` does not execute even after a number is selected. If the skill is already selected, invoking `coco-whattosay` carries it forward. A bare `/coco-review` with no purpose settled in the conversation opens this flow for `coco-review`. Use `coco-tellmeskill` when discovery or explanation itself is the goal.
