# Simplify slug formatting while retaining live legacy consumers

Public behavior to preserve: trim/lowercase whitespace-separated text and join words with `-`; empty input returns empty string; Unicode letters survive lowercasing; `None` raises `ValueError('slug requires text')`. No new accepted input type, error, side effect or ordering change is authorized. The fixture is pure, so product timing/side effects outside it remain unknown.

Inventory found a direct legacy helper, canonical `slug`, `runtime-config.json` selecting `legacy_slug`, and `dynamic-caller.py` resolving the configured string with `getattr`. A symbol-only direct-call search would miss this caller. The runtime-config path is still active in the check.

Smallest proposed simplification: let one canonical implementation own formatting and have the temporary legacy public name forward to it while real consumers move. This removes duplicated rules, not a promised permanent abstraction. Do not delete the legacy name yet. Migrate the configured string, generated bindings, runtime registry and any independently deployed/other-language callers; use expand/migrate/contract where they cannot move atomically.

Local public-boundary expectations are hard-coded for empty, whitespace, Unicode and error cases. Both helpers match them in the fixture. Removing `legacy_slug` from a scratch namespace made the real configured consumer fail; restoring it made that consumer pass. Passing equivalence examples do not prove unknown product behavior. No repository helper was replaced or deleted.

Actual deletion gate: all known runtime/config/generated/cross-language consumers are migrated and run under the canonical interface; active legacy resolution is measured zero through the actual deployment/retry/replay window; ownership confirms remaining strings are inert; compatibility obligations are met; the legacy-name removal itself passes public behavior and integration checks on the final snapshot. Then remove obsolete adapter/config/docs/tests of removed internals while retaining required behavior tests. A date or empty static search alone is insufficient.

Record dynamic usage owner and window before implementation. If one transaction/release cannot cover these consumers, retain the real compatibility need explicitly and route migration. The observed deletion failure, restoration and four boundary cases are in `evidence/observations.json:simplify`. Build owns any product refactor commit and final current-scope review.
