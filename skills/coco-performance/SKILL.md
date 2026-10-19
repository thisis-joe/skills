---
name: coco-performance
description: "Use when a measured latency, responsiveness, memory, throughput or bundle problem needs diagnosis, or a benchmark result needs validation. 성능 측정·최적화·벤치마크."
license: MIT
---

# coco-performance

Keep only improvements supported by controlled measurement and correct behavior.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/performance.md) only when the task needs their additional procedure. The [integration decisions](../_coco-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Define the user/workload problem, metric, environment and fixed measurement budget. Capture representative baseline and variability before optimizing.
2. Find the bottleneck using suitable profiles/traces/query plans. Do not infer that an expensive-looking line is the limiting factor.
3. Compare one targeted change under identical workload, cache state, build, sampling and resource budget. Verify correctness and critical user behavior as well as speed.
4. Keep a result only when improvement exceeds noise and the relevant trade-off is acceptable. Revert neutral/regressing experiments; log all attempts including reverted ones. A microbenchmark does not establish a production user benefit.
5. For caches include every response-varying input in the key, state staleness/invalidation, and address stampedes and tenant isolation. For formal benchmark claims use the advanced validity checklist.
6. Add an appropriate regression measurement and report unavailable real-user validation honestly. Hand retained changes to build for normal closure.

Return: baseline/after data, method and variance, bottleneck evidence, keep/revert decision, trade-offs and regression guard.
