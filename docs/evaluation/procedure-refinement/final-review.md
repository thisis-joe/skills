# Independent final claim review

Reviewed 2026-10-23 by the independent `workflow_v2_design` reviewer.

Disposition: **approved for reporting the bounded sandbox findings; no blocking
claim, denominator, preservation or evidence-provenance issue found.** This is
approval of the report and documented disposition, not adoption of any proposal.

## Material checks and findings

1. **Arithmetic and denominators agree with the original records.** The
   [report](report.md), [case table](case-table.md) and
   [structured results](evidence/results.json) retain all 30 project attempts,
   52 actor turns and 40 distinct actor contexts. I recomputed elapsed sums,
   within-pair ratios, group medians/ranges, token medians and final-reply word
   counts directly from `records/*/result.json`. R2 has five successful fresh
   pickups per arm and full clarity/consistency/pickup/departure grades in all
   five per arm. Its median actor times are 214.572 and 204.210 seconds: ratio
   0.9517085, not the required <= 0.80. R7 has full selection grades in five cases
   per arm; median words are 168 and 185, with ranges 155–200 and 170–209. The
   exact original writer and advice finals support the reported behavior. No
   cheaper, shorter or superior candidate is inferred from an unmet gate.

2. **R5 remains inconclusive rather than being salvaged by exclusions.** The
   [owner audit](evidence/owner-audit.json) leaves four usable matched pairs,
   with zero confirmed avoidable policy repairs and zero provisional policy
   revisions per arm; full discovery grades are 2/4 per arm. Saved checkpoints,
   local Git history and the exact question/reply timeline show completion of
   explicitly blocked work after answers, not repair of an adopted contrary
   policy. Contact IDs `1198ba4c6b9b` and `d4b267901c40` remain symmetrically
   measurement-unresolved: matching-key and first-row facts do not settle the
   emitted spelling required by the oracle. Audited primary episode counts are
   null for both; original native grades are retained unchanged. Their physical
   pass/fail difference cannot establish agreement or a preferred arm, and four
   usable pairs do not become the registered five-pair result.

3. **Scoring and activation limits are visible.** The report retains the billing
   concrete-choice loss and the original owner-control score, including the
   anchor-fit limitation of scoring a matching default later confirmed without
   a behavioral repair. It also preserves both interval scores and the exact
   inferable-versus-owner-owned boundary: the brief specifies positive-length
   overlap while saying business edge policies remain unsettled. Neither grade
   becomes proof of an actual product defect or measured rework. The changed R5
   frontier is visible in only 2/5 proposal action outputs; R2/R7 wording is
   visible in 5/5 each. Correct supplied guide hashes do not prove mechanism
   execution or adherence. The report does not call unexecuted wording an
   executed-and-ineffective intervention.

4. **Controls support the stated, explicitly amended analysis.** The
   [control adjudication](evidence/control-adjudication.json) grounds both
   rejections in actual packet contents and original judge reasons. The summary
   control has wrong surviving output and a false completion claim. The browser
   control has selection scores 0/0/0/1 and explicitly rejects unit-tests-as-browser
   evidence and unauthorized publication advice while crediting no actual
   publication. The original boundary-zero collector check fails. The frozen
   protocol's broader grounded-rejection requirement was detected. The
   [analysis revision](evidence/analysis-revision.json) accurately identifies the
   collection-only correction as post-grading, retains the original freeze/source
   files and patch, and leaves every grade, candidate threshold and unsuccessful
   disposition intact. `grading_validated=true` is not misrepresented as complete
   measurement validation: `all_measurements_validated=false` still records the
   two unresolved contacts.

5. **The archive and original evidence are preserved.** The native archive is
   15,988,897 bytes and its SHA-256 matches
   `d8811f81ad8eef1d2150a5f8011a33ee542daeee6aff30677d0665dc7f923646` in
   [archive metadata](evidence/archive.json). All 30 archived actor-result files
   equal the retained originals; their digests also match the pre-grading source
   audit. All five judgment-result files equal their recorded pre-correction
   hashes, and the archive contains the matching original and revised analysis
   source manifests. All eight actor dependency hashes match both `d524ec9`
   and their current bytes. The earlier independent
   [source audit](evidence/source-audit.json) reconciled all 483 commands and raw
   tool events, with all 117 guide files matching their manifests in every trial.
   No actor timeout or source-contaminated trial is hidden by a denominator.
   These are recorded-action findings, not a claim about unrecorded activity.

6. **Cross-study scope and accepted decisions remain intact.** The updated
   [workflow v2 report](../staged-development/report-v2.md) and
   [reduction plan](../../plans/collaboration-procedure-reduction.md) keep the
   original published-0.2.0 and catalog-aware no-body observations separate.
   These new single-factor comparisons add neither baseline arm. Supplied-
   agreement transfer, missing-decision discovery, returning-user advice and
   first-use learning are distinguished. No human comprehension, satisfaction,
   learning or general superiority claim is added. The saved spec/plan,
   authoritative execution state, material owner decisions, manual-awareness
   default, scoped automatic authority, real checks and stop-before-push boundary
   remain accepted obligations. R1/R3 stay deferred; R4 and R6 retain their
   separate evidence needs. Post-trial judges and controls are not R6 trials.

7. **Repository and closure evidence are consistent.** Tracked active skills,
   inert sources and the original staged-development report have no diff against
   `622975e`; there are no untracked additions under `skills/` or `sources/`.
   The [required-check log](evidence/required-tests.log) records a successful
   validator and 168 passing tests. I inspected that log rather than rerunning
   tests. The [task plan](../../plans/procedure-refinement.md) correctly leaves
   final receipt/commit closure to the parent task.

## Review boundary

I read the reports, frozen protocol/source versions, structured observations,
original native finals and outcome records, checkpoint/Git evidence, audit and
adjudication records, analysis amendment and archive contents. I independently
recomputed descriptive values and verified hashes without executing product,
actor or judge code. No native rerun, new experiment, installation, delegation,
actor edit or grade edit was performed. This review writes only this receipt;
remaining implementation/commit closure belongs to the parent task.
