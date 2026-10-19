# Documentation, writing and learning procedures

Apply the [common contract](../contracts.md). Use [research](research.md) for facts and [context](context.md) for state ownership. Choose a mode by the reader's purpose; do not make every writing request an interactive course or interview.

## Input and selection

Retain audience, purpose, prior knowledge, source artifacts, required facts/uncertainty, destination and edit scope. Read the live target before every change and preserve user edits. Select technical documentation, decision record, prose repair, agent instructions, questionnaire, course exercises, learning workspace, or opt-in experimental writing collaboration.

## Technical documents and prose repair

1. Choose tutorial for a guided visible result, how-to for a specific task, reference for lookup, or explanation for mechanism/rationale. Keep these purposes distinct rather than building an unfocused hybrid.
2. Start with the concrete result or smallest complete definition. Walk a real user/caller action and introduce prerequisites before later sections use them.
3. Verify symbols, flags, commands, paths, counts, units, links, conditions and examples against their landing revision. Provide a regeneration method for generated facts.
4. Name the actor, place conditions before actions, use one stable term and split ambiguous compound instructions. Favor complete sentences over cryptic fragments.
5. Remove filler, promotional certainty, vague attribution and repeated summaries while preserving necessary qualifiers, constraints and technical repetition.
6. A plain-language repitch preserves the preceding answer's meaning, restores missing context and uses familiar domain language; it need not add more depth.
7. Check the edited text against its sources and original: clearer prose must not introduce a stronger guarantee or invent an example to cover missing evidence.

For public interfaces document inputs, outputs, errors, ordering, compatibility and a real usage example. Update README setup/commands or changelog only where the behavior changed. Comments explain nonobvious intent or constraints; delete obsolete commented-out code instead of narrating self-explanatory code.

## Decision records and domain language

Follow existing ADR location, numbering, markup and lifecycle. With no convention, use a short context/decision/why record when the choice is costly to reverse, surprising without context and based on a real tradeoff. Add alternatives/consequences only when useful. Supersede historical ADRs rather than deleting them.

Keep a glossary to canonical project terms with concise definitions and avoided aliases. Follow the existing context map when there are multiple domains; create records lazily when a term/decision is actually resolved. Implementation notes and task status belong elsewhere.

Output: updated document/record, factual checks and remaining uncertainty. Completion means the intended reader can use it without unsupported promises; it does not mean the feature or deployment is verified.

## Agent-facing instructions and reusable recipes

1. Give a pointer both a clear leading concept and the distinct conditions that should trigger reading its target. Avoid synonyms that merely repeat one trigger.
2. Put ordered steps and universal rules where needed; disclose branch-specific detail behind a pointer and colocate a concept's rules/caveats.
3. End each step with a checkable, sufficiently exhaustive completion criterion. If later actions cause premature completion, sharpen the gate before splitting at a real context boundary.
4. Keep one authoritative copy of a meaning and reference it. Do not cache cheap environment lookups or reproduce another workflow inside a personal rule.
5. Prefer positive target behavior, retaining hard prohibitions when essential. Remove stale/no-op prose based on observed behavior, not arbitrary brevity targets.
6. Use the actual target runtime's authoring and invocation metadata. Test trigger coverage and consequential behavior; never assume another product's metadata semantics.

## Async discovery questionnaire

Use when someone else holds required knowledge. Establish who receives it, what they know, the relationship/tone and the decisions/facts needed back. Ask about the send rather than forcing the user to answer the unknown subject.

Write purpose, sender/recipient/use, short context, deadline/effort and answer guidance, then themed questions in importance order. Each question asks one idea and has an answer stub; explain why only when misreading is likely. Accept partial/unknown answers and end with a catch-all.

Check every requested decision/fact has a question. Save and report the artifact; sending it requires separate direct authorization. Questionnaire completion is coverage of the knowledge gap, not receipt of answers.

## Explain or teach now

Start from the learner's purpose and known context. Explain the smallest complete definition, connect it to the actual system and combine mechanism with evidenced rationale. Reveal depth at the learner's pace; avoid obligatory quizzes or artificial pacing. Use code, debugger evidence or an incrementally built diagram only when it improves understanding.

## Opt-in multi-session learning workspace

Reuse existing learning files. With no convention, use `MISSION.md`, annotated `RESOURCES.md`, `NOTES.md`, sequential `learning-records/NNNN-slug.md`, short `lessons/*.html`, quick `reference/*.html`, shared `assets/` and a learned-term glossary. Keep one mission per workspace; unrelated subjects need separate state.

1. Establish one concrete mission with observable success, constraints and exclusions; use existing knowledge records to find the next useful challenge.
2. Curate annotated high-trust knowledge sources and optional practice communities. Respect a community opt-out; do not join or message one for the learner.
3. Produce short lessons with one tangible win, only necessary prerequisite knowledge and immediate feedback for practice.
4. Build retention through retrieval, spacing and interleaving where suitable; momentary fluency is not evidence of lasting understanding.
5. Reuse shared lesson styles/widgets and maintain linked quick-reference sheets. A lesson plus its shared assets must travel together when exported.
6. Record demonstrated understanding, stated prior knowledge/depth, corrected misconceptions and mission shifts. Covered material alone is not learned material.
7. Add glossary terms once understood, revise definitions as understanding develops, and supersede conflicting learning records rather than erasing history.
8. Make quiz options comparable in length and vary correct-answer position. Confirm a changed mission before letting it redirect future lessons.

Output: mission-aligned lesson/reference and justified learning-state updates. Stop at the requested learning unit; a multi-session goal does not authorize scheduling reminders.

## Conditional course-exercise scaffolding

Use the target course's conventions and linter. The conditional ordered TypeScript-course recipe is `exercises/XX-section/XX.YY-exercise/{problem,solution,explainer}/`, using lowercase dash-case names and matching numeric prefixes. Create only requested variants; unspecified conceptual stubs default to `explainer`.

Each variant needs a nonempty `readme.md` with valid links; code variants require `main.ts` longer than one line, while readme-only stubs are allowed. This recipe requires a primary `problem`, `explainer` or `explainer.1` variant, excludes `.gitkeep` and `speaker-notes.md`, and excludes obsolete exercise-run commands from readmes. Use the actual configured course linter, history-preserving moves when renumbering, and rerun validation. Do not impose this layout or an unavailable private CLI on a different course.

Output: plan-matched scaffold and lint evidence. Build owns any implementation commit; this mode does not stage unrelated files.

## Experimental writing collaboration

These modes are opt-in. Establish the destination once, reread the live file before each write and preserve author edits. They support different phases and must not overwrite each other's sources.

### Explore fragments

Interview for raw author-readable sentences, claims, vignettes, half-thoughts, quotes or observation clusters, starting with the initial prompt. Append to one working-title document with horizontal-rule separators and no imposed body outline/tags. Seek a useful leading metaphor/term when ideas recur. Save without a permission dialog per fragment; apply requested cut/rewrite/merge edits precisely. Output is a raw pile, not a finished argument.

### Shape an article

Read the full input pile and keep it read-only; write a separate article. Establish audience prerequisites, offer distinct openings/theses and let the chosen promise guide each next paragraph/block. Debate format when it affects comprehension: prose for argument, lists for parallel items, tables for repeated fields, quotes when wording matters. Ground concepts before relying on them. Name a missing example/foundation and obtain it or cut the section. Append agreed blocks and let the author decide completion.

### Journey of beats

Offer two or three reachable starting/next beats, each making one move and naming what concepts it requires and grounds. Write only the chosen beat, reread the article and offer the next alternatives. A beat can be a sentence or several paragraphs; split one doing multiple jobs. Keep a running grounded-concept set and preview unlocked directions. End when the journey is complete, even if raw fragments remain.

## Output and stopping conditions

Report changed artifact pointers, mode, factual/example/link validation, preserved uncertainty and any required author decision. Do not publish or add platform formatting/frontmatter unless requested. Routine documentation can finish autonomously within scope; collaborative modes stop only at their actual user-owned choice, not at an invented general approval gate.
