# Graphify navigation evaluation

## Comparison

Use the same FastAPI source and review range in both arms. The target is
`f02ef4900bacc28942a051b95b9719c5002a7858` and the base is
`80c8742d141e67beaf747343405c8facf999bc0c`. The range includes
[nullable form union schemas](https://github.com/fastapi/fastapi/pull/16598)
and [omitted boolean form fields](https://github.com/fastapi/fastapi/pull/16605).

1. Trace changed form extraction through regular request bodies and model extraction to
   the HTTP handler. Find the union normalization path, including the validator's
   `partial` binding. Confirm omitted and explicitly supplied checkbox behavior in
   `tests/test_union_form_normalization.py`.
2. Trace the schema change in `_get_body_field` through
   `_populate_api_route_state` to its construction and route-copy callers. Confirm
   the OpenAPI expectation in `tests/test_forms_optional_unions.py`.

The direct arm ran scoped `rg -n` word-boundary searches on the changed symbols
and discovered callers in `fastapi/`. The candidate checked the graph root,
top-level `built_at_commit`, and current source status. It ran Graphify 0.9.102
`affected _extract_form_items --depth 4 --relation calls` and
`affected _get_body_field --depth 3 --relation calls`. Both arms used direct
search for the validator binding and read identical source and test excerpts.
The two review obligations were confirmed in both arms. The graph query also
surfaced paths beyond the HTTP obligation, and the indirect validator binding
still needed direct search.

| Measurement | Direct search | Graphify and source |
| --- | ---: | ---: |
| Discovery output tokens | 529 | 355 |
| Extra guide and index status tokens | 0 | 424 |
| Common source excerpt tokens | 5,045 | 5,045 |
| Total measured context tokens | 5,574 | 5,824 |
| Median local navigation time, seconds | 0.0408 | 0.2603 |

Seven paired command runs alternated order. Counts use the `o200k_base`
tokenizer on the collected text. The common review instructions and diff are
outside the measurement. Time covers local navigation commands and source
reads. This is a controlled command comparison with a source-backed rubric.
Model inference, agent behavior, billing, and production execution are outside
its measurement. The separately timed cold code-only extraction took 6.25 s
for 54 code files using two workers, with docs, examples, tests, and tooling
directories excluded from the graph.

## Fallback and rollout

With a missing graph path the comparison took the direct search route. With a
stale build commit it took the same route. After switching the disposable
checkout to the older base, direct search recovered its old boolean inference
while the graph still referenced the newer revision. An untracked source file
invalidated the readiness check despite a matching commit. The graph digest
was unchanged throughout the queries and fallback checks.

The initial pilot kept the conditional review integration. The graph reduced
discovery output by 174 tokens, while the full measured context grew by 250
tokens and local navigation took longer. This comparison did not meet the
criterion for connecting research, debug, and build.

## Codex session comparison and retirement

Six pairs of read-only Codex sessions reviewed three frozen application
changes, with two pairs per change and alternating starting arms. The direct
arm used ripgrep and source reads. The indexed arm used a prepared local graph
and direct search for gaps. Both used the same model and reasoning setting.

| Measurement | Direct search | Graphify and source |
| --- | ---: | ---: |
| Total reported input and output tokens | 1,850,787 | 2,063,435 |
| Uncached input plus output tokens | 372,131 | 314,955 |
| Median session time, seconds | 61.4 | 70.8 |
| Command executions | 48 | 70 |
| Required uses found | 16/16 | 16/16 |

Cache hits varied by run. The total token comparison includes cached input.
Each case has two paired repeats, and this experiment covers the local CLI and
the measured review tasks. The user chose to retire the review integration
and its unused shared reference after this comparison.

## Flow tracing in coco-askme

The follow-up evaluated whether an optional Graphify step would help
[`coco-askme`](../../skills/coco-askme/SKILL.md) explain an unfamiliar execution
path. Twelve fresh read-only Codex CLI 0.166.0-alpha.6 sessions used
`gpt-6.1-sol` with low reasoning effort and the same 660 tracked production
Kotlin files from S15P31E102 at `12a69db9a6e80238279fef694d7f79da89777212`.
Each flow ran twice per method, with the order reversed for its second pair.
Both methods used `rg` and targeted source reads. The Graphify method also
made one bounded query per session against a prepared Graphify 0.9.102
code-only index. Index preparation took 4.770 seconds outside the session
measurements.

First-path time runs from session launch to the first message reporting the
expected connection with source citations, after the session retrieved that
source. The three checkpoints were the upload transaction's handoff to an
after-commit listener, the retry endpoint's handoff to a persisted queue
update, and the screen's stop event reaching the polling cancellation. Each
answer was scored against four predefined links for its flow. Incorrect path
claims were checked in progress messages and final answers.

Paired results are listed in execution order. Each cell with two values gives
direct search first and Graphify with direct search second.

| Pair | Flow | First path, seconds | Full session, seconds | Total tokens |
| ---: | --- | ---: | ---: | ---: |
| 1 | Recording upload to AI analysis | 20.896 → 24.416 | 46.887 → 58.365 | 181,112 → 218,097 |
| 2 | Sheet conversion retry to recognition | 19.218 → 20.634 | 43.196 → 42.733 | 137,551 → 153,841 |
| 3 | Analysis polling and result navigation | 18.252 → 30.314 | 63.060 → 68.523 | 243,154 → 287,820 |
| 4 | Recording upload to AI analysis | 17.597 → 20.022 | 40.263 → 48.285 | 120,326 → 149,763 |
| 5 | Sheet conversion retry to recognition | 18.033 → 27.380 | 39.465 → 49.489 | 117,533 → 212,837 |
| 6 | Analysis polling and result navigation | 19.039 → 20.933 | 73.151 → 67.792 | 271,649 → 245,251 |

| Measurement | Direct search | Graphify and direct search | Change |
| --- | ---: | ---: | ---: |
| Median first-path time, seconds | 18.645 | 22.675 | +21.6% |
| Median session time, seconds | 45.041 | 53.927 | +19.7% |
| Total reported input and output tokens | 1,071,325 | 1,267,609 | +18.3% |
| Uncached input plus output tokens | 187,613 | 204,441 | +9.0% |
| Required links missed | 0/24 | 0/24 | — |
| Incorrect path claims | 0 | 0 | — |

Total tokens include cached input. Cache hits varied by session. The results
cover static source tracing of these three flows with a prepared local index.

The adoption criteria required at least a 15% reduction in median first-path
time, wins in both repeats for at least two flows, no loss of accuracy in any
pair, and at most 10% more total tokens. All twelve sessions were usable and
accuracy was equal. Graphify surfaced the correct sheet retry controller in
one query, but first-path confirmation was slower in all six pairs and total
tokens exceeded the cap. The integration evaluation ended after this trial,
and `coco-askme` did not adopt the optional step.
