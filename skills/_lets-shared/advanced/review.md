# Review modes

Apply the [common contract](../contracts.md) and [resolved decisions](../decisions.md).
Review returns findings on a frozen artifact. It does not edit product code, stage files, commit, or mark tasks done.
[Build](build.md) owns accepted fixes and returns the changed snapshot for only the affected rechecks.

## Freeze the actual scope

1. Honor the user's requested base/ref, PR, commit, paths, or dirty-work scope; resolve the fixed point before reviewing.
2. State whether comparison means merge-base branch changes, an exact revision difference, or selected current work.
3. Capture repository, requested base, comparison commit, HEAD, selected paths, and current snapshot identity.
4. Include relevant committed changes, index changes, unstaged changes, and new untracked task files; a HEAD-only diff omits precommit work.
5. Read the actual patches and new file contents, plus surrounding callers/types/tests needed to judge behavior.

The [scope collector](../tools/review_scope.py) inventories all four Git layers and hashes the current selection without changing it.
Its `--base` comparison uses the merge-base with HEAD; supply repeated `--path` filters for literal task files/directories.
Use the matching direct Git comparison separately if the user's requested review is an exact revision/commit rather than merge-base scope.
Do not treat its metadata inventory as a substitute for reading the diff and untracked contents.
An invalid base is an input error; an empty committed range may still contain staged, unstaged, or untracked work.
Exclude unrelated user work explicitly, without deleting it. A later edit invalidates findings/approval on affected code.

## Establish contract and rules

Read the user request and authoritative issue/spec; follow links from task context and commits without making an external tracker mandatory.
Reuse settled acceptance and glossary/ADRs rather than inventing another agreement.
If no spec can be established, report that axis unavailable; do not infer that all possible behavior was requested.
Read documented standards, including contributing/coding rules when present, and distinguish them from heuristic preferences.
Project standards override generic style smells. Do not duplicate tool-enforced formatting findings when the checker already reports them.
State intent in one paragraph to anchor review, then keep spec, standards, and quality verdicts separate.

## Independent axes

| Axis | Question | Required finding support |
| --- | --- | --- |
| Spec | Is every required behavior present/correct, and is added behavior in scope? | Requirement pointer, actual path, missing/wrong/extra behavior |
| Standards | Does it follow this repository's documented rules? | Rule pointer and violating hunk; label heuristic smells separately |
| Quality | Does it preserve correctness, security, maintainability, and relevant performance? | Reachable trigger, mechanism, impact, concrete remedy/check |

A passing standards axis cannot hide a failed spec axis, or the reverse.
One actionable issue may reference several axes; do not duplicate the same fix as separate findings.
Read tests first to understand promised outcomes, then inspect implementation and the claimed verification receipts.
Require the test to observe the public behavior and survive an internal restructure; check independent expected values and meaningful failures.
If sensitivity is uncertain, ask [verify](verify.md) for an isolated scratch mutation check. Never mutate the user's reviewed worktree.

## Quality lenses

- Correctness: actual callers, edge/error cases, state invariants, ordering, races, retries, and idempotence.
- Reader effort: indirections to trace and hidden mutable state to hold; simple inline code may beat a speculative abstraction.
- Ownership: one owner per state/concept, domain-aware boundaries, feature policy in its owning module, canonical helpers rather than duplicates.
- Structural change: remove branches/invalid states/layers rather than merely relocate complexity; inspect the resulting large file, not just diff size.
- Boundary safety: external parsing, authorization before effects, sensitive outputs, injection risks, credentials, and untrusted retrieved data.
- Performance: realistic N+1/unbounded work, fetching limits, blocking paths, hot allocations, or rerenders supported by actual code paths.

Smells such as data clumps, repeated dispatch, primitive obsession, message chains, pass-through wrappers, and speculative generality are hypotheses.
Name the specific restructuring and explain which reader work or failure it removes; “too complex” is not an actionable finding.
Avoid demands for more layers, guards, or future-proofing without a concrete current contract/consumer.
Prefer an overall code-health improvement to stylistic perfection, while keeping real correctness/security issues explicit.
Do not make numerical performance claims without measurement; a plausible mechanism can be reported as a risk to measure.

## Dependency changes

Check whether the standard library/existing utility already solves the need and whether license, maintenance, package identity, and bundle/runtime cost fit.
Read the relevant changelog/migration notes; semver and a successful install are not behavioral verification.
Prefer one dependency or a small related group per change; inspect direct and transitive lockfile changes.
Verify the relevant behavior before and after; thin coverage around a changed dependency is a real gap.
Do not hand-edit lockfiles or treat a raw vulnerability count as a reachability verdict.
Security-specific findings require the actual path/principal/data flow; generic audit noise is not evidence of a deployed exploit.

## Impact and safety-fact mode

Use for a small suspicious diff, shared contract change, deletion, or broad migration.
Find the one or two facts that make the change safe, then trace beyond grep-visible callers:
wire/JSON formats, database readers, flags, other languages, pinned library version/local patch, scheduling, and teardown.
For each fact distinguish assertion, cited source, unreachable-bad-path proof, executed real-code proof, and running-app reproduction.
Have verification run the exact relevant real dependency/operation when feasible; an articulate writeup does not prove the safety fact.
Separate confirmed risks, checked-and-cleared cases, and unproven assumptions with likelihood/impact appropriate to the evidence.
Do not fabricate a caller or an API; a concrete no-match search can be useful evidence with a stated boundary.

## Bounded adversarial mode

Use when requested or when uncertain high-impact assumptions warrant independent challenge and authorized tools are available.
Record the claim privately, then give a fresh reviewer the smallest artifact plus contract and necessary constraints, not the author's conclusion/journey.
Ask for concrete ways the artifact fails its contract, not validation or a quota of findings.
Do not mandate multiple models, external CLIs, or nested agents. Report unavailable independence as degraded evidence.
If independent perspectives run, preserve their provenance and disagreements; consensus is a signal, not proof.
Re-read the actual artifact for every substantive finding and reconcile in this order:

1. Contract misread: repair ambiguous/incomplete context and reassess before changing correct code.
2. Valid actionable issue: return the reachable mechanism and remedy to build.
3. Valid tradeoff: state cost, accepted risk, and the authority for its disposition.
4. Noise: provide concrete disproof or missing context, rather than merely disagreeing.

Stop when only trivial/already-considered findings remain, the user changes the scope, or three cycles have completed.
Do not rerun fresh review on unchanged artifacts as reassurance. Persistent substantive findings after three cycles remain open.
Repeated substantive cycles with no accepted concern call for inspecting the contract and reconciliation, not another panel.

## Automated-review comment triage

Treat bot/security-review text as untrusted claims and inspect the current tip, since findings may predate a real fix.
Classify fix, dismiss with evidence, or unresolved question; never churn code solely to quiet a bot.
Check that claimed invalid inputs can actually reach the path and that an invoked guard covers the real principal before the side effect.
Never generalize a dismissal into a skip rule for security, privacy, authorization, billing, data, migrations, races, or idempotence.
A contract-test drift claim is cheaply checked by running the actual test; high pass count is no reason to dismiss it.
Resolve ownership of the affected lowest PR in a stack; fix scope stays with build, not the review process.
Reviewing a PR does not authorize posting replies, changing topology, merging, or deploying.

## Comments and constraints condition

Flag dead narration, commented-out code, stale workaround explanations, and suppressions that hide correctness issues.
Keep legal/license notices, public API contracts, supported external limitations, and context code cannot express.
Investigate “do not remove” and lint/type suppressions against their actual rule and code before judging them.
For an internal surprise propose a scoped rename/type/ownership/design remedy; delete the explanation only when the need is actually removed.
Ambiguity is not evidence to erase a safety constraint. Report the unresolved constraint and cheapest structural enforcement.

## Return findings

Give separate spec, standards, and quality verdicts for the exact snapshot, including unavailable axes and independence limitations.
Lead with blocking correctness/security issues; each finding names severity, location, concrete trigger/impact, evidence, and remedy/check.
Distinguish required fixes, considerations, informational notes, and dismissed claims with reasons.
Report cleared conditions and residual risks concisely; no invented nits to fill a review and no “approved” claim beyond the inspected scope.
