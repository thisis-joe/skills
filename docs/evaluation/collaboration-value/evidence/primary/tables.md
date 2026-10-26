# Descriptive paired collaboration observations

All paired cells show **COCO / no skills**. Distributions show median [minimum, maximum].

Five projects per family when complete. Lifecycle stages belong to the same projects; they are not independent trials. No overall quality score or significance claim is calculated.

All-attempt costs retain failures and unfinished work. A lower intervention count on unfinished work does not demonstrate a more efficient completed task.

## Paired actor cost: all attempts

| Family | Seed | Seconds COCO / no skills | COCO/no-skills ratio | Difference seconds |
| --- | ---: | ---: | ---: | ---: |
| lifecycle | 0 | 882.627 / 391.605 | 2.254 | 491.022 |
| lifecycle | 1 | 581.743 / 454.653 | 1.28 | 127.09 |
| lifecycle | 2 | 759.226 / 397.667 | 1.909 | 361.559 |
| lifecycle | 3 | 491.343 / 344.194 | 1.428 | 147.149 |
| lifecycle | 4 | 674.91 / 435.883 | 1.548 | 239.027 |
| review | 0 | 72.669 / 46.827 | 1.552 | 25.842 |
| review | 1 | 62.88 / 47.854 | 1.314 | 15.026 |
| review | 2 | 48.803 / 58.782 | 0.83 | -9.979 |
| review | 3 | 65.201 / 34.35 | 1.898 | 30.851 |
| review | 4 | 45.084 / 49.247 | 0.915 | -4.163 |

| Family | Available matched pairs | COCO cost increased | Paired ratio distribution |
| --- | ---: | ---: | --- |
| lifecycle | 5 | 5 | 1.548 [1.28, 2.254]; n=5 |
| review | 5 | 3 | 1.314 [0.83, 1.898]; n=5 |

## Lifecycle acceptance

First-pass and after-repair outcomes are retained separately; unavailable is neither pass nor fail.

| Seed | Initial first | Initial final | Changed checkpoint | Resume first | Resume final | Pending summary exposed |
| ---: | --- | --- | --- | --- | --- | --- |
| 0 | fail / fail | pass / pass | pass / pass | pass / pass | pass / pass | True / True |
| 1 | fail / fail | pass / pass | pass / pass | pass / pass | pass / pass | True / True |
| 2 | fail / fail | pass / pass | unavailable / pass | unavailable / pass | unavailable / pass | unavailable / True |
| 3 | fail / fail | pass / pass | pass / pass | pass / pass | pass / pass | True / True |
| 4 | fail / fail | pass / pass | pass / pass | pass / pass | pass / pass | True / True |

Boolean observations below show **true / false / unknown** counts. Pending summary exposure is a context observation; first-pass failures can subsequently pass after repair.

| Lifecycle observation | COCO true / false / unknown | No skills true / false / unknown |
| --- | --- | --- |
| initial_first_pass | 0 / 5 / 0 | 0 / 5 / 0 |
| initial_final_pass | 5 / 0 / 0 | 5 / 0 / 0 |
| changed_checkpoint_pass | 4 / 0 / 1 | 5 / 0 / 0 |
| resumed_first_pass | 4 / 0 / 1 | 5 / 0 / 0 |
| resumed_final_pass | 4 / 0 / 1 | 5 / 0 / 0 |
| pending_summary_exposure | 4 / 0 / 1 | 5 / 0 / 0 |
| stable | 4 / 1 / 0 | 5 / 0 / 0 |
| owned_work_committed | 4 / 0 / 1 | 5 / 0 / 0 |
| feature_branch | 4 / 0 / 1 | 5 / 0 / 0 |

| Lifecycle completion | COCO | No skills |
| --- | ---: | ---: |
| demonstrated | 4 | 5 |
| not_demonstrated | 1 | 0 |

## Jointly completed lifecycle pairs

Both arms demonstrated completion for 4 matched seeds: 0, 1, 3, 4. Completion requires stable observation, final resume acceptance, ready resume status, committed owned work and a feature branch. The table conditions on that same subset in both arms; excluded attempts remain above. This is descriptive selection, not a causal success-adjusted estimate.

| Metric | COCO median [min, max] | No skills median [min, max] | Paired COCO minus no skills |
| --- | --- | --- | --- |
| actor_seconds | 628.327 [491.343, 882.627]; n=4 | 413.744 [344.194, 454.653]; n=4 | 193.088 [127.09, 491.022]; n=4 |
| actor_commands | 46 [39, 59]; n=4 | 29.5 [27, 39]; n=4 | 16 [11, 22]; n=4 |
| owner_messages_delivered | 3 [3, 3]; n=4 | 3 [2, 3]; n=4 | 0 [0, 1]; n=4 |
| correction_messages | 1 [1, 1]; n=4 | 1 [1, 1]; n=4 | 0 [0, 0]; n=4 |
| private_choices_requested | 3 [3, 3]; n=4 | 3 [2, 3]; n=4 | 0 [0, 1]; n=4 |
| resumed_public_contract_requests | 0 [0, 1]; n=4 | 0 [0, 1]; n=4 | 0 [-1, 1]; n=4 |
| procedure_questions | 0 [0, 0]; n=4 | 0 [0, 0]; n=4 | 0 [0, 0]; n=4 |

Review completion/quality remains subject to the separate blinded judge. All question metrics are classifier-based observations; uncovered actor finals require the owner audit.

## Cost distributions and usage coverage: all attempts

| Family | Arm | Metric | Median [min, max]; projects observed | Total |
| --- | --- | --- | --- | ---: |
| lifecycle | coco | actor_seconds | 674.91 [491.343, 882.627]; n=5 | 3389.849 |
| lifecycle | coco | actor_turns | 6 [5, 6]; n=5 | 29 |
| lifecycle | coco | actor_commands | 44 [39, 59]; n=5 | 234 |
| lifecycle | coco | input_tokens | 2703768 [1780911, 4260270]; n=5 | 14878279 |
| lifecycle | coco | cached_input_tokens | 2467584 [1627136, 4033408]; n=5 | 13848832 |
| lifecycle | coco | output_tokens | 28065 [20070, 40897]; n=5 | 151394 |
| lifecycle | coco | synthetic_owner_seconds | 41.717 [38.209, 60.197]; n=5 | 223.14 |
| lifecycle | coco | synthetic_owner_calls | 5 [4, 5]; n=5 | 24 |
| lifecycle | coco | usage coverage | 28 recorded turns; 1 unavailable turns | 4 complete projects |
| lifecycle | bare | actor_seconds | 397.667 [344.194, 454.653]; n=5 | 2024.002 |
| lifecycle | bare | actor_turns | 6 [5, 7]; n=5 | 30 |
| lifecycle | bare | actor_commands | 30 [27, 39]; n=5 | 155 |
| lifecycle | bare | input_tokens | 1706958 [1376672, 1948276]; n=5 | 8600357 |
| lifecycle | bare | cached_input_tokens | 1556480 [1223552, 1779200]; n=5 | 7760512 |
| lifecycle | bare | output_tokens | 22374 [16665, 31673]; n=5 | 115994 |
| lifecycle | bare | synthetic_owner_seconds | 40.677 [34.988, 45.852]; n=5 | 203.998 |
| lifecycle | bare | synthetic_owner_calls | 5 [4, 6]; n=5 | 25 |
| lifecycle | bare | usage coverage | 30 recorded turns; 0 unavailable turns | 5 complete projects |
| review | coco | actor_seconds | 62.88 [45.084, 72.669]; n=5 | 294.637 |
| review | coco | actor_turns | 1 [1, 1]; n=5 | 5 |
| review | coco | actor_commands | 6 [6, 7]; n=5 | 32 |
| review | coco | input_tokens | 143097 [108049, 170864]; n=5 | 716841 |
| review | coco | cached_input_tokens | 125312 [86528, 140544]; n=5 | 597632 |
| review | coco | output_tokens | 1657 [1487, 2035]; n=5 | 8627 |
| review | coco | synthetic_owner_seconds | 8.15 [7.308, 10.769]; n=5 | 42.687 |
| review | coco | synthetic_owner_calls | 1 [1, 1]; n=5 | 5 |
| review | coco | usage coverage | 5 recorded turns; 0 unavailable turns | 5 complete projects |
| review | bare | actor_seconds | 47.854 [34.35, 58.782]; n=5 | 237.06 |
| review | bare | actor_turns | 1 [1, 1]; n=5 | 5 |
| review | bare | actor_commands | 4 [3, 5]; n=5 | 21 |
| review | bare | input_tokens | 93939 [75198, 118993]; n=5 | 483057 |
| review | bare | cached_input_tokens | 80384 [58752, 107904]; n=5 | 391936 |
| review | bare | output_tokens | 1308 [1128, 1431]; n=5 | 6392 |
| review | bare | synthetic_owner_seconds | 7.336 [6.791, 7.717]; n=5 | 36.38 |
| review | bare | synthetic_owner_calls | 1 [1, 1]; n=5 | 5 |
| review | bare | usage coverage | 5 recorded turns; 0 unavailable turns | 5 complete projects |

Token totals with unavailable turns are lower bounds. They must not be compared as complete costs.

## Owner intervention and elicitation: all attempts

Counts are synthetic proxies, not measured human time. Private choices are distinct topics actually asked per project; correction messages do not create elicitation credit. Public requests can be first disclosure or recall.

| Family | Arm | Metric | Median [min, max]; projects observed | Total |
| --- | --- | --- | --- | ---: |
| lifecycle | coco | owner_messages_delivered | 3 [3, 3]; n=5 | 15 |
| lifecycle | coco | correction_messages | 1 [1, 1]; n=5 | 5 |
| lifecycle | coco | private_choices_requested | 3 [2, 3]; n=5 | 14 |
| lifecycle | coco | settled_private_topic_requests | 0 [0, 0]; n=5 | 0 |
| lifecycle | coco | resumed_settled_private_requests | 0 [0, 0]; n=5 | 0 |
| lifecycle | coco | public_contract_topic_requests | 0 [0, 1]; n=5 | 1 |
| lifecycle | coco | resumed_public_contract_requests | 0 [0, 1]; n=5 | 1 |
| lifecycle | coco | procedure_questions | 0 [0, 1]; n=5 | 1 |
| lifecycle | bare | owner_messages_delivered | 3 [2, 4]; n=5 | 15 |
| lifecycle | bare | correction_messages | 1 [1, 1]; n=5 | 5 |
| lifecycle | bare | private_choices_requested | 3 [2, 3]; n=5 | 14 |
| lifecycle | bare | settled_private_topic_requests | 0 [0, 0]; n=5 | 0 |
| lifecycle | bare | resumed_settled_private_requests | 0 [0, 0]; n=5 | 0 |
| lifecycle | bare | public_contract_topic_requests | 0 [0, 1]; n=5 | 2 |
| lifecycle | bare | resumed_public_contract_requests | 0 [0, 1]; n=5 | 2 |
| lifecycle | bare | procedure_questions | 0 [0, 0]; n=5 | 0 |
| review | coco | owner_messages_delivered | 0 [0, 0]; n=5 | 0 |
| review | coco | correction_messages | 0 [0, 0]; n=5 | 0 |
| review | coco | private_choices_requested | 0 [0, 0]; n=5 | 0 |
| review | coco | settled_private_topic_requests | 0 [0, 0]; n=5 | 0 |
| review | coco | resumed_settled_private_requests | 0 [0, 0]; n=5 | 0 |
| review | coco | public_contract_topic_requests | 0 [0, 0]; n=5 | 0 |
| review | coco | resumed_public_contract_requests | 0 [0, 0]; n=5 | 0 |
| review | coco | procedure_questions | 0 [0, 0]; n=5 | 0 |
| review | bare | owner_messages_delivered | 0 [0, 0]; n=5 | 0 |
| review | bare | correction_messages | 0 [0, 0]; n=5 | 0 |
| review | bare | private_choices_requested | 0 [0, 0]; n=5 | 0 |
| review | bare | settled_private_topic_requests | 0 [0, 0]; n=5 | 0 |
| review | bare | resumed_settled_private_requests | 0 [0, 0]; n=5 | 0 |
| review | bare | public_contract_topic_requests | 0 [0, 0]; n=5 | 0 |
| review | bare | resumed_public_contract_requests | 0 [0, 0]; n=5 | 0 |
| review | bare | procedure_questions | 0 [0, 0]; n=5 | 0 |

## Limits

- Five paired projects per family when complete; lifecycle stages are not independent samples.
- All-attempt costs include unfinished work. Lower intervention on an unfinished attempt is not completion efficiency.
- Jointly completed distributions use the same matched seeds in both arms and condition on observed completion; they are descriptive, not a causal success-adjusted estimate.
- Completion requires stable observation, final resume acceptance, ready resume status, committed owned work and a feature branch. Unknown evidence cannot demonstrate completion.
- Descriptive observations only: no significance test, overall quality score or causal speedup claim.
- Actor elapsed time is not human effort or monetary price; synthetic owner costs remain separate.
- Unavailable usage is not zero. Partially recorded token totals are lower bounds; inspect coverage.
- Private elicitation uses actual questions only, excluding corrective fact disclosure. Raw records are required.
- Public contract requests and already-settled private requests are separate; neither automatically proves waste.
- Review quality requires separate blinded grading; report status and source checks are not defect recall.
- Procedure reduction requires the frozen quality/rework screen and later single-rule ablation.
