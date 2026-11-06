# Troubleshooting case format

A case records one resolved problem and gives the reader a procedure to follow on recurrence. It shares the [resolved TIL root](../SKILL.md#resolve-durable-storage) and `INDEX.md` with concept notes.

## Workspace layout

Store the case as `cases/<slug>.md`, using lowercase ASCII letters or digits separated by hyphens. On the first case write, create `CASE_TEMPLATE.md` at the TIL root from the template below. Translate the four section labels once for the workspace, then use those exact labels in that order. Keep the frontmatter keys in English. A workspace with only cases can contain just the case template, case files and index.

In `INDEX.md`, prefix the exact `CASE_SECTION` value from the [case checker](../tools/check_cases.py) with `## `. Each case gets one bullet there with its title, a relative link to `cases/<slug>.md` and a brief hook. Keep the section alongside existing concept topics.

## Match existing cases

Before creating a case, search the index titles and hooks and read the relevant files under `cases/`. Compare the affected component or workflow, the conditions where the symptom appeared, and the diagnostic finding or resolution path. A changed title, build number or SHA alone does not make a separate case. A matching symptom with a distinct evidenced failure or resolution path can be a separate case.

Update a matching case only when the session adds a material observation, an evidenced diagnostic branch, a correction or a new recheck result. Keep prior evidence and user content, and explain conflicting observations by their conditions when known. When all evidence is already covered, skip the write and keep the file, its dates and index entry as they are.

## CASE_TEMPLATE.md

````markdown
---
title: <problem title>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources: [<build or artifact reference>, <revision and repository path>]
---

# <problem title>

## Symptoms and success criteria

<What happened, in which conditions, and which observable result counts as recovery.>

## Diagnostic sequence

<For each decisive step: hypothesis → actual check → observation → next decision. Identify evidence that ruled out a hypothesis. Give the actual command or interaction when available, with its observed result and evidence pointer.>

## Procedure for next time

<Where to run each step and which inputs to replace, such as job, build number or SHA. Label reusable example commands before showing them. Classify each step as read-only or state-changing before the command or action. For an important fork, give the observable result and the next action for each supported branch.>

## Fix and revalidation

<What was done, why it fit the evidence, and which check met the success criteria. Compare the relevant conditions and outcomes before and after. State differences in conditions, uncertainty and unchecked behavior.>
````

## Writing and checking

- Keep the decisive steps. Use the check actually performed, whether it was a log, a metric, a command, a UI interaction or a combination. Label commands already run as actual and examples as reusable. Redact sensitive values and mark any redaction. Save the procedure without rerunning it.
- Give stable evidence pointers in `sources` and connect observations to the applicable pointer in the body. Use a job and build number, a commit plus repository-relative path, or an identifiable artifact or document. For an uncommitted code observation, label that state and cite available durable corroboration. Keep each pointer free of commas so the list stays unambiguous.
- Tie the observation to the next action. For a Jenkins delay, a long interval before the first stage calls for comparing executor occupancy with queue or wait logs. A long stage calls for examining that stage's logs and process. If the build completes but deployment fails, the next check may reproduce the failing check as the deployment account. Treat these as example branches and record only the actual branches and results as session evidence.
- Run `python3 <coco-til folder>/tools/check_cases.py <resolved-til-root>` after a case write. It checks the file and template structure, source pointer fields and the designated index entries. Review evidence quality, decision branches, replay instructions and semantic duplicates separately.
