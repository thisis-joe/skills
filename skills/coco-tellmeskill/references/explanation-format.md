# Common explanation format for every skill

Use this format for COCO, system, plugin, and every other target. Simple and detailed explanations use the same heading and eight items in the same order. Do not substitute a different heading, merge items, or omit them. The labels below are English reference labels: translate them, the mode name, and all explanatory text into the user's language while preserving their meanings and order.

## Output format

**<exact skill identifier> — <simple explanation or detailed explanation>**

**Purpose:** The problem this skill solves and its role.

**When to use:** Requests or situations that actually fit it.

**Inputs:** Required user information, targets, and existing material.

**Workflow:** Main steps, decision criteria, and necessary choices.

**Output:** Deliverables or judgments the user receives.

**Example:** One correct invocation with a concrete request in the current runtime's syntax (`$name` in Codex, `/name` in Claude Code), preserving the exact catalog identifier and namespace.

**Cautions:** Actual dependencies, support conditions, execution/authority boundaries, and unverified information.

**Source:** A clickable absolute path to the `SKILL.md` read and any necessary linked material.

## Depth by mode

| Mode | Depth |
| --- | --- |
| Simple explanation | One line per item. Summarize only the main flow under Workflow. Give one example. |
| Detailed explanation | Expand within the same eight items as needed. Under Workflow, specify main stages, branches, and stopping conditions; under Output, deliverables and completion criteria; under Cautions, confirmed constraints. Explain one example. |

If the source does not provide information, write the user's language equivalent of "Not specified in the source" in that item. If inapplicability is confirmed, write "Not applicable — <reason>." If reading fails, state under Cautions that guidance uses only the catalog because the source could not be read, and record the inaccessible location and state under Source. Retain all items in every case; do not fill gaps with guesses.

This format applies only to **explanations of the selected skill**. It does not change that skill's deliverable format when it is subsequently executed.
