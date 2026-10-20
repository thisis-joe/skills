# Clarification, idea refinement and domain terms

Use this reference when intent, terminology or a material design decision is unsettled.
Apply the [common contract](../contracts.md); reuse existing agreements first.
The deliverable is a settled decision or explicit open item, not an interview transcript.

## Inputs

- Requested outcome and the user's existing acceptance, limits and approvals.
- Relevant spec, issue comments, glossary, ADRs and observed code behavior.
- Missing decisions and the factual evidence needed to choose between them.
- Whether the user wants clarification, divergent ideas or adversarial stress testing.

## Select a conditional mode

| Condition | Mode | Next action |
|---|---|---|
| Requirements and boundaries already settled | Reuse | Summarize/reference them and continue |
| A material outcome or constraint is missing | Focused interview | Ask the next decision only |
| A rough idea needs alternative directions | Diverge then converge | Explore bounded variants |
| User asks to grill or stress-test a plan, decision or idea | Grill mode | Ask the whole ready frontier each round until it is empty and confirmed |
| A domain term has conflicting meanings | Domain modeling | Resolve the term with scenarios |

A synthesis/spec request does not reopen a requirements interview.
An unambiguous static edit, explanation or mechanical rename needs none of these modes.

## Reuse and investigate

1. Read the available decisions and separate settled facts from missing choices.
2. Fetch or inspect accessible facts yourself: versions, existing interfaces, prior art.
3. Name the exact conflict if documents, code and user terminology disagree.
4. State a concise interpretation and the uncertainty that would change the work.
5. Ask only when the answer materially affects scope, acceptance or an irreversible choice.

Do not ask the user for a fact the repository can supply.
If external evidence is unavailable, identify that gap rather than presenting a guess as fact.
Preserve already approved test seams unless the interface or required behavior changes.

## Focused interview

This is the default for a missing decision; an explicit grill or stress-test request uses grill mode below instead.
Ask one focused question with a recommended answer and its concrete tradeoff.
Explain what remains unknown; a numerical confidence estimate is optional, not proof.
Wait for that answer before asking a dependent question.
Independent decisions may be grouped briefly when none depends on another answer.
Use the user's actual words; probe vague goals such as scalable with a concrete scenario.
When convention substitutes for a need, ask which real outcome matters most.
Update the interpretation after a correction rather than replaying the same questions.

Restate outcome, beneficiary, why now, observable success, binding constraint and out of scope.
Accept an unambiguous affirmative in context; require no special confirmation phrase.
Existing scope authorization persists after clarification.
If the user has authorized the next step and no required decision remains, continue it.
If the user only requested exploration, return the resolved intent without implementing.

## Divergent-to-convergent refinement

Start only when the direction is genuinely open or the user requests alternatives.
Frame the problem as an outcome for a specific user under its actual constraint.
Generate a small set of reasoned variants, typically five to eight when useful.
Use selected lenses: inversion, audience shift, combination, simplification or constraint change.
Ground variants in the project's architecture and available resources.
Do not generate more variants merely to fill a quota.

After the user's reaction, cluster promising ideas into two or three distinct directions.
Compare user value, feasibility and differentiation against current workarounds.
For each direction name the assumption, how it could fail and the cheapest validation.
Distinguish must-be-true dealbreakers from secondary or optional assumptions.
Recommend one direction with the smallest experiment that tests its riskiest assumption.
Keep an explicit Not Doing list with reasons and a time-box for the experiment.

## Grill mode

Use when the user asks to grill, stress-test or relentlessly interview a plan, decision or idea, with or without saving documentation.
It keeps the source decision-tree mechanics in place of the focused interview's one-question default.

1. Map the plan as a design tree: every decision branches into the decisions that depend on it.
2. Work in rounds. The frontier is every open decision whose prerequisites are settled. Ask the whole frontier in one round; a question that depends on another question still open in this round belongs to a later round.
3. Number each question with a short title, its body and choices, then your recommended answer. Word each question so "yes" accepts that recommendation.
4. Finding facts is your job: use the repository, tools, authorized research or optional authorized sub-agents. A pending lookup blocks only the questions downstream of it; ask the rest now. Decisions are the user's: put each to them and wait.
5. After each round recompute the frontier: settled answers unblock dependents and resolved branches stay closed. Probe consequences, hidden coupling and counterexamples rather than asking for generic approval.
6. End only when the frontier is empty, every branch visited and nothing silently assumed, and the user confirms the shared understanding. Do not act on the result before that confirmation.

```text
Q1 - <title>: <question, with choices when useful>
Recommended: <answer>
---
Q2 - <title>: <question>
Recommended: <answer>
```

With documentation in scope, apply domain modeling below as terms and tradeoffs crystallize.
For a high-impact assumption, hand the small artifact/contract to an available independent reviewer.
Treat reviewer output as claims to check, with at most three unresolved review cycles.
Unavailable independence is disclosed; do not force a tool or model.

## Domain modeling

Read the appropriate glossary/context map and nearby ADRs before changing terms.
Use concrete edge scenarios to distinguish overloaded nouns and relationships.
Compare the agreed meaning with actual code and expose substantive disagreement.
Record a resolved domain definition in the existing glossary format when saving is in scope.
Keep implementation decisions out of the glossary.
An ADR is useful when a real tradeoff is costly to reverse and surprising without context.
Follow existing ADR paths/formats and supersede old decisions rather than erase history.

## Output and stop

Return the chosen outcome/direction, constraints, exclusions and evidence-linked decisions.
Include only unresolved questions that block a specific next action.
Save a durable intent or idea artifact in the established location when authorized or requested.
Stop interviewing when remaining answers would not change the chosen work; grill mode instead ends only on an empty frontier and the user's confirmation.
If repeated questions fail to narrow the issue, state the foundational gap and reframe.
Unattended runs record underspecification as a blocker and continue independent permitted work.
