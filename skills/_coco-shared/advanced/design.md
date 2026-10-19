# Design procedures

Apply the [common contract](../contracts.md). Use [research](research.md) for uncertain mechanisms or lineage and [spec](spec.md) for the resulting behavioral agreement.

## Input and scope

Retain the user/caller outcome, existing interfaces, domain vocabulary, relevant decisions, observed friction, compatibility limits, test seams and reversibility. Reuse settled requirements. Select contract design, architecture survey, alternatives, disposable prototype or optional boundary enforcement; combine only modes needed to resolve the uncertainty.

## Ground and model

1. Trace the actual caller path and state ownership before sketching. If ownership or layering changes, establish historical constraints too.
2. Write a caller usage example first. Derive the smallest useful types, operations and ownership from that usage.
3. Model access patterns and invariants before adding branches: a state machine, discriminated union, registry, reducer or collection may remove invalid states and duplicated policy.
4. Group a module around domain knowledge it owns, rather than repeated load/validate/transform/save phases. Keep ordinary local code when an abstraction removes no real complexity.
5. Give mutable state one owner. Before actors share it, ask what another actor's simultaneous mutation changes; prefer isolation before locks or serialization.
6. If a new requirement causes repeated workarounds, reconsider the shape as though the requirement existed on day one. Redesign only the affected scope.

## Deep interfaces and dependency strategy

An interface includes types, ordering, invariants, errors, required configuration and relevant performance behavior. Depth means capability hidden per unit of caller knowledge, not an implementation-to-interface line ratio.

- Apply the deletion test: would deleting the module redistribute real complexity to callers, or merely remove a pass-through?
- Keep representation, storage/wire shapes and private phases behind the interface. A deep module is not a deep call chain.
- Test observable behavior through the caller-facing seam. Internal seams can remain private.
- In-process computation needs no adapter. A locally runnable dependency can use a real local stand-in.
- An owned remote dependency can use production transport plus an in-memory adapter; an uncontrollable external dependency may use an injected mock adapter.
- Justify a port with actual variation, commonly production plus test adapters. A single hypothetical adapter is avoidable indirection.
- When deepening replaces shallow modules, replace obsolete internal tests with interface behavior coverage rather than stacking redundant suites.

## Public contracts and retry safety

1. Define input/output shapes separately, consistent error semantics and observable ordering. Existing consumer conventions override aesthetic naming preferences.
2. Treat observable quirks as potential consumer contracts. Prefer compatible additions and one converged interface; plan caller migration before removal.
3. Parse untrusted user, external-service, configuration and storage-boundary data into domain types. Do not duplicate validation between trusted internal functions.
4. Specify pagination/filter behavior for growing lists and whether partial updates preserve absent fields. Document unsafe-to-retry mutations explicitly.
5. For idempotent effects, use one intent key stable across retries and different for distinct intents. A new UUID/timestamp per retry does not provide idempotency.
6. Claim the key atomically using an enforced uniqueness mechanism before the effect; compare a stored request fingerprint and reject key reuse with a different payload.
7. Decide duplicate-in-flight behavior: conflict, bounded wait, or pending status. Never retry the effect merely because the first attempt seems stuck.
8. Persist intent before calling out and distinguish success, failure and unknown outcome. A timeout does not prove the side effect failed.
9. Retain keys beyond every allowed redelivery path, including delayed replay. Verify race, crash-window, mismatch and unknown-outcome behavior where consequential.

## Type discipline

Use schema-derived types when a schema owns the shape. Parse external values as unknown; a type guard must verify the claim it makes. Prefer discriminant narrowing, exhaustive handling and checked construction over casts or optional-field bags.

Give semantically different IDs distinct validated types. Use nonempty/range/variant shapes when looser types force assertions or impossible-case throws; keep simple total types otherwise. In TypeScript, preserve literal inference with checked conformance and derive from authoritative types before hand-maintaining parallel interfaces. A production cast needs a verified reason, not a compile-error bypass.

## Architecture opportunity survey

1. Scope to a named pain point or history hotspots, then read relevant glossary/decisions.
2. Look for scattered understanding, shallow pass-throughs, information leakage, hand-synced lists, split state ownership, importable internals and tests missing real caller patterns.
3. Present each candidate's files, concrete friction, consolidation idea, dependency category, test impact, before/after shape and recommendation strength.
4. Flag an existing decision conflict only when evidence warrants reopening it. Record durable rejection reasons so the same unsuitable idea does not recur.
5. Choose the candidate before designing a detailed interface. A temporary visual report is optional; generated reports must not require unsafe scripts or remote CDNs.

## Alternatives and synthesis

For consequential novel architecture or interaction, compare at least two structurally different candidates; local precedent can make a single modest change sufficient.

1. Freeze a shared brief and 3–6 concrete criteria before generation. Use separate writable targets for independent candidates.
2. Vary real constraints: minimal interface, common caller, flexibility, or cross-process dependency strategy. Color/copy changes are not distinct designs.
3. Compare usage, full contract, hidden complexity, leverage, locality, seam placement and tradeoffs criterion by criterion.
4. Read every completed candidate. Reconcile disagreement from evidence, choose one coherent base, and adopt only useful compatible ideas from alternatives.
5. No graft is required when candidates converge; wild divergence means reframe the brief. Record rejected options, dropouts and the synthesis rationale.

Delegation is optional and authorized, with a sequential fallback. Implementation friction, repeated casts, unexpected shared state or callers learning internals are reasons to revisit the sketch, not silently stack exceptions.

## Disposable prototype mode

State the single question and mark artifacts disposable. Keep them trivial to run, in memory by default, with no real mutations. Scratch persistence is allowed only when persistence itself is the question. Prototype speed does not lower the later shipping quality bar.

- **Logic:** one portable HTML demo with an isolated pure model, readable relevant state after each action, free-play controls and tabbed deterministic awkward-case walkthroughs. Keep DOM code outside the liftable logic.
- **UI:** prefer variants inside the existing populated page, retaining data/auth context. Use about three structurally different renderings selected by a shareable URL parameter and a clearly experimental switcher. Preserve keyboard input behavior and hide prototype controls in production.
- Use a new clearly marked route only when no sensible host exists. Stub writes; do not evaluate a layout by accidentally changing production data.
- Capture the question, verdict and full prototype as a separate primary-source artifact/branch when useful. Main retains the validated decision and properly built winner, not losing variants or the demo shell.

## Optional TypeScript package-boundary recipe

Use only when the repository chooses this experimental convention. Each package root file is a public entry point; nested folders are private. Implementation can import within its package; tests use entry points plus their own fixtures; outsiders cannot import internals or fixtures; reject cycles.

Detect package manager/root, merge the existing boundary-check configuration, preserve capture-group same-package exceptions and wire the rule into the established check command. Prefer several small entry points over a giant barrel. Do not add path aliases or move the repository merely to fit the recipe.

Prove clean pass → temporary forbidden test deep-import failure → restored pass. Document the convention beside the packages with one discovery pointer. A proposed scaffold/example is optional, and absent tool support is unavailable enforcement, not a passing result.

## Output and stopping conditions

Return the chosen caller example, interfaces/types, ownership, dependency/test strategy, alternatives and reasons, compatibility/migration implications and unresolved decisions. Update domain terms or qualifying ADRs using [document](document.md), not a duplicate design checklist.

Stop when the design resolves the stated uncertainty and its contract can be implemented and verified. A requested design-only deliverable ends here. A missing material product decision or repeated structural contradiction requires that specific decision/re-grounding; routine implementation can proceed within existing authorization through build.
