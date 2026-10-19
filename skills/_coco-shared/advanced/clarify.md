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
| User asks to stress-test a plan | Decision tree | Work dependency-ready decisions |
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

## Decision-frontier stress test

Map the decision and its downstream dependencies as a small tree.
Work only the frontier whose prerequisites are settled.
Question consequences, hidden coupling and counterexamples rather than asking for generic approval.
After each answer recompute the frontier; keep already resolved branches closed.
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
Stop interviewing when remaining answers would not change the chosen work.
If repeated questions fail to narrow the issue, state the foundational gap and reframe.
Unattended runs record underspecification as a blocker and continue independent permitted work.
