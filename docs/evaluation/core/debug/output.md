# Duplicate-processing diagnosis

The isolated supplied worker has a confirmed check-then-effect race. The production cause remains unverified because no production revision, service, event stream or telemetry is available. The source report's “1 in 40” has an unknown sample definition and is not a measured rate in this evaluation.

Run from this directory:
```sh
python3 repro.py --mode sequential --attempts 10
python3 repro.py --mode race --attempts 10
```

Both call the same real fixture process function with the same stable message ID and fresh independent seen/effects collections per trial. The race harness schedules two public process calls to reach the supplied before_effect boundary together; it never sets hidden seen/effect state or fakes a successful effect. A barrier pins the previously uncertain interleaving.

Sequential: 10/10 trials produced one effect and processed/duplicate results, exit 0 (`evidence/sequential.json`). Concurrent: 10/10 trials produced two identical effects and processed/processed results, exit 1 (`evidence/red-race.json`). The recorded target SHA-256 binds both to worker.py. These rates describe the controlled fixture, not production prevalence.

Hypotheses: (1) concurrent non-atomic check/effect/mark is supported: both calls pass membership before either records completion; (2) different IDs are not needed: both use order-17:v1; (3) sequential replay alone is sufficient is contradicted by the positive control. The minimized pair preserves the triggering mechanism with no network or queue setup. The original production path cannot be rerun in this environment.

No product fix is authorized or applied. Build handoff: make stable-key ownership/claim atomic before the effect, preserve sequential deduplication, and rerun this harness plus the actual production redelivery path; persistence/remote unknown outcomes require stronger evidence than this in-memory example. A simple lock would address this one process only and must not be sold as distributed correctness.

Cleanup: threads were joined, no owned persistent service was launched, worker.py is unchanged; repro.py is intentionally retained as the reproducible artifact. No temporary instrumentation was added to production code. Regression-after-fix and actual production-cause claims remain unavailable.
