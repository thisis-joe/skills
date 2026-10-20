# 푸시 후 draft PR/MR 생성 평가

`coco-push`에 추가한 단계를 평가합니다. 푸시가 확인되면 열린 PR/MR을 찾고, 없을 때만 개발 기준 브랜치를 대상으로 **draft**를 만드는 단계입니다. 평가는 다음 방식으로 진행했습니다.

- 사례마다 새 컨텍스트의 에이전트 하나가 수정된 스킬([`485d661`](../../../skills/coco-push/references/pull-request.md))을 읽고 fixture에 적용했습니다.
- 요청문에는 PR이라는 말을 넣지 않았습니다. 기본 동작을 보기 위해서입니다.
- Git은 실제로 실행했습니다. 임시 작업 저장소, 로컬 bare 원격, fetch·merge·commit·push를 모두 실제로 했습니다.
- forge는 [`fake_forge.py`](fake_forge.py)입니다. 파일 기반의 **모의 `gh`/`glab`**이며, PR/MR의 head 커밋은 bare 원격에서 읽습니다.
- Jira는 [모의 어댑터](jira_adapter.py)입니다.
- 원격 URL은 `github.example.test`/`gitlab.example.test`를 저장소 로컬 `insteadOf`로 bare 원격에 연결했습니다. 따라서 외부 서비스에는 아무것도 쓰지 않았습니다.

| 사례 | 상황 | 관찰한 결과 | 판정 |
|---|---|---|---|
| `gh_template` | `.github/pull_request_template.md`(한국어) 있음 | develop 병합·검사 후 푸시. `develop` 대상 draft PR #40 생성. 템플릿 제목 5개를 순서대로 유지했고, 근거 있는 체크박스만 체크했으며, `리뷰어 지정`은 비워 둠 | 통과 |
| `gh_default` | 템플릿 없음 | 기본 양식의 필수 5개 절을 한국어로 작성. 동기화 커밋 기록 포함. UI·위험 변경이 없어 조건부 절은 생략 | 통과 |
| `gh_existing_open` | 같은 브랜치에 열린 draft PR #12 있음 | 푸시 후 #12를 조회해 보고만 함. 생성·수정 없음 | 통과 |
| `glab_default_template` | `Default.md`와 `Hotfix.md` 있음 | `Default.md`로 draft MR !40 생성. `Hotfix.md`는 선택 템플릿이라 쓰지 않음 | 통과 |
| `gh_draft_unsupported` | forge가 draft를 거절 | 푸시는 확인됨. draft 생성이 거절되자 일반 PR로 재시도하지 않음. 준비한 제목·본문과 선택지를 보고 | 통과 |
| `check_fails` | 병합 후 의미 충돌로 필수 검사 실패 | 푸시·forge 호출 없음. 병합 상태를 보존하고 제품 결정을 질문 | 통과 |
| `renamed_with_old_pr` | 할인과 쿠폰 검증을 함께 구현 | 요약 `할인_적용`이 적절하다고 판단해 이름 유지. 같은 브랜치의 열린 PR #21을 보고만 함. **이름 변경 경로는 실행되지 않음** | 통과(제한적) |
| `scope_drift_old_pr` | 요약이 이관된 다른 기능을 가리키고, 옛 브랜치에 열린 PR #21 있음 | 이름을 `쿠폰_코드_검증`으로 변경. Jira Summary/Description을 조건부로 수정하고 다시 읽어 확인. 새 이름으로 푸시. 새 브랜치와 옛 브랜치를 모두 조회해 #21을 찾았고, 중복 draft를 만들지 않은 채 새 draft 생성 여부를 질문. 옛 원격 브랜치와 #21은 그대로 | 통과 |

각 사례 폴더에 다음 자료를 보존했습니다.

- 요청: `request.json`
- 에이전트 원문 보고: `agent-report.md`
- forge 호출 기록과 최종 상태: `forge-calls.jsonl`, `forge-state.json`
- Jira 기록: `jira-*`
- 원격 ref 전후: `before-refs.txt`, `after-refs.txt`
- Git bundle 2개
- 자동 판정: `result.json`

[집계](result.json)에는 평가한 스킬 커밋과 파일 해시가 들어 있습니다. 판정 조건은 [`collect_evidence.py`](collect_evidence.py)에 있습니다. 확인하는 항목은 draft 여부, 대상·소스·head 커밋, 제목의 Jira 키, 템플릿 제목 순서, 기존 요청 무수정, 중복 생성 없음, 리뷰어·라벨 미지정, `--fill` 미사용, `main`·`develop` 무변경입니다. fixture는 [`build_fixtures.py`](build_fixtures.py)로 다시 만들 수 있습니다.

## 관찰과 제한

- **모의 forge의 범위:** `gh api`·`glab api`를 지원하지 않습니다. 그래서 조직 `.github` 저장소와 GitLab 프로젝트·그룹 기본 템플릿은 읽지 못했습니다. 세 에이전트가 이를 "확인 불가"로 보고했고, 이것은 스킬이 요구하는 동작입니다.
- **1차 실행 중 고친 mock:** 1차 실행의 mock은 `headRepositoryOwner`를 비워 반환했습니다. 에이전트들은 저장소 범위 조회와 head 커밋 일치로 판단했습니다. 보강 실행 전에 이 필드를 채웠고, 보강 사례 하나는 `build_fixtures.py`에 추가한 뒤 따로 실행했습니다.
- **스킬과 무관한 행동:** 두 에이전트가 자기 실행 환경의 커밋 서명 규칙에 따라, 푸시 전 병합 커밋 메시지에 trailer를 추가했습니다(트리 동일, 검사 재실행). 보강 사례의 준비 본문 끝에도 같은 환경의 생성 표기가 붙었습니다. 다른 두 에이전트는 메모 파일을 fixture 바깥에 잠깐 만들었다가 지웠습니다. 둘 다 스킬 규칙이 아닌 평가 환경의 영향입니다.
- **같은 작성자의 제한:** 같은 작성자가 fixture와 판정 조건을 만들었고, 사례마다 한 번씩만 적용했습니다. 반복 시험이나 모든 모델에서의 준수를 보장하지 않습니다.
- **검증하지 않은 것:** 실제 GitHub·GitLab의 권한·요금제·API 응답, fork 간 PR, Azure DevOps·Bitbucket, 네트워크 응답 유실 후 재조회는 검증하지 않았습니다.
- **경로 표기:** 기록 속 `/private/tmp/…` 경로는 당시 임시 실행 위치입니다.
