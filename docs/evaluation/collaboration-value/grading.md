# Blinded outcome audit

The experimental inputs, owner profiles and quality checks are frozen separately.
This document makes the independent judgment format explicit. Judges receive
random packet identifiers, copied source, contract, proposed diff and actual
review text. They do not receive the condition mapping or actor costs. An audit
is not an additional opportunity for the actor to repair its result.

## Review judgments

For each report, identify concrete supported findings rather than counting
headings. Check the proposed code and public CLI where needed. The seeded root
causes are: D1 cache lookup before tenant authorization; D2 request replay without
payload identity; D3 rejected over-refund mutation due to late bounds checking.
A report must explain the reachable mechanism and consequence to receive recall.
Report whether the actor itself supplied a reproduction, a trace, or only a
claim; a judge's later reproduction does not become actor evidence.

Actual probes established that oversized refunds also crash at SQLite binding.
Moving only the D3 bound check before writes fixes both that crash and rejected
refund mutation, leaving D1/D2. It is a valid additional D3 manifestation, not a
fourth root or false positive. Investigate any other actual unexpected finding;
apply the same independent-root criterion to both conditions. An allowlisted
ORDER BY and a non-boolean integer guard are not defects by themselves.

Each verdict records packet ID, recalled root IDs, supported manifestations,
unsupported findings with reasons, actor evidence, actionable remedies, and any
unsupported approval. Two hidden sensitivity packets contain false approval
and a false SQL-injection accusation. They must be recognized before accepting
the judge's aggregate. Report disputes and resolve against actual source/CLI,
retaining original verdicts. No verbosity, document or checklist bonus.

## Owner/intervention audit

Audit the actual actor final message, classifier output, previous disclosures and
delivered exact reply. Classifications are instrumentation, not ground truth.
Check that questions are genuine, topics match what was asked, no unasked private
fact was released, trial feedback advanced the scheduled event, and a repeated
fact had actually been delivered before. Separate asking for an as-yet-unknown
choice from forgetting one; separate public contract reminders from private
choices. Count only actual subsequent actor delivery as intervention.

Record instrumentation disagreements without rewriting the native trace. Assess
whether each disagreement could change a quality result or the direction of a
comparison. Human time, satisfaction and comprehension remain unmeasured.
