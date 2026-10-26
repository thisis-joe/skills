# Waited recovery: cooldown succeeded; the fixed execution budget stopped the cohort

Waiting worked. A native owner call returned HTTP429 with a 77.999-second retry
interval, kept the same CLI process alive and completed after 99.647 seconds. The
announced cooldown overlap was 77.999 seconds; the charged remainder estimate was
21.73 seconds. This resolves the narrow question of whether honoring the provider
wait can recover a call. It does not complete the comparison.

All nine native calls used explicitly requested `gpt-6.1-sol` with `high` reasoning,
verified from a fresh model context inside each invocation's start/end interval.
Four were fresh owner controls, three were development turns and two were project
owner classifiers. Those four controls were reused once by exact byte provenance,
not rerun or counted twice. [Calls and cleanup](evidence/waited-shutdown-and-costs.json).

## Instrument repair before development

The first frozen waited root prepared 12 projects and passed four controls. Its
first development admission failed before any native development call because
macOS Python 3.9.6's process-local monotonic origin cannot be compared across
separate control/run processes. The first root, STOP and control records were
preserved. A separate adapter persisted UTC for cross-process start spacing and
used local monotonic time for the actual wait and within-call budgets. Two real
Python processes started 30.005325 seconds apart in the focused regression.
The repaired root froze 19 inputs and the same two guide manifests; it reused the
four controls with unchanged model/prompt/classifier/owner/engine provenance.
[Repair provenance](evidence/clock-repair-provenance.json),
[clock test](evidence/clock-fixed-tests.log).

## Actual development and stop

One current-arm profile was launched; no candidate actor ran. Turn 1 asked owner
questions. The ordinary reply supplied only the asked collision and malformed-row
policies. Completed turn 2 implemented the CLI but its public checks failed on
identity/file collision, emitted SKU spelling and exact large-integer prices.
The predeclared single corrective reply then supplied the complete agreed
requirements. This was ordinary instrument behavior, not manual intervention.

Turn 3 modified the implementation and executed tests, but reached the predeclared
420-second non-cooldown budget. The adapter requested SIGINT; the native leader
exited 1 after 421.163 seconds without a completed-turn event or final report. It had
no new 429. This second stop was **our execution-time bound**, not a continuing
server-capacity failure. The original limit and timeout remain recorded; this run
was not resumed, relabeled successful or replaced by a favorable outcome.

After the stop, two source/state reads one second apart matched. The independent
oracle ran on a copy and left the surviving actor state unchanged. All public CLI
checks passed on that surviving code. That observation does not supply the missing
final turn, completed review/reporting or completed implementation commitment.
The partial result remains partial, with **zero stable trials and zero valid
matched pairs**. Eleven other projects were not admitted, including both candidate
preservation probes. The14-case blind packet contains one partial project,
eleven unstarted projects and two negative controls; it remains ungraded.

Every tracked native leader PID was absent at collection and the cancelled CLI's
owned process group was absent. Unmanaged tool descendants remain separately
unverified, as recorded by the unchanged engine; leader absence is not proof of
arbitrary descendant cleanup. Native duration sums total 1036.957 seconds, including
all four controls and the interrupted turn. This sum is not overall study wall
time. Per-call token records retain missing interrupted usage as unavailable.

## Evidence and consequence

Three archives were reread against every entry's hash and mode:

- [Initial clock-failure root](evidence/waited-clock-failure-native.tar.gz):
  `9a1a7f9862c9fe753ec3ef948252d735edc09d8dc0dfbd64929df623240a002f`.
- [Repaired root and 420-second stop](evidence/waited-budget-stop-native.tar.gz):
  `d4e1afd14de2c730053a47657984d0945cbcf42ccc03c6b76dd500faa2bbdca6`.
- [Ungraded blind packet](evidence/waited-budget-stop-blind-ungraded.tar.gz):
  `cd891ac3ffa3011e508ba83293544871c9fb2b1e8097293970735a2e506c9c32`.

Adjacent manifests retain all file bytes/modes. The original ten instrument tests,
current-call model checks and focused clock regression are preserved. No model
was switched in response to a product result. The user's subsequent prohibition
of Astra applies to future work; no blind review was performed for this packet.
The full comparison and adoption gate are still unfulfilled. A separately frozen
900-second actor cohort may be authorized by the parent; it cannot change these
420-second observations or support comparisons of their execution time.
