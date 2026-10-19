# Planning and dependency procedures

Apply the [common contract](../contracts.md). Read [spec](spec.md) for behavior authority and [context](context.md) for restartable state. Planning saves artifacts; it does not implement the feature or create external-write authority.

## Input and route

Retain the accepted outcome/spec, selected capability IDs, current code and baseline, existing work, constraints, required evidence, branch policy, task-state target and execution mode.

Choose scoped breakdown for known work, a decision map for a huge unclear effort, bespoke investigation for work without a fitting recipe, or an explicit whole-spec orchestration plan. Single-task versus continuous execution is independent of lightweight/standard/strengthened rigor.

## One plan and one task-state target

1. Read the current plan and task target before writing. Update the same effort; preserve incomplete work belonging to another effort and resolve any destination conflict.
2. Record design/risk rationale in the plan and mutable task status in exactly one designated file/tracker. The plan can index task IDs without duplicating checkboxes.
3. Reuse existing repository locations. With no convention, choose a feature-scoped plan and task target that cannot overwrite unrelated work, then state the choice.
4. Read full referenced specs/issues and relevant comments. Explore local precedent before turning facts into user questions.
5. Keep required checkpoints explicit; reuse approval for settled scope and do not turn every phase into a mandatory new conversation.

## Break down executable work

1. Map dependencies and state ownership. Define shared contracts before splitting consumers; verify that every edge is a genuine start blocker.
2. Prefer a narrow complete user/caller path per task, spanning only the layers needed to demonstrate it. Avoid building all schemas, then all APIs, then all UI.
3. Put evidence-building and risky unknowns early. Use prefactoring only when it removes demonstrated friction, not as a general cleanup mandate.
4. Give each task a stable ID/title, delivered behavior, acceptance conditions, verification method, blockers, expected scope, branch/base and required environment.
5. Size work to one focused context and independently reviewable commit. File counts and elapsed-time estimates are warnings, not hard universal limits.
6. Add integration checkpoints where contracts, persistence or shared workflows meet. Each checkpoint names actual tests/build/runtime evidence rather than a vague green label.
7. Publish blocker-first only when tracker writes are authorized; use native dependencies when supported. A local tracker uses one feature-scoped ticket file per task with explicit blocker IDs.
8. Keep durable tickets behavioral; current file estimates belong in the plan as navigation hints, not immutable acceptance requirements.

The **frontier** is pending tasks whose blockers are all satisfied. Completion uses acceptance, required checks/review and a recorded work-unit commit, not merely a worker's report.

## Wide mechanical migrations

When one rename/retype/API replacement fans across callers and cannot land as independent vertical features:

1. **Expand:** add the new representation beside the old without breaking consumers.
2. **Migrate:** move caller batches by package/directory/blast radius; each depends on expansion and stays green where feasible.
3. **Contract:** remove the old form only after every caller batch and compatibility check is done.
4. If no batch can remain independently green, declare an integration-only branch and a final integrate-and-verify task blocked by every batch. Red intermediate work is not normally done or shippable.
5. Define rollback/forward-recovery and the final old-caller search. Do not silently normalize permanent parallel APIs.

## Whole-spec integration and optional concurrency

Keep scoped execution distinct from fulfilling every ticket in a spec. For whole-spec work, create one integration branch, freeze accepted contracts and schedule its ready frontier.

Inventory every jointly mutable file, branch, key, fixture and state object before delegation. Different fields in one JSON file are still shared mutation. Prefer separately owned outputs; a canonical shared target needs enforced single-writer, locking, atomic updates or compare-and-swap.

Each authorized worker gets a self-contained goal/scope/base, owned paths, check method and report contract. Use isolated branches/worktrees where code writes can conflict; establish the actual integration base without resetting user changes. Merge completed work through one integration writer, refresh blockers and schedule newly ready tasks. A final integration review/check must inspect the real combined state.

For a partition, require every assigned slice. For a race, declare first-passing, ranked-all or best-of selection before results arrive. Require PASS, ISSUES or BLOCKED with exact revision/input/method/evidence. A missing receipt gets one correction, then remains a coverage gap; a dropout is not a pass.

Delegation depends on available tools and authorization. Sequential execution preserves the same dependency and evidence contract.

## Decision-map mode for large uncertainty

Use this when the destination cannot yet be reduced to implementable work. A map produces decisions by default, then feeds [spec](spec.md); it is not a build checklist.

1. Name the destination and scope before charting. If the whole path is already clear, use ordinary planning.
2. Keep an index containing Destination, standing Notes, named linked decision gists, Not-yet-specified fog and Out-of-scope.
3. Create one child per sharp question; label its type as research, prototype, discussion or prerequisite task. Do not apply implementation-ready triage states to decision tickets.
4. Create children before wiring real blocking IDs. Claim one open/unblocked/unclaimed ticket before work so another session does not duplicate it.
5. Research can be independent; prototypes/discussions requiring the user's judgment cannot be resolved by impersonating that judgment. A prerequisite task belongs only if it unblocks a decision.
6. Resolve with an answer/evidence pointer, close that decision, add its gist to the map, and graduate newly precise fog into tickets.
7. A sharp blocked question is a ticket; an in-scope question not yet expressible is fog; work beyond the destination is out of scope. Close mis-scoped tickets into Out-of-scope rather than recording them as route decisions.
8. For interactive work, normally resolve one substantive decision per session and retain the rest. Existing authorization may explicitly allow a broader AFK investigation or execution mandate.

Use task titles in human narration, with IDs carried by links. Keep full reasoning once in the decision artifact, not repeated in the index. Stop mapping when the destination is decidable and collapse it into a buildable spec.

## Bespoke investigation mode

For unfamiliar work, define a falsifiable done predicate, quantified scope, blockers, rigor, baseline and verification method before making changes. Sequence the riskiest unknown first as hypothesis → smallest reversible intervention → real-artifact measurement → keep or revert.

Record each unit as verified, not verified or inconclusive with evidence. Repair an invalid measurement/gate contract explicitly instead of weakening it to pass. Verify the final whole against the original outcome, not only intermediate checks.

## Output and stopping conditions

Return the plan pointer, authoritative task target, dependency graph/frontier, integration strategy, evidence gates, unresolved decisions and next executable task. Preserve user branch and task-commit conventions.

Planning is ready when tasks are implementable, blockers acyclic/resolved as appropriate, checks runnable or explicitly unavailable, and material scope decisions settled. A planning-only request stops here. Continuous authorized work can proceed through build; required failed checks or a new material decision stop dependent advancement, not independent permitted work.
