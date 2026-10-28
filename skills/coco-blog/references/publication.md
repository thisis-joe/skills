# Prepare and verify the actual publication

Read for publication preparation, authorized Git/forge actions or requested deployment checks. Use the profile from [project discovery](project-discovery.md) and preserve user/project action ownership.

## Content and build checks

Reread the exact post and metadata. Preserve drafts until the author accepts the content and the request permits a public transition. Verify required fields and renderer/date/timezone behavior; drafts and future dates may be excluded from normal builds.

Run discovered validation and preview/build commands rather than invented stack commands. Check the intended output path and representative rendered content, metadata, links and images. Confirm private notes, internal links and source tracking are excluded. Record passed, failed and unavailable results separately.

Use the approved image destination and filenames. Uploads need authorization; do not choose another public host silently. URL syntax does not prove loading or public suitability. For read-only source builds processing images, discover writable cache as well as output locations instead of making the source writable or removing checks.

## Scoped Git and request preparation

1. Confirm content base, source branch, worktree state and authorized action. For local-TIL posts use [workspace separation](workspaces.md): the skill creates the isolated publication worktree and branch. Stage only the explicitly selected public post Markdown files. Do not stage raw notes, conversation logs, application changes, private tracking, images or site configuration. If a discovered helper requires other files, choose a compatible public-only preparation path or resolve the scope before using it.
2. A draft/review request permits preparation. Commit/push permission does not imply PR/MR creation, merging or deployment. Human-owned request creation remains so until explicitly changed by the user.
3. A general development-branch publisher may integrate dev/develop and create a request by default. Do not invoke it unchanged for an orphan/unrelated content base or push-only task. Use the verified consumer workflow and write destination; never combine histories to fit a helper.
4. For an authorized push, run required checks, commit selected work, push the confirmed work branch normally and reread its remote ref. Inspect or neutralize inherited push options that could create an unauthorized request. Do not publish a temporary post to test permissions.
5. Read the actual PR/MR template from its authoritative repository/ref even when the content branch lacks it. Fill from the actual diff and check results, with truthful boxes. Use only real linked issues; leave unresolved fields visibly unlinked instead of inventing keys or closing unrelated issues.
6. Return title, body, source, target and verification when the human creates the request. If creation was explicitly requested and supported, create the requested state, verify source/target/head, and follow the runtime's attachment convention. A prepared body or creation link is not an existing request.

If push succeeds but request creation/readback fails, report partial success. Do not circumvent an authentication-origin/access rejection through another browser or hidden API. Continue independent permitted preparation and identify missing access. Never request tokens in chat or print credential files.

## Merge, build and public evidence

Merge and publisher triggering retain their own authorization and ownership. Describe the next human action when only preparation was requested. Pushing a work branch does not establish content-base integration or public visibility.

For requested verification correlate the merged source revision, actual trigger, publisher result, output destination/revision and public page when accessible. Local build success, an organization/repository rename, queued work or an unrelated green build do not prove this post was deployed. A polling interval is not exact publication latency.

Check the public URL and title/body/author, relevant images and links. Read logs only within available authority and redact private details. If CI is inaccessible, separate observable public content from an unverified revision/trigger link. A valid no-op is not a newly published article.

## Handoff

Distinguish local draft, author-reviewed content, checks/build, commit, confirmed push, request body/request URL, merge, publisher result and public observation. Give the smallest next action and its owner. Do not mark tracker work complete merely because a draft or request body exists.

## Invocation-based local-note selection

Support explicitly selected untracked local notes without requiring a Git source ref or candidate marker. Follow [the local-note workflow](local-notes.md) for recent-note discovery, single/multiple selection, iterative author questions, reviewed public-only output and the author-owned draft release. Start on skill invocation; note creation must not produce a blog-writing offer. A bare invocation opens the note list, not a generic request menu.
