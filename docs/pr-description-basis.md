# Default PR/MR description basis

`coco-push` uses this default description when a repository has no PR/MR template ([pull-request.md](../skills/coco-push/references/pull-request.md#default-description)). The research table below moved here from that procedure so the push hot path does not reread it on every run; the decision record row "Push-only publication versus opening a review request" points here.

The structure comes from forge and engineering guidance researched on 2026-10-20. The sources agree on what every description needs and differ on the rest, which is why checklists are left to repository templates:

| Section | Basis |
|---|---|
| Summary | Every source: what and why, leading with the problem and resulting behavior ([Google CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html), [GitHub reviewer guidance](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/helping-others-review-your-changes), [GitLab `Default.md`](https://gitlab.com/gitlab-org/gitlab/-/raw/master/.gitlab/merge_request_templates/Default.md)) |
| Related issue | Near-universal: Google, GitLab, [Kubernetes](https://raw.githubusercontent.com/kubernetes/kubernetes/master/.github/PULL_REQUEST_TEMPLATE.md). Jira links a request through the key in its title ([Atlassian](https://support.atlassian.com/jira-software-cloud/docs/reference-issues-in-your-development-work/)) |
| Changes | Kubernetes "What this PR does", [Angular](https://raw.githubusercontent.com/angular/angular/main/.github/PULL_REQUEST_TEMPLATE.md) current versus new behavior |
| Verification | GitLab "How to set up and validate locally", [React](https://raw.githubusercontent.com/facebook/react/main/.github/PULL_REQUEST_TEMPLATE.md) "How did you test this change?" |
| Reviewer notes | GitHub reviewer guidance, Kubernetes reviewer notes, Google's known shortcomings, [Atlassian](https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests) guiding the reviewer; the sync record is specific to `coco-push` |
| Risk and rollback | Conditional: Angular and [Home Assistant](https://raw.githubusercontent.com/home-assistant/core/dev/.github/PULL_REQUEST_TEMPLATE.md) breaking-change sections, and `coco-ship`'s rollback criteria |
| Screenshots | Conditional: GitLab requires them for UI, and Atlassian recommends them for front-end changes |
