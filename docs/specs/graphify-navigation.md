# Optional Graphify code navigation

This document records the original pilot contract. See the [work plan](../plans/graphify-navigation.md) for its disposition.

COCO may query a prepared local Graphify index belonging to the application repository under inspection when locating callers or dependencies across files. The project owns its index and its update policy. The consumer workflow uses read-only queries and follows repository instructions and tool permissions.

Start with the impact and safety-fact mode of `coco-review`. Resolve the comparison and inspect the actual changes before using the graph to locate candidate source. Check the index against the worktree and revision being examined, including relevant local changes. Use direct search when index provenance or freshness is uncertain, the tool is unavailable, or results are missing or insufficient. Inspect the relevant source and tests to substantiate findings and search the comparison revision for removed or renamed symbols when needed.

The rollout starts with review. Connect research, debug, and build after a paired application comparison demonstrates reduced exploration cost without missing any required source-backed impact facts. Reuse the guidance only at their respective multi-file relationship tracing steps. Simple lookups, bare topic orientation and the existing review scope and evidence requirements retain their established behavior.

## Acceptance

- A suitable prepared index can narrow a review to source locations that establish the required impact facts.
- With a missing or stale index, review reaches the necessary source evidence by direct search without generating or refreshing artifacts.
- Compare the same real application change and evidence rubric with direct search and with the prepared index plus source reads. Record revision, tool version, surfaced facts, measured output size and elapsed time, and index preparation cost separately.
- Confirm that Codex and Claude Code package installations include the shared reference and resolve the active links. Run the repository validator and full unit suite.
