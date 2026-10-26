"""Inert sandbox-only proposals; never write the repository's active skills."""
from pathlib import Path

CHANGED = {
    'R5': ['_coco-shared/advanced/clarify.md'],
    'R2': ['_coco-shared/workflow.md'],
    'R7': ['_coco-shared/workflow.md', 'coco-start/SKILL.md'],
}


def replace_once(path, old, new):
    text = path.read_text()
    if text.count(old) != 1:
        raise ValueError('Expected exactly one proposal anchor: ' + str(path))
    path.write_text(text.replace(old, new, 1))


def apply(root, variant):
    root = Path(root)
    if variant == 'R5':
        path = root/'_coco-shared/advanced/clarify.md'
        replace_once(path, '| A material outcome or constraint is missing | Focused interview | Ask the next decision only |',
                     '| A material outcome or constraint is missing | Focused interview | Map the current slice and ask its ready material choices |')
        replace_once(path,
            'This is the default for a missing decision; an explicit grill or stress-test request uses grill mode below instead.\nAsk one focused question with a recommended answer and its concrete tradeoff.',
            '''This is the default for a missing decision; explicit grill keeps its separate full-tree procedure below.
Before product implementation, show a short frontier: agreed behavior, open choices
that can change this slice's observable results, and reversible details you can choose.
Use the actual input/output examples to find boundary cases and hidden coupling;
do not substitute a universal checklist for the domain. Put this frontier in the
existing specification or plan, never a third tracker or a mandatory extra round.
For each ready material choice show a concrete counterexample, understandable
alternatives, their effects and your recommendation. Ask those choices before coding;
explicitly defer choices that affect only later slices. Offer the existing further-
question preview or adoption of displayed recommendations. Automatic technical
progress does not adopt an undisplayed business default.''')
    elif variant == 'R2':
        path = root/'_coco-shared/workflow.md'
        replace_once(path, '## Manual and automatic basic transitions',
            '''For continuation of the same feature, inspect its existing saved specification
and sole execution plan first. Update adequate files in place at scope changes
and pickup. Keep the original expectation and a superseding decision with its
reason in the specification; link that decision from the execution plan instead
of copying the contract into another tracker or checkpoint document. The plan
owns current completed/pending work, next action, commits and evidence pointers.
Preserve usable provenance and the original/actual/reason comparison in the final
report. A genuinely new feature may still need its own specification and plan.

## Manual and automatic basic transitions''')
    elif variant == 'R7':
        path = root/'_coco-shared/workflow.md'
        replace_once(path, '## Manual and automatic basic transitions',
            '''When a user explicitly already saw the introductory map and asks for a next
step, lead with the current stage and one primary recommended skill, its purpose,
expected result and a usable request. Reference the overview when needed or asked
instead of repeating its ten-row inventory. Preserve initial four-stage/ten-skill
orientation, explicit full-catalog requests, applicable specialist discovery and
the manual awareness pause. A recommendation still does not execute itself.

## Manual and automatic basic transitions''')
        replace_once(root/'coco-start/SKILL.md',
            'Read the [common contract]',
            'For a returning next-step question, use the repeat-guidance condition in the shared workflow.\n\nRead the [common contract]')
    else:
        raise ValueError('Unknown sandbox proposal: ' + variant)
