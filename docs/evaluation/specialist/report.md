# LET’S specialist behavioral application report

Twelve requested cases produced concrete local artifacts. Nine bounded applications passed their artifact/diagnosis check; three deliverables remain inconclusive because required browser/formal/runtime evidence is unavailable. The 15 local behavioral checks exited 0. Passing those checks includes observing unsafe fixture behavior; it does not mean the fixture targets are safe or production-ready.

This is one fresh agent applying the supplied scenarios, not independent repeated trials per skill. No no-guidance comparison, blinded judge, real browser run, formal verifier run, production telemetry/backend access, provider webhook delivery or deployment occurred. The evaluation therefore does not establish general skill effectiveness or a numerical improvement.

The only repository content read was selected `skills/lets-*/SKILL.md` and relevant `skills/_lets-shared` material. Active skill hashes are in [skill-snapshot.json](/tmp/lets-specialist-validation/evidence/skill-snapshot.json). No repository/user-skill writes, external service writes, agents, dependency installs or external service CLIs were used. Disposable scratch is cleaned; retained artifacts are under this directory.

## Case outcomes

| Case | Status | Observed result | Concrete artifact |
|---|---|---|---|
| security | passed | Cross-tenant delete observed; dependency execution gated. | [security-review.md](/tmp/lets-specialist-validation/outputs/security-review.md) |
| migrate | passed | Race reproduced; expand/migrate/contract and recovery gates retained. | [migration-plan.md](/tmp/lets-specialist-validation/outputs/migration-plan.md) |
| performance | passed | No supported gain; cache/noise confounding disclosed. | [performance-decision.md](/tmp/lets-specialist-validation/outputs/performance-decision.md) |
| frontend | inconclusive | State/driver recipe supplied; live acceptance unavailable. | [frontend-acceptance.md](/tmp/lets-specialist-validation/outputs/frontend-acceptance.md) |
| observe | passed | Bounded schema plus local telemetry self-test; no production claim. | [observability-plan.md](/tmp/lets-specialist-validation/outputs/observability-plan.md) |
| automate | passed | Duplicate/timeout/restart/crash/concurrency checks; inactive artifact. | [automation-runbook.md](/tmp/lets-specialist-validation/outputs/automation-runbook.md) |
| ship | passed | Readiness blocked by exhausted budget and untested recovery. | [release-readiness.md](/tmp/lets-specialist-validation/outputs/release-readiness.md) |
| document | passed | Existing .rst ADR convention and facts preserved; exercise created. | [0008-dual-email.rst](/tmp/lets-specialist-validation/outputs/0008-dual-email.rst) |
| retro | passed | Biased success claim rejected; defensible comparison protocol created. | [retrospective.md](/tmp/lets-specialist-validation/outputs/retrospective.md) |
| simplify | passed | Dynamic configured caller blocks deletion; restoration observed. | [simplification-plan.md](/tmp/lets-specialist-validation/outputs/simplification-plan.md) |
| verify-formal | inconclusive | Stale atomic model exposed actual double-winner trace; no formal proof. | [formal-verification-status.md](/tmp/lets-specialist-validation/outputs/formal-verification-status.md) |
| verify-runtime-helper | inconclusive | Launch failure retained; 0/1 live mapped journeys; draft blocked. | [runtime-helper-status.md](/tmp/lets-specialist-validation/outputs/runtime-helper-status.md) |

Additional artifacts: [automation trigger/claim/recovery/activation contract](/tmp/lets-specialist-validation/outputs/automation-contract.json), [teaching exercise](/tmp/lets-specialist-validation/outputs/email-migration-exercise.rst), [evaluation protocol](/tmp/lets-specialist-validation/outputs/evaluation-protocol.json), [runtime feature map](/tmp/lets-specialist-validation/runtime-helper/features.json).

## Reproduce and inspect

```sh
python3 /tmp/lets-specialist-validation/checks.py
```

The harness uses Python standard-library fixtures only. It records 15 expectation checks, including the dangerous negative cases; it is not a substitute for required real-target project checks. See [check receipt](/tmp/lets-specialist-validation/evidence/checks.stderr), [summary](/tmp/lets-specialist-validation/evidence/check-summary.json), [observed values](/tmp/lets-specialist-validation/evidence/observations.json) and [runtime receipts](/tmp/lets-specialist-validation/evidence/runtime-helper/check-evidence.json). The three unavailable deliverables are not converted to passing product acceptance by the green fixture suite.

Machine results: [results.json](/tmp/lets-specialist-validation/results.json). Reproduction inputs: [preparation script](/tmp/lets-specialist-validation/prepare_artifacts.py) and [check harness](/tmp/lets-specialist-validation/checks.py). [Run metadata](/tmp/lets-specialist-validation/evidence/run-metadata.json) identifies method and limits; [artifact manifest](/tmp/lets-specialist-validation/evidence/artifact-manifest.json) freezes file hashes.

## Contradictions, ambiguity and coverage limits

No forced unsafe action or direct contradiction among the selected active procedures was demonstrated in these bounded applications. No skill was edited to obtain a desired result. Three interpretation/availability edges remain visible:

- Performance says to revert neutral owned experiments and to report invalid comparisons as inconclusive. Because the cache mismatch invalidates this comparison before adoption analysis, the report returns inconclusive and leaves any actual owned-edit reversion to its execution owner. No edit was silently kept or reverted.
- The common contract requires commits for product work completion, while verify/review return evidence and do not own product commits. This run delivers scratch review/evidence artifacts and makes no product-task done claim; no repository commit is fabricated.
- The dependency gate needs current official pinned-client behavior, graph ownership and real lockfile/CI evidence, none of which this restricted fixture supplies. It blocks lifecycle execution rather than guessing a manager policy.

Further gaps are listed per case in results.json: missing real consumer/usage windows, untested data recovery, no image pixels or UI driver, synthetic telemetry, provider boundary stand-ins and absent formal sync history. A local model/pass, source check or successful arithmetic calculation is never promoted to proof of unavailable real behavior. The ADR preserves uncertainty; the exercise does not claim demonstrated learning; the retrospective does not claim prevention from a proposed protocol.

No author source audit, desired-answer document or hidden scoring source was consulted. Nonetheless this agent authored both scratch fixtures and checks from the scenario, so assertions are not independent blinded evidence, and small local fixtures cannot establish discovery performance on a full repository.
