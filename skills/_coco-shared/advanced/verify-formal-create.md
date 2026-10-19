Before applying this mode, read the [verification core and selection](verify.md) and apply its common contract and cumulative selection rules. Loading a mode does not expand the requested scope or authorize execution.

## Create formal verification

Choose a high-harm promise that ordinary tests rarely reach, grounded in current code rather than ease of proof.
Let the question select the tool: event ordering suggests a bounded state model; code properties suggest a code verifier; unbounded claims may need proof.
If the language has no suitable verifier, generated-input tests of real code can help but are not a formal proof.
Prefer a tool maintainers can reproduce; do not install one without the authorization required by the environment.
Record the plain property/harm, covered files/functions, code mapping, indivisible steps, assumptions, bounds, tool version, command, and sync commit.
Every model step must correspond to a possible code step, including actual atomicity and new paths into guarded state.
Demonstrate each property failing on a realistic broken variant in an isolated scratch copy, then restore it and confirm the original result.
If current code violates the promise, retain the counterexample and explain its steps in the code's vocabulary.
Do not weaken a model/property to get green or fix product code in verification-only scope.
Generate cold-reader instructions to run, interpret, and update the check; execute them before handoff.
A passing model or bound covers only that stated model/bound, never the whole system.

