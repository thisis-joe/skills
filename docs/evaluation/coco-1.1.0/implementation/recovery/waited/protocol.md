# Waited recovery: preserve execution budgets while honoring provider cooldowns

This is a new prospective cohort authorized by the user's 2026-10-26 request to
wait and retry the full comparison. It does not waive the comparison, pool old
results, resume interrupted projects, replace poor outcomes or modify old evidence.
The same five matched policy profiles and two candidate-only preservation probes,
private facts, prompts, authority, exact-integer oracle and rubric are inherited
from [recovery](../protocol.md) and [revision 2](../revision2/protocol.md), except
for the explicitly replaced source and capacity policy below.

The current arm remains `622975e349e6276b225aa9ef02ee69d664dd2927`. The candidate is
the final release skill commit supplied by the owner after the Windows path fix;
its full commit and exact guide-file manifest must be frozen in control.json
before any development actor. The tagged 1.0.0 release remains a separate package
compatibility baseline. Preparation is twelve fresh projects, not twelve results.

## What the old capacity evidence actually says

The native command is `codex exec --ignore-user-config --approve-for-me --json`,
in the old cohort, using the unchanged repository native engine. Its stderr
reported HTTP `429 Too Many Requests`, then its own sampling retry after about
514 or 341 seconds. Those records do not identify an account quota versus service
capacity. The old 90-second classifier wall limit was shorter than these announced
waits. The previous stopped cohorts remain unavailable, not failures of the skills.

## Prospective call policy

- One admitted project and one native call at a time; at least 30 seconds between
  native call starts, equally for both arms and owner classifiers.
- Preserve the 420-second actor and 90-second classifier non-cooldown budgets.
  Parse only exact native stderr lines containing the UTC timestamp, the native
  sampling retry delay and `429 Too Many Requests`.
- Track the union of the provider-announced retry intervals, clipped to observed
  call time. Their elapsed overlap is a **cooldown estimate**, not measured model
  compute time. Subtract only this observed overlap when enforcing the original
  non-cooldown budgets. Never subtract intervals before their timestamp or after
  their announced end; overlapping/duplicate messages cannot double the credit.
- Permit at most 1,800 seconds of such cooldown credit per call. Independent hard
  wall limits are therefore 2,220 seconds for actors and 1,890 for classifiers.
  These operational allowances apply before outcomes to every arm, not selectively.
  Report full wall time, pacing, declared cooldown overlap and charged remainder
  separately. Do not infer performance improvement from the charged remainder.
- Across this one cohort, including native controls, permit at most 5,400 seconds
  (90 minutes) of cumulative cooldown credit. Retained per-call receipts carry this
  total across control/run process boundaries; reaching it stops admission without
  starting another cohort. Persist the last native start so the 30-second pacing
  also survives that intentional process boundary.
- Let the same native CLI process perform its built-in sampling retries. A 429
  alone does not cancel it. Do not create a substitute process, replay a product
  turn, supply extra owner answers or remove STOP records to obtain a success.
- Malformed/unrecognized cooldown messages provide no time credit. Other native
  failures, exhausted call budgets, uncertain process state or a final invalid owner
  classification stop new queue admission and remain visible. Preserve the inherited
  classifier's maximum two calls for JSON/schema repair; this is not a retry of a
  failed development actor. A cancelled CLI, malformed event stream or missing
  completed-turn event is invalid even when the original process exit is zero.
  Existing bounded
  owned-process cancellation is reused unchanged. No unsafe project is resumed.
- Per project retain five actor turns, three ordinary owner-answer rounds, one
  corrective reply and one no-facts continuation. Successful retry within the same
  process is one turn with its full event history, not another product opportunity.

This replaces revision 2's stop-on-any-429 and fixed wall-clock caps prospectively.
It does not make the old time/cost observations comparable. A native success after
cooldown must still pass ordinary process/event/instrument validity checks.

## Checks and execution

Before dispatch, freeze this addendum, adapter, cooldown regression tests, collector
adapter and all inherited runner/engine/oracle dependencies. Test that long valid
waits do not exhaust the shorter classifier budget, that overlapped waits do not
double-count, that processing after the wait still has the original cap, and that
malformed messages and excessive delays cannot remove the hard bound. Reuse the
strict-integer sensitivity code unchanged and rerun it against this adapter before
actors. A fresh native range-question control checks availability; the fresh
identity, public-contract and unknown-choice controls check owner routing. All
must pass before development actors. Availability is no promise of later capacity.

Retain every question, reply, delivery/settlement state, checkpoint, command,
public outcome, exit, usage record, cooldown and queue decision. Source manifests
and instrument hashes must remain frozen. Blind collection and independent grading
use the unchanged behavior rubric and two false-completion controls. No source
edit or product-quality failure is repaired inside this cohort. The root evaluates
actual results against the existing release gate; this protocol authorizes no
publication or global installation by experiment actors.

## Explicit model selection before the first native call

After this adapter was prepared but before any freeze or native call, the user
explicitly delegated appropriate model selection and excluded Luna. Both comparison
arms and all native owner controls/classifiers use **gpt-6.1-sol, high reasoning**.
The separate condition-blind reviewer uses the root-selected Astra/high reviewer.
This is not an outcome-driven model switch. All old unspecified-model records
remain unchanged and are not pooled with this cohort.

A local module-scoped Popen adapter injects `--model gpt-6.1-sol -c
model_reasoning_effort="high"` into the same native CLI: into `exec` for an initial call and into
`exec resume` for a resumed call, using each command's supported options. It does not edit the historical engine, bypass approvals, alter tools,
read other session contents or change actor prompts. The engine's actual argv
receipt contains these explicit options. Read only the returned thread's latest
`turn_context` model/effort fields timestamped within the current invocation's
started_at/finished_at window, and require the selected values after every
call, including resumed turns; missing/mismatching metadata is unavailable, not
assumed equivalent. Freeze this adapter and test first/resumed command binding.
