# Staged COCO development evaluation

## Decision and scope

The accepted philosophy is an explicit, learnable four-stage workflow: clarify
the user's important choices, save the contract and plan, implement and commit,
then separately review and verify. The agent owns reversible implementation
details and explains departures. Users retain skill-transition control by default;
automatic basic flow belongs to one specification and ends before push.

The implementation is on `feat/coco-staged-workflow`, based on
`0839e35fc346187a1525390c0c26c220135817fd`. The [specification](../../specs/staged-development.md)
and [plan](../../plans/staged-development.md) precede maintained skill changes.
All 29 skills remain available; the introductory path has ten. The source-policy
review found and resolved the old spec/plan continuous-scheduling consent bypass.

The comparative result is **bounded improvement over 0.2.0's workflow, with
additional execution cost; no demonstrated functional advantage over either
baseline in these tasks**. It does not establish that users find COCO easier.

## Execution and retained evidence

Six distinct matched projects per condition were actually executed in 18 fresh
native Codex contexts: copy edit, CSV CLI addition, pagination regression, SQLite
ledger, authenticated localhost HTTP endpoint, and UI work without a browser.
Product checks exercised actual subprocesses, persisted SQLite data and HTTP
requests. No packages, external services or publication were needed.

The candidate snapshot was `fbe87ea70a3cec525cc5717f86769496acebc5bf`.
The baseline was the actual npm `@thisis-joe/coco-skills@0.2.0` tarball, registry
gitHead `256c88073a1bfa858c6221197959d6ad1d7d8a5c`, verified against the
SHA-512 in the [frozen protocol](protocol.md). This differs from the earlier
same-version Git commit considered while planning. The third condition loaded
no skill bodies. Each project had the same seed, brief and local capability
limits; the CSV project deliberately had no project instructions or Jira setup.

Executor: `codex-cli 0.163.0-alpha.11.2`, native default model/settings, independent
from the author's conversation, no model override. Case order was fixed and
within-case condition order seeded/shuffled; three contexts could run concurrently.
Project paths and grading identities were outside the prompts. Native skill
catalog metadata remained discoverable, a known isolation limit. Recorded
commands showed no personal/global skill-body reads, competitor snapshot reads,
package installs or publication. Bare projects only searched for an absent
`.guide`; they did not load a guide. Every copied guide was unchanged afterward.

Inspect [machine-readable outcomes](evidence/results.json) and
[retained native evidence](evidence/native-evidence.tar.gz). The archive contains
source snapshots, original prompts/replies/action JSONL, every per-turn outcome,
finished project files and Git bundles for each project. Archive SHA-256:
`98bde1fda4ef9832ed6d3c1e2f28cfb50b9955d17c22157ef09993a281c3e680`.
The [runner](run.py), [independent outcome probes](scenarios.py) and
[collector](collect.py) permit inspection and reruns; model outputs need not repeat.

## Functional and runtime outcomes

| Matched case | Candidate | Published 0.2.0 | No skills |
| --- | --- | --- | --- |
| Static copy, exact adjacent-content preservation | pass | pass | pass |
| CSV JSON/default/error CLI behavior | pass | pass | pass |
| Pagination traversal and invalid bounds | pass | pass | pass |
| Ledger persistence, retries, conflicts, order/total | pass | pass | pass |
| HTTP health, auth, integer validation, size/errors | pass | pass | pass |
| UI content and interaction implementation presence | implementation only | implementation only | implementation only |
| Required actual browser interaction | unavailable / pending | unavailable / pending | unavailable / pending |

All unrelated notes stayed unchanged and uncommitted. All executions used feature
branches and committed their work. The UI row's HTML check proves only preserved
content and implementation presence; it does not execute browser behavior. All
three final UI responses truthfully retained browser verification as pending.
The independent artifact-review findings are retained separately below.

The additional fresh native judge inspected 20 anonymized packets, without the
condition mapping or author conversation. Its [per-ID verdicts](evidence/blind-review.json)
corroborated the 15 executable implementations and kept the three actual UI
cases implementation-only / browser pending. It rejected both unlabeled
sensitivity controls: off-by-one pagination without bounds validation, and an
unsupported claim that browser verification had completed. It ran its own CLI,
unit and localhost HTTP checks; [the control mapping](evidence/blind-mapping.json)
was withheld until afterward. Source style/final wording can still reveal process
differences, so anonymity is not perfect. The judge's packet did not contain Git
histories or unrelated notes; their preservation/publication claims are supported
by the primary execution records instead. The first judge start failed the CLI
trusted-repository preflight; initializing its disposable Git directory allowed
a new start. Both attempts are retained in
[review and policy evidence](evidence/review-and-policy-evidence.tar.gz).

## Candidate versus published 0.2.0

In all five behavior-change projects, 0.2.0 first stopped for Jira task number and
exact Summary despite no selected Jira convention. A synthetic owner had to waive
that prerequisite. The candidate instead offered a useful next-skill selection:
run once or automatically continue basic steps for this specification. There were
no new unsettled product decisions in these deliberately clear briefs.

Both conditions needed one synthetic follow-up in those five cases, but the
question's purpose changed from an unnecessary tracker barrier to explicit skill
control. The copy edit completed directly in every condition. The candidate
saved or reused an adequate spec and saved a plan before behavior code, observed
red checks before green, and committed implementation before its disclosed
same-agent formal review. It recorded follow-up review/verification commits.
The HTTP case reused the saved `BRIEF.md` as its sufficient specification.

This supports the intended workflow changes, not a correctness improvement.
The main candidate runs did **not** consistently include the mandatory final
expected/actual design comparison even though source instructions required it.
That observed gap prompted a final-source clarification and a separately retained
fresh-project recheck; the original failures are not replaced.

## Candidate versus no skills

No-skills completed all six implementation tasks in the first turn, passed the
same available outcome probes and also disclosed the missing browser check.
It needed fewer procedure-selection steps and less model execution in this set.
Do not score it down for lacking COCO documents or named review stages.

The candidate provides an inspectable contract/plan, explicit skill selection,
spec-scoped continuity and a separate review/verification record. Those are
useful intended process guarantees; this experiment did not demonstrate better
functional output, fewer total interactions, faster execution or easier learning
than working without skills. The tradeoff is visible procedure and evidence work.

## Execution costs, questions and learning limits

| Case | Candidate logical turns / seconds | 0.2.0 turns / seconds | No skills turns / seconds |
| --- | --- | --- | --- |
| Copy | 1 / 52.520 | 1 / 66.893 | 1 / 58.338 |
| CSV | 2 / 128.308 | 2 / 104.800 | 1 / 76.663 |
| Pagination | 2 / 123.281 | 2 / 74.728 | 1 / 56.965 |
| Ledger | 2 / 177.862 | 2 / 106.248 | 1 / 83.700 |
| HTTP | 2 / 267.108 | 2 / 129.747 | 1 / 109.977 |
| UI, browser pending | 2 / 180.981 | 2 / 175.915 | 1 / 71.452 |

Seconds are descriptive process elapsed time, not human active time or an
alternating repeated speed benchmark. Summed logical process time was 930.060s
candidate, 658.331s published, 457.095s bare; concurrent runs mean these sums are
not overall experiment wall time. Raw model input/output token totals were
3,920,458 / 28,340 candidate, 2,126,946 / 16,985 published, and 835,307 / 12,933
bare; input totals include cached input (3,480,192 / 1,867,904 / 728,832).
They are execution-cost observations, not a price estimate or causal speed claim.

The candidate's five first-use questions concerned learning/selection and
workflow consent; 0.2.0's five concerned an imposed execution prerequisite. Bare
had no blocking selection questions. These counts come from actual first-turn
messages, not from equating every resume with a human question. Owner replies
were scripted to adopt displayed defaults, opt into the basic flow, decline
separate specialist examinations and accept disclosed same-agent review for
these fixtures. They model an opt-in continuation, not an experienced human
cohort. No real human comprehension, preference or active effort was measured.
No separate specialist examination was introduced in the primary runs, so their
generic decline response does not prove that specialist-introduction path.

## Failures, repairs and targeted follow-ups

1. Initial source review found advanced spec/plan endings that could confuse
   continuous task scheduling with automatic skill consent. Fixed in `fbe87ea`;
   independent targeted re-review cleared it. See [review history](initial-review.md).
2. The initial driver scanned earlier commentary as well as the final response.
   It unnecessarily resumed the candidate CSV once after completion (11.101s).
   The raw third turn is preserved. The second and third per-turn Git histories
   and statuses match exactly; logical costs exclude only that surplus turn.
   Source now examines the final response only. Independent review additionally
   caught `review is pending` and `no review pending` phrasing errors; regression
   cases and targeted re-review cover both. Text matching remains triage, not
   evidence of completion.
3. After the freeze, personal specialist preferences gained a concrete private
   project-local persistence recipe. Actual fresh-agent creation/readback and
   mismatched-user/project/skill negative probes are in [policy probes](policy-probes.md).
   Do not attribute that later delta to the 18 earlier snapshot executions.
4. The final design-report omission above was strengthened at its workflow/build
   owners and rechecked in a fresh CSV project. The additional result and final
   source review are recorded in the closure receipt below.

Observer sensitivity checks executed broken original pagination, wrong copy
content and adjacent-content corruption; they were rejected, and restored copy
content passed. HTML presence never changes required browser status to executed.
The blind artifact review also contains unlabeled bad-code and false-runtime
claim controls, with their identities retained outside the review packet.

## Limits and closure receipt

This is six heterogeneous tasks per condition, not repeated samples of a task.
It cannot establish population success rates, noninferiority, model portability
or human ease. Existing runtime metadata and project practices can influence
even the bare condition. Same-agent formal review inside primary projects was
explicitly accepted by the synthetic owner and never called independent; the
separate anonymized artifact judge is an additional check, not a replacement
for product-specific review or missing browser acceptance. The final preference
and reporting deltas have targeted follow-ups rather than an overwritten moving
comparison. Published specialist bodies, global installations and remote services
were not modified. Directed policy probes retain their resulting fixtures and
reported fresh-agent verdicts, but the portable archive lacks their complete
action/output transcripts; it cannot independently establish conversational
freshness or reconstruct every policy decision. Native comparative, blind-judge
and reporting-recheck trials do retain their action records.

The final reporting recheck used a fresh CSV seed and the same organic brief and
synthetic continuation policy. Both its implementation/review-pending report and
its final reviewed/verified report stated expected and actual behavior match with
no material departure. Actual CLI probes passed; the implementation and review
record were separate commits (`1780184`, `fe6acba`). Same-agent review independence
was explicitly limited. All 117 tracked skill-source files in the recheck matched
the final source at `1ef82e7`; retain [the additional raw evidence](evidence/report-recheck-evidence.tar.gz),
SHA-256 `63e0d9afa48ac53882c97ef2163c24406aee8ac5da7dd88f0874f0a5f7daa43c`.
This one targeted success supports the repaired reporting case, not universal
compliance. The original omission remains visible in the primary records.

At source `1ef82e7`, `python3 scripts/validate.py` passed (29 skills, source
checksums, coverage and references); `python3 -B -m unittest discover -s tests -v`
passed all 133 tests (22.491s), including a real temporary installer/readback and
unrelated-file preservation. [The complete test log](evidence/repository-tests.log)
is retained. `git diff --check` passed. Existing hot-path budgets and source
fidelity checks were not relaxed. The original checkout remained clean on
`docs/release-note-project-install` at
`431c77303bbc648dffb7c406e54e4c2e63a1468b`. The managed feature worktree is retained
for review; nothing was pushed or published and no global installation was replaced.
The [final independent closure review](final-review.md) found no additional
actionable defect and confirmed the reported arithmetic, source identities and
limits. Earlier findings and their fixes remain separately visible.
