# Purpose groups for the complete list

Group the complete list so the user can scan by intent. Classify every catalog entry, including COCO, system, and plugin skills, from its catalog description; do not read skill bodies to classify. The table is a classification guide, not a skill list: never add, drop, or rename entries to fit it. Translate group names and descriptions into the user's language.

| Group | Description shown to the user | Belongs here |
| --- | --- | --- |
| **Guide and discovery** | Find the right skill or workflow, see what a skill does, decide what to ask it, or adapt and create skills. | Workflow selection, skill explanation, request suggestions, skill or plugin authoring and maintenance, guided setup. Examples: `coco-start`, `coco-tellmeskill`, `coco-whattosay`, `coco-updateskill`. |
| **Requirements and planning** | Settle what to build and how before writing code: clarify, investigate, design, specify, and split work. | Requirements, research, interfaces and architecture, specifications, task plans, issue triage. Examples: `coco-clarify`, `coco-research`, `coco-design`, `coco-spec`, `coco-plan`, `coco-triage`. |
| **Implementation and change** | Write or reshape code: build features, fix failures, refactor, migrate, and work on UI. | Feature and bug-fix implementation, debugging, simplification, migrations, frontend work. Examples: `coco-build`, `coco-debug`, `coco-simplify`, `coco-migrate`, `coco-frontend`. |
| **Quality and verification** | Prove the work is correct, safe, and fast enough before trusting it. | Behavior verification, code review, security, performance measurement. Examples: `coco-verify`, `coco-review`, `coco-security`, `coco-performance`. |
| **Release and operations** | Get verified work merged, released, automated, and observable. | PRs and releases, branch synchronization and pushes, CI and recurring automation, scheduling, logs and alerts. Examples: `coco-ship`, `coco-push`, `coco-automate`, `coco-observe`. |
| **Knowledge and context** | Keep and reuse what was learned: documentation, study, handoffs, and retrospectives. | Project documents, explanations and quizzes for the user, context handoff and recall, retrospectives, memory. Examples: `coco-askme`, `coco-context`, `coco-retro`. |
| **Files and visual output** | Produce or edit documents, spreadsheets, slides, PDFs, charts, and pages. | Office and PDF files, shared docs, data visualization, artifact and diagram design. |
| **Agent settings** | Configure the coding agent itself: settings, permissions, hooks, shortcuts, and usage. | Runtime configuration, permissions, keybindings, status line, repository instruction files, usage reports. |
| **Other** | Skills that fit none of the groups above. | Use only when no other group fits. |

Place an entry that fits several groups in the group of its primary purpose and list it once. Show groups in table order and omit groups with no entries. Within each group, sort by identifier and continue the list numbers from the previous group so every entry keeps one unique number.
