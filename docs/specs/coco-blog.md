# coco-blog: public developer writing

## Purpose and source

Add a team-authored COCO skill for selecting development notes, shaping evidence-backed public posts, preparing repository-native publication, and checking an authorized publication. Requirements come from the user's agreed blog workflow and editorial decisions, generalized without private project identifiers. This is not an imported upstream skill; existing source snapshots, checksums and coverage remain unchanged.

## Agreed behavior

- Discover the consumer project's writing instructions, editorial criteria, metadata, source and publication branches, importer, checks, image policy, request template and publication ownership. Reuse settled context and actual artifacts.
- Support candidate discovery, drafting/revision, publication preparation and requested publication verification. A content request authorizes content preparation, not unrelated code changes or external writes.
- Keep source notes intact. Import only explicitly selected public material into the content workspace; preserve hand edits and duplicate tracking. Never merge unrelated development history into a blog branch.
- Accept accomplishments, design decisions, completed features, prevention, automation, troubleshooting and experiments as candidates. Before publication require a concrete first-hand contribution, reasons for choices, and evidence. Measurements are one evidence type; never invent metrics or rationale.
- Shape a post for the intended reader and angle, preserving project category/tag conventions. Ask for missing facts that change the story; retain unmeasured/unverified claims as such.
- Use existing import and check tooling when available. Preserve drafts until the author accepts the content and the requested action permits a public transition. Pattern checks do not replace author review.
- Reuse authorized commit/push scope, but never infer PR/MR creation from a commit/push request. Read the actual request template and confirmed target. Human-owned request creation remains human-owned. Missing issue links remain unlinked, not fabricated.
- Distinguish local draft, author review, validated artifact, committed, pushed, request prepared/created, merged, publisher result and observed public page. Do not equate an address rename, a successful local build or an accepted queue request with deployed content.
- Keep the public package generic. Discover project hosts, paths, credentials identifiers, job names and category values at execution; never embed a private project profile or install user configuration as a side effect.

## Scope

One skill entrypoint, UI metadata and conditional references; registry, routing, documentation boundary and provenance notes. Reuse consumer tooling rather than copying a project-specific importer into COCO. No personal skill installation, package release, new tracker issue, commit, push, PR/MR, or production action is requested for this creation task.

## Acceptance

1. Skill and package validators pass; supporting references are included and resolvable after a temporary installation.
2. Required repository unittest suite passes, with environmental limitations reported separately.
3. Isolated writing exercises preserve their source notes, produce a draft with supported claims, retain the author's choices, and return a repository-template request body without creating an unauthorized request.
4. No private operational identifiers from the originating project enter changed public files; no upstream source file or user installation is changed.
5. The main user checkout remains unchanged; work is isolated on `feat/coco-blog` from `d4599e1`.

## Implementation and verification plan

1. Discover current COCO boundaries and conventions; record this contract.
2. Create concise entrypoint and reader/evidence, project-discovery and publication references.
3. Register the skill and record team authorship; clarify routing against general docs and development-branch publishing.
4. Validate structure, package installation and realistic offline behavior. Fix demonstrated problems without widening the workflow.
5. Run required checks, inspect the final diff and report created source versus actual installation and publication state.

## Development checkout and publication workspace

A developer starts on a feature branch derived from develop. The skill discovers and refreshes the publication ref, creates a separate worktree and topic branch using repository rules, carries the settled public narrative into a draft there, and preserves the original branch, index, dirty files and ignored TIL. Git delivery contains only selected public post Markdown; no application commits, raw notes, conversation logs or private tracking. Commit/push retain explicit authorization and human-owned MR creation remains unchanged. See [workspace separation](../../skills/coco-blog/references/workspaces.md).

## Invocation-based local-note selection

Support explicitly selected untracked local notes without requiring a Git source ref or candidate marker. Follow [the local-note workflow](../../skills/coco-blog/references/local-notes.md) for recent-note discovery, single/multiple selection, iterative author questions, reviewed public-only output and the author-owned draft release. Start on skill invocation; note creation must not produce a blog-writing offer. A bare invocation opens the note list, not a generic request menu.
