# Optional Graphify code navigation plan

Contract: [Optional Graphify code navigation](../specs/graphify-navigation.md).

Work started on `feat/graphify-navigation` from `8705060749cd3d5e7f6c6d63e9c8a07da2f3cdfa`. This plan records local task status.

## GF-01 — Apply and evaluate review navigation

Status: completed in `f1342f7`. See the [comparison record](../evaluation/graphify-navigation.md).

Added a shared reference and a conditional link from the review impact mode. Compared targeted direct search with Graphify-assisted source verification and checked fresh, missing, and stale indexes in isolated copies. The initial rollout kept the review pilot for further evaluation.

## GF-02 — Connect the remaining scoped consumers

Status: closed without adoption. The command and Codex session comparisons did not demonstrate lower overall exploration cost.

The proposed consumers were runtime mechanism research, post-reproduction debugging, and build's caller migration guidance.

## GF-03 — Retire the review pilot

Status: completed. Restored the original review procedure, removed the pilot reference, and preserved the measurements and decision. An upgrade of each isolated pilot installation removed the obsolete reference and restored the review procedure in Codex and Claude Code.
