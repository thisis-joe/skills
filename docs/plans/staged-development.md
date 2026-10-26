# Staged development implementation plan

Spec: [accepted contract](../specs/staged-development.md).
Base: `0839e35fc346187a1525390c0c26c220135817fd` (remote main, including recent latency work).
Branch: `feat/coco-staged-workflow`.
Worktree: `/Users/Joseph/.codex/worktrees/coco-staged-workflow/skills`.
Starting checkout: `/Users/Joseph/workspaces/skills`, `docs/release-note-project-install`,
`431c77303bbc648dffb7c406e54e4c2e63a1468b`, clean; preserve it unchanged.
Single writer, continuous authorized execution; separate fresh-context evaluation/review.

This file is the authoritative task-state owner. Commit IDs are recorded after
actual commits, using the next work-unit commit to persist the previous receipt.

| Task | Depends on | Acceptance and verification | State / commit |
| --- | --- | --- | --- |
| W1 Specify and freeze evaluation | — | S1–S10 mapped; immutable baselines and scenarios described before runs | complete / `cbf8994` |
| W2 Apply stages and transition rules | W1 | Entry/shared/advanced instructions agree; provenance retained; targeted checks and meaningful policy probes | complete / `243a406`; follow-ups `fbe87ea`, `dadacf0`, `1ef82e7` |
| W3 Build isolated evaluation support | W2 | Pinned 0.2.0, candidate and no-skill projects; independent CLI/HTTP checks; no external publication; negative checks | complete / `d71331a`; driver follow-up regression fixed after first execution |
| W4 Execute comparative scenarios | W3 | At least five matched scenarios per arm, real artifacts/actions, separate pairwise results and explicit limitations | complete / `aef867d`; 18 primary trials + directed policy/report follow-ups; frozen comparison `fbe87ea` |
| W5 Independently review and close | W4 | Resolve fresh review; required repository checks; isolated install/readback; starting checkout preserved | complete / [independent closure review](../evaluation/staged-development/final-review.md); 133 tests/validator passed; final documentation commit records closure |

## Work units and checkpoints

- W1 saves the specification/plan before maintained procedures change.
- W2 changes common/conditional rule owners, core entrypoints, discovery and user
  guide; keeps specialist operational bodies, source evidence and registrations.
- W3 freezes organic inputs and a source-independent correctness rubric. Keep the
  scorer and variant identity outside candidate directories. Each project has
  its own Git identity/branch, data and command evidence; no shared writers.
- W4 exercises a clear static edit, a small CLI feature, a regression fix, a
  multi-step stateful feature, and boundary/recovery work. Capture requests,
  synthetic user answers, actual files/commands, commits, question categories
  and execution time. Native independent contexts are preferred; any unavailable
  or translated part stays explicit and does not become a passed claim.
- W5 reviews the frozen diff/acceptance without the author's explanation. Only
  affected checks repeat after a fix. No push, PR, merge, release or deployment.

## Baselines and claims

- COCO 0.2.0 version-change commit: `feb3beb36f74ac62104838444d430f00c4eab264`.
  Registry lookup after W1 found the actual published `gitHead` is
  `256c88073a1bfa858c6221197959d6ad1d7d8a5c`. Use the registry tarball with
  its SHA-512 integrity as the comparison source, rather than an arbitrarily
  chosen same-version Git tree; retain both identities and lookup evidence.
- No-skills arm: same task, project rules, inputs, checks and capabilities, without
  loading COCO procedures. Do not grade it down merely for lacking COCO documents.
- Candidate: freeze actual active file hashes at the W4 boundary, record repairs
  and reruns separately. Do not rewrite initial failures or compare moving trees.
- Report outcome accuracy independently of process conformity. Single matched
  cases permit bounded observations, not general speed/quality superiority.

## Recovery and limits

Read this plan, actual commits and retained evidence before resuming. A failed
required check blocks dependent completion. Independent permitted work may
continue. Use temporary destinations for installation; update an existing user
installation only through its supported ownership-preserving installer when
authorized. Keep this worktree and branch for review.
