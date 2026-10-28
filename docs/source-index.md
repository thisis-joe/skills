# 원본별 통합 대응표

고정 버전의 모든 스킬·명령을 빠짐없이 기록합니다. `merged`는 공통 절차에 흡수, `adapted`는 팀/도구/권한에 맞춘 수정, `reference`는 필요할 때 적용하는 전문·실험 모드입니다. 원본 파일은 실행하지 않는 `.source` 자료입니다.

`coco-verify`와 `coco-automate`의 전문 모드는 [검증 선택표](../skills/_coco-shared/advanced/verify.md#mode-selection)와 [자동화 선택표](../skills/_coco-shared/advanced/automate.md#mode-selection)에서 연결합니다. 원본 운영 본문은 그대로 분리했으며 정확한 새 구현 위치는 `sources/coverage.json`의 `implemented_references`에 기록합니다. 원본의 `essential_rules`·채택 이유·체크섬은 바꾸지 않습니다. [구조와 보존 검증](context-loading.md)을 함께 확인합니다.

팀 요청으로 추가한 [coco-whattosay](../skills/coco-whattosay/SKILL.md)는 선택된 스킬에 맞는 요청문을 추천하는 신규 절차입니다. 원본에서 유래한 동작이 아니므로 아래 원본 대응과 `sources/coverage.json`의 131개 항목은 추가·변경하지 않습니다. 선택과 실행의 경계는 [결정 기록](../skills/_coco-shared/decisions.md)에 남깁니다.

팀 요청으로 추가한 [coco-askme](../skills/coco-askme/SKILL.md)는 선택한 작업·코드를 질의응답으로 학습하는 신규 절차입니다. 원본에서 유래한 동작이 아니므로 원본 대응과 `sources/coverage.json`은 변경하지 않습니다.

팀 요청으로 추가한 [coco-merge](../skills/coco-merge/SKILL.md)는 푸시한 PR/MR을 출시 준비 판단 없이 그 대상 브랜치에 머지하는 신규 절차입니다. 원본에서 유래한 동작이 아니므로 원본 대응과 `sources/coverage.json`은 변경하지 않습니다. 병합 큐 대기·자동 병합 예약을 머지로 보지 않는 확인 규칙은 `coco-ship`의 스택 머지 규칙을 따르며, 선택 이유는 [결정 기록](../skills/_coco-shared/decisions.md)에 남깁니다.

팀 요청으로 기존 `coco-document`를 공식 프로젝트 문서용 [coco-docs](../skills/coco-docs/SKILL.md)와 개인 학습용 [coco-learn](../skills/coco-learn/SKILL.md)으로 나눴습니다. matt·pstack의 `teach`와 pstack의 `bro`는 `coco-learn`으로, 나머지 문서 원본은 `coco-docs`로 옮겼고 `sources/coverage.json`에서는 `family`와 `implemented_references`만 바꿨습니다. 학습 노트의 고정 양식·분량 제한·검사 도구는 원본에서 유래하지 않은 팀 규칙이며, 선택 이유는 [결정 기록](../skills/_coco-shared/decisions.md)에 남깁니다.

[coco-blog](../skills/coco-blog/SKILL.md) is a team-authored procedure for public developer writing and publication preparation, grounded in the team-agreed writing and publication workflow. It does not introduce an upstream snapshot or coverage claim; `sources/manifest.json` and `sources/coverage.json` remain unchanged. Its request ownership, content-base isolation and evidence rules are recorded in the [decision record](../skills/_coco-shared/decisions.md).

| 출처 | 원본 | 통합 절차 | 처리 |
|---|---|---|---|
| matt | [skills/engineering/ask-matt](../sources/matt/skills/engineering/ask-matt/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| matt | [skills/engineering/code-review](../sources/matt/skills/engineering/code-review/SKILL.md.source) | [coco-review](../skills/coco-review/SKILL.md) | adapted |
| matt | [skills/engineering/codebase-design](../sources/matt/skills/engineering/codebase-design/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | merged |
| matt | [skills/engineering/diagnosing-bugs](../sources/matt/skills/engineering/diagnosing-bugs/SKILL.md.source) | [coco-debug](../skills/coco-debug/SKILL.md) | merged |
| matt | [skills/engineering/domain-modeling](../sources/matt/skills/engineering/domain-modeling/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | merged |
| matt | [skills/engineering/grill-with-docs](../sources/matt/skills/engineering/grill-with-docs/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | merged |
| matt | [skills/engineering/implement-spec](../sources/matt/skills/engineering/implement-spec/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | adapted |
| matt | [skills/engineering/implement](../sources/matt/skills/engineering/implement/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | merged |
| matt | [skills/engineering/improve-codebase-architecture](../sources/matt/skills/engineering/improve-codebase-architecture/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | adapted |
| matt | [skills/engineering/pr](../sources/matt/skills/engineering/pr/SKILL.md.source) | [coco-ship](../skills/coco-ship/SKILL.md) | adapted |
| matt | [skills/engineering/prototype](../sources/matt/skills/engineering/prototype/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | adapted |
| matt | [skills/engineering/research](../sources/matt/skills/engineering/research/SKILL.md.source) | [coco-research](../skills/coco-research/SKILL.md) | adapted |
| matt | [skills/engineering/retro](../sources/matt/skills/engineering/retro/SKILL.md.source) | [coco-retro](../skills/coco-retro/SKILL.md) | merged |
| matt | [skills/engineering/setup-matt-pocock-skills](../sources/matt/skills/engineering/setup-matt-pocock-skills/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| matt | [skills/engineering/tdd](../sources/matt/skills/engineering/tdd/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | adapted |
| matt | [skills/engineering/to-spec](../sources/matt/skills/engineering/to-spec/SKILL.md.source) | [coco-spec](../skills/coco-spec/SKILL.md) | adapted |
| matt | [skills/engineering/to-tickets](../sources/matt/skills/engineering/to-tickets/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| matt | [skills/engineering/triage](../sources/matt/skills/engineering/triage/SKILL.md.source) | [coco-triage](../skills/coco-triage/SKILL.md) | adapted |
| matt | [skills/engineering/wayfinder](../sources/matt/skills/engineering/wayfinder/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| matt | [skills/engineering/wizard](../sources/matt/skills/engineering/wizard/SKILL.md.source) | [coco-automate](../skills/coco-automate/SKILL.md) | reference |
| matt | [skills/in-progress/chief-of-staff](../sources/matt/skills/in-progress/chief-of-staff/SKILL.md.source) | [coco-automate](../skills/coco-automate/SKILL.md) | reference |
| matt | [skills/in-progress/claude-handoff](../sources/matt/skills/in-progress/claude-handoff/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | reference |
| matt | [skills/in-progress/loop-me](../sources/matt/skills/in-progress/loop-me/SKILL.md.source) | [coco-automate](../skills/coco-automate/SKILL.md) | adapted |
| matt | [skills/in-progress/setup-ts-deep-modules](../sources/matt/skills/in-progress/setup-ts-deep-modules/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | reference |
| matt | [skills/in-progress/writing-beats](../sources/matt/skills/in-progress/writing-beats/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | reference |
| matt | [skills/in-progress/writing-fragments](../sources/matt/skills/in-progress/writing-fragments/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | reference |
| matt | [skills/in-progress/writing-shape](../sources/matt/skills/in-progress/writing-shape/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | reference |
| matt | [skills/misc/git-guardrails-claude-code](../sources/matt/skills/misc/git-guardrails-claude-code/SKILL.md.source) | [coco-security](../skills/coco-security/SKILL.md) | reference |
| matt | [skills/misc/migrate-to-shoehorn](../sources/matt/skills/misc/migrate-to-shoehorn/SKILL.md.source) | [coco-migrate](../skills/coco-migrate/SKILL.md) | reference |
| matt | [skills/misc/scaffold-exercises](../sources/matt/skills/misc/scaffold-exercises/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | reference |
| matt | [skills/misc/setup-pre-commit](../sources/matt/skills/misc/setup-pre-commit/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | reference |
| matt | [skills/productivity/grill-me](../sources/matt/skills/productivity/grill-me/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | merged |
| matt | [skills/productivity/grilling](../sources/matt/skills/productivity/grilling/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | adapted |
| matt | [skills/productivity/handoff](../sources/matt/skills/productivity/handoff/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | merged |
| matt | [skills/productivity/teach](../sources/matt/skills/productivity/teach/SKILL.md.source) | [coco-learn](../skills/coco-learn/SKILL.md) | reference |
| matt | [skills/productivity/to-questionnaire](../sources/matt/skills/productivity/to-questionnaire/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | adapted |
| matt | [skills/productivity/wait-what](../sources/matt/skills/productivity/wait-what/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | merged |
| matt | [skills/productivity/writing-for-agents](../sources/matt/skills/productivity/writing-for-agents/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | merged |
| addy | [.claude/commands/build.md](../sources/addy/.claude/commands/build.md.source) | [coco-build](../skills/coco-build/SKILL.md) | adapted |
| addy | [.claude/commands/code-simplify.md](../sources/addy/.claude/commands/code-simplify.md.source) | [coco-simplify](../skills/coco-simplify/SKILL.md) | merged |
| addy | [.claude/commands/constraints.md](../sources/addy/.claude/commands/constraints.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| addy | [.claude/commands/plan.md](../sources/addy/.claude/commands/plan.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| addy | [.claude/commands/review.md](../sources/addy/.claude/commands/review.md.source) | [coco-review](../skills/coco-review/SKILL.md) | merged |
| addy | [.claude/commands/ship.md](../sources/addy/.claude/commands/ship.md.source) | [coco-ship](../skills/coco-ship/SKILL.md) | adapted |
| addy | [.claude/commands/spec.md](../sources/addy/.claude/commands/spec.md.source) | [coco-spec](../skills/coco-spec/SKILL.md) | adapted |
| addy | [.claude/commands/test.md](../sources/addy/.claude/commands/test.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | adapted |
| addy | [.claude/commands/webperf.md](../sources/addy/.claude/commands/webperf.md.source) | [coco-performance](../skills/coco-performance/SKILL.md) | reference |
| addy | [skills/api-and-interface-design](../sources/addy/skills/api-and-interface-design/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | merged |
| addy | [skills/browser-testing-with-devtools](../sources/addy/skills/browser-testing-with-devtools/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | reference |
| addy | [skills/ci-cd-and-automation](../sources/addy/skills/ci-cd-and-automation/SKILL.md.source) | [coco-automate](../skills/coco-automate/SKILL.md) | adapted |
| addy | [skills/code-review-and-quality](../sources/addy/skills/code-review-and-quality/SKILL.md.source) | [coco-review](../skills/coco-review/SKILL.md) | adapted |
| addy | [skills/code-simplification](../sources/addy/skills/code-simplification/SKILL.md.source) | [coco-simplify](../skills/coco-simplify/SKILL.md) | merged |
| addy | [skills/constraint-driven-development](../sources/addy/skills/constraint-driven-development/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| addy | [skills/context-engineering](../sources/addy/skills/context-engineering/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | adapted |
| addy | [skills/debugging-and-error-recovery](../sources/addy/skills/debugging-and-error-recovery/SKILL.md.source) | [coco-debug](../skills/coco-debug/SKILL.md) | merged |
| addy | [skills/deprecation-and-migration](../sources/addy/skills/deprecation-and-migration/SKILL.md.source) | [coco-migrate](../skills/coco-migrate/SKILL.md) | merged |
| addy | [skills/documentation-and-adrs](../sources/addy/skills/documentation-and-adrs/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | merged |
| addy | [skills/doubt-driven-development](../sources/addy/skills/doubt-driven-development/SKILL.md.source) | [coco-review](../skills/coco-review/SKILL.md) | adapted |
| addy | [skills/frontend-ui-engineering](../sources/addy/skills/frontend-ui-engineering/SKILL.md.source) | [coco-frontend](../skills/coco-frontend/SKILL.md) | merged |
| addy | [skills/git-workflow-and-versioning](../sources/addy/skills/git-workflow-and-versioning/SKILL.md.source) | [coco-ship](../skills/coco-ship/SKILL.md), [coco-build](../skills/coco-build/SKILL.md), [coco-push의 팀 적용](../skills/coco-push/references/branch-and-ticket.md) | adapted |
| addy | [skills/idea-refine](../sources/addy/skills/idea-refine/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | reference |
| addy | [skills/incremental-implementation](../sources/addy/skills/incremental-implementation/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | merged |
| addy | [skills/interview-me](../sources/addy/skills/interview-me/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | adapted |
| addy | [skills/observability-and-instrumentation](../sources/addy/skills/observability-and-instrumentation/SKILL.md.source) | [coco-observe](../skills/coco-observe/SKILL.md) | merged |
| addy | [skills/performance-optimization](../sources/addy/skills/performance-optimization/SKILL.md.source) | [coco-performance](../skills/coco-performance/SKILL.md) | merged |
| addy | [skills/planning-and-task-breakdown](../sources/addy/skills/planning-and-task-breakdown/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| addy | [skills/security-and-hardening](../sources/addy/skills/security-and-hardening/SKILL.md.source) | [coco-security](../skills/coco-security/SKILL.md) | adapted |
| addy | [skills/shipping-and-launch](../sources/addy/skills/shipping-and-launch/SKILL.md.source) | [coco-ship](../skills/coco-ship/SKILL.md) | adapted |
| addy | [skills/source-driven-development](../sources/addy/skills/source-driven-development/SKILL.md.source) | [coco-research](../skills/coco-research/SKILL.md) | merged |
| addy | [skills/spec-driven-development](../sources/addy/skills/spec-driven-development/SKILL.md.source) | [coco-spec](../skills/coco-spec/SKILL.md) | adapted |
| addy | [skills/test-driven-development](../sources/addy/skills/test-driven-development/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | adapted |
| addy | [skills/using-agent-skills](../sources/addy/skills/using-agent-skills/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| pstack | [pstack/automations/benny/skills/reproduce-and-fix-issues](../sources/pstack/pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md.source) | [coco-debug](../skills/coco-debug/SKILL.md) | adapted |
| pstack | [pstack/automations/benny/skills/setup-benny](../sources/pstack/pstack/automations/benny/skills/setup-benny/SKILL.md.source) | [coco-automate](../skills/coco-automate/SKILL.md) | adapted |
| pstack | [pstack/automations/benny/skills/triage-issue-reports](../sources/pstack/pstack/automations/benny/skills/triage-issue-reports/SKILL.md.source) | [coco-triage](../skills/coco-triage/SKILL.md) | adapted |
| pstack | [pstack/skills/architect](../sources/pstack/pstack/skills/architect/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | adapted |
| pstack | [pstack/skills/arena](../sources/pstack/pstack/skills/arena/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | adapted |
| pstack | [pstack/skills/automate-me](../sources/pstack/pstack/skills/automate-me/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | adapted |
| pstack | [pstack/skills/benchmark-checklist](../sources/pstack/pstack/skills/benchmark-checklist/SKILL.md.source) | [coco-performance](../skills/coco-performance/SKILL.md) | merged |
| pstack | [pstack/skills/blast-radius](../sources/pstack/pstack/skills/blast-radius/SKILL.md.source) | [coco-review](../skills/coco-review/SKILL.md) | merged |
| pstack | [pstack/skills/bro](../sources/pstack/pstack/skills/bro/SKILL.md.source) | [coco-learn](../skills/coco-learn/SKILL.md) | merged |
| pstack | [pstack/skills/correct](../sources/pstack/pstack/skills/correct/SKILL.md.source) | [coco-retro](../skills/coco-retro/SKILL.md) | adapted |
| pstack | [pstack/skills/create-formal-verification-skill](../sources/pstack/pstack/skills/create-formal-verification-skill/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | adapted |
| pstack | [pstack/skills/create-verification-skill](../sources/pstack/pstack/skills/create-verification-skill/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | adapted |
| pstack | [pstack/skills/figure-it-out](../sources/pstack/pstack/skills/figure-it-out/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| pstack | [pstack/skills/how](../sources/pstack/pstack/skills/how/SKILL.md.source) | [coco-research](../skills/coco-research/SKILL.md) | adapted |
| pstack | [pstack/skills/in-your-own-words](../sources/pstack/pstack/skills/in-your-own-words/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | merged |
| pstack | [pstack/skills/interrogate](../sources/pstack/pstack/skills/interrogate/SKILL.md.source) | [coco-review](../skills/coco-review/SKILL.md) | adapted |
| pstack | [pstack/skills/ketchup](../sources/pstack/pstack/skills/ketchup/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | adapted |
| pstack | [pstack/skills/maintain-formal-verification-skill](../sources/pstack/pstack/skills/maintain-formal-verification-skill/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | adapted |
| pstack | [pstack/skills/maintain-verification-skill](../sources/pstack/pstack/skills/maintain-verification-skill/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | adapted |
| pstack | [pstack/skills/make-bot-ui](../sources/pstack/pstack/skills/make-bot-ui/SKILL.md.source) | [coco-automate](../skills/coco-automate/SKILL.md) | adapted |
| pstack | [pstack/skills/no-comments](../sources/pstack/pstack/skills/no-comments/SKILL.md.source) | [coco-simplify](../skills/coco-simplify/SKILL.md) | adapted |
| pstack | [pstack/skills/poteto-help](../sources/pstack/pstack/skills/poteto-help/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| pstack | [pstack/skills/poteto-mode](../sources/pstack/pstack/skills/poteto-mode/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| pstack | [pstack/skills/principle-attack-the-premise](../sources/pstack/pstack/skills/principle-attack-the-premise/SKILL.md.source) | [coco-debug](../skills/coco-debug/SKILL.md) | merged |
| pstack | [pstack/skills/principle-boundary-discipline](../sources/pstack/pstack/skills/principle-boundary-discipline/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | merged |
| pstack | [pstack/skills/principle-build-the-lever](../sources/pstack/pstack/skills/principle-build-the-lever/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | adapted |
| pstack | [pstack/skills/principle-encode-lessons-in-structure](../sources/pstack/pstack/skills/principle-encode-lessons-in-structure/SKILL.md.source) | [coco-retro](../skills/coco-retro/SKILL.md) | merged |
| pstack | [pstack/skills/principle-exhaust-the-design-space](../sources/pstack/pstack/skills/principle-exhaust-the-design-space/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | adapted |
| pstack | [pstack/skills/principle-experience-first](../sources/pstack/pstack/skills/principle-experience-first/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | merged |
| pstack | [pstack/skills/principle-explain-the-number](../sources/pstack/pstack/skills/principle-explain-the-number/SKILL.md.source) | [coco-performance](../skills/coco-performance/SKILL.md) | merged |
| pstack | [pstack/skills/principle-fix-root-causes](../sources/pstack/pstack/skills/principle-fix-root-causes/SKILL.md.source) | [coco-debug](../skills/coco-debug/SKILL.md) | merged |
| pstack | [pstack/skills/principle-foundational-thinking](../sources/pstack/pstack/skills/principle-foundational-thinking/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | merged |
| pstack | [pstack/skills/principle-guard-the-context-window](../sources/pstack/pstack/skills/principle-guard-the-context-window/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | adapted |
| pstack | [pstack/skills/principle-laziness-protocol](../sources/pstack/pstack/skills/principle-laziness-protocol/SKILL.md.source) | [coco-simplify](../skills/coco-simplify/SKILL.md) | merged |
| pstack | [pstack/skills/principle-make-operations-idempotent](../sources/pstack/pstack/skills/principle-make-operations-idempotent/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | merged |
| pstack | [pstack/skills/principle-migrate-callers-then-delete-legacy-apis](../sources/pstack/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md.source) | [coco-migrate](../skills/coco-migrate/SKILL.md) | merged |
| pstack | [pstack/skills/principle-minimize-reader-load](../sources/pstack/pstack/skills/principle-minimize-reader-load/SKILL.md.source) | [coco-simplify](../skills/coco-simplify/SKILL.md) | merged |
| pstack | [pstack/skills/principle-model-the-domain](../sources/pstack/pstack/skills/principle-model-the-domain/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | merged |
| pstack | [pstack/skills/principle-never-block-on-the-human](../sources/pstack/pstack/skills/principle-never-block-on-the-human/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| pstack | [pstack/skills/principle-outcome-oriented-execution](../sources/pstack/pstack/skills/principle-outcome-oriented-execution/SKILL.md.source) | [coco-migrate](../skills/coco-migrate/SKILL.md) | merged |
| pstack | [pstack/skills/principle-prove-it-works](../sources/pstack/pstack/skills/principle-prove-it-works/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | merged |
| pstack | [pstack/skills/principle-redesign-from-first-principles](../sources/pstack/pstack/skills/principle-redesign-from-first-principles/SKILL.md.source) | [coco-design](../skills/coco-design/SKILL.md) | merged |
| pstack | [pstack/skills/principle-separate-before-serializing-shared-state](../sources/pstack/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | merged |
| pstack | [pstack/skills/principle-sequence-verifiable-units](../sources/pstack/pstack/skills/principle-sequence-verifiable-units/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| pstack | [pstack/skills/principle-subtract-before-you-add](../sources/pstack/pstack/skills/principle-subtract-before-you-add/SKILL.md.source) | [coco-simplify](../skills/coco-simplify/SKILL.md) | merged |
| pstack | [pstack/skills/principle-test-behavior-not-implementation](../sources/pstack/pstack/skills/principle-test-behavior-not-implementation/SKILL.md.source) | [coco-verify](../skills/coco-verify/SKILL.md) | merged |
| pstack | [pstack/skills/principle-type-system-discipline](../sources/pstack/pstack/skills/principle-type-system-discipline/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | merged |
| pstack | [pstack/skills/recall](../sources/pstack/pstack/skills/recall/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | adapted |
| pstack | [pstack/skills/reflect](../sources/pstack/pstack/skills/reflect/SKILL.md.source) | [coco-retro](../skills/coco-retro/SKILL.md) | adapted |
| pstack | [pstack/skills/setup-pstack](../sources/pstack/pstack/skills/setup-pstack/SKILL.md.source) | [coco-start](../skills/coco-start/SKILL.md) | adapted |
| pstack | [pstack/skills/sharpen](../sources/pstack/pstack/skills/sharpen/SKILL.md.source) | [coco-clarify](../skills/coco-clarify/SKILL.md) | merged |
| pstack | [pstack/skills/show-me-your-work](../sources/pstack/pstack/skills/show-me-your-work/SKILL.md.source) | [coco-context](../skills/coco-context/SKILL.md) | adapted |
| pstack | [pstack/skills/swarm](../sources/pstack/pstack/skills/swarm/SKILL.md.source) | [coco-plan](../skills/coco-plan/SKILL.md) | adapted |
| pstack | [pstack/skills/tdd](../sources/pstack/pstack/skills/tdd/SKILL.md.source) | [coco-debug](../skills/coco-debug/SKILL.md) | merged |
| pstack | [pstack/skills/teach](../sources/pstack/pstack/skills/teach/SKILL.md.source) | [coco-learn](../skills/coco-learn/SKILL.md) | adapted |
| pstack | [pstack/skills/technical-writing](../sources/pstack/pstack/skills/technical-writing/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | merged |
| pstack | [pstack/skills/typescript-best-practices](../sources/pstack/pstack/skills/typescript-best-practices/SKILL.md.source) | [coco-build](../skills/coco-build/SKILL.md) | adapted |
| pstack | [pstack/skills/unslop](../sources/pstack/pstack/skills/unslop/SKILL.md.source) | [coco-docs](../skills/coco-docs/SKILL.md) | merged |
| pstack | [pstack/skills/why](../sources/pstack/pstack/skills/why/SKILL.md.source) | [coco-research](../skills/coco-research/SKILL.md) | adapted |
