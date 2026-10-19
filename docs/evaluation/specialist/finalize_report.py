from pathlib import Path
import hashlib
import json
import platform
from datetime import datetime, timezone

b=Path('/tmp/lets-specialist-validation')
command='python3 /tmp/lets-specialist-validation/checks.py'
summary=json.loads((b/'evidence/check-summary.json').read_text())
def case(name,skill,status,output,observed,target_status,ambiguity):
 return {'case':name,'skill':skill,'status':status,
         'evidence':{'artifact':str(b/'outputs'/output),'observations':str(b/'evidence/observations.json'),
                     'observation_key':name,'command':command,'exit':0,
                     'check_receipt':str(b/'evidence/checks.stderr')},
         'observed_behavior':observed,'target_acceptance':target_status,'uncovered_ambiguity':ambiguity}
rows=[
 case('security','lets-security','passed','security-review.md',
 'Own-file positive control and A-shaped symlink attack both returned 204; the foreign victim was actually removed. Pending dependency script was inspected only as text; no install ran.',
 'Unsafe route: failed security promise. Dependency install/audit/current pinned-client policy: unavailable.',
 'Production hierarchy/owner binding/races, real lockfile root and official pinned-client policy were absent; no safety sign-off.'),
 case('migrate','lets-migrate','passed','migration-plan.md',
 'Concrete old/new consumer plan, bounded phases and destructive gate produced. Naive backfill overwrote a newer write; revision-guarded preview retained current data; normalization was non-injective.',
 'Local compatibility race reproduced; production adoption/restore/contract remain unproven and contraction blocked.',
 'Actual retry/replay duration, complete consumer set and backup restoration capability are unknown.'),
 case('performance','lets-performance','passed','performance-decision.md',
 'Computed 100ms versus 97ms medians from explicitly constructed scenario data and refused adoption because spread and cache mismatch invalidate inference, regardless of sunk cost.',
 'Performance gain inconclusive; no benchmark timed or bottleneck profiled.',
 'Within-noise revert guidance and invalid-comparison inconclusive guidance overlap; report selected inconclusive first and left any owned-edit disposition to execution owner.'),
 case('frontend','lets-frontend','inconclusive','frontend-acceptance.md',
 'Produced loading/error/keyboard/mobile state matrix and concrete next driver recipe. Only source-associated label was checked; no live browser claims made.',
 'Live required states and screenshot/console/network/focus evidence unavailable; UI completion withheld.',
 'The scenario references a desktop screenshot but provides no local pixels; it cannot be treated as an inspected visual artifact.'),
 case('observe','lets-observe','passed','observability-plan.md',
 'Rejected user_id/raw URL metric labels, bounded cardinality, emitted/found synthetic success and failure logs/series/spans, checked correlation and units, and exercised local alert predicate.',
 'Local telemetry check passed; backend ingestion, cross-service propagation and external delivery unavailable.',
 'Real SLO alert window, backend, on-call owner and retention policy not supplied; local alert sensitivity does not verify paging.'),
 case('automate','lets-automate','passed','automation-runbook.md',
 'Runnable SQLite preview atomically claimed intent, survived duplicate after timeout/restart with one effect, reconciled readback, rejected origin/action escalation, blocked missing adapter, retained exhausted budget, and handled concurrent local deliveries with one effect.',
 'Prepared local preview only; inactive with explicit activation requirements in automation-contract.json.',
 'trusted_origin is a stand-in, provider effect is local, and production signature/envelope/ownership/readback/concurrency/retention remain unverified.'),
 case('ship','lets-ship','passed','release-readiness.md',
 'Produced readiness-only BLOCKED report on exhausted budget and missing rollback test, preserving supplied green-test premise without inventing candidate receipts or deployment commands.',
 'Not ready; deployment/publication/PR actions not performed.',
 'No real immutable candidate or project rollback command was supplied; these remain unavailable rather than fabricated.'),
 case('document','lets-document','passed','0008-dual-email.rst',
 'Created numbered reStructuredText ADR and a separate teaching exercise, preserved existing decision file and facts (normalization loss, revision rule, 500-row maximum, untested recovery).',
 'Local ADR/exercise artifacts created; no production decision approval, publication or observed learner mastery.',
 'A course layout/linter was not supplied, so the unrelated conditional TypeScript recipe was not imposed.'),
 case('retro','lets-retro','passed','retrospective.md',
 'Rejected general improvement claim from one selected biased sample, retained it as a narrow demonstration, and produced protocol/limitations without new global instructions or external tickets.',
 'Skill-improvement comparison inconclusive; no no-guidance baseline, held-out repetitions or independent judge run.',
 'One consequential unsupported claim does not establish a recurring mistake; the local metadata gate is not an installed CI guardrail.'),
 case('simplify','lets-simplify','passed','simplification-plan.md',
 'Stated behavior and caller inventory including config/getattr. Hard-coded public expectations matched both fixture helpers; scratch legacy deletion broke the configured caller, and restoration passed.',
 'Legacy deletion blocked until all live callers and measured usage conditions hold; no product refactor performed.',
 'Finite fixture cases do not establish product-wide equivalence, actual external consumers or the required replay window.'),
 case('verify-formal','lets-verify (advanced formal creation/maintenance)','inconclusive','formal-verification-status.md',
 'Old atomic abstraction passed two Python orderings, but actual split-step fixture produced two successful workers. Reported stale mapping/bug, kept sync unchanged and refused formal-proof language.',
 'Fixture safety promise failed; formal verifier/tool proof unavailable. No tool installed and no product fix.',
 'No real sync commit/tool was provided; historical baseline is provisional and Python exploration is not formal verification.'),
 case('verify-runtime-helper','lets-verify (advanced helper creation/maintenance)','inconclusive','runtime-helper-status.md',
 'Executed launch/doctor/drive/capture/cleanup/evidence check. Launch failed on exact missing fixture; no actions/screenshot invented, 0/1 mapped journeys verified, all receipts survived cleanup.',
 'Helper draft blocked; baseline unusable and browser driver unavailable, so cannot return clean/ready.',
 'A concrete startup prerequisite is unreachable; no live journey evidence establishes product regression or UI verified-unreachable state.')
]
(b/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
metadata={'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'python_version':platform.python_version(),'command':command,'exit':0,
 'check_summary':summary,'scope':'single fresh agent applying 12 synthetic specialist scenarios',
 'independence':'no source audits/author conversation or expected-answer files read; no separate trials per skill; evaluator not blinded',
 'repository_mutations':False,'external_service_writes':False,'external_service_clis_or_installs':False}
(b/'evidence/run-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
manifest=[]
for path in sorted(b.rglob('*')):
 if path.is_file() and path.name!='artifact-manifest.json' and '__pycache__' not in path.parts:
  manifest.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
(b/'evidence/artifact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
lines=['# LET’S specialist behavioral application report','',
 'Twelve requested cases produced concrete local artifacts. Nine bounded applications passed their artifact/diagnosis check; three deliverables remain inconclusive because required browser/formal/runtime evidence is unavailable. The 15 local behavioral checks exited 0. Passing those checks includes observing unsafe fixture behavior; it does not mean the fixture targets are safe or production-ready.','',
 'This is one fresh agent applying the supplied scenarios, not independent repeated trials per skill. No no-guidance comparison, blinded judge, real browser run, formal verifier run, production telemetry/backend access, provider webhook delivery or deployment occurred. The evaluation therefore does not establish general skill effectiveness or a numerical improvement.','',
 'The only repository content read was selected `skills/lets-*/SKILL.md` and relevant `skills/_lets-shared` material. Active skill hashes are in [skill-snapshot.json]('+str(b/'evidence/skill-snapshot.json')+'). No repository/user-skill writes, external service writes, agents, dependency installs or external service CLIs were used. Disposable scratch is cleaned; retained artifacts are under this directory.','',
 '## Case outcomes','',
 '| Case | Status | Observed result | Concrete artifact |','|---|---|---|---|']
for row in rows:
 label=row['case']; artifact=row['evidence']['artifact']
 short={'security':'Cross-tenant delete observed; dependency execution gated.',
 'migrate':'Race reproduced; expand/migrate/contract and recovery gates retained.',
 'performance':'No supported gain; cache/noise confounding disclosed.',
 'frontend':'State/driver recipe supplied; live acceptance unavailable.',
 'observe':'Bounded schema plus local telemetry self-test; no production claim.',
 'automate':'Duplicate/timeout/restart/crash/concurrency checks; inactive artifact.',
 'ship':'Readiness blocked by exhausted budget and untested recovery.',
 'document':'Existing .rst ADR convention and facts preserved; exercise created.',
 'retro':'Biased success claim rejected; defensible comparison protocol created.',
 'simplify':'Dynamic configured caller blocks deletion; restoration observed.',
 'verify-formal':'Stale atomic model exposed actual double-winner trace; no formal proof.',
 'verify-runtime-helper':'Launch failure retained; 0/1 live mapped journeys; draft blocked.'}[label]
 lines.append(f"| {label} | {row['status']} | {short} | [{Path(artifact).name}]({artifact}) |")
lines += ['',
 'Additional artifacts: [automation trigger/claim/recovery/activation contract]('+str(b/'outputs/automation-contract.json')+'), [teaching exercise]('+str(b/'outputs/email-migration-exercise.rst')+'), [evaluation protocol]('+str(b/'outputs/evaluation-protocol.json')+'), [runtime feature map]('+str(b/'runtime-helper/features.json')+').','',
 '## Reproduce and inspect','',
 '```sh',command,'```','',
 'The harness uses Python standard-library fixtures only. It records 15 expectation checks, including the dangerous negative cases; it is not a substitute for required real-target project checks. See [check receipt]('+str(b/'evidence/checks.stderr')+'), [summary]('+str(b/'evidence/check-summary.json')+'), [observed values]('+str(b/'evidence/observations.json')+') and [runtime receipts]('+str(b/'evidence/runtime-helper/check-evidence.json')+'). The three unavailable deliverables are not converted to passing product acceptance by the green fixture suite.','',
 'Machine results: [results.json]('+str(b/'results.json')+'). Reproduction inputs: [preparation script]('+str(b/'prepare_artifacts.py')+') and [check harness]('+str(b/'checks.py')+'). [Run metadata]('+str(b/'evidence/run-metadata.json')+') identifies method and limits; [artifact manifest]('+str(b/'evidence/artifact-manifest.json')+') freezes file hashes.','',
 '## Contradictions, ambiguity and coverage limits','',
 'No forced unsafe action or direct contradiction among the selected active procedures was demonstrated in these bounded applications. No skill was edited to obtain a desired result. Three interpretation/availability edges remain visible:','',
 '- Performance says to revert neutral owned experiments and to report invalid comparisons as inconclusive. Because the cache mismatch invalidates this comparison before adoption analysis, the report returns inconclusive and leaves any actual owned-edit reversion to its execution owner. No edit was silently kept or reverted.',
 '- The common contract requires commits for product work completion, while verify/review return evidence and do not own product commits. This run delivers scratch review/evidence artifacts and makes no product-task done claim; no repository commit is fabricated.',
 '- The dependency gate needs current official pinned-client behavior, graph ownership and real lockfile/CI evidence, none of which this restricted fixture supplies. It blocks lifecycle execution rather than guessing a manager policy.',
 '',
 'Further gaps are listed per case in results.json: missing real consumer/usage windows, untested data recovery, no image pixels or UI driver, synthetic telemetry, provider boundary stand-ins and absent formal sync history. A local model/pass, source check or successful arithmetic calculation is never promoted to proof of unavailable real behavior. The ADR preserves uncertainty; the exercise does not claim demonstrated learning; the retrospective does not claim prevention from a proposed protocol.',
 '',
 'No author source audit, desired-answer document or hidden scoring source was consulted. Nonetheless this agent authored both scratch fixtures and checks from the scenario, so assertions are not independent blinded evidence, and small local fixtures cannot establish discovery performance on a full repository.']
(b/'report.md').write_text('\n'.join(lines)+'\n')
# Include final report in manifest after it exists.
manifest=[]
for path in sorted(b.rglob('*')):
 if path.is_file() and path.name!='artifact-manifest.json' and '__pycache__' not in path.parts:
  manifest.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
(b/'evidence/artifact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'passed':sum(r['status']=='passed' for r in rows),'inconclusive':sum(r['status']=='inconclusive' for r in rows),'checks':summary,'report':str(b/'report.md'),'results':str(b/'results.json')},indent=2))
