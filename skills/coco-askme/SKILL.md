---
name: coco-askme
description: "Use when exploring concepts from the current session, understanding code or design decisions, investigating technical questions with evidence, or being quizzed on selected work."
license: MIT
---

# coco-askme

Explore the user's questions with evidence; quiz only when requested. Follow the [common contract](../_coco-shared/contracts.md). Localize choices, explanations, questions and feedback to the user's language. `coco-research` is a compatibility alias for this single procedure.

## Entry and conversation mode

- **Bare invocation:** offer session concepts below, also for bare `coco-research`. Never route through whattosay or resume an earlier implementation request.
- **Explicit question/investigation:** answer directly; no menu or compulsory quiz. Clarify only material ambiguity. Return answer, sources, causal explanation, uncertainty and cheapest useful next check; explanation-only requests end there.
- **Explicit quiz:** resolve only missing scope/topic, then enter Quiz. Scopes: session work, feature/flow, code or change. Topics: principles, flow, architecture, performance, readability, reliability, mixed or custom. Skip choices already supplied.
- A concept selection starts a short explanation with user-led follow-up. Change mode or topic on request without repeating setup.

## Topic orientation (wide)

Wide is internal orientation.

1. Use visible conversation, compaction summary and supplied handoff. Prefer concepts central to session work, decisions, errors or open questions. Apart from instruction loading, sufficient context needs no content-discovery calls. Do not preload research or quiz references for a menu.
2. Offer up to three numbered concepts with one short line of session relevance each. Ask "What would you like to understand?" and allow a different topic in free text. Never fill the menu with generic concepts, reveal quiz answers or investigate candidates before selection.
3. After compaction or unclear continuity, allow one bounded recovery batch: at most two already identified session-linked sources, relevant excerpts only (up to 120 lines combined). Use a supplied task/handoff section or named changed symbol. Never scan a repository, full diff, web, transcript store, unrelated chats or Git history for menu ideas. Branch, timestamp or dirty state alone does not prove session ownership. This opening cost bound does not waive evidence checks after selection.
4. If recovery fails, disclose missing context and ask for a target; offer only supported candidates. Whenever the menu relies on compressed or handoff context, disclose that boundary even without recovery; never imply complete session coverage. Always allow free-text entry.
5. Before compaction or an existing handoff, retain a short capsule: concepts/relevance, unresolved questions, source pointers with revision/version, mode and pending quiz question. Reuse it on resumption; recover only missing parts. Do not copy transcripts, create files or claim control over automatic compaction.

## Evidence gathering (deep)

Deep gathers evidence for an explanation or quiz only when there is a material evidence gap, conflict or changed scope/revision/version/environment. Do not repeat it for every reply, wrong answer or simpler wording. Reuse verified evidence for a matching snapshot; user statements and earlier assistant claims are not automatically verified.

For the selected question, check for version-specific API facts, a runtime mechanism or state-ownership trace, historical rationale behind defensive code or thresholds, a bounded multi-source investigation, claim-confidence grading, or a durable cited findings artifact. If any applies, read the relevant [research procedures](../_coco-shared/advanced/research.md) before dependent work. Topic orientation alone does not trigger this.

Return a concise answer with sources, causal explanation and explicit gaps. Distinguish facts, inferences and unknowns; current code cannot prove historical intent. Separate optimization techniques from measured effects. For a proposed change retain preserve/change/avoid/risk constraints; save cited findings only when requested under repository conventions. Research does not authorize implementation or publication.

## Quiz

Read the [quiz procedure](references/quiz.md) only when quizzing. Ask exactly one source-grounded question, withhold the answer and wait; then give feedback at an adjusted depth. Preserve hint, answer, mode/topic switch and stop controls. Answer user questions before resuming.

## Boundaries

Exploration and quizzing do not modify code, run state-changing commands, commit or publish. Requested cited findings are the limited artifact exception; they do not authorize code edits or commits. For an implementation request, state the switch and continue separately through `coco-build` within the user's authorization. Use `coco-til` to capture reusable personal session notes; never save them automatically.

## Stop signals

Correct course when any of these occurs, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "I know this API": verify the installed version's primary source or mark the claim unverified.
- Replacing verification with "it might be outdated", using secondary posts instead of available primary sources, or writing version-specific code before checking manifests/lockfiles.
- Sweeping history because context was compressed, or treating recommendations as complete session coverage.
- Running deep research on every answer, re-reading unchanged sources, or turning a direct question into compulsory quizzing.

## Examples

`$coco-askme` and bare `$coco-research` offer session concepts. Adding `trace the retry flow` investigates directly; `quiz me on this component` starts one grounded question at a time.
