# Situation, purpose and expected result

Read only the selected entrypoint and the conditional reference relevant to the task. Existing sufficient artifacts skip their creation step. All names are `coco-*` for invocation and `coco-*` for display.

| Situation / desired output | Entry | Expected result |
|---|---|---|
| Browse all available skills or understand a selected skill | tellmeskill | Recent skills first on a bare invocation, then the full current catalog grouped by purpose; target/depth choices and source-based explanation using the common format |
| Decide what to ask an already selected skill | whattosay | Contextual full invocation options, a recommended choice, then user-selected execution or prompt-only output |
| Be quizzed on the current work or selected code to understand it | askme | Scope/topic choices, one grounded question at a time, answer feedback and a closing summary; no code changes |
| Adapt an existing skill to team rules or change its workflow | updateskill | Scoped source changes, consistent references/provenance, checks and actual installation status |
| Integrate remote dev/develop, resolve conflicts and publish the current branch | push | Verified integration commits, single-branch normal push and remote-ref readback |
| Clear static color/copy edit | Direct lightweight edit; start only if routing is unclear | Requested edit and necessary visual/content check |
| Establish commands, standing quality bar or select a workflow | start | Project profile, checks with owners, chosen route |
| Unsettled requirements, terms or idea, or a plan to grill/stress-test | clarify | Settled decisions, explicit open items, glossary/ADR only when warranted |
| Understand runtime behavior, historical rationale or an external API | research | Cited explanation, verified facts versus inferences, preservation constraints |
| Choose module/API boundaries or test an uncertain design | design | Compared alternatives, contract and test surface; disposable prototype evidence if needed |
| Turn agreed behavior into a durable contract | spec | One authoritative spec with scope and observable acceptance |
| Break work into dependency-ready, verifiable units | plan | Ordered task graph, verification and risk checkpoints |
| Implement one task or an authorized sequence | build | Tested behavior, runtime evidence, reviewed work-unit commits and state |
| Unexpected failure, hard bug or failed required check | debug | Red-capable repro, supported cause, verified fix handoff |
| Establish actual behavior or a safety/proof claim | verify | Evidence, cleared and unresolved conditions; no inferred pass |
| Compare a change with requirements, rules and quality | review | Separate per-axis findings and verdict on a frozen actual scope |
| Authentication, trust boundary, sensitive input or hardening | security | Threat paths, scoped defenses and abuse-case verification |
| Schema/API replacement, wide rename or removal | migrate | Expand/migrate/contract plan, compatibility and rollback conditions |
| Slow behavior or disputed benchmark | performance | Reproducible baseline, bottleneck, controlled before/after results |
| UI behavior, styling, accessibility or interaction design | frontend | Existing design conventions, correct states and browser evidence |
| Logs, metrics, traces or operational diagnosis | observe | Useful signals and alerts, bounded cardinality and verified incident visibility |
| CI, recurring automation, bots or reusable verification helpers | automate | Idempotent scoped automation, tests and explicit activation boundary |
| PR preparation or release readiness | ship | Evidence-backed ready/blocked decision, release/rollback steps; deployment state separately |
| ADR, README, API reference, guide, runbook, agent instructions or prose for other readers | docs | Convention-following project document with verified commands, links and examples |
| Explanation for the user's own understanding, personal study notes or a learning workspace | learn | Plain explanation or short uniform notes that pass the note checker |
| Context window, handoff, recall or long-run decision trail | context | Compact resumable packet and resolvable evidence pointers |
| Retrospective, evaluation or durable lessons | retro | Verified failure pattern, targeted structural improvement and a checking scenario |
| Incoming report, issue prioritization or autonomous issue selection | triage | Evidence-backed disposition, deduplication and dependency/ownership-aware work choice |
| Complexity reduction or refactoring without new behavior | simplify | Removed complexity, preserved interfaces/behavior and regression evidence |

Specialist work adds relevant checks to the chosen route; it does not force every task through every row. Review/verification failures return to the current execution owner, not into recursive orchestration. A user asking only for an explanation does not authorize implementation.
