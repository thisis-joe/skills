# Fresh LET'S core workflow scenario exercise

This is one fresh agent applying 12 requested scenarios, with concrete saved outputs and real local Git/command evidence where required. It is **not** 12 independent model runs, a production validation, a formal proof, a blinded benchmark, or a measured quality/speed comparison. All fixtures and outputs live under `/tmp/lets-core-validation`; the repository and user-installed skills were not modified by this evaluator. No external service, message or agent was called.

Observed case results: 11 passed for the scenario behavior, one inconclusive procedural-ownership case (context). A passed evidence-boundary case can correctly end with unavailable product evidence: the UI journey, original timeout rationale and production duplicate cause are not established by this run. The case status is separate from underlying test pass/fail: debug and review deliberately preserve real failures.

A single fixed-bundle claim is **inconclusive**: five consulted integrated files changed while this read-only evaluation was in progress. The initial/final hashes are in [bundle-snapshot.json](bundle-snapshot.json), [bundle-snapshot.final.json](bundle-snapshot.final.json), and [bundle-drift.json](bundle-drift.json). The final consulted files were copied with their relative installed-format paths into [frozen-current-bundle](frozen-current-bundle). Relevant changed references were reread, and the changed current collector was rerun against the unchanged review fixture with identical scope output. This confirms the recorded scenario behavior on that final collector snapshot; it does not reconstruct one uniform snapshot for all earlier reasoning.

Only the current integrated entrypoints plus common/conditional references were read. No upstream `sources/`, source audits, author chat or intended-answer material was consulted. Synthetic fixture elaborations were authored within the requested scenarios and are visible as each case's `input.md` and source files. The same evaluator authored these small fixtures and applied the skills, and several inputs contain explicit scope constraints from the assigned scenario; results should not be treated as a blinded effectiveness estimate.

## Findings requiring interpretation

1. **Context completion-state ownership is ambiguous.** [contracts.md:21](/Users/Joseph/workspaces/skills/skills/_lets-shared/contracts.md:21) says lets-build owns completion-state updates. [advanced/context.md:35](/Users/Joseph/workspaces/skills/skills/_lets-shared/advanced/context.md:35) says to verify an already-succeeded commit and “reconcile the task state”. The reference also permits saved/updated artifacts when requested. The fixture explicitly authorized recovery-state reconciliation, so this run performed it safely and recorded the evidence; however, the bundle does not expressly say whether context should make the completion write itself or hand that mutation to build. The case remains inconclusive for procedural ownership rather than silently resolving the rule overlap. A narrow clarification could assign the write while retaining context's inspection/packet role.
2. **The evaluation target moved.** This is an evaluation reproducibility limitation, not attributed to any particular actor and not a skill-behavior defect. Initial artifact-integrity assertion that read files stayed fixed failed; the final integrity checker instead records the drift and verifies the retained final copy. Avoid claiming a uniform “current bundle passed all cases”.
3. **Fixture/evidence limits remain visible.** The spec fixture's accepted “formula-like” term lacks exhaustive classification; no new accepted set was invented. The plan has a source map rather than an executable application. The race harness confirms the provided check-then-act mechanism, not the original service's causal history. These are input/evidence limits, not verified production regressions. No additional skill defect was established by this single exercise.

## Per-case outputs and evidence

### start — lets-start — passed

One stdlib test passed. No product task was supplied, and no policy/spec/task file was invented.

Concrete response: [start/output.md](start/output.md). Source input: [start/input.md](start/input.md).

Command/action: `python3 -m unittest discover -s tests -v`.

Evidence: [start/evidence/discovery.json](start/evidence/discovery.json), [start/evidence/baseline.json](start/evidence/baseline.json).

Limit: The one-test fixture is small; no real service or CI run is proved.

### clarify — lets-clarify — passed

Produced two ready policy questions with alternatives and recommendations; no settled vocabulary was rewritten.

Concrete response: [clarify/output.md](clarify/output.md). Source input: [clarify/input.md](clarify/input.md).

Command/action: `Read approved agreement and glossary; concrete draft in output.md`.

Evidence: [clarify/agreement.md](clarify/agreement.md), [clarify/glossary.md](clarify/glossary.md), [clarify/evidence/inputs-read.json](clarify/evidence/inputs-read.json).

Limit: No human answers were obtained; policy is correctly still unsettled. Recommendations are draft proposals.

### research — lets-research — passed

Actual rename-aware history/blame showed initial import only; capture probe established 0.3 passed to the client, with no invented causal rationale.

Concrete response: [research/output.md](research/output.md). Source input: [research/input.md](research/input.md).

Command/action: `git log --follow --format=fuller -- client.py; git blame -L 1,4 -- client.py; git show HEAD -- client.py`.

Evidence: [research/evidence/history.json](research/evidence/history.json), [research/evidence/probe.json](research/evidence/probe.json), [research/base.txt](research/base.txt).

Limit: Downstream HTTP timeout semantics, pre-import discussion, metrics and tracker evidence unavailable.

### design — lets-design — passed

Defined caller usage, durable stable key/fingerprint, atomic uniqueness, pending/unknown states, recovery, retention and public effect-oriented test cases.

Concrete response: [design/output.md](design/output.md). Source input: [design/input.md](design/input.md).

Command/action: `Read on_message caller and brief; concrete interface/alternative table in output.md`.

Evidence: [design/brief.md](design/brief.md), [design/caller.py](design/caller.py), [design/evidence/inputs-read.json](design/evidence/inputs-read.json).

Limit: Draft design only: actual provider guarantees, DB semantics and crash-window implementation not executed.

### spec — lets-spec — passed

Updated existing ISSUE-42 v0 -> v1; observable CSV acceptance and library boundary retained, no re-interview or implementation.

Concrete response: [spec/output.md](spec/output.md). Source input: [spec/input.md](spec/input.md).

Command/action: `Saved and read back specs/ISSUE-42.md`.

Evidence: [spec/specs/ISSUE-42.md](spec/specs/ISSUE-42.md), [spec/evidence/inputs-read.json](spec/evidence/inputs-read.json), [spec/evidence/saved-spec.json](spec/evidence/saved-spec.json).

Limit: Fixture issue says formula-like without exhaustive classifier; preserved/disclosed that precision limit, not an invented accepted set.

### plan — lets-plan — passed

Nine task files; acyclic dependencies; initial frontier CSV-1 and MIG-EXPAND; one mutable state convention; final combined gate and rollback.

Concrete response: [plan/output.md](plan/output.md). Source input: [plan/input.md](plan/input.md).

Command/action: `python3 /tmp/lets-core-validation/check_artifacts.py; read task graph via evidence/graph.json`.

Evidence: [plan/plans/invoice-export.md](plan/plans/invoice-export.md), [plan/tasks/invoice-export/CSV-1.json](plan/tasks/invoice-export/CSV-1.json), [plan/tasks/invoice-export/MIG-EXPAND.json](plan/tasks/invoice-export/MIG-EXPAND.json), [plan/evidence/graph.json](plan/evidence/graph.json).

Limit: Source map only, so actual Git base and executable command availability are unverified. Plan only, no task completion claimed.

### build — lets-build — passed

New CLI test failed for unrecognized --excited; minimal change passed two tests and both CLI paths; committed only greet.py/test; NOTES hash unchanged and still dirty.

Concrete response: [build/output.md](build/output.md). Source input: [build/input.md](build/input.md).

Command/action: `python3 -m unittest discover -s tests -v; python3 greet.py Ada --excited; python3 greet.py Ada; git add -- greet.py tests/test_greet.py; git commit`.

Evidence: [build/review.md](build/review.md), [build/task-state.json](build/task-state.json), [build/evidence/red.json](build/evidence/red.json), [build/evidence/green.json](build/evidence/green.json), [build/evidence/runtime-excited.json](build/evidence/runtime-excited.json), [build/evidence/runtime-normal.json](build/evidence/runtime-normal.json), [build/evidence/review-scope.json](build/evidence/review-scope.json), [build/evidence/commit.json](build/evidence/commit.json), [build/evidence/closure.json](build/evidence/closure.json).

Limit: Required scoped review is same-agent self-review explicitly permitted by fixture rules; no independent reviewer, production acceptance or external publish.

### debug — lets-debug — passed

Sequential 10/10 single effects; pinned concurrent schedule 10/10 duplicate effects, exit 1; same stable input ID/target hash, joined threads, no product edits.

Concrete response: [debug/output.md](debug/output.md). Source input: [debug/input.md](debug/input.md).

Command/action: `python3 repro.py --mode sequential --attempts 10; python3 repro.py --mode race --attempts 10`.

Evidence: [debug/worker.py](debug/worker.py), [debug/repro.py](debug/repro.py), [debug/evidence/sequential.json](debug/evidence/sequential.json), [debug/evidence/red-race.json](debug/evidence/red-race.json).

Limit: Confirms supplied isolated worker race only. Production path/cause/rate and regression-after-fix unavailable, and no fix requested.

### verify — lets-verify — passed

Claim/evidence matrix kept Saved-state, DOM/visual/console/network and reload persistence unavailable; did not invent a driver or substitute unit success.

Concrete response: [verify/output.md](verify/output.md). Source input: [verify/input.md](verify/input.md).

Command/action: `python3 -m unittest discover -s tests -v`.

Evidence: [verify/input.md](verify/input.md), [verify/evidence/unit.json](verify/evidence/unit.json), [verify/evidence/inputs-read.json](verify/evidence/inputs-read.json).

Limit: No UI target/version or alternative reachable driver supplied. This passes evidence-boundary behavior; it does not pass UI acceptance. Prompt states the scope gap explicitly.

### review — lets-review — passed

Collector included discount.py untracked and modified tracked test; actual arithmetic defect found; independent axes spec failed/standards passed/quality failed; scope unchanged.

Concrete response: [review/output.md](review/output.md). Source input: [review/input.md](review/input.md).

Command/action: `python3 skills/_lets-shared/tools/review_scope.py --repo <fixture> --base main --path discount.py --path tests/test_discount.py; python3 -m unittest discover -s tests -v`.

Evidence: [review/evidence/before.json](review/evidence/before.json), [review/evidence/inspected.json](review/evidence/inspected.json), [review/evidence/tests.json](review/evidence/tests.json), [review/evidence/after.json](review/evidence/after.json), [review/evidence/current-bundle-before.json](review/evidence/current-bundle-before.json), [review/evidence/current-bundle-after.json](review/evidence/current-bundle-after.json).

Limit: One fixture covers unstaged/untracked plus empty committed range; not an exhaustive collector test of every Git edge. Current copied collector rerun matches original snapshot.

### context — lets-context — inconclusive

Verified existing successful T1 commit and unchanged receipt hashes; reconciled stale open -> done in authorized fixture state; no new product commit, count remains 2; T2 retained pending.

Concrete response: [context/output.md](context/output.md). Source input: [context/input.md](context/input.md).

Command/action: `git status --short --branch; git log -2 --format=%H; git show HEAD -- double.py; file-hash receipt checks; external fixture state reconciliation`.

Evidence: [context/task-state.before.json](context/task-state.before.json), [context/task-state.json](context/task-state.json), [context/receipt.json](context/receipt.json), [context/evidence/fixture-commit.json](context/evidence/fixture-commit.json), [context/evidence/resume-inspection.json](context/evidence/resume-inspection.json), [context/evidence/reconciliation.json](context/evidence/reconciliation.json).

Limit: Common contract reserves completion updates to build; advanced context explicitly says reconcile task state. User authorized fixture reconciliation, but skill ownership of the write is not explicit. This procedural claim is inconclusive; implementation was not repeated.

### triage — lets-triage — passed

Matched version/trigger/symptom to ISSUE-81; proposed existing-fix verification/needs-info; no duplicate fix, ticket, closure or external call.

Concrete response: [triage/output.md](triage/output.md). Source input: [triage/input.md](triage/input.md).

Command/action: `rg -n -i duplicate|timeout|retry|version|fix|owner report.md existing-issue.md`.

Evidence: [triage/report.md](triage/report.md), [triage/existing-issue.md](triage/existing-issue.md), [triage/evidence/concept-search.json](triage/evidence/concept-search.json).

Limit: Fix is a local evidence label and summary, without executable repository or verified tracker URL; runtime confirmation unavailable.

## Cross-case artifact checks

`python3 /tmp/lets-core-validation/check_artifacts.py` completed successfully. [artifact-integrity.json](artifact-integrity.json) confirms all 12 outputs exist, the nine-task graph is acyclic with the stated frontier, the review scope is identical before/after/current collector, the build commit owns exactly its two paths, the unrelated dirty file hash is unchanged, recovery did not create another product commit, and the frozen final read-file copy matches its manifest. This checker validates retained evidence consistency; it does not establish that skill prose is effective across agents or unseen tasks.

Build commit: `0accc817b35be9d05b8d1a192e72cda44c85203d` on fixture feature/build. Recovered context commit: `03b7e6a2131b4eec2d177c6591a22084c554e3f6` on fixture feature/context. Fixture histories/status and command stdout/stderr/exit codes are retained in per-case evidence JSON/TXT. [fixture-setup-evidence.json](fixture-setup-evidence.json) distinguishes initialization/feature-branch setup from evaluated actions. Context's `fixture-*` receipts establish the interrupted state before its resume actions.

This scoped evaluator did not run the parent repository's scripts/validate.py or its unittest suite because the assigned instruction-source boundary excluded repository code outside the integrated skill bundle; those required project checks remain the parent execution owner's responsibility. All executed application/collector checks here are named in per-case evidence.

Machine-readable summary: [results.json](results.json).
