# COCO 1.0.0 → 1.1.0: 어떤 지침을 왜 바꾸는가

1.1.0의 목표는 **사용자가 중요한 선택을 하고, 에이전트가 그 선택대로 개발하며, 다음 작업자도 같은 약속을 이어받게 하는 것**이다. 이를 위해 처음에는 네 단계로 사용법을 안내하고, 실제 구현 직전에는 빠진 결정을 확인하며, 완료 보고에는 처음 예상과 달라진 이유를 남긴다.

이 문서는 그 목표를 실제 수정 위치와 예시로 연결한다. 변경 전 인용은 `84a59a2`, 변경 후 인용은 현재 1.1.0 후보의 실제 지침에서 가져왔다. 긴 문단은 필요한 문장만 발췌했고, 줄바꿈과 링크 표시는 읽기 좋게 정리했다. 작업 상태와 검증 결과는 [작업 계획](plans/coco-1.1.0.md)에서 관리한다. 후보에 지침이 들어갔다는 사실만으로 검증 통과나 출시 완료를 뜻하지는 않는다.

- **비교 출발점:** 로컬 `v1.0.0` 태그의 `84a59a2`. `88d1c84`와 같은 파일 내용을 가진다. 배포된 npm 파일을 새로 검사했다는 뜻은 아니다.
- **가져온 기존 작업:** 실험 버전 `622975e`에 작성된 네 단계 흐름. 이 흐름은 위 1.0.0 태그에는 없다.
- **이번에 보완한 부분:** 빠진 결정을 구현 전에 찾는 위치, 구현 중 발견한 제약의 재확인, 최초 예상 보존과 최종 보고, 기존 호출을 방해할 수 있는 조건문.
- **유지할 결정:** [38개 답변으로 정한 개발 규칙](specs/staged-development.md)과 [1.1.0 명세의 C1–C8](specs/coco-1.1.0.md). 스킬 29개와 전문 스킬의 직접 호출을 유지한다.

## 1. 처음 쓰는 사람에게 네 단계와 다음 행동을 보여준다

**수정 위치:** [coco-start의 첫 안내](../skills/coco-start/SKILL.md#coco-start)와 [다음 단계 추천](../skills/coco-start/SKILL.md#procedure-and-output), [coco-tellmeskill의 탐색 안내](../skills/coco-tellmeskill/SKILL.md), 공통 [routing.md](../skills/_coco-shared/routing.md). 단계·전환 규칙의 원본은 새 공통 파일 [workflow.md](../skills/_coco-shared/workflow.md#introductory-path) 한 곳에 둔다.

1.0.0의 `coco-start`는 “적절한 경로를 선택하라”는 지침과 전체 목적별 표를 제공한다.

> Choose an appropriate workflow and establish the project quality bar.

1.1.0에서는 첫 안내의 기준을 명시한다.

> Start with the four stages and ten introductory skills in the workflow; offer specialists/help by purpose, preserving expert direct invocation and complete-list requests.

| 사용자가 있는 단계 | 처음 안내할 스킬 | 사용 후 기대하는 결과 |
| --- | --- | --- |
| 요구사항 정리 | `coco-clarify`, `coco-spec`, `coco-plan` | 원하는 동작과 중요한 선택을 정하고, 명세와 작업 계획을 저장한다. |
| 구현 | `coco-build`, `coco-debug` | 동작을 만들고 확인하여 작업 단위로 커밋한다. 정식 리뷰 상태는 별도로 알린다. |
| 리뷰·검증 | `coco-review`, `coco-verify` | 변경을 검토하고 실제 동작을 확인한다. 필요한 수정은 구현 단계에서 처리한다. |
| 출시 | `coco-push`, `coco-merge`, `coco-ship` | 사용자가 요청한 푸시·PR·병합·출시 작업을 수행한다. |

**사용 예:** “CSV 가져오기를 만들고 싶어”라고 시작하면 먼저 입력과 결과를 명확히 한다. 명세와 계획이 이미 충분하면 새로 쓰지 않고 구현으로 갈 수 있다. “전체 스킬을 보여줘” 또는 “`coco-performance`로 분석해줘”라는 요청은 그대로 처리한다.

**이유:** 초보자는 개발 단계에서 출발하고, 익숙한 사용자는 필요한 스킬을 직접 선택할 수 있게 한다. 열 개를 매번 순서대로 실행하도록 만드는 변경은 아니다.

**검증 V1:** 첫 안내, 기존 계획이 있는 재개, 전체 목록, 전문 스킬 직접 호출, 단순 문구 수정, 인자 없는 `coco-start`를 확인한다. 마지막 경우는 읽기만 하고 경로를 안내해야 하며, 공통의 “요청 없는 호출” 규칙 때문에 별도 질문 메뉴로 빠지면 실패다.

### 동작을 바꿀 때는 명세와 계획을 코드보다 먼저 남긴다

**수정 위치:** [workflow의 시작 경로](../skills/_coco-shared/workflow.md#introductory-path), [coco-spec](../skills/coco-spec/SKILL.md#coco-spec), [coco-plan](../skills/coco-plan/SKILL.md#coco-plan), [build 절차 1](../skills/coco-build/SKILL.md#procedure-and-output).

1.0.0 build는 기존 요청이나 명세를 읽게 한다.

> Read the agreed brief/spec and authoritative task state.

1.1.0은 기능의 동작을 추가하거나 바꿀 때 저장된 명세와 계획을 먼저 갖추도록 명시한다. workflow의 실제 문구는 다음과 같다.

> A behavior change requires saved spec and plan before code, even for a single task: reuse adequate files; follow project conventions, otherwise `docs/specs/<feature>.md` and `docs/plans/<feature>.md`. A small contract needs behavior/scope/acceptance; its plan can be one task with a check. Explanations and clear static edits are exempt.

**사용 예:** “CSV에 잘못된 행이 있으면 그 행만 건너뛰게 해줘”는 결과가 바뀌므로, 그 규칙과 확인 방법을 기존 명세·계획에 남기고 구현한다. 이미 충분히 적혀 있으면 새 파일을 만들거나 다시 승인받지 않는다. “버튼 문구의 오타를 고쳐줘”와 설명만 요청한 경우에는 이 두 문서가 필요하지 않다.

**이유·검증 V1/V6:** 다음 작업자가 대화 전체를 다시 읽지 않아도 합의한 동작과 할 일을 찾을 수 있어야 한다. 기존 파일 재사용, 작은 한 항목 계획, 정적 수정의 예외, 미정 선택의 보존을 함께 확인한다.

## 2. 사용자가 고른 작업은 이어가고, 고르지 않은 다음 스킬은 소개한다

**수정 위치:** [workflow의 수동·자동 전환](../skills/_coco-shared/workflow.md#manual-and-automatic-basic-transitions), [contracts의 작업 선택](../skills/_coco-shared/contracts.md#work-input-and-selection), `coco-spec`·`coco-plan`·`coco-build`·`coco-debug`·`coco-review`·`coco-verify`의 단계 연결 문구와 관련 상세 지침. 각 파일은 아래 수정 파일 표에서 열 수 있다.

1.0.0은 다음 원칙을 두지만, 스킬 간 전환 방식은 따로 정의하지 않는다.

> Existing approval for a defined scope persists; a missing material decision is not approval to guess.

1.1.0에서는 아직 선택하지 않은 전환과 이미 요청한 실행을 구분한다.

> Manual is the default. Before switching skills, including returning from review to build, state the current stage, next exact skill, purpose, expected result and why it is needed in plain language.

> An explicit next-skill request already chooses that execution. Reuse existing authorization, selections and valid evidence rather than asking again for them.

기존 지시가 같은 명세의 구현·리뷰·검증까지 명확히 포함하면 그 범위의 선택도 유지한다. 단순히 “계획을 실행해”라는 말만으로 모든 단계와 전문 스킬을 자동 선택한 것으로 확대하지 않는다. 자동 진행은 명세 하나에 연결하고, 단계가 바뀔 때 알리며, 리뷰·검증·수정·커밋을 마친 뒤 푸시 전에 멈춘다.

> An explicit request for implementation, review, verification and fixes for the same spec already selects those named stages; preserve that scope on resume without a new opt-in interview. Continuous task scheduling alone does not select unrequested stages.

**사용 예:** 사용자가 “이 명세를 구현하고 리뷰·검증까지 끝내줘”라고 했다면 각 단계에서 같은 허락을 다시 묻지 않는다. 구현만 요청했다면 완료 후 “다음은 `coco-review`입니다. 명세와 실제 변경을 대조합니다”라고 소개하고 한 번 실행 또는 이 명세의 기본 단계 자동 진행을 선택하게 한다.

**이유:** 스킬의 목적을 배울 시간을 주면서, 이미 한 선택을 반복해서 묻는 불편은 피한다.

**검증 V2:** 수동 전환 한 번, 명시적으로 요청한 다음 스킬, 기존의 구현·리뷰·검증 위임, 단순 계획 실행, 다른 명세로 이동, 재개 후 같은 명세의 권한 복구, 푸시 전 중지를 구분한다. 자동 모드가 다른 명세나 외부 공개로 번지면 실패다.

## 3. 전문 스킬 자동 사용은 정확히 선택한 범위에만 적용한다

**수정 위치:** [workflow의 전문 스킬 선택·개인 선호](../skills/_coco-shared/workflow.md#specialist-consent-and-personal-preferences), 공통 [routing.md](../skills/_coco-shared/routing.md)와 단계 안내.

1.0.0에는 전문 절차를 필요한 경우 선택하고 도구·권한을 확인하는 규칙이 있다. 사용자·프로젝트·스킬 하나로 제한한 개인별 자동 선택의 저장·철회 규칙은 없다.

1.1.0에서는 다음 경계를 둔다.

> A previously explicit user/project/skill opt-in can satisfy this gate; a basic-flow opt-in cannot. Selecting security never selects performance or migration as well.

**사용 예:** 이 프로젝트에서 `coco-security`를 자동으로 쓰기로 했어도 `coco-performance`까지 자동 실행하지 않는다. 철회하면 그 스킬의 선택만 지운다. 개인을 확인할 수 없거나 안전한 개인 저장 위치가 없으면 이번 작업의 선택만 유지하고, 다음 채팅에도 기억한다고 약속하지 않는다.

**이유:** 기본 흐름의 자동 진행과 전문 검사의 선택은 서로 다른 결정이기 때문이다. 개인 선호를 팀의 `AGENTS.md`에 써서 다른 사람에게 적용하지 않는다.

**검증 V3:** 특정 스킬 허용·다른 스킬 미허용, 다른 사용자·프로젝트 불일치, 하나만 철회, 저장 불가 시 수동 선택을 확인한다. 전문 스킬을 거절해도 필수 테스트와 보안 경계가 사라지면 실패다.

## 4. Jira가 없는 프로젝트에서도 기존 브랜치로 작업할 수 있게 한다

**수정 위치:** [coco-build의 브랜치 준비](../skills/coco-build/SKILL.md#feature-branch-preparation), [공통 Git 규칙](../skills/_coco-shared/contracts.md#ownership-git-and-recovery), [build의 재개 규칙](../skills/_coco-shared/advanced/build.md#resume-the-actual-task), [coco-push 절차 6](../skills/coco-push/SKILL.md#workflow)과 [브랜치·티켓 정렬](../skills/coco-push/references/branch-and-ticket.md).

1.0.0의 build 지침은 Jira 형식을 기본으로 요구한다.

> Use this team format for each new feature branch, including during continuous execution:

1.1.0에서는 프로젝트 규칙이 먼저다.

> Follow actual project naming rules. Without one use a descriptive feature branch and atomic commits; Jira is not required. Only when the project/team explicitly selects this Jira convention, apply it, including during continuous execution:

실험안에는 이 조건을 넣고도 뒤에 “이 형식과 다르면 확인하라”는 문장이 남아 있었다. 다음처럼 적용 대상을 좁힌다.

> When resuming a suitable same-task branch, keep it unless it conflicts with an actually selected project naming rule; only then explain the conflict and confirm how to proceed. Do not require a Jira-shaped name in a non-Jira project or automatically rename, delete, or reset a branch. Preserve existing user changes and record branch/base, plus Jira key and original Summary only when applicable.

push도 같은 조건을 따라야 한다. 1.0.0의 절차 6은 목적이 바뀌면 Jira Summary와 Description까지 갱신·확인하도록 되어 있다. 변경 후에는 실제로 연결된 Jira 작업이 있거나 프로젝트에서 그 형식을 선택한 경우에만 그 부분을 적용한다.

> Follow project naming rules; update and reread Jira Summary and Description only for an actual linked Jira task or explicitly selected Jira convention. Without either, do not invent a ticket or block on Jira access. Stop before pushing only when an applicable required decision, capability, authority or readback is missing.

**사용 예:** Jira를 쓰지 않는 저장소에서 `feat/csv-import` 작업을 재개할 때 티켓 번호를 묻지 않는다. Jira를 쓰는 저장소에서는 사용자가 정한 Summary를 그대로 보존하고 Git에서 허용하지 않는 문자만 별도로 확인한다.

**이유:** 공통 지침 한 줄만 조건부로 바꾸면 build 재개와 push에서 예전 필수 조건이 다시 나타날 수 있다. 연결된 경로 전체를 맞춘다.

**검증 V4:** Jira 없는 기존 브랜치의 재개, Jira 있는 정확한 Summary, Git에서 사용할 수 없는 Summary, 로컬 임시 원격을 사용한 push를 확인한다. 실제 Jira나 공개 원격에는 실험용 쓰기를 하지 않는다.

## 5. 구현 결과를 정하기 전에 빠진 중요한 선택을 찾는다

**수정 위치:** [workflow의 질문·위임·보고](../skills/_coco-shared/workflow.md#questions-delegation-and-reports)에 확인 방법을 한 번 정의한다. [contracts의 작업 선택](../skills/_coco-shared/contracts.md#work-input-and-selection)에서 연결하고, [coco-build 절차 1](../skills/coco-build/SKILL.md#procedure-and-output)과 [coco-clarify 절차 1](../skills/coco-clarify/SKILL.md#procedure-and-output)에서 이 확인을 적용하도록 명시한다. 상세 clarification 파일에만 숨겨두지 않는다.

1.0.0에도 다음 원칙은 있다.

> Reuse settled requirements and test boundaries; ask only for missing decisions that materially affect the result.

하지만 기존 실험에서는 “중복을 어떻게 처리할지”를 물은 뒤, “무엇을 같은 항목으로 볼지”는 묻지 않고 구현한 사례가 있었다. 원칙을 읽었다는 사실만으로 필요한 질문을 찾았다고 볼 수 없었다.

workflow에 들어간 지침은 다음과 같다.

> Before writing a behavioral test or implementation for a slice, use its actual input/output examples to find unsettled choices that change the public result. Recover answers from the request, accepted decisions and existing contracts first. Matching identity, handling a collision and choosing emitted representation are separate choices when they affect this task; settling one does not settle the others. Ask only the unresolved material choice. If its owner has no answer, leave dependent behavior pending and continue independent permitted work. This is not a fixed questionnaire or renewed approval for settled work; reversible implementation details remain the agent's choice.

build와 clarify에는 해당 확인을 적용하라는 연결을 추가했다. build는 테스트나 코드 작성 전이라는 실행 위치를 명시하고 다음 행동을 적었다.

> recover recorded answers, and check actual input/output for unresolved identity, collision or output choices that affect this slice. Ask only missing material choices; keep dependent behavior pending when unanswered.

clarify도 기존 답을 먼저 복구하도록 연결했다.

> recover settled answers before asking about public results that remain undecided. Separate discoverable facts from decisions the user must make.

**사용 예:** 상품 코드 ` A1 `과 `a1`을 받은 상황에서는 다음 세 가지가 다를 수 있다.

1. 앞뒤 공백과 대소문자를 무시하여 같은 상품으로 볼 것인가?
2. 같은 상품이 두 번 들어오면 첫 행을 유지할 것인가, 합칠 것인가, 거절할 것인가?
3. 화면과 내보내기에는 첫 행의 원래 표기를 보여줄 것인가, 정리한 표기를 보여줄 것인가?

이미 “같은 상품으로 보고, 첫 행과 원래 표기를 유지한다”고 정했다면 다시 묻지 않는다. 1번만 정했다면 2·3번까지 승인된 것으로 간주하지 않는다. 이 기능에 실제로 영향을 주는 미정 항목만 구체적인 예와 추천 이유를 붙여 묻는다. 답이 없으면 그 부분은 미정으로 남겨 다음 작업자도 알 수 있게 한다.

**이유:** 테스트의 기대값을 쓰는 순간에도 사용자가 정하지 않은 정책을 선택할 수 있다. 코드 직전뿐 아니라 기대값을 정하기 전에 확인해야 한다. 이번 변경이 질문 누락을 줄이는지는 새 사례에서 검증해야 한다.

자세한 설명은 workflow에 두고 구현 진입점에서 읽도록 한다. 관련 없는 push·merge·ship 실행 때마다 읽는 공통 본문을 크게 늘리지는 않는다. 검증에서는 링크가 있는지만 확인하지 않고 build가 해당 지침을 실제로 읽고 적용했는지도 확인한다.

**구현 중 새 제약을 발견한 경우도 다시 확인한다.** 실제 후보 실행에서는 SQLite가 큰 정수를 저장하지 못하자, 사용자와 정하지 않은 가격 상한을 코드와 테스트에 넣고 마지막에 허락을 물었다. 완료 상태를 대기로 표시한 것은 정확했지만, 그 전에 입력 범위를 좁힌 것은 승인된 선택이 아니었다. `workflow.md`의 같은 확인 절과 build 절차 2에 다음 조건을 추가했다.

> Repeat this check when implementation or verification exposes a technical constraint that would change agreed inputs, outputs or failure behavior. Preserve the agreement with an in-scope solution where possible; otherwise settle the material choice before adopting a new limit or fallback in tests, code or the contract, and keep dependent behavior pending while unanswered.

예를 들어 저장 방식만 조정해서 합의한 가격 범위를 그대로 지원할 수 있으면 에이전트가 해결한다. 현재 허용된 범위 안에서 지원할 수 없다면 입력 범위를 줄일지, 저장 방식 변경을 허용할지를 정책으로 굳히기 전에 묻는다. 모든 기술적 제한을 질문으로 바꾸라는 뜻은 아니다. 합의한 동작이 달라질 때 적용한다.

**검증 V5:** 최소 다섯 쌍의 고정된 사례에서 실험 버전 `622975e`와 후보를 비교한다. 이미 정한 선택 복구, 새로 물어야 할 선택, 답을 얻지 못한 안전한 중지, 출력 표기까지 포함한 소유자의 완전한 답을 넣는다. 구현 중 발견한 저장소 제한도 별도의 집중 사례로 확인한다. 실제 잘못 채택한 정책 때문에 고친 횟수를 세고, 단순 질문 수·예상된 실패·막혀 있던 작업의 완료와 구분한다. 사용자의 선택권·절차·결과·실행 실패가 늘면 채택을 막는다. 기존에 문제가 없는 사례에서 효과가 같으면 우위를 주장하지 않는다.

## 6. 처음 예상과 달라진 이유가 최종 보고에 남게 한다

**수정 위치:** [공통 완료 보고](../skills/_coco-shared/contracts.md#evidence-and-completion), [workflow의 질문·위임·보고](../skills/_coco-shared/workflow.md#questions-delegation-and-reports), [coco-build의 결과 보고](../skills/coco-build/SKILL.md#procedure-and-output), [상세 spec의 변경 처리](../skills/_coco-shared/advanced/spec.md#output-and-stopping-conditions). 기존 명세와 계획을 사용하며 새 기록 파일을 의무화하지 않는다.

1.0.0의 공통 보고 지침은 결과·필요한 결정·확인한 근거를 우선한다.

> Report the outcome first: the final state, then what the user must decide or do.

1.1.0에서는 보고할 비교 항목을 명시하고, 명세를 고쳤다는 이유로 처음의 가정이 사라지지 않게 한다.

> Keep the original expectation, superseding decision, reason and effect in the existing spec/decision record; a rewritten current agreement must not erase that history.

> Always include this comparison in the final user-facing development report, even when unchanged: `Expected: ...; actual: ...; departure and reason/effect: none / ...`. A work-record link alone does not satisfy it. Compare against the original expectation and any superseding decision, not only the latest spec text; say no material departure when appropriate.

**변경 전 보고 예:** 처음에는 ` A1 `과 `a1`을 다른 상품으로 구현했다가 사용자 답변으로 바꿨는데, 마지막에는 “수정된 명세대로 구현했고 설계 변경은 없습니다”라고 보고한다.

**변경 후 보고 예:** “처음에는 코드를 그대로 비교할 것으로 예상했습니다. 실제로는 앞뒤 공백과 대소문자를 무시하도록 바꿨습니다. 사용자가 같은 상품으로 취급한다고 결정했기 때문입니다. 첫 행의 원래 표기는 유지하며, 두 입력이 하나로 처리되는 것을 확인했습니다.” 처음부터 이 선택이 정해져 있었다면 “최초 예상과 실제 동작이 같고 중요한 변경은 없습니다”라고 보고한다.

**이유:** 현재 코드가 최신 명세와 일치하는지와, 개발 중 어떤 선택이 달라졌는지는 다른 정보다. 둘 다 있어야 사용자가 결과를 이해하고 다음 작업자도 변경 이유를 알 수 있다.

임시 프로젝트의 첫 실행에서는 “오타를 고쳤고 명세에서 달라진 점 없음”까지 말했지만 최초 기대를 따로 밝히지 않았다. 그래서 공통 지침의 **최종 보고를 작성하는 문단**에도 아래 조건을 넣고 같은 유형의 결과 보고를 다시 확인한다. 기존 실행의 부족한 결과는 그대로 남긴다.

> In every development final reply state the original expectation, actual choice and departure reason/effect (or none); a spec link or "matches spec" alone is insufficient.

**검증 V6:** 최초 선택 → 변경된 선택 → 새 작업자 인수인계 → 최종 보고를 확인한다. 현재 명세만 읽어 과거 변경을 없앤 보고, 선택을 지어낸 보고, 최종 답변 대신 내부 기록에만 비교를 남긴 보고를 실패로 구분한다.

## 7. 구현 커밋·리뷰·실제 실행 확인을 구분한다

**수정 위치:** [coco-build의 완료 보고](../skills/coco-build/SKILL.md#procedure-and-output), [상세 build의 작업 완료](../skills/_coco-shared/advanced/build.md#close-a-work-unit), [coco-review](../skills/coco-review/SKILL.md#coco-review), [coco-verify](../skills/coco-verify/SKILL.md), [contracts의 완료 규칙](../skills/_coco-shared/contracts.md#ownership-git-and-recovery)·[workflow의 완료 보고](../skills/_coco-shared/workflow.md#questions-delegation-and-reports)와 단계 연결 지침.

1.0.0 build는 요구사항·검사·리뷰 해결·커밋을 작업 완료 조건으로 묶는다. 1.1.0은 사용자가 결정한 순서대로 테스트와 자체 점검 후 구현 커밋을 만들고, 정식 리뷰 상태를 별도로 보고한다.

> Report implementation complete/review pending after build's checks, self-inspection and commit.

> Development complete requires acceptance, required reviews/resolutions, actual execution checks and commits.

리뷰가 커밋 뒤에 온다는 기본 흐름 때문에 기존의 작업 중 리뷰가 막혀서는 안 된다. 실험안의 “This is formal review after implementation commits” 문구는 다음처럼 범위를 분명히 한다.

> The normal build handoff is formal review after implementation commits; a direct request can review work in progress or an exact revision range without requiring a new commit.

**사용 예:** “커밋 전에 이 변경을 리뷰해줘”라고 하면 즉시 해당 범위를 검토한다. 자체 점검만 한 경우에는 독립 리뷰를 받았다고 표현하지 않는다. 브라우저 확인이 필수인데 실행하지 못했다면 단위 테스트가 통과해도 “브라우저 검증 대기”로 남긴다.

**이유:** 작업 단위의 이력을 남기면서, 무엇까지 확인했는지 정확하게 구분하려는 변경이다. 기존 직접 리뷰 요청과 실제 변경 범위의 검사는 유지한다.

**검증 V7:** 구현 커밋 후 리뷰, 커밋 전 직접 리뷰, 새 파일을 포함한 전체 변경 범위, 지적 후 수정 커밋, 독립 리뷰 불가, 필수 실행 환경 불가를 각각 확인한다. “완료”라는 단어만으로 서로 다른 상태를 합치면 실패다.

## 실제 파일에 어떻게 나누어 반영하는가

| 담당하는 규칙 | 수정한 파일 |
| --- | --- |
| 공통 원칙·질문·단계·개인 선택·출처 결정 | [contracts.md](../skills/_coco-shared/contracts.md), [workflow.md](../skills/_coco-shared/workflow.md), [routing.md](../skills/_coco-shared/routing.md), [decisions.md](../skills/_coco-shared/decisions.md) |
| 처음 안내와 스킬 탐색 | [coco-start](../skills/coco-start/SKILL.md), [coco-tellmeskill](../skills/coco-tellmeskill/SKILL.md) |
| 요구사항·명세·계획의 단계 연결 | [coco-clarify](../skills/coco-clarify/SKILL.md), [coco-spec](../skills/coco-spec/SKILL.md), [coco-plan](../skills/coco-plan/SKILL.md); 상세 [clarify](../skills/_coco-shared/advanced/clarify.md), [spec](../skills/_coco-shared/advanced/spec.md), [plan](../skills/_coco-shared/advanced/plan.md) |
| 구현·복구·리뷰·검증 | [coco-build](../skills/coco-build/SKILL.md), [coco-debug](../skills/coco-debug/SKILL.md), [coco-review](../skills/coco-review/SKILL.md), [coco-verify](../skills/coco-verify/SKILL.md); 상세 [build](../skills/_coco-shared/advanced/build.md), [context](../skills/_coco-shared/advanced/context.md) |
| 프로젝트에 맞는 브랜치·Jira 처리 | 위 build·공통 규칙과 [coco-push](../skills/coco-push/SKILL.md), [브랜치·티켓 정렬](../skills/coco-push/references/branch-and-ticket.md) |
| 사용 안내와 변경 근거 | [README](../README.md), [coverage.json](../sources/coverage.json), 관련 명세·계획·검증 기록. 원본 스냅샷과 라이선스는 보존한다. |

실험 버전의 스킬 변경 19개 파일을 검토해 필요한 단계 규칙을 가져왔다. 여기에 push 진입 지침의 조건 누락과 위 질문·보고 경로를 보완했다. 원본의 모든 규칙을 다시 넣거나 29개 진입 스킬을 합치는 작업은 아니다.

**검증 V8:** 파일·출처·링크 검사, 필수 저장소 테스트, 임시 설치 위치에서 설치와 다시 읽기, 기존 파일 보존을 확인한다. `python3 scripts/validate.py`와 `python3 -m unittest discover -s tests -v`를 실행한다. 실제 개인 설치 상태와 원격 공개 상태는 소스 변경 결과와 따로 보고한다.

## 이번에 유지하거나 보류할 부분

**명세와 계획을 더 줄이는 변경은 현재 하지 않는다(F5).** 현재 지침은 명세에 동작을, 계획에 실행 순서를, 지정된 한 곳에 작업 상태를 둔다. 이전 다섯 인수인계는 양쪽 모두 성공했고, 더 강하게 재사용을 지시한 문구는 정한 시간 감소 기준을 충족하지 못했다. 실제로 같은 상태를 두 곳에서 수정하는 문제가 확인되지 않으면 기존 구조를 유지한다. 위의 최초 예상 보존은 보고 누락을 고치기 위한 제한된 변경이며, 새 상태 기록소를 추가하지 않는다.

**돌아온 사용자에게 안내를 더 줄이는 변경도 보류한다(U1/U2).** 이전 다섯 안내 사례에서 기존 버전도 처음의 전체 표를 반복하지 않았다. 새 문구가 오히려 길었다. 실제 사용자의 불편과 서로 다른 안내 방식이 확인되어야 사람을 대상으로 비교할 이유가 생긴다. 모델의 짧은 답변만으로 “사람이 더 쉽게 고른다”고 판단하지 않는다.

**원본과의 차이는 근거로 보존한다.** [통합 결정 문서](skill-integration-decisions.md)와 [한국어판](skill-integration-decisions.ko.md)은 `8c81c9b`·`6f01c14`에서 공유된 감사 결과다. 원본 131개를 대응시켰다는 사실과 세부 방식까지 모두 보존했다는 주장을 구분한다. context 조건, 코드 냄새 목록, 가설 개수, mutation 실험과 모델 구성 등의 차이가 있다는 이유만으로 이번에 모두 복원하지 않는다. 이번 사용자 결정·관찰된 문제와 직접 연결되는 수정만 한다.

## 근거와 결과를 읽는 순서

이 문서는 **무엇을 어떻게 고칠지** 설명한다. 지켜야 하는 결과는 [명세](specs/coco-1.1.0.md), 현재 작업 상태와 커밋·검증 결과는 [작업 계획](plans/coco-1.1.0.md)이 맡는다. 같은 완료 상태를 여기에도 복사해 관리하지 않는다.

기존 관찰은 [절차·인수인계 보고서 v2](evaluation/staged-development/report-v2.md), [협업 가치 보고서](evaluation/collaboration-value/report.md), [개별 개선안 비교](evaluation/procedure-refinement/report.md)에 남긴다. 새 검증은 새 후보에 대한 결과로 기록하며, 기존 실패·미확정 사례를 고쳐서 성공으로 바꾸지 않는다. 검증 V1–V8은 이 문서의 확인 항목 이름이며, 실행 전에는 통과 결과가 아니다.

이번 실행에서 확인한 항목과 한계는 [작업 계획의 실제 실행 기록](plans/coco-1.1.0.md#recorded-behavior-with-evidence-limits)을 보면 된다. [비교 실험 기록](evaluation/coco-1.1.0/implementation/observations.md)은 실행 환경 오류로 끝내지 못한 사례까지 보존한다. 이 문서의 수정 항목 전체를 설명했다는 사실을, 모든 상황에서 효과가 입증됐다는 뜻으로 읽으면 안 된다.
