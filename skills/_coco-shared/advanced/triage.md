# Triage and configured intake

Apply the [common contract](../contracts.md). Triage evaluates incoming work and prepares a durable next action; it does not automatically fix, merge, deploy or grant permission to post externally.

## Input and mode

Retain the report/issue/PR reference, repository, tracker configuration, labels, authorized actions and relevant source artifacts. Choose maintainer issue triage or explicitly configured automated intake. Generated implementation tickets already ready for execution bypass raw-request triage.

A read-only recommendation is always separate from an authorized label/comment/closure. Use authenticated supported adapters; do not invent vendors, IDs, owners or priorities.

## Canonical roles and discovery

Use one category: bug or enhancement. Preserve useful subcategories such as performance, question/feedback or reroute during intake classification. Use exactly one mapped state: needs-triage, needs-info, ready-for-agent, ready-for-human or wontfix.

Resolve canonical roles to existing tracker strings. Conflicting states require maintainer resolution rather than a guessed mutation. Unlabeled incoming work normally enters needs-triage; needs-info returns to evaluation when the reporter answers. An explicit maintainer override uses their direction without a new full interview.

For attention discovery, show oldest-first unlabeled, needs-triage and needs-info items with reporter activity since the last notes. Include external PR/MRs only when the repository enables that discovery surface; an explicitly named PR is inspectable regardless of author. Distinguish issues and PRs in the list and show actual items, not counts alone.

## Maintainer triage procedure

1. Read the full body, comments, labels, author, dates and prior triage notes; inspect a PR's actual diff. Reuse resolved answers instead of asking them again.
2. Read relevant domain vocabulary/decisions. Search the code by concept for behavior already implemented and read any durable rejection records.
3. Recommend category/state with reasoning and relevant codebase facts. Ask only for an unresolved maintainer decision outside the authorized outcome.
4. Verify before refining the request: reproduce the reported bug or check the PR's claimed behavior with relevant commands. Record confirmed, failed or insufficient-detail evidence; a nearby unrelated failure does not confirm the report.
5. Clarify missing behavior using independent ready questions, while the agent discovers available facts. Capture newly resolved language/decisions in their authoritative documents.
6. Prepare the appropriate brief/notes/rejection. Execute only the authorized tracker mutations, preserving unrelated fields.
7. Read back resulting labels/comments/state when supported and report exact outcomes. An unavailable write or verification is not completed triage.

Every actual AI-authored triage issue/comment begins with a clear AI-generated-triage disclaimer. Preparing a draft does not imply sending it.

## Durable agent and human briefs

A ready brief is the execution contract, with:

- Category and concrete summary.
- Current behavior, including verified reproduction or the state of an existing PR diff.
- Desired observable behavior, relevant errors and edge cases.
- Key interfaces/types/config contracts that need to change.
- Independent, testable acceptance conditions.
- Explicit exclusions and necessary evidence.

Use behavioral contracts rather than brittle line numbers and file-by-file implementation instructions. For a PR, specify remaining gaps/fixes on that diff rather than pretending the work starts from nothing. Human-ready uses the same structure plus why judgment, access or manual work prevents delegation.

Needs-info notes preserve what is established and ask specific actionable remaining questions. A quick state override need not invent a brief; identify if one remains missing for later execution.

## Rejection, duplicates and already-built behavior

Search by concept, trigger, symptom and evidence, not wording alone. Distinguish a confident duplicate, a plausible related item, superficial resemblance and no match.

An already-implemented request points to the existing behavior and may close as wontfix under the maintainer's policy; it is not a rejected feature. Rejected bugs receive a reason but do not enter the enhancement-rejection knowledge base.

For a durable rejected enhancement, maintain one concept record with decision, substantive rationale and all prior request links. Avoid recording temporary lack of time as a permanent rejection. Check existing records early; on a match, surface the reasoning rather than automatically rejecting. Reconsideration updates/removes the current rejection record without rewriting historical issue discussion.

Do not close a parent implementation issue merely because its child work was triaged.

## Configured automated intake: fail-closed preflight

Use only when the user explicitly authorizes an intake workflow with source/tracker adapters and trusted identity/marker configuration. The automation mode does not inherit a general permission to contact people.

1. Validate configuration, authorized source and capabilities. Freeze original source container/root coordinates and stable permalink before delegation; later reads/writes must use them.
2. Read the complete report/thread and relevant screenshots/video/logs. Capture versions/environment, expected/actual behavior, trigger/frequency, signatures, existing fixes and explicit ownership. Mark unreadable media unavailable.
3. Preflight the original parent before tracker writes and immediately before posting. Missing/deleted/inaccessible/uncertain parent means no writes; never substitute another container or a root broadcast.
4. Keep exactly one authorized coordinator writer. Other workers are read-only and lack source/tracker write credentials; if isolation cannot enforce that, investigate in the coordinator.
5. Verify source permalink/prior verdict dedupe before creating anything. Existing trusted intake handling means no duplicate post or ticket.

## Configured intake: investigate and decide

Trace the reported action to the likely code path and dependency before routing; check history for regressions and existing fixes. This bounded pass distinguishes facts/hypotheses and avoids assigning the visible symptom to the wrong owner. It does not perform a fix.

Classify bug, measurable performance problem, feature, question/feedback or reroute. If bug versus feature remains unclear, ask one focused question in the authorized verdict and create nothing. Routing follows confirmed area/path/signature and configured destinations; unknown ownership remains unknown. Owner pings require explicit configured permission and strong relevant evidence, never a broad group by default.

Search source URL, signature, area, trigger, symptom, version/date and suspected regression. A confident duplicate can receive a source link and short recurrence note when authorized; do not reopen/relabel/reassign by default. A plausible match gets an uncertainty link and no new issue. A long-closed item is a regression lead, not proof of a current duplicate.

Create a ticket only for a clear new live bug/performance defect with no confident/plausible live duplicate, valid source/target fields and a compensation-capable adapter. Never create for feature requests, questions, reroutes, already-fixed reports or uncertain cases in this intake mode.

The ticket contains report evidence, expected/actual behavior, environment or unknown, trigger/frequency, original permalink, labeled tracing hypotheses and artifact links. Do not guess root cause in the title or invent labels, priority or ownership.

## Configured intake: one verdict and compensation

Preflight the original parent again, then post one substantive outcome reply in that original thread only, with the tracker link/missing fact/reroute and exactly one configured verdict marker. Never broadcast, DM or start a replacement thread. Read back the same coordinates and verify the marker came from the configured trusted identity.

If this run created a ticket and the handoff did not land, invoke its configured cancel/close/delete compensation and verify that outcome. If compensation is unavailable before creation, do not create; if it fails afterward, report the orphan risk in the run output without posting elsewhere.

A configured bounded follow-up window can answer direct questions or apply safe factual corrections only. Emit no second marker, stay out of side coordination, stop on request and do not extend indefinitely. Reproduction/fix work is a separate authorized workflow; an existing fix switches that later workflow to verification rather than competing implementation.

## Output and stopping conditions

Return report identity, classification/state, evidence and dedupe result, recommended next action, drafts or actual authorized mutations, and unavailable checks. Maintainer triage ends with the chosen disposition and durable brief/notes. Configured intake ends after its verified verdict/compensation and bounded follow-up, with no merge/deployment claim.
