# Specification procedures

Apply the [common contract](../contracts.md). A spec owns expected behavior; [plan](plan.md) owns execution structure and the designated task target owns status.

## Input and mode

Read the user request, settled conversation, existing spec system, relevant code/contracts, terminology, decisions and project checks. Retain the desired outcome, actors, preserved behavior, constraints and authority to save or publish.

- **Synthesis:** conversation/design already settled the behavior; collapse it without restarting the interview.
- **Discovery:** ask only material unanswered product/interface questions, after investigating facts locally.
- **Capability map:** one request contains independently testable capabilities with distinct consumers/data.
- **Revision:** update an existing agreement because a requirement or verified constraint changed.

A typo or clear static edit needs a compact scope and acceptance check, not a ceremonial specification package.

## Establish one authority

1. Find the repository's current spec/decision convention and task-state target. Keep an existing external specification format instead of creating a competing spec file.
2. Read existing unresolved work before saving. Revise the same effort in place; do not overwrite another effort's incomplete spec or task state.
3. Name the spec, scope and relevant revision. Link its source agreements and decisions.
4. Separate confirmed facts, accepted decisions and remaining assumptions. A consequential assumption is not accepted merely because time passed.
5. Reuse prior approval for the defined work and already-agreed test seams. Do not demand another approval turn because a new document was synthesized.

## Conditional capability decomposition

Use a capability map before per-capability specs only when acceptance groups can be cut, replaced or verified independently.

Record stable capability IDs, responsibilities, dependencies and provider/consumer interfaces. Order the dependency graph and detect cycles. A cycle may indicate wrongly split ownership or a missing shared contract; investigate rather than forcing arbitrary order.

Keep the map an index, not a giant spec. Define a provider contract in its owning spec, then reference it from consumers. Use the IDs to select the right artifact in later sessions. Confirm materially uncertain boundaries; preserve settled ones.

## Write the behavioral contract

Include the following content in the repository's format, scaling length to actual complexity:

1. **Problem and objective:** affected user, present difficulty, desired result and why it matters.
2. **Scope:** included capabilities, explicitly preserved behavior and exclusions that could otherwise invite adjacent work.
3. **Stories/scenarios:** actor, desired capability and benefit, with normal, failure, recovery and boundary conditions needed for complete behavior.
4. **Contracts:** operations, input/output meaning, validation, errors, state transitions, ownership and compatibility expectations.
5. **Decisions:** selected modules/interfaces, schemas and rationale established by the design; refer to durable ADRs rather than copying them.
6. **Testing strategy:** observable seams, what each catches/misses, independent expected results, relevant prior art and required test/runtime levels.
7. **Success criteria:** concrete independently verifiable outcomes and relevant measured limits with units, environment and rationale.
8. **Open questions:** owner/needed fact or decision, consequence and what work it blocks.

Cover all necessary user behavior; do not manufacture a long story list to meet a length target. Use glossary language and surface contradictions with existing decisions.

Prefer durable interface/behavior descriptions to detailed file instructions. A small prototype reducer, schema or state shape may be included when it captures an accepted decision more precisely than prose; omit disposable demo plumbing.

## Project guidance and constraints

Reference existing commands, layout and style sources. Record exact relevant verification commands discovered from the repository/CI, including required environment or target URL. Avoid maintaining an independent copy of every changing script or folder.

When no project guidance exists, supply enough executable setup/check instructions and one representative pattern to make the spec usable. Mark unrun commands unverified and do not invent a package-manager command for another stack.

Separate standing constraints into:

- Required behavior and checks that already govern this work.
- Actions needing a material decision or authorization under user/repository policy.
- Prohibited outcomes such as lost user work, exposed secrets or weakened failing checks.

These categories do not create a universal ask-first list for routine authorized changes. If a quality target matters, name the metric, current baseline, target, measurement method and reason. A number with no check is a goal, not enforced evidence.

## Test seams and validation

Prefer existing highest useful public interfaces, keeping the number small without hiding critical caller interactions. Do not add private seams solely to make tests easy.

For each acceptance condition, identify the check or evidence needed. Distinguish test coverage from full user-flow proof and document unavailable runtime needs. If a target such as faster or accessible is vague, propose a measurable interpretation and resolve that material choice before treating it as the contract.

Review the draft for contradictory requirements, missing state/error behavior, unsupported performance promises, unowned shared state and unnecessary scope. Record the actual unresolved items rather than claiming the spec is implementation-ready.

## Save and hand off

Save to the established local convention. A tracker-hosted spec is published only within authorized external-write scope using authenticated tools; otherwise prepare a local draft and report its destination.

A spec created from resolved decisions can be marked agent-ready by the chosen workflow without raw-request triage. Save no duplicate completion checklist; link the authoritative task target when one exists. Do not close a parent issue merely because its spec was written.

## Output and stopping conditions

Return the spec/capability-map pointer, agreed behavior, acceptance approach, remaining decisions and readiness for planning. A spec-only request ends with this artifact. When the user already authorized continuous work and no material questions remain, continue into [plan](plan.md) without manufacturing a new permission gate.

If a decision changes during implementation, update the affected agreement before building against the new behavior. Preserve historical ADR supersession and refer task progress back to its designated owner.
