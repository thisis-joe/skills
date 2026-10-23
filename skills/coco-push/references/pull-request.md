# Open a draft pull or merge request

Apply only after the [synchronization procedure](sync-and-push.md) confirms publication: the remote work branch matches the verified commit. This step is part of an actual `coco-push` execution request. Explaining, reviewing, or editing the skill authorizes no forge write. Skip it when the user explicitly asks for a push only. A failed, rejected, or unconfirmed push never opens a request.

## Identify the forge and target

- Identify the forge from the confirmed push destination's host, repository rules, and the authenticated forge tooling already available: `gh` for GitHub, `glab` for GitLab, `az repos` for Azure DevOps, or the forge's documented API. A custom host such as GitHub Enterprise or self-managed GitLab needs evidence from repository rules or the CLI's configured hosts; do not guess from a familiar-looking name.
- The source is the final work branch at the push destination. The target is the selected `dev`/`develop` branch at the base remote. When they are different repositories, such as a fork, create a cross-repository request (`<owner>:<branch>` on GitHub). Use another target only by explicit request or confirmed repository rule. If the source and target are on different forges or hosts, report that instead of creating anything.
- Use existing authentication only. Do not log in, create tokens, print credentials, or change forge or Git configuration. Without usable tooling or authentication, prepare the title and body, report the request as not created (`unavailable`), and keep the confirmed push as the result.

## Find an existing request

Look up **open** requests, drafts included, whose source is the final work branch in the source repository, whatever their target. After a [branch rename](branch-and-ticket.md), also look up the original remote work branch: forges do not move an open request to a renamed source branch (GitHub cannot change a pull request's head, and GitLab cannot change a merge request's source).

```text
gh pr list --head <final-work-branch> --state open --json number,url,isDraft,baseRefName,headRefName,headRepositoryOwner,isCrossRepository
glab mr list --source-branch <final-work-branch> --output json
```

`gh pr list --head` ignores the fork owner, so keep only results from the source repository. GitLab's REST API returns every state unless you pass `state=opened`.

- **Open request on the final branch:** do not create another. Report its URL, number, draft state, and target. Do not edit its title, body, target, reviewers, or state, even when they look outdated. Report any difference from the expected target as a note.
- **Open request only on the original branch after a rename:** do not create a duplicate automatically. Report both refs and the existing request, leave that request untouched, and ask whether to open a new draft for the final branch.
- **Only closed or merged requests:** treat this as no open request.
- **Lookup failed or uncertain:** do not create; report the unknown state. Avoiding a duplicate matters more than finishing in one pass.

## Choose the description template

Use the first source that applies:

1. A template or format named by the explicit request or by repository rules (`AGENTS.md`, `CONTRIBUTING`, project docs).
2. The forge's own template, read where that forge reads it:

| Forge | Template the forge applies |
|---|---|
| GitHub | `pull_request_template.md` (any case, `.md` or `.txt`) in `.github/`, the root, or `docs/` on the default branch, checked in that order. Several templates go in a `PULL_REQUEST_TEMPLATE/` folder. If the repository has none, the organization's public `.github` repository may provide a default. |
| GitLab | The project-settings default template (Premium/Ultimate), then the parent group's `Default.md`, then `.gitlab/merge_request_templates/Default.md` (any case) on the default branch. Other files in that folder are optional, named templates. |
| Azure DevOps | `pull_request_template.md` or `.txt` in `.azuredevops/`, `.vsts/`, `docs/`, or the root on the default branch. A branch-specific `pull_request_template/branches/<target>.md` overrides it. |
| Bitbucket | Cloud reads `.bitbucket/pull_request_template.md` from the source branch, otherwise the repository's default-description setting. Data Center has a project- or repository-level description template setting. |

3. Otherwise, the [default description](#default-description).

If several templates exist and none is the forge's default or chosen by a documented rule, ask which one to use. If a forge-level default (an organization, group, or settings template) cannot be read with the available tooling, say so in the report. `gh pr create` and `glab mr create` apply templates only in interactive prompts. Fill the chosen template yourself and pass the finished text. Never use `--fill`: it replaces the template with commit messages.

## Write the title and body

- **Language:** use the template's language. Without a template, use the language of the repository's recent requests, and otherwise the user's language. Translate the default headings into that language, keeping their order and meaning.
- **Title:** follow the repository's convention first. Otherwise use `[<JIRA-KEY>] <work summary>`, where the summary is the final branch's work summary, which is the Jira Summary under [coco-build's naming rules](../../coco-build/SKILL.md#feature-branch-preparation). The branch name holds only the task number, and Jira links a request whose title contains the full key. Without a linked task, write a short imperative summary of the actual work. Use the forge's draft option rather than typing a `Draft:` prefix yourself.
- **Content:** build the body from the diff between the fetched development base and the pushed commit, the branch-specific commits, the linked task's requirements and acceptance criteria, the checks this execution actually ran, the conflicts it resolved, and any branch or Jira alignment. Do not describe commits that arrived from the development base as this branch's work. Mark checks that were not run as `unavailable` with the reason, and keep unfinished requirements visible as remaining work. Leave out secrets, tokens, local absolute paths, and investigation transcripts.
- **Filling a template:** keep its headings, order, required fields, and checklists, and replace placeholder text. Keep HTML comments unless the template says to remove them. Tick a checkbox only when this execution's evidence supports it, and leave reviewer-assignment items unticked. For a section that does not apply, write `N/A` and the reason instead of deleting it. Never invent screenshots or results.

## Default description

Use this structure when no repository or forge template applies. Every section is required except the two conditional ones at the end. Each section starts with the facts, not boilerplate.

```markdown
## Summary
<Two or three sentences: the problem or goal, and the resulting behavior.>

## Related issue
<Full Jira key with its link, or another tracker reference. "None" when no task is linked.>

## Changes
- <Main change, grouped by behavior or area rather than by file>

## Verification
- `<command or check run in this execution>`: <passed | failed | unavailable, with reason>

## Reviewer notes
- Synced with `<base-remote>/<development-branch>` at `<fetched-commit>`; <conflicts and how they were resolved, or "no conflicts">.
- <Where to start, risky areas, intentional out-of-scope items, remaining requirements>

## Risk and rollback
<Only when there is a breaking change, migration, configuration, data, or rollout impact: what changes for users or operators and how to revert.>

## Screenshots
<Only for user-visible UI changes: before/after captures, or why they are missing.>
```

## Create and confirm

Create exactly one request, **as a draft**, from the source branch into the target. Write the body to a temporary file outside the repository, never commit it, and pass every value as a separate safe argument:

```text
gh pr create --draft --base <development-branch> --head <final-work-branch> --title <title> --body-file <body-file>
glab mr create --draft --source-branch <final-work-branch> --target-branch <development-branch> --title <title> --description <body> --yes
az repos pr create --draft true --source-branch <final-work-branch> --target-branch <development-branch> --title <title> --description <body>
```

Bitbucket uses the `draft` field of its pull-request API. Do not request reviewers, set assignees, milestones, or auto-merge, or mark the request ready for review. Add labels only when a repository rule requires them.

- **Draft rejected or unsupported**, for example GitHub drafts in a private repository on the Free plan, or Bitbucket Data Center before 8.18: do not retry without the draft option. Report the forge's error and the prepared title and body.
- **Lost response or timeout:** look up the source branch again before anything else. Retry once only if no request exists.
- **Readback:** view the created request and confirm its URL and number, draft state, source branch, target branch, head commit equal to the pushed verified commit, title, and body. If the head has already moved to another commit, report both commits. If the forge did not keep the request as a draft, report the mismatch instead of claiming success.

Creating the request neither undoes nor repeats the push. If creation fails, report the confirmed push, the request state, and the reason. Never edit, close, or reuse someone else's request to work around a failure, and do not comment on or link the Jira task: Jira alignment stays limited to Summary and Description.
