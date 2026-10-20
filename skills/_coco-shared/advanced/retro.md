# Retrospective and structural learning

Apply the [common contract](../contracts.md). A retrospective improves how future work succeeds; it is not authority for unrelated product changes, global rule installation or external backlog writes.

## Input and modes

Retain the requested session/range, user goal, primary evidence, corrections, checks, artifacts and authorized improvement scope. Default to the current session when no other session is named; historical mining stays within the authorized workspace.

Select a session retrospective, recurring-error prevention, agent-instruction/recipe maintenance or work-environment audit. Use several reasoning lenses when helpful, without requiring multiple workers or models.

## Reconstruct the outcome

1. Compare the original goal and acceptance conditions with actual artifacts, commits and execution evidence.
2. Identify failures, recoveries, wasted exploration, missing access and effective choices. Preserve facts that contradict the tidy narrative.
3. Read actual check scripts/configuration/CI before proposing a new check. An existing unwired/broken check is a finding, as is an important quality bar with no enforcement.
4. Group repeated corrections by mistake class rather than by message. Two independent occurrences justify investigating a recurring class, not automatically imposing a new global rule.
5. Separate a one-off environmental incident, a mechanical preventable defect, a structural ownership/model error and an irreducible judgment call.

## Examine the environment

- **Navigation:** find missing/weak pointers, hidden relationships and expensive rediscovery; improve the pointer before dumping the target into always-loaded instructions.
- **Checks:** inspect existing lint/types/tests/CI/pre-commit wiring and real failure behavior. Do not add another tool that duplicates a working guardrail.
- **Ownership and types:** look for split mutable state, duplicated authoritative lists, invalid constructible states and interfaces that force caller workarounds.
- **Context/tool economy:** identify oversized tool output, repeated raw payloads, stale drafts and unnecessary repeated successful checks.
- **Information access:** identify missing logs, read-only environments, runtime observability or test fixtures that caused guesswork.
- **Instructions:** identify no-op, stale, contradictory, overbroad or misplaced rules, including global instructions that only reviewers need.

Use [context](context.md) to repair loading/handoff and [docs](docs.md) to write a precise pointer or recipe.

## Choose the strongest suitable intervention

Prefer the highest effective enforcement level that matches the mistake:

1. Ownership/architecture removes the possibility or gives one authoritative owner.
2. Types/schema/metadata make invalid states or missing entries unrepresentable.
3. Diagnostic lint, build or CI checks reject mechanical patterns.
4. Behavioral tests catch an observable regression at the correct caller seam.
5. Review guidance captures a real judgment no deterministic check can substitute for.
6. A narrowly triggered recipe/instruction handles a distinct reusable workflow when existing material cannot.

Do not write prose for a syntactic pattern that the repo's tooling can enforce cheaply. Do not force structural redesign to prevent a trivial typo. The intervention must earn its maintenance cost and stay within scope.

## Recurring-error prevention procedure

1. Name the mistake class, representative evidence, root mechanism and desired prevented outcome.
2. Find the authoritative location for enforcement and any existing rule that should be repaired instead.
3. Design a diagnostic naming the actual violation and remediation. Use the same underlying command locally and in CI.
4. Prove the new guardrail rejects a real past mistake or faithful minimal fixture; then restore clean state and observe acceptance.
5. Run appropriate nearby checks and show the guardrail is wired into the workflow where the mistake previously escaped.
6. For existing debt, ratchet a recorded baseline or isolate scoped exceptions with reason/owner/review date according to project policy. Do not silently disable the entire guardrail.
7. Remove redundant prose after structure makes the error impossible; keep judgment rationale when still needed.
8. Let build land each independent mistake class as an atomic work unit with its evidence; keep a rule-to-enforcement map when multiple classes warrant one.

A check that only passes has not shown it can prevent the mistake. A claimed test seam that cannot reproduce the real caller pattern is an architecture finding, not proof.

## Reflection into maintained procedures

Review candidate lessons through judgment, tooling and divergent lenses: was the decision actually wrong, could structure prevent it, and what alternative explanation fits the evidence?

For each lesson record evidence, recurrence, current coverage, proposed destination and expected behavioral change. Prefer editing the existing relevant rule, workflow, trigger or reference over adding a new standalone skill. Keep one source of truth.

Classify outcomes as accepted, changed, proposed, backlog, deferred or rejected, with reasons. Do not turn a subjective preference into standing policy without a user mandate. A recurring issue already covered by a sound rule may indicate discovery/enforcement failure rather than missing text.

For substantive procedure changes, validate internal references and authoring metadata, then run representative behavior evaluations. Formatting success does not prove the new procedure will change behavior. Preserve unresolved evaluation gaps.

## Output and priority

Present the highest-consequence findings first. Each includes symptom/evidence, mechanism, proposed intervention, exact enforcement point, verification and expected tradeoff. Distinguish changes already made under authorization from recommendations awaiting a material choice.

Record relevant unavailable sources, independent-review limitations and rejected alternatives. Keep proposed external tickets as local drafts unless tracker writes are authorized. A retrospective does not silently alter credentials, user profiles or global instructions.

## Stopping conditions

A retrospective is complete when material lessons have evidence-backed dispositions and the requested scoped improvements are implemented/verified or explicitly left as proposals. Do not claim prevention when only prose was added or a new check never demonstrated rejection.

If the same blocker persists after the bounded attempts in the common contract, return attempts, evidence and the specific needed input. Stop adding speculative rules; more instructions are not a substitute for missing access or a correct model.
