# Release readiness, PR preparation and safe rollout

Use this reference for a release decision, PR preparation or an authorized deployment.
Apply the [common contract](../contracts.md) and [security policy](security.md).
Ready/blocked is a decision; deployed/healthy is a separately evidenced state.

## Inputs and modes

- Frozen change scope, work-unit commits, spec/acceptance and task-state references.
- Current test/build/runtime/review evidence and accepted risks/exceptions.
- Release target, artifact/version, deployment authority and rollout owners.
- Operational baseline, SLO/error budget, feature flags and recovery capability.

| User's authorized goal | Mode | Stop boundary |
|---|---|---|
| Prepare a reviewable change | PR preparation | Concrete diff, description and verification |
| Assess launch readiness | Readiness | Evidence-backed ready/blocked decision |
| Execute release/deployment | Authorized rollout | Actual deployment and monitored state |
| Routine tiny low-risk change | Lightweight readiness | Applicable evidence without forced fanout |

Do not infer merge, publish, tag, push or deployment authority from selecting this reference.
Prepare all authorized reviewable work before an action requiring a new approval.

## Readiness gate

1. Confirm acceptance, current required checks and review findings on the actual scope.
2. Verify behavior at runtime, not merely compilation; retain missing evidence as pending.
3. Inspect dependencies, secrets, trust boundary and compatibility exceptions.
4. Check relevant [UI/accessibility](frontend.md), [performance](performance.md) and migration gates.
5. Confirm production configuration, health checks and [instrumentation](observe.md).
6. Ensure documentation, consumer-impact changelog and necessary ADRs are current.
7. Establish rollback triggers, executable steps, data consequences and recovery owner.

Use independent specialist review when uncertainty/blast radius warrants and tools permit.
Independent reviewers receive the same frozen artifact with separate relevant contracts.
Keep reports attributable, deduplicate shared fixes and preserve separate review axes.
Sequential/self-review is labeled honestly when independence is unavailable.
No fixed model, persona registry or fanout tool is required.
Critical unresolved defects block readiness; accepted risk must be explicit and authorized.
Do not lower the [standing quality bar](start.md) to obtain a release verdict.

## PR and version preparation

Keep one feature branch and atomic verified work-unit commits under repository rules.
Lead a PR description with the concrete problem and resulting behavior.
Add only review-relevant scope, verification, material risk and source/spec links.
Use the repository template and avoid dumping the investigation transcript.
Verify the proposed diff contains the intended work and no unrelated user edits.
Create/send the PR only within existing authorization and report its actual result.

For published consumers, choose major/minor/patch from observable compatibility.
Include migration notes/deprecation windows for breaking changes.
Use the existing release/tag convention and keep artifact/version/changelog aligned.
Tagging or publishing remains an authorized external action, not an automatic readiness step.

## Conditional dependent PR stack

When merging an authorized stack, verify each PR on its actual dependency base and current patch.
Record reviewer independence, runtime result and the snapshot each verdict covers.
Choose the contiguous verified run from the lowest unmerged dependency and fix its ceiling.
An unverified lower PR blocks dependent upper ones even if their individual checks are green.
Land one PR at a time, bottom-up, through the forge actually available to the project.
Read back merged state and target branch; queued or auto-merge-armed is not merged.
After a base/patch change, establish whether evidence still covers the actual code and dependencies.
Rerun affected verification when coverage is uncertain; patch identity alone proves no runtime property.
Do not alter a landing stack or extend the ceiling without the needed new evidence/authorization.

## Rollout and SLO budget gate

Record the measured baseline, observation window and advance/hold/rollback thresholds.
Use project-specific error, tail latency, client error, business and data-integrity criteria.
When no policy exists, propose justified limits rather than pretending generic numbers are agreed.

| Error-budget condition | Default action when applicable |
|---|---|
| Healthy remaining budget | Normal approved rollout with monitoring |
| Low remaining budget | Slow rollout and defer high-risk change |
| Exhausted budget | Freeze feature release and restore reliability |
| Canary burns faster than justified baseline | Hold and investigate |

If a project needs starting numbers, propose 20% as the low-budget boundary and record its reason.
Missing SLO/budget evidence is a gap for a service requiring this gate, not assumed healthy.

Deploy to staging and verify critical flows before production.
Use an owned flag or other safe cutoff for incomplete/risky features when appropriate.
Test both flag states, give it an expiry and avoid nested combinations.
Advance through internal/canary/cohort stages only after the agreed window and checks pass.
Compare each stage with baseline, including data consistency and the primary business effect.
Keep long observation windows pending or use an authorized monitoring mechanism.
Remove retired flags/dead paths after stable rollout; track the owner and cleanup date.

## Rollback and post-deploy proof

Before deployment verify the exact rollback command/runbook and access needed.
State recovery-time objective, trigger, owner and what happens to new or migrated data.
For data changes use [migration recovery](migrate.md); code revert cannot restore deleted rows.
Prefer a reversible flag/cutoff where it fulfills the actual recovery requirement.

After an authorized deploy, verify target/version, health, new errors, latency and critical flow.
Check real logs/metrics/traces and recovery readiness.
Roll back or hold according to agreed triggers, preserving evidence and task state.
A failed deployment remains failed even if the readiness review was positive.

## Output and stop

Return ready/blocked, blockers, accepted risks, evidence links and rollback plan.
For executed releases separately report deployment ID/version and current monitored state.
Do not call a multi-day rollout complete while observations remain uncollected.
Stop advancement at failed checks, exceeded budget, missing required authority or unknown data state.
