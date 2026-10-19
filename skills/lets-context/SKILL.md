---
name: lets-context
description: "Use when preparing a handoff, resuming work after interruption, managing context limits, recalling task history or maintaining a long-run decision trail. 인수인계·맥락 관리·재개."
license: MIT
---

# let's-context

Preserve the minimum truthful context required to resume work safely.

Read the [common contract](../_lets-shared/contracts.md) before acting. Load [advanced modes](../_lets-shared/advanced/context.md) only when the task needs their additional procedure. The [integration decisions](../_lets-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Anchor the task identity and permitted scope, current branch/commit, authoritative artifacts and actual outstanding work. Inspect current state before trusting an older summary.
2. Load only the context needed for the next action. Prefer pointers, relevant sections and stable contracts over copying entire transcripts or source trees.
3. Keep a compact handoff: objective, decisions/constraints, completed commits/evidence, pending work/blocker, next command and authority boundaries. Include unavailable evidence and abandoned directions that still constrain work.
4. For long runs keep one decision trail of significant what/why/evidence/result events, not every keystroke. On resumption read recent entries and reconcile with Git and task status; do not silently rewrite history.
5. Recall only task-authorized history/artifacts. Distinguish remembered claims from current evidence; no cross-project private-history globbing or source-specific transcript paths.
6. Profile-only forensics uses derived metadata and citations without copying unrelated private content. Cross-tool handoff adapts to available capabilities rather than forcing a particular model or agent product.

Return: compact resumable packet or evidence trail, current verification limits and next permitted action.
