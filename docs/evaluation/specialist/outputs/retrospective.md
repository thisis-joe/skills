# The improvement claim is not supported

Boundary: `fixtures/retro-one-run.json`, one constructed scenario summary. No raw run transcript or baseline artifact exists. The reported 1/1 success came from an author-selected familiar task, with scoring chosen after the run and no blind judge. It can support a narrow demonstration, not a comparative quality or speed claim.

The consequential failure is treating that demonstration as an improvement result. Mechanisms include selection bias, hindsight rubric, no no-guidance comparator and author-as-judge. Recurrence is not established. A competing explanation is that the task was easy or the author already knew the desired behavior; the skill may have helped, but this evidence cannot separate those causes.

Disposition: reject the generalized success claim; accept the retained demonstration as a fixture only; propose the bounded protocol in `outputs/evaluation-protocol.json`; defer any maintained instruction change until the missing comparison exists. Existing LET’S retro/verify already demand baseline, held-out tasks and actual artifacts, so more motivational prose or a new global skill would duplicate coverage. No user settings, credentials, files in the repository or external tickets were changed.

Checking scenario: the local check reads the biased sample and refuses to call it a valid comparison because baseline/held-out/frozen-rubric/blinding conditions are absent. This is a local metadata sensitivity check, not validation that the proposed protocol improves skills or that a maintained guardrail is wired into CI. A future implementation must demonstrate rejection on real/fidelity-preserving bad artifacts, acceptance of restored valid artifacts and actual local/CI wiring before prevention is claimed.

Future comparison uses organic held-out inputs, same completed-work/error accounting and environment, multiple predeclared repetitions, sanitized artifacts and a shared scale for an independent authorized judge. Report case results, trial spread, confounders and missing slices. Speed claims additionally need separately profiled actual work and alternating samples with valid timing. No such comparison ran here.

This entire specialist validation is one fresh agent applying 12 scenarios. It is independent of the skill author conversation but neither blinded nor independent repeated trials per skill. There is no defensible numerical estimate of skill-improvement magnitude.
