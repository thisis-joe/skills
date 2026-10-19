Before applying this mode, read the [verification core and selection](verify.md) and apply its common contract and cumulative selection rules. Loading a mode does not expand the requested scope or authorize execution.

## Create a runtime verification helper

Use when asked for a reusable project driver or when the authorized work includes establishing missing verification support.
Interview the repository for primary/secondary surfaces, startup, usable readiness, authentication, fixtures, drivers, evidence, and instance isolation.
Establish that the baseline builds and starts before writing instructions against it; report a broken base precisely.
Write a project-local helper/skill using supported project conventions, with registering metadata when the runtime requires it.
Give the next cold reader exact commands and paths, with no placeholders:

- **Launch:** build/start, migrations, seed data, readiness of a usable instance, and owned teardown.
- **Doctor:** read-only target/build/owned-port/auth/session health checks before driving and after surprise.
- **Drive:** real user actions through the existing driver and stable handles, plus independent reset.
- **Evidence:** action, result, relevant side effects, proof standards, and retained artifact locations.
- **Cleanup:** owned sessions and scratch data only; never proof or user work.
- **Helpers:** executable scripts with their documented invocation, inputs, outputs, and failure behavior.

Seed an indexed feature map for the discoverable primary journeys, initially the most important few.
For each feature record subfeatures, user-visible route, concrete drive recipe, states/preconditions, success observation, and gotchas.
Retain alternate mapped entrypoints and load-bearing states; proving one convenient route does not cover the rest.
Do not freeze internal file paths as the user's navigation path or weaken a journey when seed data is missing.
Run launch, doctor, one mapped journey, capture, cleanup, and evidence-existence checks as a cold reader would.
Clean failed attempts too. A helper never executed is a draft; list stand-in setup that remains unverified on the real target.

