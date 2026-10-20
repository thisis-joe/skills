# Align the branch and Jira task with actual work

Apply after synchronization, conflict resolution, and required checks, before the final push. This procedure is part of an actual `coco-push` execution request. A request to explain, modify, or review the skill does not authorize changes to a user repository or Jira.

## Compare actual work with the name

Read the diff between the fetched development-base commit and final HEAD, branch-specific commits, and the linked task's requirements and acceptance criteria together. Do not summarize from commit titles or only the last changed file. Do not count others' changes arriving from the development base as this branch's new work, or describe reverted changes or unfinished requirements as implemented. Keep uncommitted user files out of the work being pushed.

Judge whether the branch summary describes the actual main purpose and scope. Do not rename an appropriate branch because of a small internal implementation change or wording preference. If it describes another feature or omits important scope, derive a new summary and reason from the actual changes. If scope is unclear or unrelated tasks are mixed together, obtain the necessary decision instead of using a rename to justify the mixture.

## Establish targets and proposed changes

- Confirm the **full Jira key** and project from task records, ticket links, PRs, or the explicit request. Do not infer the project from a branch's number or choose another similarly named ticket. Read the current Summary, Description, and links. If required information or read/write capability is missing, retain the proposed changes and ask only about the missing part.
- Follow [coco-build's naming rules](../../coco-build/SKILL.md#feature-branch-preparation). Preserve type, area, and task number; change only the work-summary portion to match actual work. A different task or area needs a separate scope decision. Match the final branch summary to Jira Summary. Handle characters invalid in Git according to the naming rules.
- Reflect this branch's actual changes, verified behavior, and remaining scope in Description. Preserve existing requirements, acceptance criteria, links, and others' records; edit only the relevant work-description portion or add a clearly identified section for this branch. Do not replace the entire description with a generated summary or delete unfinished requirements. Update an existing equivalent section instead of adding a duplicate. For a rich-document field, use the supported format and preserve existing formatting.

Validate the new name with `git check-ref-format --branch` and check for local and remote collisions. Do not overwrite another same-name branch or rename with `-M`. If the new remote name exists, confirm whether it belongs to the same task; return to integration, verification, and summary review for unintegrated commits. Ask about a collision whose relationship remains unclear.

Before renaming, record the old local name, HEAD, upstream, remote ref/OID, new name, and final write destination. **Fetch and integrate unique commits from the original remote work branch first.** Renaming must not skip reading existing remote work. Default to pushing the new name. If the user explicitly named another destination, resolve the destination decision without silently changing the request.

## Apply and confirm

1. Once comparison, related information, the Git candidate, and destination are established, rename the current work branch with `git branch -m <new-name>`. Pass arguments safely. Confirm that HEAD and user files are preserved. Do not request the same authorization again for name/field changes already within scope.
2. Reread Jira immediately before writing. If someone changed it since the first read, merge only the relevant portion against the latest content; ask only about conflicting intentions. Use supported versioned/conditional updates when available. Update only the confirmed ticket's Summary and Description. Status transitions, completion, assignee, priority, and comments are outside scope.
3. Reread Jira to confirm the new Summary and description are present and preserved content remains. If a response was lost, read back first; do not write twice or assume success. Do not bypass permission, field, or network restrictions.
4. Recheck final HEAD and remote refs, then normally push the **final-name branch** using the synchronization procedure's single refspec. If new commits require integration, repeat verification and summary comparison and align Description with the changed work. Retain the original limits of three refresh/integration rounds and three push attempts.

Local rename, Jira update, and remote push are not atomic. If the Jira update or readback fails, do not push; distinguish the already changed local name from the unapplied ticket state. A failed push after a successful Jira update is not completion. Do not automatically roll back over someone else's records. On resumption, inspect actual state and avoid repeating completed steps.

Publishing a new ref does not rename or delete the original remote ref. Retain the original remote branch and report both refs and effects on PR links. An open PR/MR cannot follow a renamed source branch; the [pull/merge request procedure](pull-request.md#find-an-existing-request) prevents a duplicate draft. Editing or closing an existing PR/MR and remote deletion need a separate request. If the local upstream still points to the old work ref, compare it with the final destination and report the difference. Do not trust upstream alone to push to the old name or development base.
