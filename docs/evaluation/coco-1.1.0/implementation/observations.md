# Partial native implementation observations

Status: **F4 comparison unavailable; the five-pair adoption gate is not met.**
The frozen actor driver is `027e5c3`; compared skill sources were current
`622975e349e6276b225aa9ef02ee69d664dd2927` and candidate
`17e342556cb3465780bff18bd358c262d6f47736`. The protocol, question meanings,
owner answers, public oracle and limits were fixed before primary execution.

## What actually ran

Twelve projects were prepared: five current/candidate pairs and two candidate
preservation probes. Only profile 0's two projects started. Current used three
actor invocations; candidate used two. Their actual questions used three owner
classifier invocations in total. The remaining eight primary projects and both
preservation projects were **not attempted**, not observed failures.

Before primary, the first classifier sensitivity control encountered HTTP429
and its permitted retry also encountered HTTP429. Both records remain. After the
server-reported cooldown, three single-attempt recovery controls passed: emitted
SKU spelling, public interface, and an outside-contract business question retained
as unresolved. These five preflight calls are separate from development attempts.

The initially prepared `9949121` candidate had zero comparison actor launches.
A concrete reporting repair produced `17e3425`; a pre-exposure bookkeeping repair
separated delivered-but-undecided topics from settled choices. A fresh root pinned
the final candidate and corrected driver. The unchanged classifier controls were
reused with explicit provenance; their prompts contain no candidate skill bodies.

## Observed behavior and its limits

The current actor asked about collisions and malformed rows, then committed and
reported completion without first resolving SKU identity. Its independently
executed CLI checks exposed the identity mismatch. The owner correction was
delivered, but that repair turn met another HTTP429 wait and exhausted the original
420-second limit. Its final repair state is unavailable; the last commentary is
preserved as provisional, not renamed a final report.

The candidate actor asked all three material choices, including identity and
stored/emitted spelling. It received the actual owner answers. Its second native
stream emitted a final message and `turn.completed`; however, the queue was halted
before the driver finalized that process's exit metadata. The raw final remains
available for inspection with an explicit **process-exit-unavailable** label.
No synthetic exit 0 or stable-trial completion was inserted.

After shutdown, both project trees were unchanged across a five-second hash
observation. Separate disposable copies were checked through the real CLI:
current profile 0 failed and candidate profile 0 passed the public probes. These
are labeled **post-stop observations**. They do not replace a completed native
trial, establish all process guards, or fill any of the missing matched pairs.
There is no comparative quality, speed, usability or human-effort claim.

## Stop and evidence preservation

After recurring capacity failures following the reported cooldown, the root
stopped unstarted work. Python's executor shutdown would otherwise drain queued
futures. The exact owned driver was suspended to prevent queue advancement; its
active CLI was already observed defunct before cleanup. Only that driver received
SIGTERM followed by SIGCONT. The driver exited 143. All nine recorded driver,
actor and trial-owner CLI leaders were absent at the final process check.
Leader absence and briefly stable files do not prove arbitrary child-tool cleanup.
No quarantined project was resumed by another actor.

The collection-only correction retains incomplete raw events, distinguishes
provisional commentary from an actually emitted final, and labels unstarted cases
`not_attempted`. Three focused collector tests verify those distinctions. It does
not change frozen actor input, source, criteria, owner choices, budgets or grades.

The condition-blind packet contains all twelve planned projects, including the
ten explicitly unstarted entries, plus two unlabeled false-completion controls.
Its independent review is separate from these observations. Grounded review of
partial evidence cannot certify a completed five-pair cohort.

Durable receipts:

- [Archive manifest and source identities](evidence/archive.json)
- [Raw native records, snapshots and checkpoints](evidence/native-partial-evidence.tar.gz)
- [Shutdown, actual attempts and unstarted IDs](evidence/shutdown-receipt.json)
- [Initial capacity failure and server cooldown](evidence/capacity-unavailable.json)
- [Pre-exposure candidate/instrument reconciliation](evidence/pre-exposure-reconciliation.json)

The raw archive retains original failures, successful preflight recovery, owner
exchanges, source manifests, checkpoints and post-stop copies. No further cohort
was run to replace the incomplete one. F4 and any final adoption claim depending
on it remain pending an available execution environment and an explicitly recorded
recovery plan; completed source changes and independent acceptance observations
must be reported separately.
