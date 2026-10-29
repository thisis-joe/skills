# Session TIL capture

Base: `04507c149787c9792bfedd1cd8f1f65dd2c59a6a`. Original behavior: coco-learn offered explanation, notes, review and mission-led teaching, storing notes under the current worktree. The user requests coco-til: immediately capture current-session knowledge, with at most three concepts per meaningful topic, always using the primary checkout's TIL in Git repositories.

## Contract

- Bare and explicit TIL capture requests run without candidate/save selection. Use only visible session evidence and directly relevant sources; zero worthwhile concepts means no filesystem changes.
- Group meaningful topics; select zero to three reusable, evidenced concepts per topic. Do not invent topics or filler to increase output. One concept per note; merge semantic duplicates, update existing notes only for new information, and make repeated capture a no-op when nothing changed.
- Keep the exact note schema, translated template sections, budgets, index and checker. New notes start as learning, never inferred understood.
- Resolve the primary working tree through Git metadata, independent of branch name. Never fall back to a linked worktree when resolution or writing fails. Outside Git, use cwd/TIL. Preserve existing notes and conflicting user content.
- Ignore TIL at the primary checkout; never commit notes. Keep code investigation at its actual source checkout and record repository-relative source, symbol and revision (or uncommitted state), not temporary absolute paths alone.
- Remove explanation/review/mission modes from this entrypoint. Preserve frozen upstream facts, and explicitly record the narrower adoption. Align registration, UI, callers, blog note discovery and tests. No remote publication.

## Acceptance

Real temporary repositories prove primary and linked invocations share a destination, notes survive linked-worktree removal, missing/bare primary and escaping symlinks fail without fallback, and non-Git behavior remains local. Existing checker cases prove format preservation. Scenario review covers sparse/empty sessions, selection limits, semantic duplicates and repeated capture. Run package validation, all unittests and isolated installer migration/readback.
