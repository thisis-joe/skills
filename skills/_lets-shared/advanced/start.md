# Project setup and route selection

Use this reference when the project commands, standing quality bar, or next workflow are unclear.
Apply the [common contract](../contracts.md) and [route table](../routing.md).
A clear static edit can proceed directly with its relevant check.
Setup creates evidence and useful conventions, not permission for unrelated changes.

## Inputs

- Requested outcome, scope, existing user decisions and execution mode.
- Repository rules, glossary, ADRs, spec/plan and authoritative task-state location.
- Branch/base, working-tree status, dependency manifests, lockfiles and CI.
- Available test, browser, scanning and deployment capabilities.

## Choose the mode

| Observable condition | Mode | Result |
|---|---|---|
| Rules and quality bar already exist | Reuse | Read relevant rules and verify actual commands |
| One clear low-impact static edit | Lightweight | Direct edit plus content/visual check |
| New behavior with settled requirements | Standard | Public test boundary and build/verify route |
| Uncertain contract, security or costly failure | Strengthened | Add the relevant specialist proof |
| Quality bar missing, live user available | Establish | Brief defaulted intake and executable constraints |
| Quality bar missing, unattended run | Floor only | Enforce the floor and flag missing policy |

Single-task and continuous execution are independent of these modes.
Reuse approval for the defined scope; continuous mode adds no deployment or deletion authority.

## Discover before asking

1. Read project instructions and identify the installation/workspace boundary.
2. Detect language, pinned package manager, lockfile, test runner and checked-in wrappers.
3. Read CI and existing scripts for focused tests, full tests, build, types and lint.
4. Inspect the current branch, base and pre-existing dirty paths without changing them.
5. Find the existing spec/plan and task-state owner; preserve incomplete other work.
6. Run only the baseline checks needed to establish a missing fact.
7. State the findings briefly and ask only for material policy still missing.

If manager signals disagree, use the [security installation gate](security.md) before installs.
Use a feature branch for feature work and keep commits scoped to work units.
The execution owner handles branch changes, fixes, commits and task completion.

## Establish a standing bar

When a bar exists, follow it rather than creating another rules file.
When creating one, use the repository convention or a root `CONSTRAINTS.md`.
Record rule, reason, exact checker, scope, lifecycle stage and blocking/warning policy.
Separate enforced rules from measured-only metrics and accepted exceptions.
Ask at most four policy questions, each with a usable default:

1. Which dimensions beyond the floor matter here?
2. Which failures block advancement rather than warn?
3. Use justified targets, or measure today's level and hold it?
4. What checking latency is tolerable during edits and task closure?

Read known answers from files and prior agreement instead of asking them again.
Do not run this interview in CI or an unattended loop.

## Quality floor

Inspect the actual task diff, including committed, staged, unstaged and untracked work.
Flag lowered thresholds, weakened or deleted assertions, skipped/deleted tests,
new checker suppressions, unfinished stubs/empty catches and unexplained exceptions.
Keep secret values out of output; report redacted rule/location evidence.
Do not silence a checker or weaken the bar to make implementation pass.
Legitimate removals and exceptions need an explicit reason and their actual authorization.
An exception records rule, path, reason, owner, tracking item and expiry/review date.
A heuristic guard finding needs inspection; it is not proof of malicious intent.
Guard outcomes must distinguish clean, violation and unable-to-run.
If a helper uses exit codes, preserve `0` clean, `1` violation, `2` unavailable/error.
An absent merge base or failed scanner never becomes a clean result.

## Ratchets and checking cost

Measure an inherited baseline before choosing a target the project cannot meet.
For a ratchet, record value, units, direction, conditions and justified noise tolerance.
Advance the recorded floor after a real improvement; surface regressions.
Place fast changed-file checks in the edit loop, related tests at task closure,
and expensive security, mutation or browser budgets at review/CI as appropriate.
Use existing coverage artifacts rather than rerunning a suite just to read coverage.
Choose established tools already supported by the stack; install only in authorized scope.
Web performance/accessibility tools need a real URL; mark non-web dimensions inapplicable.
Combine suite checks with an external or independently owned check when available.
Record unavailable capabilities instead of inventing a replacement verdict.

## Output and stop

Return a compact project profile, selected route, task-state owner and verified commands.
Include standing checks with scope/stage, baseline, exceptions and missing capabilities.
Link one canonical quality policy from the project's existing agent rules when authorized.
Stop setup when enough is known to execute the requested work safely.
Unresolved material decisions block their dependent action; other permitted work can continue.
Use the [context contract](../contracts.md) for evidence and interruption recovery.
