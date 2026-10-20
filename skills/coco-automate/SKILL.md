---
name: coco-automate
description: "Use when building CI/CD, recurring workflows, issue bots, reusable verification helpers or task automation."
license: MIT
---

# coco-automate

Create scoped, resumable automation with explicit activation and effect boundaries.

Read the [common contract](../_coco-shared/contracts.md) before acting. Read the [automation core](../_coco-shared/advanced/automate.md) before preparing or changing anything that runs on a schedule or trigger, runs unattended, retries, or writes externally, or when any mode below applies; once read, the whole core applies even if no mode matches. A one-off local helper run by hand with no retries or external effects needs only this entrypoint. Initially and on new scope, risk, state, or missing prerequisites, check for CI/deployment, sustained execution, webhook/bot work, report intake (setup/triage/fix), manual setup wizards, and workflow specifications. If any applies or is unclear, read the core's mode selection and all matching modules before dependent work.

## Procedure and output

1. Identify trigger, owner, input trust boundary, intended effect, retry semantics and stopping condition. Reuse existing platform/CI conventions and actual commands.
2. Define minimum permissions and separate test/deploy secrets. Validate untrusted issue/webhook/model data; verify trusted event origin and ownership before privileged work.
3. Make effects idempotent: retain a stable initiating key, atomically claim it, bind it to the payload/result, handle unknown outcomes without blindly retrying, and retain deduplication state across replay/recovery windows.
4. Build a testable local/preview workflow with dependency ordering, meaningful quality gates, bounded retries, logs and rollback/recovery. Review dependency lifecycle scripts before first execution.
5. For bots, verification-skill lifecycle, evaluation loops or multi-task workers use the relevant advanced mode. Artifact-only preparation is distinct from activation; do not create schedules, send messages or deploy merely because the workflow mentions them.
6. Test duplicates, crashes, malformed/untrusted input, missing tools, exhausted retries and resumption. Return the concrete artifact and activation requirements.

Return: runnable automation artifacts, permissions/effects inventory, tests and recovery evidence, activation state and outstanding approvals.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "This change is trivial, skip CI" or "CI is too slow": optimize the pipeline; never skip it.
- "The test is flaky, just rerun": fix the flakiness; flakes mask real defects.
- Tests disabled or failures silenced to get a green pipeline.
- Production deploys without staging verification or a rollback mechanism.
- Secrets in code or CI configuration instead of the secret store.
