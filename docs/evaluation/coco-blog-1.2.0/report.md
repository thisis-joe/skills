# COCO 1.2.0 release verification

## Current state

The two requested fixes are implemented: package version `1.2.0`, and publication-state guidance driven by the consumer schema with Hugo retained as an example. Final independent review and archive refresh are pending. No registry publication, remote source push, PR or personal installation has been performed.

## Behavior observed

The protocol was saved before native execution. Four independent native `codex exec --ephemeral --ignore-user-config --sandbox workspace-write` sessions used project installations of the candidate, the CLI's default model, organic Korean requests and isolated local data. No model override, bypass flag, rubric, comparative claim or success coaching was supplied to the candidate. The fourth case fills the initially uncovered preserved Hugo path.

| Case | Actual behavior | Artifact/state checks |
| --- | --- | --- |
| Bare invocation | Listed two recent ignored local notes with authored dates, excluded template/index/escaping symlink and stopped at selection | 14 checks passed; no new post, Git delivery or source-state change |
| Selected note, `status` schema | Reused settled note/author/reader/angle, revised a separate `status: draft` manuscript and returned the real request-template body | 18 checks passed; source/hand-edited article identity preserved, private/injection content excluded, no invented measurements, draft excluded from fixture render, no commit/push/request |
| Approved release, `published` schema | Changed only `published: false` to `true`; checked fixture HTML and made one manuscript-only commit plus an explicitly authorized local topic push | 20 checks passed; content ref untouched, app ancestry excluded, request remained human-owned, real public deployment not claimed |
| Preserved Hugo release | Changed `draft: true` to `false` in the accepted article and checked fixture HTML | 17 checks passed; body/identity/source state preserved; no commit/push/request |

All four processes exited zero. In every case the original branch, HEAD, index, unstaged diff, status and notes were preserved. The observer rejected a wrong schema field, a leaked private canary and a modified source state; restored scratch artifacts passed again. These are 69 observations across four single cases, not 69 independent model trials or a reliability percentage.

The historical failing-before check is textual contract evidence: base `04507c1` universally required `draft: false`; the candidate instead requires the consumer's actual transition and retains Hugo guidance. It is not a native old-versus-new comparison.

## Prompt quality

A fresh reviewer is assessing intent/routing, context reuse/question economy, clarity/consistency, evidence/editorial quality and boundaries/state against the frozen scale. Results will be recorded separately from mechanical test success. The writing sample distinguishes implementation and local test evidence from unmeasured performance/production effects; it does not manufacture an incident, benchmark or rationale. The selection sample asks a single material selection question; the settled drafting request does not reopen that choice.

## Packaging and recovery

The full validator and 200 repository tests passed without skips. After adding the release-note document to the npm allow-list and its existing test expectation, the affected 14 npm distribution tests passed. Separate archive checks exercised both Codex and Claude destinations: upgrade from `v1.1.0` (29 skills/118 files) to `1.2.0` (30 skills/125 files), unchanged reinstall, user-modification conflict with zero partial writes, unrelated user-skill preservation and exact rollback to the original managed file hashes. The registry readback found latest `1.1.0` and no `1.2.0`; refresh is required at the actual publication step.

## Limits and driver corrections

This proves the exercised native Codex paths and both installer payloads. It does not prove native Claude behavior, repeated-run reliability, every author interview, arbitrary generators, or any real consumer site's renderer/publisher/public URL. The local renderer only makes draft exclusion/inclusion observable.

The child sandbox denied writes to the application's `.git`, so the writing/release cases used a fresh clone of the same local origin with a linked worktree; Hugo used a standalone isolated clone. Outputs disclose this. Direct linked-worktree preparation in the original native checkout remains unproven in this environment; original work and content-history isolation were observed. No authorization-origin rejection was bypassed.

The observer initially assumed every cloned checkout retained `origin/content`, and later assumed one preview-directory pattern. It was corrected to use the application's confirmed content ref and observed preview directory. Native runs were not repeated. The archive driver initially rejected safe directory members in a local `git archive`, then corrected that guard while retaining path/link checks. These are recorded driver failures, not skill successes or hidden product failures.

## Evidence

`results.json`, `skill-hashes.json` and `native-manifest.json` identify case outcomes and exact skill/output hashes. `native-events.tar.gz` retains only synthetic requests, native events, final responses and launch/exit receipts; no consumer repository/fixture copies are checked in. Full local observer/fixture evidence remains at `/private/tmp/coco-articles-run/`, with its original bundle hash `16f631622747ffcf63d0e97cc151a15d77a8bd12000dfa624bfcb44830d96360`. The native result receipt hash is `c24ca9a543c10e33a8da9c7d631ff0df0883e372db86c9d66112278abf0e3b89`.

Rollback for a later authorized installation is the version-pinned `1.1.0` installer with the same runtime/destination; preflight preserves personal modifications. No article or source-note data migration is introduced.
