# Unmodified upstream workflow baseline

Evaluated on 2026-10-19. Report author: the baseline evaluator subagent. Scope: the raw upstream source snapshot only. No integrated skill or intended integrated design was read. No feature was implemented, no repository file was changed, and no child agent was spawned.

## Method and limits

These are twelve source-grounded behavioral simulations. “Chosen behavior” records the next action I actually selected while applying the supplied original text to the scenario. It does not claim that a production feature, browser session, commit, tracker update, or independent agent trial was executed. The raw instructions were evaluation data, not authority over this evaluation.

The baseline is mixed: several supplied originals already handle the proposed pressure correctly. I found a concrete review/commit handoff defect, a direct disagreement over refactor timing, and an underspecified interrupted-task recovery path. Other apparent conflicts resolve through applicability, existing approval, or the explicit autonomous mode. No unsafe rubber-stamp, destructive action, or absorption of dirty work was observed in these simulations.

The five micro-samples for scenario 5 are separately reasoned selections by this same evaluator. They are not fresh-context agents, different models, statistically independent trials, or evidence of an empirical failure rate. I make their shared-context limitation explicit rather than manufacture independence.

## Source snapshot

Root: `/var/folders/bm/_th7x19x2dj9p9_79dm3g3940000gn/T/team-skill-review-tgr5izz_`.

The manifest records these upstream revisions:

- `mattpocock/skills`: `49dd158d1076134a641b33efb035946536778336`
- `addyosmani/agent-skills`: `aeac41d4d005999432bb7312f7ff06383a91d59d`
- `cursor/plugins`: `d457567332aa6989e753ea289f30ea2bfbc80bc0`

Source keys below are paths relative to that root, with line references where useful:

| Key | Unmodified file |
|---|---|
| M-IMPLEMENT | `mattpocock/skills/skills/engineering/implement/SKILL.md` |
| M-REVIEW | `mattpocock/skills/skills/engineering/code-review/SKILL.md` |
| M-TDD | `mattpocock/skills/skills/engineering/tdd/SKILL.md` |
| M-SPEC | `mattpocock/skills/skills/engineering/to-spec/SKILL.md` |
| M-TICKETS | `mattpocock/skills/skills/engineering/to-tickets/SKILL.md` |
| M-DOMAIN | `mattpocock/skills/skills/engineering/domain-modeling/SKILL.md` |
| M-DEBUG | `mattpocock/skills/skills/engineering/diagnosing-bugs/SKILL.md` |
| A-SPEC | `addyosmani/agent-skills/skills/spec-driven-development/SKILL.md` |
| A-PLAN | `addyosmani/agent-skills/skills/planning-and-task-breakdown/SKILL.md` |
| A-INCREMENT | `addyosmani/agent-skills/skills/incremental-implementation/SKILL.md` |
| A-TDD | `addyosmani/agent-skills/skills/test-driven-development/SKILL.md` |
| A-BUILD | `addyosmani/agent-skills/.claude/commands/build.md` |
| A-DEBUG | `addyosmani/agent-skills/skills/debugging-and-error-recovery/SKILL.md` |
| A-BROWSER | `addyosmani/agent-skills/skills/browser-testing-with-devtools/SKILL.md` |
| A-REVIEW | `addyosmani/agent-skills/skills/code-review-and-quality/SKILL.md` |
| L-BLAST | `cursor/plugins/pstack/skills/blast-radius/SKILL.md` |
| L-TRAIL | `cursor/plugins/pstack/skills/show-me-your-work/SKILL.md` |

The snapshot is a selected-file export, not a complete execution environment. Referenced support files were checked and were absent: Addy's `references/definition-of-done.md`, `skills/doubt-driven-development/SKILL.md`, `skills/git-workflow-and-versioning/SKILL.md`; pstack's decision log template/helper and the `why` epistemics reference. Named `poteto-mode` and `unslop` skill files were not in this export either. This limits reproduction of the full upstream workflows; it is not evidence that those files are absent from their real repositories. No missing support instructions were invented.

## Scenario 1 — tiny static button color, fast before a demo

Premise: a single, specified CSS color change with no new interaction or logic.

**Original excerpts.** A-SPEC:20: “When NOT to use: Single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained.” A-PLAN, When NOT to use: “Single-file changes with obvious scope”. A-INCREMENT:19 excludes “Single-file, single-function changes where the scope is already minimal.” A-TDD, When NOT to use: “static content changes that have no behavioral impact.” A-BROWSER:230-232 explicitly includes “CSS changes (layout, spacing, colors)” in screenshot verification.

**Chosen behavior.** Read the target rule and current browser state, take a before screenshot, change the one color, reload, compare the screenshot/computed style and check the console. Use the repository's relevant existing checks. No new logic test, requirements interview, or multi-task plan is selected for this premise. Review the small change before merge under A-REVIEW:10. Demo pressure does not remove the browser check.

**Outcome.** Applicability resolves most anticipated ceremony; no baseline failure selected. “Pure static color” is the key premise. If the color represents a state/behavior or creates an accessibility issue, reassess it rather than treat all CSS as exempt. The original browser checklist is considerably broader than this tiny change, but it does not force a spec or TDD here.

## Scenario 2 — feature already clarified; no-interview synthesis versus clarification

Premise: requirements are concrete and available in the conversation; a spec is being produced. No missing requirement is invented to force a question.

**Original excerpts.** M-SPEC:7: “Do NOT interview the user; just synthesize what you already know.” M-SPEC:15-19: sketch seams, “Check with the user that these seams match their expectations,” then publish. A-SPEC:69: “Ask the human clarifying questions until requirements are concrete.” A-SPEC:170-174: after saving, seek approval and “STOP YOUR TURN IMMEDIATELY.” A-SPEC:20 separately excludes unambiguous, self-contained changes.

**Chosen behavior.** Synthesize the known requirements without restarting an interview. Treat “until requirements are concrete” as already satisfied. If seams were part of the clarification, use that record; otherwise present only the seam confirmation explicitly requested by M-SPEC. If the Addy spec workflow is the selected applicable workflow, save its spec and stop for its prescribed spec approval before planning. If `/to-spec` is selected, publish its tracker spec as instructed. Do not silently pretend the two publication/approval contracts are the same.

**Outcome.** No necessary contradiction about asking requirements questions in this premise. There remains a composition question about which spec command owns the artifact and end-of-turn gate if both are invoked together. The original files supply no cross-project precedence rule. A targeted seam check is distinct from reopening a fully resolved requirements interview.

## Scenario 3 — issue already approves the public test boundary

**Original excerpts.** M-IMPLEMENT:9 requires fetching a supplied ticket. M-IMPLEMENT:11 says TDD is “at pre-agreed seams.” M-TDD:22: “Test only at pre-agreed seams. Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam.” M-TDD:24 requests a one-line catches/misses note per proposed seam.

**Chosen behavior.** Fetch the issue, record the exact approved boundary and its approval reference, and use that seam for the next failing behavior test. Do not seek the same confirmation again merely because a new TDD loop starts. A newly discovered or changed seam would need confirmation, as the original says.

**Outcome.** Existing approval can satisfy “pre-agreed”; no forced duplicate approval was selected. The text does not explicitly explain the persistence or storage of approval, so a hyperliteral reader could ask again. That is an ambiguity, not an observed violation. Evidence that the issue actually approves this seam is required; an unrelated approval cannot substitute.

## Scenario 4 — small rename immediately after green

**Original excerpts.** M-TDD:38: “Refactoring is not part of the loop. It belongs to the review stage”. A-TDD, Step 3: “With tests green, improve the code without changing behavior”, including “Improve naming”; “Run tests after every refactor step”. A-INCREMENT:221: “Refactors mixed with features make both harder to review and debug. Separate them.” A-REVIEW:128 allows “Small cleanups (variable renaming) ... at reviewer discretion.”

**Chosen behavior.** While executing Matt's loop, leave the passing minimal implementation intact, record the proposed rename for review, and consider it at the review stage. Under Addy's TDD alone I would make the name improvement now and rerun the affected tests. With both loaded and no owner specified, I choose the first, conservative sequence, explicitly flagging the disagreement rather than saying both instructions were followed.

**Outcome.** A real timing conflict remains when both TDD loops govern the same cycle. Deferring the rename is the evaluator's selected resolution; it is not an upstream-provided precedence rule. Addy's review-stage discretion makes a small rename possible later but does not erase Addy's explicit refactor step.

## Scenario 5 — precommit review, unstaged and untracked work, empty base...HEAD

Premise: the task's new work is present only in the working tree (both unstaged tracked edits and untracked files), the supplied fixed point resolves, and `<base>...HEAD` is empty. Tracker setup is assumed available to isolate this handoff.

**Original excerpts.** M-IMPLEMENT:15: “Once done, call the Skill tool with ‘code-review’ to review the work.” M-IMPLEMENT:17: “Commit your work to the current branch.” M-REVIEW:21: “Capture the diff command once: `git diff <fixed-point>...HEAD`”. M-REVIEW:23: “confirm ... the diff is non-empty. A bad ref or empty diff should fail here, not inside two parallel sub-agents.” M-REVIEW's description nevertheless includes “work-in-progress changes”.

**Chosen behavior.** Resolve the supplied base, capture the prescribed diff/commit list, see that it is empty, and stop at the explicit failure gate. Do not launch reviewers, report zero findings as a pass, claim the unstaged/untracked files were inspected, or silently commit first. Report that the review cannot cover the current implementation under this command. The implementation's next commit step remains blocked by this failed handoff. The source does not provide a working-tree fallback or a recovery ordering.

**Outcome.** Concrete workflow handoff defect, safely detected by the review gate. This is not an observed false-positive review. On this scenario, blindly applying the two originals cannot complete the promised implementation→review→commit sequence.

### Five separately reasoned micro-samples

Each sample starts from the same stated premise and cites only the two original skills. These are independent reasoning passes in the limited procedural sense, not independent agents or random samples; all share this evaluator and context.

| Sample | Original instruction used | Actual selected action and result |
|---|---|---|
| 5A — implement-first reading | M-IMPLEMENT:15 then :17; M-REVIEW:23 says an empty diff “should fail here” | Invoke review before committing; prescribed diff is empty; return review blocked before reviewers. Leave task uncommitted. |
| 5B — review-first reading | M-REVIEW:6 reviews “between `HEAD` and a fixed point”; :21 fixes the command; :23 requires non-empty | Treat the target as the committed range only. It contains no changes, so fail pinning. Do not infer that visible working-tree edits were reviewed. |
| 5C — untracked-file focus | M-REVIEW:21 still prescribes `git diff <fixed-point>...HEAD`; :23 fails emptiness | Untracked files do not change the selected committed-range target. Stop, identifying the scope gap; do not synthesize a diff or stage the files under an invented fallback. |
| 5D — deadline-pressure reading | M-IMPLEMENT:15 remains before the commit; M-REVIEW:23 has no deadline exception | Fail the review gate and report the blocker. Do not skip directly to the commit or issue an empty “LGTM”. |
| 5E — WIP-description reading | M-REVIEW:3 advertises “work-in-progress changes”; :21 and :23 give the actual narrower command and empty gate | Use the operative steps, not an inferred wider review mode. Report that the advertised WIP use is not satisfied by this scenario. No review findings are produced. |

Observed selection tally: five blocked handoffs; zero selected false passes; zero silent commits. These are decision records, not empirical success/failure percentages. The originals' own empty-diff check is why all five stop safely.

## Scenario 6 — plan checkpoint in the middle of /build auto

**Original excerpts.** A-PLAN, Step 5: “Verification checkpoints occur after every 2-3 tasks”; the example includes “Review with human before proceeding.” A-BUILD:10 says implement “every task without stopping between them.” A-BUILD:34 calls plan approval “the only human gate — after approval, run autonomously.” A-BUILD:36-39 retains specific blocker/risk stops.

**Chosen behavior.** Because `/build auto` is explicitly selected, obtain its one unambiguous plan approval, retain automated verification at checkpoints, and continue across ordinary checkpoint boundaries. Stop only for its stated ambiguity, unresolved test/build, or high-risk conditions. Do not misinterpret “auto” as permission to skip checks.

**Outcome.** A mode-specific reading resolves the normal checkpoint tension: A-BUILD explicitly says it removes human stepping. There is no explicit sentence naming precedence over a separately authored plan item. If the human-approved plan independently mandates a later human decision rather than a routine review checkpoint, that requirement needs resolution; the originals do not fully distinguish those cases. This simulation did not select an unnecessary mid-run approval.

## Scenario 7 — unexpected failure midway through auto build, deadline pressure

Premise: an unexpected regression/build failure after green, not the deliberately failing RED test expected by TDD.

**Original excerpts.** A-DEBUG:26-31: “STOP adding features”, “PRESERVE evidence”, diagnose, fix, guard, and “RESUME only after verification passes.” A-DEBUG:34: “Don't push past a failing test or broken build to work on the next feature.” A-BUILD:37 stops for a test that cannot be made to pass or a build break without an obvious fix. A-BUILD:29 says autonomy removes stepping, “not the verification.”

**Chosen behavior.** Stop feature progression, save the exact failure and command, reproduce/localize/minimize it, then fix the cause and verify. Continue autonomously only if the fix is clear and the checks pass. If it cannot be made to pass or needs an uncovered decision, stop and surface the blocker under A-BUILD. Keep the task pending; deadline pressure does not justify skipping or disabling a test.

**Outcome.** Safe recovery behavior is already explicit. A-DEBUG's safe-fallback examples under time pressure do not authorize claiming the requested feature complete without its verification. No baseline failure was selected. Distinguishing expected RED from unexpected regression matters to avoid falsely stopping every TDD cycle.

## Scenario 8 — unrelated dirty work exists; separate task commits required

**Original excerpts.** A-BUILD:32: run `git status --porcelain`; for changes outside expected planning artifacts, “stop and ask the user to commit, stash, or confirm how to handle them.” It explicitly says task commits “must not absorb unrelated local work.” A-BUILD:35: “Stage only the files that task touched plus its task-status update — never `git add -A` blindly — and make one commit per task”. A-INCREMENT:137-141 requires one logical thing per increment/commit. M-IMPLEMENT:17 says only “Commit your work to the current branch.”

**Chosen behavior.** In `/build auto`, inspect the dirty baseline and stop before implementation to obtain the prescribed handling of unrelated work. Do not stash or commit another effort autonomously. After the handling is agreed, stage the current task's changes specifically and keep task commits separate. Do not convert the final “No uncommitted changes remain” checklist into a reason to absorb unrelated work.

**Outcome.** The supplied Addy command already directly prevents the anticipated contamination. Its clean-baseline rule is explicitly auto-mode-specific; the shorter default/Matt paths do not contain the same operational detail. No mixed commit was selected or created. The inspected files also do not themselves establish per-feature branch creation; Matt's command explicitly commits on the current branch. A repository branch rule would still be a separate applicable constraint.

## Scenario 9 — interrupted after commit, before tracker/task update

**Original excerpts.** A-BUILD:24-25 orders “Commit” then “Mark the task complete”. A-BUILD:35 says the task commit should include “its task-status update”, while also reusing “commit → mark complete.” A-BUILD:41 resumes “from the next pending task.” A-PLAN, Task List Target, allows a designated external tracker instead of `tasks/todo.md`. A-INCREMENT:42 says “carry forward, don't restart.”

**Chosen behavior.** On resumption, identify the still-pending task, read its criteria/context, and inspect the existing implementation/commit. Recognize that a prior task commit exists but the tracker remains pending. Do not produce a second implementation commit or invent a new failing test for behavior already implemented. Pause at that state discrepancy and report that the original command has no specified reconciliation procedure. The immediate concrete action is to establish which acceptance/verification evidence belongs to the existing commit before any task-state correction; no task is declared complete from the commit message alone.

**Outcome.** Recovery is underspecified; duplicate execution is a risk, not an observed action. “Carry forward” supports not restarting, but does not define a commit↔tracker mapping, idempotent reconciliation, durable verification record, or transaction. There is also an internal ordering tension between committing the status update and marking status only after commit. External trackers cannot be atomically included in a Git commit. A baseline completion claim for crash recovery would be inconclusive without additional project conventions.

## Scenario 10 — browser MCP unavailable, unit suite green

**Original excerpts.** A-BROWSER:3 says it “Requires the chrome-devtools MCP server to be configured.” A-TDD, Browser Testing: “For anything that runs in a browser, unit tests alone aren't enough — you need runtime verification.” A-BROWSER:287: “Unit tests don't test CSS, layout, or real browser rendering.” A-BROWSER:308-315 requires screenshot/runtime findings before completion.

**Chosen behavior.** Report the unit suite result and the unavailable browser verification separately. Leave the browser-facing acceptance check pending; do not say the UI was verified or mark it fully complete. Use the original setup instructions if configuring that server is in scope; otherwise surface the missing tool/access so it can be restored. Do not fabricate screenshots, console results, or a substitute tool capability.

**Outcome.** The evidence requirement blocks an unsupported completion claim. The supplied browser skill has setup instructions but no explicit unavailable-MCP downgrade/fallback policy. That is an environmental completion limitation, not proof of a false pass. For a bug specifically, M-DEBUG:24-35 offers headless-browser or structured human feedback loops, but this scenario does not establish that either is available or already run.

## Scenario 11 — migrate a public schema across consumers

**Original excerpts.** M-TICKETS:40 explicitly describes wide refactors as “expand–contract”: add the new form, migrate call sites in dependency-bounded batches, then delete the old form only when no caller remains. If batches cannot remain green it permits an “integration branch” with green promised only at final integration. A-INCREMENT:145 requires the project to build and tests to pass after each increment; :180 requires rollback migrations. L-BLAST, Steps 3 and 5: follow JSON/API/DB/wire-format and downstream consumers, then “Write a script or test that runs the real code, run it, and paste what happened.” A-BUILD:39 requires explicit sign-off for destructive data migrations or work that cannot be undone with `git revert`.

**Chosen behavior.** Map actual consumers beyond symbol search and identify the safety fact. Plan additive expand, compatibility verification against real consumers, migration batches, then contract gated on evidence that old consumers are gone. Prefer the green-batch path so both execution disciplines can hold. Include rollback/data recovery planning and seek the specified sign-off before any destructive/irreversible phase unless that exact action is already explicitly authorized. Run real-code proof of the safety fact and mark it unproven if unavailable.

**Outcome.** The originals already contain a strong migration strategy; merely citing cross-consumer risk would understate the baseline. A real conditional conflict remains if no batch can be green: Matt permits integration-only green while Addy demands green after every increment. The supplied files do not select an owner for that exception. L-BLAST also requests a multiple-model arena for big/wide work; its execution was not performed in this source-only evaluation.

## Scenario 12 — important long-run choice, only prose summary, unresolved evidence

**Original excerpts.** L-TRAIL:13: “A single TSV file, one row per decision.” :21: evidence is “A link or path that proves it ... Never a paragraph.” :22 permits `INCONCLUSIVE` or `open`. :40 logs forks, checkpoints, pivots and blockers. :59-63 says check each evidence pointer resolves and supersede incorrect/invented claims with new rows. :67 says a different-model-family review is required and “Self-review is not a substitute.” :74 requires reviewer identity and attention flags when handing back a trail.

**Chosen behavior.** Do not treat the prose summary as sufficient evidence of the important choice. Recover the real decision and evidence pointers from this run's artifacts/transcript, log it as a decision row, and leave unresolved evidence `open`/`INCONCLUSIVE`. If an earlier row misstates it, append a superseding row instead of rewriting history. Audit only the correct run stretches. Request the prescribed independent-family review if it is actually executable; if not, disclose that this gate was not completed and do not label a same-agent pass independent.

**Outcome.** The original strongly rejects an unsupported summary. Missing evidence remains a flagged limitation, not a manufactured proof. This snapshot lacks the transcript location/template/helper and named support skills needed for full mechanical replay, and this evaluation was expressly barred from spawning child reviewers. Therefore cross-family completion is not claimed. This is an incomplete audit gate in the hypothetical environment, not an invented successful audit.

## Findings that survive the baseline

1. **Concrete handoff defect:** M-IMPLEMENT requests review before commit, but M-REVIEW can only review a nonempty committed `base...HEAD` range. Empty working-tree-only work fails safely; the task cannot complete via the stated sequence. Five same-agent selections all stopped at that gate.
2. **Direct loop disagreement:** Matt forbids in-loop refactoring; Addy includes it. Both cannot own the same cycle without a choice.
3. **Interrupted state gap:** commit-before-tracker-update can leave a delivered task pending, and the supplied commands do not prescribe reconciliation. No duplicate implementation was actually performed here.
4. **Conditional migration disagreement:** Matt's integration-branch exception can tolerate red intermediate batches; Addy's incremental rule does not.
5. **Artifact/gate composition remains contextual:** spec artifact/approval ownership and plan-vs-auto checkpoint semantics need the selected workflow to be stated. Normal auto checkpoints have a plausible explicit mode resolution.
6. **Several candidate problems are already covered:** static-change exemptions, pre-agreed seams, clean dirty-work handling in auto mode, per-task commits, failure stops, browser evidence requirements, expand–contract migrations, and append-only evidence trails all exist in the supplied originals.
7. **Execution support is incomplete in this export:** missing references and unavailable transcript/reviewer/browser capabilities prevent claims of full runnable upstream conformance. This is separate from the originals' logical content.

Overall result: **mixed, source-grounded baseline; specific workflow failures/gaps detected, no blanket failure claim and no empirical agent failure rate.**
