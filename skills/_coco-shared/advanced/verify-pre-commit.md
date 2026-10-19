Before applying this mode, read the [verification core and selection](verify.md) and apply its common contract and cumulative selection rules. Loading a mode does not expand the requested scope or authorize execution.

## Conditional pre-commit verification setup

Use when asked to establish commit-time formatting, typechecking and tests.
Inspect the existing hook runner and preserve it; adding a second runner is not the default.
Corroborate the package manager and lockfile with CI and discover actual formatter/typecheck/test scripts.
Use [security](security.md) for new dependency script approvals and install only within requested scope.

For a JavaScript project explicitly choosing Husky, add reviewed development dependencies
`husky`, `lint-staged` and `prettier` with its pinned manager, and initialize the supported Husky version.
Merge its prepare hook with any existing `prepare` behavior; do not overwrite another setup command.
Reuse the existing Prettier configuration. Create defaults only if no project formatting policy exists.
Configure lint-staged for supported staged files; one concrete rule is
`{"*": "prettier --ignore-unknown --write"}` when that matches the project policy.
The pre-commit runs the manager's lint-staged command first, then its existing typecheck and test scripts.
If a script does not exist, omit the invented command and explicitly report that missing check.
Use the chosen hook runner's current executable/shebang convention rather than an obsolete copied header.

Verify the configuration and hook locally in an isolated Git fixture: stage a disposable supported
file, run lint-staged, confirm only the intended staged content is formatted, and exercise a real
temporary commit through the hook. Demonstrate a failing check blocks that fixture commit.
Use the manager's real commands; never use `--no-verify` to call the smoke test successful.
Keep unrelated user index/worktree changes intact and do not stage them as test inputs.
Return owned hook/config changes, observed pass/fail behavior and unavailable checks to build;
the requested project changes receive the normal reviewed work-unit commit.
