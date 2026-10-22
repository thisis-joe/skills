---
name: coco-frontend
description: "Use when building or changing browser UI behavior, visual hierarchy, responsive states, interactions or accessibility."
license: MIT
---

# coco-frontend

Deliver the intended user experience within the existing visual and interaction system.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for a new screen or open visual direction, component state ownership or optimistic updates, accessibility verification (focus order, modals, live announcements), the runtime finish gate across supported widths, exact visual parity, and missing browser capability. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/frontend.md) before dependent work.

## Procedure and output

1. Read existing components, tokens, layout and interaction conventions. For a new screen clarify its job, primary action, required states and responsive behavior before implementation.
2. Use visual references to understand hierarchy, density and interaction; translate useful patterns into the product's own design language. Preserve explicit brand and user choices.
3. Define loading, empty, error, success and permission states as relevant, including keyboard/focus behavior and accessible labels/semantics. Keep local state local; make shared contracts explicit.
4. Implement behavior using the build procedure and actual project conventions. A tiny static visual edit needs its relevant check, not a new architecture cycle.
5. Verify in a running browser at relevant viewport/states: layout, keyboard/focus, contrast, console/network and user-flow result. Compare baseline warnings with new regressions; do not expand scope to unrelated inherited defects.
6. If browser evidence cannot be obtained, report that acceptance as unavailable and retain reproducible steps for the next check.

Return: implemented states, relevant screenshots/runtime observations, accessibility checks and unresolved limitations.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "Accessibility is a nice-to-have" or "we'll make it responsive later": retrofitting costs far more; build both in now.
- "The design isn't final" or "it's just a prototype": use the existing design system; prototypes become production.
- Missing loading, empty or error states, or keyboard navigation never tested.
- Color as the only status cue, or inline styles and arbitrary pixel values outside the token system.
- A generic "AI look" (stock gradients, oversized cards, template layouts) instead of the product's visual language.
