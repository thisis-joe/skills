# Pull/merge request metadata

Apply this after a coco skill creates a PR/MR. A request found already open keeps its assignees, reviewers and labels unless the user asks for a change. An explicit request or repository rule (`AGENTS.md`, `CONTRIBUTING`, `CODEOWNERS` policy, project docs) that names other people or labels wins over these defaults.

## Defaults

- **Opener:** the authenticated forge account that created the request: `gh api user --jq .login` on GitHub, `glab api user` (`username`) on GitLab. Never guess it from the Git author name or email.
- **Assignee:** the opener.
- **Reviewer:** the opener. Some forges refuse the author as reviewer; GitHub answers `Review cannot be requested from pull request author`. Report that as `unavailable` with the forge's message and do not substitute anyone else.
- **Labels:** read the repository's existing labels (`gh label list --json name,description`, `glab label list`). Use the mapping a repository rule gives; otherwise pick by the change's main kind and the label's name and description, such as `bug` for a fix, `enhancement` for a feature, `documentation` for documentation-only work. Add every label that clearly applies and none that only might. Never create, rename or recolor labels; when nothing clearly fits, add none and say so.

## Apply and read back

Create the request first, then set metadata in separate calls so a metadata failure can never fail or repeat the creation:

```text
gh pr edit <request-url> --add-assignee <opener> --add-label <label>
gh pr edit <request-url> --add-reviewer <opener>
glab mr update <iid> --repo <base-repository> --assignee <opener> --reviewer <opener> --label <label>
```

Other forges use their documented API fields for assignees, reviewers and labels. Read the request back and report the assignees, reviewers and labels it actually shows. A failed or refused metadata write leaves the request created: report which field did not apply and why, without retrying creation.
