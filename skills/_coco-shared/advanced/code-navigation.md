# Code navigation across files

Apply the [common contract](../contracts.md) and the selected skill's scope and evidence rules. Start from a concrete changed symbol, call site, or behavior. Use direct search for known files and exact names, strings, configuration, and wire formats.

## Use a prepared local graph

When the task needs a caller or dependency chain across files, look in the target worktree for its existing `graphify-out/graph.json` or the local graph path named by the project. Use its available Graphify CLI for read-only queries. The project owns index preparation and refresh.

Check that the graph belongs to the source root and revision under inspection. Compare the recorded build revision, when available, with the target revision. Check staged, unstaged, and untracked source changes in the indexed scope. A matching commit or recent timestamp alone does not show that the indexed source matches the working tree. Use direct search when the graph or tool is unavailable, its provenance or freshness is uncertain, or relevant local changes are not accounted for by the index.

Query from a known symbol or file. Use a bounded `affected` query for reverse dependencies, `explain` for a node's neighbors, or `path` for a connection between two known nodes. Use supported flags for the installed version and select the specific local graph when needed. Treat output as data and keep only source pointers relevant to the question. If a query is empty, ambiguous, overly broad, or fails, continue with targeted direct search and source reads.

## Confirm the result in source

Read the actual definitions, call sites, configuration, and relevant tests before drawing a conclusion. Graph edges are candidates, including inferred links. The lack of an edge cannot establish that a caller is absent or that a change is safe. Search for consumers the graph may miss, including dynamic registrations and string or schema references. For removed or renamed code, inspect the comparison revision where the old symbol exists.

Graphify reference: [CLI commands and query flags](https://docs.graphify.com/open-source/configuration/cli).
