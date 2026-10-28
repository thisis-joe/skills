# Prepare the publication workspace from a development checkout

Read when drafting or preparing Git delivery from a development checkout. A developer commonly invokes this skill on an application feature branch based on develop. The skill owns publication-workspace preparation; the developer does not need to switch branches or create a blog branch manually.

## Capture source context

Record the original absolute worktree root, current branch and HEAD, staged/unstaged status and selected local note paths before any runtime directory change. Preserve this source context across turns. Read the original repository instructions and branch naming rules; discover the actual publication remote/ref and content conventions. Do not infer the publication base from the current feature branch or its develop ancestor.

Dirty development files are expected and are not a reason to stash, reset, clean, commit or abandon the checkout. Do not write the public draft into its application tree or index. Keep source notes and conversation state local. Carry the author's settled facts and choices forward in the same conversation; transferring context means writing an edited public article, never copying a chat transcript into Git.

## Prepare the target yourself

1. Verify the publication ref and refresh that remote-tracking ref through the configured Git remote when access is available. If unavailable, report freshness and continue independent local drafting; do not silently use develop or an unverified stale ref as the publication base. Missing or ambiguous publication configuration needs clarification only for dependent actions.
2. Inspect registered worktrees and branch ownership. Reuse a suitable workspace belonging to this post only if its base and changes are understood. Do not commandeer another task's checkout, reset an existing branch, force a checkout or replace an occupied directory.
3. Choose a unique work branch using the consumer's naming convention and the post's topic. Use a confirmed issue identifier if the convention requires one; never invent it. Create the worktree from the refreshed publication ref, never the application feature HEAD. Use managed worktree tools when appropriate; if they create a detached checkout, create the topic branch inside that new checkout. A CLI equivalent is `git -C <source-root> worktree add -b <post-branch> <new-path> <publication-ref>` with each value passed as one argument. This is local preparation, not commit/push authorization.
4. Use the returned target path explicitly for subsequent post tooling and Git commands. Keep reading selected notes by their saved original absolute paths. For an orphan publication branch, separate history is intentional; do not merge/cherry-pick develop, the feature branch or application commits to obtain notes.
5. Create only the public manuscript under the target content root with draft state retained. A compatible helper may take a separately reviewed public manuscript; it must not import private notes or require committed source TILs. Keep temporary input, interview records, caches and provenance outside the publication tree. If no helper fits, write the Markdown directly using project metadata and run the discovered checks. Preserve an existing author's post and reconcile changes deliberately.

If local workspace creation fails, keep the conversation and draft local, identify the actual blocker, and do not ask the developer to perform a routine branch setup that the skill can complete itself. Do not change their active checkout as a workaround.

## Markdown-only Git delivery

The local-TIL route delivers selected public post `.md` files only. Reuse approved public image URLs; image uploads or site/tooling changes are separate actions. Do not include private tracking records to satisfy a legacy importer; choose a compatible route. Drafting, accepting wording and creating a local worktree do not authorize commit or push. Reuse explicit delivery authorization if already present; otherwise return the draft and next owner.

Before an authorized commit, inspect the target branch's commits/diff against the confirmed publication base and its index. Only the intended public post Markdown may be included. Unexpected application commits, unrelated staged changes or other file types must not enter the delivery. Do not unstage or discard another person's work; resolve the workspace instead. Stage exact owned paths with `git add -- <post.md> ...`, never a blanket add, and inspect the staged diff. Commit only when authorized. Before an authorized push, verify outgoing commits still contain only intended post files, neutralize inherited request-creation push options, and push the topic branch normally to the confirmed remote. Never push directly to the publication branch or force-push it.

Preserve request ownership: supply the actual repository MR/PR body with the publication branch as target when the human creates the request. Do not create an MR merely because a work branch was pushed. The draft remains excluded from public builds after integration until the author explicitly releases it through the project's draft-state change and normal integration path.

Finally check the original checkout's branch, HEAD, index and relevant dirty/source files against the initial state. Report original and target paths/branches, draft path, actual Git actions and remaining owner. Do not delete a worktree containing an uncommitted draft or unpushed work.
