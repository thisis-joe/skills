# COCO Skills

[Matt Pocock의 skills](https://github.com/mattpocock/skills), [Addy Osmani의 agent-skills](https://github.com/addyosmani/agent-skills), [Lauren Tan의 pstack](https://github.com/cursor/plugins/tree/main/pstack)을 **목적별 27개 스킬**로 합친 개발 스킬 모음입니다. Codex와 Claude Code에서 같은 스킬을 씁니다.

## 설치

필요: **Node.js 22+**, **Python 3.9+** (npm 계정 불필요)

```sh
# Codex
npx --yes @thisis-joe/coco-skills@latest install --runtime codex

# Claude Code
npx --yes @thisis-joe/coco-skills@latest install --runtime claude
```

| 런타임 | 설치 위치 | 호출 | 확인 |
|---|---|---|---|
| Codex | `~/.codex/skills` (`$CODEX_HOME/skills`) | `$coco-start` | 새 대화 또는 스킬 새로고침 |
| Claude Code | `~/.claude/skills` (`$CLAUDE_CONFIG_DIR/skills`) | `/coco-start` | 새 세션의 `/` 메뉴 |

| 하고 싶은 것 | 방법 |
|---|---|
| 업데이트 | 같은 `install` 명령 다시 실행 |
| 바뀔 내용만 미리 보기 | `--dry-run` 추가 |
| 프로젝트 한 곳에만 설치 | `--dest ./my-project/.claude/skills` |
| 버전 고정 | `@thisis-joe/coco-skills@0.3.0` |
| 설치 파일 검사 | `validate --installed <설치 폴더>` |
| Python 경로 지정 | 환경 변수 `COCO_PYTHON` |
| npm 없이 설치 | 저장소 clone 후 `python3 scripts/install.py --runtime codex` (또는 `claude`) |

- 다른 스킬과 직접 수정한 설치 파일은 덮어쓰지 않습니다. 충돌이 있으면 변경 전에 멈춥니다.
- 로컬 설치용입니다. claude.ai·Cowork 업로드 패키지는 제공하지 않습니다.

## 바로 쓰기

| 상황 | 호출 |
|---|---|
| 어떤 스킬을 써야 할지 모름 | `coco-start` + 하려는 일 |
| 스킬 목록과 설명 보기 | `coco-tellmeskill` |
| 고른 스킬에 뭐라고 요청할지 추천받기 | `coco-whattosay coco-review` |

Codex는 `$`, Claude Code는 `/`를 붙입니다.

```text
/coco-clarify 주문 취소 기능에서 아직 안 정한 동작을 확인해줘
/coco-clarify 이 마이그레이션 계획을 grill 해줘
/coco-build 승인한 계획의 다음 작업 하나를 구현해줘
/coco-review 미커밋 변경과 새 파일까지 포함해서 검토해줘
/coco-push origin/develop 기준으로 최신화하고 검증 후 푸시해줘
```

## 스킬 목록

| 단계 | 스킬 | 이럴 때 |
|---|---|---|
| 시작 | `coco-start` | 절차 선택, 실행 명령·품질 기준 설정 |
| 정의 | `coco-clarify` | 요구·용어·아이디어가 모호함, 계획을 grill(압박 질문)로 검증 |
| | `coco-research` | 코드 동작·설계 이유·외부 API 조사 |
| | `coco-design` | 인터페이스·구조·테스트 경계·프로토타입 |
| | `coco-spec` | 합의한 내용을 명세와 수용 조건으로 남김 |
| | `coco-plan` | 의존 순서가 있는 작은 작업으로 분해 |
| 구현 | `coco-build` | 기능·버그 수정·계획 실행, 작업별 커밋 |
| | `coco-debug` | 원인이 모호한 실패, 재현이 어려운 버그 |
| | `coco-simplify` | 동작은 유지하고 복잡도·죽은 코드 제거 |
| | `coco-migrate` | API·스키마 전환, 폐기, 넓은 일괄 변경 |
| 전문 | `coco-frontend` | UI·반응형·상태·접근성 |
| | `coco-security` | 인증·권한·민감 정보·외부 입력 |
| | `coco-performance` | 측정 기반 성능 개선, 벤치마크 판정 |
| | `coco-observe` | 로그·지표·추적·알림·런북 |
| 품질 | `coco-verify` | 실제 동작·변경 영향 확인, 검증 도구 |
| | `coco-review` | 명세·팀 규칙·코드 품질 검토 |
| 출시 | `coco-ship` | PR 준비, 출시 가능 판단, 롤아웃 |
| | `coco-push` | dev/develop 반영 → 충돌 해결·검증 → 작업 브랜치 푸시 |
| | `coco-automate` | CI·반복 작업·봇 자동화 |
| 기록 | `coco-document` | ADR·API 문서·설명·교육 자료 |
| | `coco-context` | 인수인계, 중단 후 재개, 긴 작업 기록 |
| | `coco-retro` | 회고, 반복 실패의 구조적 개선 |
| | `coco-triage` | 이슈 분류·중복 확인·작업 준비 상태 |
| 도우미 | `coco-tellmeskill` | 스킬 목록과 간단/상세 설명 |
| | `coco-whattosay` | 고른 스킬에 맞는 요청문 추천 후 선택 실행 |
| | `coco-askme` | 작업한 코드를 질문으로 복습 |
| | `coco-updateskill` | 기존 스킬을 팀 규칙에 맞게 수정·설치 (항상 새 브랜치·워크트리에서 작업) |

## 공통 원칙

| 원칙 | 내용 |
|---|---|
| 근거 있는 완료 | 실행하지 못한 검사는 통과로 표시하지 않음 |
| 작업 단위 | 기능별 브랜치, 작업별 커밋 |
| 권한 유지 | 배포·외부 쓰기·삭제는 요청한 범위 안에서만 |
| 멈춤 신호 | "나중에 테스트", "확실해" 같은 합리화가 보이면 멈추고 바로잡음 |
| 필요한 만큼만 읽기 | 각 스킬이 고급 절차를 읽어야 할 조건을 명시 |

`coco-build` 브랜치 이름은 `type(part)/작업번호-Jira요약`입니다. 예: `feat(be)/123-OAuth2.0_구글` ([상세 규칙](https://github.com/thisis-joe/skills/blob/main/skills/coco-build/SKILL.md#feature-branch-preparation))

## 출처와 문서

| 원본 | 주로 반영한 절차 |
|---|---|
| Matt Pocock | 요구 구체화(grill), 명세·작업 분해, TDD, 구조 설계, 인수인계 |
| Addy Osmani | 명세 기반 개발, 구현·리뷰·출시 흐름, 보안·성능·운영, 멈춤 신호 |
| Lauren Tan (pstack) | 설계 대안 비교, 변경 영향 검토, 전제 재검증, 맥락 관리·회고 |

| 문서 | 내용 |
|---|---|
| [공통 계약](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/contracts.md) | 완료 조건·검증 근거·커밋·권한 경계 |
| [결정 기록](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/decisions.md) | 원본 규칙이 충돌할 때 고른 기준과 이유 |
| [원본 대응표](https://github.com/thisis-joe/skills/blob/main/docs/source-index.md) | 원본 131개 항목의 통합 위치 |
| [배포 안내](https://github.com/thisis-joe/skills/blob/main/docs/distribution.md) | 설치 세부 옵션, 게시 절차 |
| [THIRD_PARTY_NOTICES](https://github.com/thisis-joe/skills/blob/main/THIRD_PARTY_NOTICES.md) | 원본 저작권·라이선스 고지 |

원문은 `sources/`에 체크섬과 함께 보관하며 설치하거나 실행하지 않습니다. 라이선스: MIT
