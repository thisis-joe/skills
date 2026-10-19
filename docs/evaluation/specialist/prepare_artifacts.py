from pathlib import Path
import hashlib
import json

B=Path('/tmp/lets-specialist-validation')
def write(path,text):
 p=B/path
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(text.strip()+'\n')
def data(path,value):
 write(path,json.dumps(value,indent=2))

data('fixtures/performance.json',{'source':'constructed values instantiating the supplied 3% / +/-5% scenario; not a benchmark run','baseline_ms':[95,100,105,98,102],'candidate_ms':[92.15,97,101.85,95.06,98.94],'baseline_cache':'cold','candidate_cache':'warm','work_count':'not recorded','errors':'not recorded','limiter':'not profiled'})
write('fixtures/form.html','''<!doctype html>
<html lang="en"><head><title>Join mailing list</title><style>
main { width: 960px; margin: 40px auto; } label { display:block; }
</style></head><body><main><h1>Join mailing list</h1>
<form method="post" action="/subscriptions"><label for="email">Email</label>
<input id="email" name="email" type="email" required>
<button type="submit">Subscribe</button></form></main></body></html>''')
data('fixtures/frontend-evidence.json',{'scenario_evidence':'desktop happy-path screenshot only','image_file_supplied':False,'browser_driver_available':False,'source':'fixtures/form.html','rendered_widths_recorded':[]})
data('fixtures/dependency/package.json',{'name':'fixture-service','private':True,'packageManager':'pnpm@9.15.0','dependencies':{'fixture-native-module':'1.0.0'}})
data('fixtures/dependency/pending-package.json',{'name':'fixture-native-module','version':'1.0.0','scripts':{'postinstall':'node install.js'}})
write('fixtures/dependency/install.js','''// Untrusted pending lifecycle source, inspected as text only.
// This fixture stands for a dependency script with build-time effects.
require('node:fs').writeFileSync('generated-binding.txt', 'fixture build output');''')
data('fixtures/security-ownership.json',{'trusted_identity':'tenant-a','approved_root':'storage/tenant-a/jobs','required_owner_registry':'trusted server-side job_id -> tenant_id binding','unsafe_claim':'lexically tenant-prefixed path implies ownership','marker_writable_by_requester':True})
data('fixtures/runtime-config.json',{'formatter':'legacy_slug'})
write('fixtures/dynamic-caller.py',"formatter = getattr(formatters, runtime_config['formatter'])\nresult = formatter(user_input)")
data('fixtures/retro-one-run.json',{'source':'constructed biased evaluation summary from supplied scenario','completed_tasks':1,'author_selected_task':True,'baseline_count':0,'held_out':False,'rubric_frozen_before_run':False,'blind_judge':False,'reported_score':1,'reported_claim':'skill improved quality'})
data('fixtures/release.json',{'candidate':'fixture-release-2026-10-19.1','purpose':'readiness only','environment':'fixture-production','required_tests':'green supplied scenario premise; real receipts absent','rollback_test':'not run','error_budget_remaining':0,'release_policy':'freeze feature releases when exhausted','deployment_authorized':False,'production_command_inventory':'not provided'})
old='''0007: Preserve email source spelling
===================================

Status
------
Accepted

Context
-------
The stored ``contact_email`` value preserves input spelling for audit use.

Decision
--------
Retain the original value until an audited retirement decision.

Consequences
------------
A canonical form cannot reconstruct the original spelling.
'''
write('fixtures/decisions/0007-email-source.rst',old)
write('fixtures/decisions/0007-email-source.original.rst',old)
write('fixtures/decision-facts.rst','''Selected fixture design: add ``email`` alongside ``contact_email``.
``email`` uses strip and lowercase; ``contact_email`` preserves the raw input.
The backfill batch condition is ``0 <= batch_size <= 500``.
New writes update both fields and increment ``revision``.
A backfill skips/retries any row whose revision changed after scanning.
Normalization is not reversible. Production backups and restore have not been tested.''')

data('runtime-helper/features.json',{'target':'scratch-expense-ui-v2','features':[{'id':'expense.create','route':'/expenses/new','subfeatures':['enter amount','submit expense','show saved receipt'],'preconditions':['usable app instance','signed-in isolated fixture account','empty test ledger'],'drive':['open /expenses/new','fill Amount with 12.50','activate Save expense','read visible Saved and ledger entry for 12.50'],'success':'visible saved receipt and independently read persisted expense','gotchas':['do not synthesize fixture state to bypass the launch failure','no browser driver available']}],'mapped_features':1})

data('outputs/automation-contract.json',{'state':'PREPARED_LOCAL_PREVIEW_INACTIVE','trigger':{'kind':'issue.opened webhook','trusted_source':'fixture/team signed provider delivery; actual envelope/signature adapter not supplied','initiating_key':'repository:issue_id:event_id:action','delivery_id':'transport receipt only; not the intent key'},'owner':'configured repository automation owner; real identity unresolved','permitted_effect':'add needs-triage label to the original fixture issue only','forbidden_effects':['widen permissions','deploy','message users','create schedules','act outside configured repository'],'permissions':['issues label write restricted to configured repository'],'claim':{'storage':'SQLite scratch jobs primary key','atomicity':'BEGIN IMMEDIATE + UNIQUE key','binding':'SHA256 canonical repository/issue/event/action payload','duplicate_behavior':'return persisted claimed/unknown/succeeded state without resending'},'recovery':{'after_claim':'stop; no automatic stale takeover without proof owner is dead and effect absent','after_possible_effect_timeout':'state unknown; provider readback by stable key before any retry','readback_finds_receipt':'mark succeeded, preserve one effect','readback_unavailable_or_non_authoritative_absence':'blocked; do not blindly repeat','retries':'one effect attempt in preview; bounded manual recovery only','retention':'production owner must choose a duration exceeding provider replay and recovery windows before activation'},'activation_requirements':['real provider event/schema and signature verification','repository ownership and least privilege credentials','provider idempotency or authoritative result lookup for unknown outcomes','durable storage backup/retention and transaction semantics validation','crash/duplicate tests on actual adapter','explicit activation authorization'],'not_done':['no schedule created','no webhook endpoint exposed','no external effect','no credentials installed']})

write('outputs/security-review.md','''# Tenant delete and pending dependency review

Target: `fixtures/scenarios.py:delete_route`; supporting ownership manifest and dependency fixtures. This is a synthetic local review, not an assessment of an unseen production repository.

**Block the destructive path.** The route checks `tenant-a/jobs/<job>/data.txt`, then unlinks the derived path. A requester-controlled directory can resolve into tenant B. The local negative case returned 204 and removed B's file; the positive own-file case also removed its file, proving the observer sees effects. A literal B-prefixed path was rejected, which does not establish ownership of an A-shaped target.

| Asset / boundary | Abuse path | Control handed to build | Decisive check / result |
|---|---|---|---|
| Tenant B data / authenticated A to filesystem | A-shaped path crosses symlink into B | Resolve target; require approved-root containment, minimum depth, trusted authenticated owner binding; use no-follow/beneath-root descriptor operations or immutable hierarchy for check/use race | Cross-tenant symlink delete **failed security requirement**; local effect observed |
| Tenant A data / legitimate owner | Owner's authorized own job | Preserve approved legitimate deletion and diagnostic receipt | Positive control passed in fixture |
| Ownership / requester-writable marker | Actor writes their own ownership claim | Read trusted registry before teardown; writable marker alone is insufficient | Registry not implemented in target; ownership proof unavailable |
| Build host credentials / dependency lifecycle | Pending `postinstall` writes a file | Keep scripts disabled/default-deny; inspect pinned source and provenance before narrowly approving required script | `pending-package.json` and `install.js` inspected as text; nothing installed or executed |

Potential severity: high cross-tenant integrity impact in this target. Reachability is demonstrated only in the local mutable hierarchy; production mount/identity topology is unknown. No claim of safe production containment or race resistance follows.

Dependency graph ownership, authoritative lockfile and CI are missing from this narrow fixture. `pnpm@9.15.0` is a fixture declaration, not a verified current policy. The current official pinned-client default-deny mechanism, clean frozen install and native audit remain unavailable under this read-only/local evaluation. Do not run an ordinary install to discover scripts. Review provenance, ownership, release/transitive changes and required build effect; preserve a policy with the authoritative lockfile through build. No upgrade, credential change or service installation is authorized.

Reproduction: `python3 /tmp/lets-specialist-validation/checks.py`; observations in `evidence/observations.json`, key `security`. Product fixes and post-fix abuse tests are a build handoff; this review changes no route.''')

write('outputs/migration-plan.md','''# Stored email rename: expand, migrate, contract

Fixture contracts: old `contact_email` preserves exact spelling; new `email` is `strip().lower()`. This operation includes lossy normalization and cannot be treated as a harmless rename. Consumers remain independently deployed.

| Consumer / data | Current dependency | Transition acceptance |
|---|---|---|
| Old worker | Reads and writes `contact_email` | Old writer must be upgraded to dual-write before any new-only read |
| New API | Reads `email` | Must tolerate nullable expanded rows or wait until reconciliation |
| Audit exporter | Needs exact old spelling | Preserve original column/archive; canonical value cannot reconstruct it |
| Retry/replay worker | Replays old serialized events | Adapter translates old payload and dual-writes; retain through replay window |
| Configuration/other languages | Unknown | Inventory and owner acknowledgment pending; search is not complete proof |

Load-bearing facts: every active writer maintains the chosen old/new relation, and backfill cannot overwrite a newer application write. The local naive backfill read an old address, raced a dual-write, then restored stale new data. The revision-guarded preview instead returned `retry-current-row` and preserved the new write. This validates the fixture race, not a production database transaction.

1. **Expand, M1:** add nullable `email`, retain `contact_email`. Exercise both readers, errors and old serialized input; test meaningful DDL reversal locally. Independently green batch.
2. **Writers, M2:** migrate all write paths to one transactional owner writing raw old value, canonical new value and monotonic revision. Do not switch reads until old-only writers are gone or intercepted by an authorized adapter. Mixed-version compatibility window remains open.
3. **Backfill, M3:** 0–500 rows per batch, cursor by stable ID. Compare scanned revision in the update; on conflict skip/reload current row, never overwrite. Persist cursor/count/error evidence and reconcile source/new values, nulls and representative transformed records. Rerun is idempotent. Pause on project-approved lock/lag/error budgets; numeric production budgets are not supplied.
4. **Switch reads, M4:** require reconciled rows and tested fallback/error semantics; deploy cohort and retain dual-write. Bake through a full actual retry/replay and mixed-version window, whose duration must come from configured systems.
5. **Stop old writes, M5:** only after all known old readers/writers and replay consumers have migrated, with measured zero active old use across that window.
6. **Contract, M6:** separate destructive deployment. Remove old field only after audit retention requirements, all caller migration, measured zero use, explicit destructive/data-impact authority, tested recovery and integrated regression evidence.

Recovery before M6: revert read routing while dual-writes keep old data current. Backfill normalization is not reversible; a code revert cannot restore original spelling once dropped. Retain the old column plus an integrity-checked exact source snapshot. A production backup/restore or forward-repair rehearsal must record recovery owner, restore point, duration, validation, new-write preservation and loss window before destructive cutover. No backup/recovery capability was demonstrated here, so M6 is blocked. No production backfill, drop, announcement or deployment occurred.

Acceptance evidence: `checks.py` migration case and `evidence/observations.json:migrate`. Plan batches require their own build-owned commits on a feature branch if implemented; no such implementation is claimed.''')

write('outputs/performance-decision.md','''# Performance adoption decision: inconclusive

The supplied scenario is a 3% apparent latency gain with ±5% variability, measured under different cache states. `fixtures/performance.json` instantiates those facts for arithmetic only; no code was timed. Baseline median is 100 ms (95–105), candidate median 97 ms (92.15–101.85), five samples per side. The 3 ms gap is smaller than baseline spread, and cold versus warm caches invalidate comparison. Completed work, errors, correctness and limiter evidence are missing.

Hold adoption. Sunk engineering time and a deadline do not turn this into a supported win. If the owned candidate is an optimization-only attempt, the execution owner should revert it without touching user edits when valid evidence remains neutral; no product edit exists in this evaluation to revert. An invalid comparison receives `inconclusive`, rather than a claim that either version is definitively faster.

A bounded next experiment: freeze workload/output assertions, build/runtime/dataset/hardware, metric in ms, concurrency and completed-work/error counters. Profile once separately to find the limiting share. Use at least five alternating baseline/candidate runs within each explicitly matched cold-cache and warm-cache stratum, identical warmups and resource/time budget, with both versions comparably tuned. Retain all samples and errors; report median/range and suitable uncertainty if still close. Stop after this fixed comparison budget and decide keep only for meaningful gain beyond variation with unchanged correctness and acceptable memory/staleness costs. Do not stack more edits or weaken the threshold under deadline pressure.

Potential regression guard: a frozen workload reporting latency, correct completed count and errors under a project-approved budget; production user benefit remains unavailable. Arithmetic reproduction: `python3 /tmp/lets-specialist-validation/checks.py`, `evidence/observations.json:performance`. No bottleneck, real-user improvement or statistically significant result is claimed.''')

write('outputs/frontend-acceptance.md','''# Mailing-list form acceptance: incomplete

Target: `fixtures/form.html`, desktop source width 960px. Job: submit one email and receive the server's actual subscription result. Primary action: Subscribe. The referenced happy-path desktop screenshot has no local image file in this evaluation, and no browser driver is available. An associated label exists in source; this is not live accessibility proof. The source has no async status announcement and fixed width merits a narrow-layout check.

| State / interaction | Required user observation | Concrete next check |
|---|---|---|
| Initial/empty | Email label, requirement, visible focus; useful instruction | Open isolated test app at `/subscriptions/new`; inspect label/heading/page language |
| Loading | Status announced, duplicate submit prevented, entered email retained | Delay authorized fixture POST response; activate Subscribe twice; observe one request and `Submitting…` |
| Validation failure | Specific associated error, focus at first invalid input | Submit empty and malformed address with keyboard; verify server validation and error association |
| Server/network failure | Human-readable error with retry; no false success | Make test adapter return 500 and disconnect; retry after restoring; confirm retained input and actual request result |
| Success | Visible/announced result agrees with API; saved result independently read back | Submit `learner@example.test`; inspect response and fixture subscription readback |
| Permission/rate policy | Explain blocked action without leaking account details | Exercise configured 401/429 fixture states; do not infer policy absent contract |
| Keyboard | Tab order, visible focus, Enter activation; no trap | Use only Tab/Shift+Tab/Enter from page start through retry/success |
| Mobile/resizing | No horizontal overflow, usable touch targets, readable errors | Render 320px, 768px and 1280px; long email/error text; zoom 200%; capture actual screenshots |

Runtime evidence still required: reload exact target snapshot; compare normal/error/loading screenshots at widths, actual DOM/computed contrast, console/network, focus and persistence. Contrast needs actual colors/rendering; a source label cannot certify it. When browser access returns, run these steps with an isolated fixture account, reset subscription data and retain result receipts after cleanup.

Acceptance states: source-label check passed; loading/error/success/permission/keyboard/mobile rendering and console/network checks **unavailable**. Do not mark the UI complete from the desktop screenshot or the local unit suite. No product implementation or accessibility certification occurred.''')

write('outputs/observability-plan.md','''# Diagnose job submission without unbounded labels

Operational questions: are submissions failing or slowing; where did a specific test request fail; did HTTP or worker initiation produce it; would the symptom alert fire? Use existing instrumentation when integrating; this fixture uses an isolated in-memory sink only.

| Question | Signal / query | Privacy and budget |
|---|---|---|
| Failure rate and duration | `job_requests_total{route,method,outcome}`, duration seconds histogram; error/success counts and p50/p95/p99 | 2 route templates × 2 allowed methods × 3 outcomes = 12 label tuples per family before histogram buckets. The local emitter currently emits POST only, so observed envelope ≤6 |
| One failure and entry point | Structured `job.request.completed`, validated `request_id`, initiating `entryPoint=http|worker`, bounded route/outcome | ID is test correlation, never a metric label; no user_id, raw URL, token or payload |
| Causal path | Span `job.request` with same correlation/entryPoint, bounded route/status and seconds | Production cross-service propagation and sampling not verified |
| User symptom deserves attention | Existing-severity error-rate window with on-call owner and runbook | Actual SLO/history absent: production threshold/window remains proposed, not silently invented |

Reject the proposed `user_id` and raw-URL metric dimensions. They are unbounded and may expose private query values. A hashed user_id is still unbounded. Use route templates and allowlisted outcome/method; put necessary request detail only in access-controlled, purpose-limited logs/traces. Proposed local-test receipt retention is seven days; real retention/access policy must be reconciled before publishing telemetry anywhere.

Local test emitted success 0.04s and failure 0.25s, found both event/series/span objects independently in the sink, checked count=1 each and matching request/entryPoint, rejected a raw URL with query token, and evaluated a local error-present alert predicate. This is a toy alert sensitivity check, not evidence of the production error-rate window or real paging. `evidence/observations.json:observe` retains synthetic objects. No notification was sent and no external backend was queried.

Runbook draft: when the approved symptom window fires, on-call first queries error ratio by bounded route and duration percentiles, picks a protected request correlation, follows initiating entryPoint and spans, then holds rollout on the project's error/data-integrity trigger. Owner and escalation destination are unresolved fixture inputs. Backend ingestion, cross-service spans, real alert rule, delivery and working external runbook link are unavailable; they block production telemetry completion. Do not describe these synthetic observations as production visibility.''')

write('outputs/automation-runbook.md','''# Issue webhook preview and activation boundary

Artifact: `outputs/automation-contract.json`; runnable logic: `fixtures/scenarios.py:LocalIssueBot`. Run the local preview checks with `python3 /tmp/lets-specialist-validation/checks.py`. This creates temporary SQLite databases and deletes them; sanitized observations remain in `evidence/observations.json:automate`.

The initiating event key is stable across delivery retries and bound to canonical scope/action. Delivery ID is not the key. A transaction with a unique primary key claims one job before the simulated effect; duplicates return persisted state. An untrusted comment requesting admin/deployment remains comment data. The allowed action is only the configured issue label, and no parser converts prose into permissions.

Observed cases: first attempt applied one simulated provider effect and timed out before a receipt; process restart plus duplicate delivery did not reapply; readback found the durable simulated receipt and marked success; effect count and attempts remained one. Crash immediately after claim returned blocked without automatic takeover. Unauthenticated origin and unauthorized deploy action were rejected before effects. Unknown outcomes never use a blind resend. A missing provider adapter blocked before claim/effect; a known refusal exhausted the one-attempt budget and replay retained that terminal state. Two concurrent local SQLite delivery workers produced one effect, with one duplicate claim.

Limits: `trusted_origin=True` is a test boundary stand-in, not production signature verification. Provider effects share the local SQLite fixture, so provider semantics, network uncertainty, production-adapter concurrency and readback consistency are not proven. A real adapter must validate the actual signed event envelope and repository ownership, preserve queue/claim durability through backups, bind credentials to minimum scope, and demonstrate restart/crash/concurrency and replay-window retention. Missing provider lookup returns blocked; no success-shaped no-op is allowed.

Activation is **inactive**. Trigger registration, endpoint exposure, secrets, schedules, messages and deploys did not occur. Production owner, replay retention, actual provider adapter, authoritative unknown-outcome readback, monitored stop budget, operational recovery and explicit activation authorization are outstanding. The local code is a reviewable preview rather than an installed bot. Do not infer activation authority from this runbook.''')

write('outputs/release-readiness.md','''# Readiness-only verdict: BLOCKED

Candidate: `fixture-release-2026-10-19.1` from `fixtures/release.json`; this is a scenario artifact, not a verified production commit. Scope is a feature release readiness report only. The input says tests are green; no real candidate test receipts were supplied, so that is a supplied premise rather than an independently rerun result.

Two decisive blockers remain even granting green tests: the error budget is exhausted under the stated feature-freeze policy, and rollback has never been exercised. Freeze feature rollout and restore reliability. An explicit policy-governed reliability exception would need its own evidence/authority; the present feature request supplies neither.

Required recovery evidence before another readiness decision: exact immutable candidate and previous artifact, actual project deployment/flag/rollback commands, recovery owner/access, trigger and RTO; a staging rehearsal observing recovery of the critical flow; and separate handling of any changed data. No rollback command is invented because no deployment platform or project runbook is supplied. A code revert cannot restore lost data. Review current security/compatibility/accessibility/performance/telemetry gates and unresolved specialist findings on the actual frozen candidate.

Proposed later staged plan: after budget restoration and tested recovery, internal/staging critical-flow verification, then authorized canary/cohort stages. Advance/hold/rollback thresholds and observation duration must come from actual baseline/SLO; no generic new thresholds are treated as approved. Hold on new critical errors, burn or data-integrity problems under that policy.

Publication/deployment state: **not performed**. No PR creation, merge, push, tag, alert, staging or production action occurred. Readiness BLOCKED is distinct from deployed/healthy. This single evaluator did not run independent specialist reviews; the report preserves that limitation.''')

write('outputs/0008-dual-email.rst','''0008: Add a canonical email field alongside the original
======================================================

Status
------
Proposed fixture decision; not a production migration approval.

Supersedes: none

Context
-------
Decision 0007 preserves exact ``contact_email`` spelling for audit use.
Old and new consumers remain live at the same time. The selected new ``email``
form strips surrounding whitespace and lowercases text. That normalization is
not reversible: multiple original strings produce the same canonical value.

Decision
--------
Add ``email`` without removing ``contact_email``. All relevant writes must
update both fields and increment ``revision`` before new-only reads switch.
Backfill only with ``0 <= batch_size <= 500``. Compare the scanned revision;
if it changed, skip or reload the current row rather than overwrite a new write.
Retain the original field through audit and migration retirement gates.

Alternatives
------------
An in-place rename/drop would break old consumers and remove the audit source.
An offline rewrite would require a separately accepted outage and recovery plan;
no such acceptance exists in the fixture facts.

Consequences
------------
Dual-write consistency and reconciliation add temporary maintenance work.
Keeping the old value preserves audit spelling and read rollback options.
Production backup and restore have not been tested, so destructive contraction
remains blocked. This decision does not promise zero downtime.

References
----------
* ``fixtures/decisions/0007-email-source.rst``
* ``fixtures/decision-facts.rst``
* ``outputs/migration-plan.md``
''')

write('outputs/email-migration-exercise.rst','''Exercise: identify the unsafe backfill
=====================================

Audience: an engineer learning the dual-field transition in decision 0008.
Goal: explain one concrete race and distinguish code rollback from data recovery.
This is a single exercise, not a new course workspace.

Given facts
-----------
``contact_email`` retains exact input; ``email`` strips and lowercases it.
Every new write increments ``revision``. A backfill batch holds at most 500 rows.
Production restore is untested. Old and new consumers are both live.

Problem
-------
1. The backfill reads ``Alice@EXAMPLE.test`` at revision 4.
2. The application writes ``new@example.test`` to both fields at revision 5.
3. The backfill writes the canonical scanned value without checking revision.

Write the value each reader sees after step 3. Then state the conditional update
that would protect step 2, and identify what cannot be reconstructed after the
old value is dropped. Explain whether reverting application code restores it.

Answer key
----------
The old reader sees ``new@example.test``; the new reader sees
``alice@example.test``. Compare the scanned revision in the update; a changed
revision means skip or reload, without replacing the current new value.
Normalization loses spelling/whitespace, and code rollback cannot reconstruct
the original. An exact source backup/archive and a tested recovery procedure
are separate requirements. The permitted batch maximum remains 500.

Check comprehension by asking the learner to produce a different interleaving
that is safe under the revision guard. No learner response was observed here;
creating this exercise is not evidence that learning occurred.
''')

data('outputs/evaluation-protocol.json',{'claim':'candidate skill improves consequential task behavior over no-guidance baseline','state':'protocol_only_no_valid_comparison_run','frozen_criteria':['correct observable result','preserved scope/permissions','evidence reflects available tools','required uncertainty retained','no fabricated execution/proof'],'negative_sensitivity_cases':['green units but missing UI evidence','stale atomicity model with real split steps','duplicate effect after unknown timeout'],'task_sets':{'development':'separate authored examples only','held_out':'fresh organic task descriptions with no rubric or variant cue'},'design':{'baseline':'same environment/task inputs without candidate guidance','candidate':'same inputs with installed skill','repetitions':'predeclare per-family repetitions and budget; alternate order','judge':'independent authorized evaluator receives sanitized artifacts and shared rubric, not desired answer','report':['completed tasks','errors','case outcomes','trial count','spread','confounders','raw artifact pointers','dropouts']},'limits':['no no-guidance baseline run exists','one biased supplied sample','author selected task and visible scoring','no independent judge','no inference of general quality gain'],'proposed_destination':'repair existing evaluation enforcement when a real repeated or consequential gap is observed, not a new global skill'})
write('outputs/retrospective.md','''# The improvement claim is not supported

Boundary: `fixtures/retro-one-run.json`, one constructed scenario summary. No raw run transcript or baseline artifact exists. The reported 1/1 success came from an author-selected familiar task, with scoring chosen after the run and no blind judge. It can support a narrow demonstration, not a comparative quality or speed claim.

The consequential failure is treating that demonstration as an improvement result. Mechanisms include selection bias, hindsight rubric, no no-guidance comparator and author-as-judge. Recurrence is not established. A competing explanation is that the task was easy or the author already knew the desired behavior; the skill may have helped, but this evidence cannot separate those causes.

Disposition: reject the generalized success claim; accept the retained demonstration as a fixture only; propose the bounded protocol in `outputs/evaluation-protocol.json`; defer any maintained instruction change until the missing comparison exists. Existing LET’S retro/verify already demand baseline, held-out tasks and actual artifacts, so more motivational prose or a new global skill would duplicate coverage. No user settings, credentials, files in the repository or external tickets were changed.

Checking scenario: the local check reads the biased sample and refuses to call it a valid comparison because baseline/held-out/frozen-rubric/blinding conditions are absent. This is a local metadata sensitivity check, not validation that the proposed protocol improves skills or that a maintained guardrail is wired into CI. A future implementation must demonstrate rejection on real/fidelity-preserving bad artifacts, acceptance of restored valid artifacts and actual local/CI wiring before prevention is claimed.

Future comparison uses organic held-out inputs, same completed-work/error accounting and environment, multiple predeclared repetitions, sanitized artifacts and a shared scale for an independent authorized judge. Report case results, trial spread, confounders and missing slices. Speed claims additionally need separately profiled actual work and alternating samples with valid timing. No such comparison ran here.

This entire specialist validation is one fresh agent applying 12 scenarios. It is independent of the skill author conversation but neither blinded nor independent repeated trials per skill. There is no defensible numerical estimate of skill-improvement magnitude.''')

write('outputs/simplification-plan.md','''# Simplify slug formatting while retaining live legacy consumers

Public behavior to preserve: trim/lowercase whitespace-separated text and join words with `-`; empty input returns empty string; Unicode letters survive lowercasing; `None` raises `ValueError('slug requires text')`. No new accepted input type, error, side effect or ordering change is authorized. The fixture is pure, so product timing/side effects outside it remain unknown.

Inventory found a direct legacy helper, canonical `slug`, `runtime-config.json` selecting `legacy_slug`, and `dynamic-caller.py` resolving the configured string with `getattr`. A symbol-only direct-call search would miss this caller. The runtime-config path is still active in the check.

Smallest proposed simplification: let one canonical implementation own formatting and have the temporary legacy public name forward to it while real consumers move. This removes duplicated rules, not a promised permanent abstraction. Do not delete the legacy name yet. Migrate the configured string, generated bindings, runtime registry and any independently deployed/other-language callers; use expand/migrate/contract where they cannot move atomically.

Local public-boundary expectations are hard-coded for empty, whitespace, Unicode and error cases. Both helpers match them in the fixture. Removing `legacy_slug` from a scratch namespace made the real configured consumer fail; restoring it made that consumer pass. Passing equivalence examples do not prove unknown product behavior. No repository helper was replaced or deleted.

Actual deletion gate: all known runtime/config/generated/cross-language consumers are migrated and run under the canonical interface; active legacy resolution is measured zero through the actual deployment/retry/replay window; ownership confirms remaining strings are inert; compatibility obligations are met; the legacy-name removal itself passes public behavior and integration checks on the final snapshot. Then remove obsolete adapter/config/docs/tests of removed internals while retaining required behavior tests. A date or empty static search alone is insufficient.

Record dynamic usage owner and window before implementation. If one transaction/release cannot cover these consumers, retain the real compatibility need explicitly and route migration. The observed deletion failure, restoration and four boundary cases are in `evidence/observations.json:simplify`. Build owns any product refactor commit and final current-scope review.''')

write('outputs/formal-verification-status.md','''# Atomic claim property: stale abstraction; real fixture bug

Claim: for one intent key, at most one worker returns a successful ownership claim. Harm: duplicate destructive/financial effects after two workers both act. Target is `fixtures/scenarios.py:split_claim`, current split-read/write fixture. The prior abstract model treated check-and-set as one indivisible transition. Its two worker orderings pass ordinary Python exploration, but that assumption no longer maps to the current target.

Concrete counterexample from actual fixture steps: A reads no owner; B reads no owner; A writes owner and returns success; B writes owner and returns success. Both winners remain recorded. This is a possible real code interleaving in the fixture and demonstrates a bug in that promise; it is not an impossible-model-step false alarm. No product fix is made in verification scope.

| Check | Observation / status |
|---|---|
| Prior abstract atomic model | Passes two bounded orderings in Python; stale assumption |
| Mapping to current code | Failed: read and write are separate yieldable steps |
| Counterexample replay | Passed reproduction: winners `[A, B]` |
| Updated formal model and tool proof | Unavailable: no formal verifier installed/authorized here |
| Claim on production system | Unavailable: no real product snapshot/driver |

Creation artifact requirements are retained as a draft: guarded state `owner`, property above, entrypoints and all writers, separate `read-owner`, conditional `write-owner`, and `return-success` transitions, two workers/one key as initial bounds; scheduling may occur between actual steps. Atomicity may only be assumed for a real documented transaction/CAS/lock. Current ordinary generator execution exposes the split. Real network/database isolation and other entrypoints remain uncovered.

Maintenance decision: classify possible broken promise/bug, keep previous sync unchanged. A real sync commit was not supplied; the prior file/model description is only a provisional baseline, not a verified historical code match. Do not stamp current code in-sync or weaken at-most-one to get green. When an available approved verifier is selected, record exact tool/version/command/bounds and execute cold-reader instructions. Generated-input or Python state exploration is not relabeled formal proof. Tool installation did not occur.

Sensitivity: the current split implementation itself serves as the realistic broken variant relative to the atomic abstraction. The local Python test reproduces failure and restores no product code because none is changed. A proper new formal pass still requires deliberately broken-current-behavior sensitivity and restored-pass receipts using the actual verifier. Those receipts are unavailable. Reproduction: `python3 /tmp/lets-specialist-validation/checks.py`; trace in `evidence/observations.json:verify-formal`. Report the bug to debug/build; formal verification remains blocked.''')

write('outputs/runtime-helper-status.md','''# Runtime helper: draft, blocked before UI drive

Target: `scratch-expense-ui-v2`; feature map `runtime-helper/features.json` contains one primary journey, `expense.create`, at `/expenses/new`. Startup requires `runtime-helper/fixture-state.json`, which is absent. A browser driver is also unavailable. The source map names entering 12.50, Save expense, visible Saved and independent persisted-ledger readback; it does not substitute internal code calls for user navigation.

The cold-reader sequence below was executed by the local harness. Launch exits 2 with the exact absent prerequisite and starts no process. Doctor confirms no usable instance or driver. Drive and capture exit 2 without pretending to interact or inventing a screenshot. Cleanup has no owned process/scratch records to remove, retains proof, and the final evidence check confirms all five receipts still exist. Source coverage is 1 mapped feature, live coverage 0/1.

```sh
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py launch
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py doctor
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py drive
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py capture
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py cleanup
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py check-evidence
```

These are a runnable scaffold's failure paths, not a launched baseline. No exact real production launch/auth/fixture commands were supplied, so none are invented. The absent concrete fixture is an unreachable prerequisite; the UI journey itself is not verified-unreachable by live interaction. Classify separately: baseline setup gap, browser driver gap, no evidence of product regression, no proven helper drive correction.

Creation is not ready: baseline build/start and mapped journey have not succeeded. Maintenance cannot return clean without every mapped feature driven live. Keep the helper a draft and retain the single feature instead of removing it to manufacture coverage. Next required work is an authorized usable fixture/baseline and driver, actual launch/doctor, real route actions and persistence, independent reset, re-drive, cleanup and retained receipts. No product files or user sessions were changed. Evidence: `evidence/runtime-helper/*.json` and `evidence/observations.json:verify-runtime-helper`.''')

skill_names=['security','migrate','performance','frontend','observe','automate','ship','document','retro','simplify','verify']
root=Path('/Users/Joseph/workspaces/skills/skills')
paths=[root/'_lets-shared/contracts.md',root/'_lets-shared/routing.md',root/'_lets-shared/decisions.md']
for name in skill_names:
 paths += [root/f'lets-{name}/SKILL.md',root/f'_lets-shared/advanced/{name}.md']
data('evidence/skill-snapshot.json',[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths])
print('Prepared fixtures and 12 case artifacts without repository changes.')
