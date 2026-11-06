# COCO Skills

[![npm](https://img.shields.io/npm/v/@thisis-joe/coco-skills)](https://www.npmjs.com/package/@thisis-joe/coco-skills)

Codex와 Claude Code에서 쓰는 개발 스킬 30개입니다. 중요한 결정은 사용자가 내리고, 에이전트는 명세·구현·실행 근거를 남겨 다음 작업자가 이어받을 수 있게 합니다.

**목차:** [시작하기](#시작하기) · [1.5.3에서 바뀐 점](#153에서-바뀐-점) · [기능 하나를 진행하는 네 단계](#기능-하나를-진행하는-네-단계) · [전체 스킬](#전체-스킬) · [설치 위치·업데이트·제거](#설치-위치업데이트제거) · [문제 해결](#문제-해결) · [출처와 라이선스](#출처와-라이선스)

## 시작하기

Node.js 22 이상과 Python 3.9 이상이 필요합니다. Codex나 Claude Code는 따로 설치하고 로그인하세요.

스킬을 쓸 프로젝트 폴더에서 런타임에 맞는 명령을 실행합니다. 이미 설치했다면 같은 명령으로 업데이트됩니다.

```sh
# Claude Code
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime claude

# Codex
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime codex
```

설치 위치는 터미널에서 고릅니다. 설치가 끝나면 그 프로젝트에서 **새 세션**을 열고, Claude Code는 `/`, Codex는 `$`로 스킬을 부릅니다.

```text
/coco-start 주문 취소 기능을 만들려고 해. 진행 순서를 정해줘
$coco-start 주문 취소 기능을 만들려고 해. 진행 순서를 정해줘
```

어떤 스킬이 있는지 보려면 `/coco-tellmeskill`, 특정 스킬이 궁금하면 `/coco-tellmeskill coco-build 간단 설명`을 입력하세요.

<details>
<summary>npm 없이 소스에서 설치</summary>

```sh
git clone https://github.com/thisis-joe/skills.git
cd skills
python3 scripts/install.py --runtime claude --project /path/to/your-project
# Codex는 --runtime codex
```

`/path/to/your-project`는 이미 있는 프로젝트 폴더로 바꾸세요. 이 방법에는 Node.js와 npm이 필요 없습니다.

</details>

## 1.5.3에서 바뀐 점

- `coco-til`은 실제로 진단하고 해결을 확인한 문제를 세션당 한 건씩 `TIL/cases/`에 저장하고, `TIL/INDEX.md`의 `문제 해결 사례`에 연결합니다.
- 사례에는 관찰 결과가 다음 진단을 어떻게 결정했는지, 다음에 따라 할 절차와 분기, 조치 후 재검증 결과를 기록합니다. 읽기 전용 확인과 설정 변경 같은 작업은 구분합니다.
- 개념 노트 없이 사례만 남길 수 있습니다. 재검증 근거가 없으면 사례를 건너뛰고, 기존 사례는 새 근거가 있을 때만 갱신합니다. 개념 노트는 기존 형식과 주제당 최대 3개 제한을 유지합니다.

자세한 내용은 [1.5.3 릴리스 노트](docs/coco-1.5.3.md)를 보세요. 이전 버전의 변경 사항은 [1.5.2](docs/coco-1.5.2.md) · [1.5.1](docs/coco-1.5.1.md) · [1.5.0](docs/coco-1.5.0.md) · [1.4.2](docs/coco-1.4.2.md) · [1.4.1](docs/coco-1.4.1.md) · [1.4.0](docs/coco-1.4.0.md) · [1.3.0](docs/coco-1.3.0.md) · [1.2.0](docs/coco-1.2.0.md) · [1.0.0 → 1.1.0](https://github.com/thisis-joe/skills/blob/v1.1.0/docs/coco-1.0.0-to-1.1.0.md)에 있습니다. 소스 버전 준비, GitHub 병합, npm 게시는 각각 별개의 상태입니다.

## 기능 하나를 진행하는 네 단계

COCO는 합의한 동작을 작은 변경으로 구현하고, 실제로 실행해 본 근거로 완료를 판단합니다. 처음에는 아래 10개로 흐름을 익히고, 필요할 때 조사·설계·보안·성능 같은 전문 스킬을 고르세요.

| 단계 | 먼저 익힐 스킬 | 결과 |
|---|---|---|
| 요구사항 정리 | `coco-clarify`, `coco-spec`, `coco-plan` | 합의한 동작, 저장된 명세와 작업 계획 |
| 구현 | `coco-build`, `coco-debug` | 테스트와 자체 점검을 거친 구현 커밋 |
| 리뷰·검증 | `coco-review`, `coco-verify` | 별도 리뷰, 실제 실행 확인, 수정 커밋 |
| 출시 | `coco-push`, `coco-merge`, `coco-ship` | PR 공유, 병합, 배포 |

- **질문은 필요한 것만.** 모호한 새 기능은 요구사항 정리부터 시작합니다. 문구 수정처럼 명확한 정적 변경은 바로 처리합니다. 질문에는 선택지별 동작과 비용, 추천안과 이유가 함께 나옵니다.
- **다음 단계는 사용자가 고릅니다.** 아직 고르지 않은 다음 스킬은 설명하고 선택을 받습니다. "이번 스킬만 진행"과 "이번 명세의 기본 절차를 자동 진행" 중에서 고를 수 있습니다. 자동 진행도 새로운 중요한 결정은 묻고, 리뷰·검증·수정 커밋을 마친 뒤 **푸시 직전에 멈춰** 보고합니다.
- **완료는 근거로 말합니다.** 구현 커밋만 있으면 "구현 완료·리뷰 대기", 필수 실행 확인을 못 했으면 "실행 검증 대기"로 보고하고 개발 완료라고 하지 않습니다. 보고에는 처음 예상한 설계, 실제 선택, 바꾼 이유가 남습니다.
- **출시 작업은 따로 요청합니다.** `coco-push`는 동기화·푸시 후 열린 요청이 없으면 개발 브랜치 대상 draft PR/MR을 엽니다. `coco-merge`는 체크가 통과하면 대상 브랜치에 병합합니다. `coco-ship`은 출시 판단과 요청 범위의 배포를 맡습니다. 새로 연 PR/MR은 연 사람을 담당자와 리뷰어로 지정하고, 저장소에 있는 레이블 중 맞는 것을 붙입니다([규칙](skills/_coco-shared/request-metadata.md)).

전체 기준은 [명세](https://github.com/thisis-joe/skills/blob/v1.1.0/docs/specs/staged-development.md)와 [공통 흐름](skills/_coco-shared/workflow.md)에 있습니다.

## 전체 스킬

할 일과 스킬이 정해졌다면 `coco-start`를 거치지 않고 바로 부르세요. 모든 작업에 전체 절차가 필요한 것은 아닙니다.

```text
coco-clarify → coco-spec → coco-plan → coco-build → coco-review → coco-push → coco-merge
```

| 목적 | 스킬 |
|---|---|
| 시작·스킬 탐색 | `coco-start`, `coco-tellmeskill`, `coco-whattosay` |
| 요구·설계·계획 | `coco-clarify`, `coco-research`, `coco-design`, `coco-spec`, `coco-plan` |
| 구현·개선 | `coco-build`, `coco-debug`, `coco-simplify`, `coco-migrate` |
| 검증·전문 검토 | `coco-review`, `coco-verify`, `coco-security`, `coco-performance`, `coco-frontend` |
| 운영·배포 | `coco-observe`, `coco-automate`, `coco-push`, `coco-merge`, `coco-ship` |
| 문서·학습·협업 | `coco-docs`, `coco-blog`, `coco-til`, `coco-askme`, `coco-context`, `coco-retro`, `coco-triage`, `coco-updateskill` |

요청 없이 스킬 이름만 부르면 이미 정해진 요청을 이어 가거나, 무엇을 요청할지 안내합니다. 몇 가지는 다르게 동작합니다.

- `coco-start`는 읽기만 하고 진행 경로를 알려 줍니다.
- `coco-askme`(별칭 `coco-research`)는 현재 세션의 개념을 최대 3개 보여 줍니다. 구체적인 질문에는 근거와 함께 바로 답하고, 퀴즈는 요청할 때만 냅니다.
- `coco-til`은 현재 세션의 개념 노트와 검증한 문제 해결 사례를 남기고, `coco-blog`는 로컬 노트를 고르는 데서 시작합니다.
- `coco-push`와 `coco-merge`는 현재 브랜치에서 **바로 실행**합니다. 설명만 원하면 그렇게 요청하세요.

각 스킬의 절차는 [스킬 원본](skills)에, 선택 기준은 [작업별 안내](skills/_coco-shared/routing.md)에 있습니다. 외부 서비스가 필요한 작업은 그 연결과 권한이 준비되어 있어야 합니다.

## 설치 위치·업데이트·제거

아래 명령은 **1.5.3 기준**입니다. `claude` 대신 `codex`를 쓰면 Codex에 적용됩니다.

```sh
# 현재 프로젝트에 설치하거나 업데이트
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime claude --project .

# 모든 프로젝트에서 사용
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime claude --global

# 프로젝트로 옮기면서 기존 글로벌 설치 제거
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime claude --project . --remove-global

# 현재 프로젝트에서 제거
npx --yes @thisis-joe/coco-skills@1.5.3 uninstall --runtime claude --project .
```

| 런타임 | 프로젝트 설치 | 글로벌 설치 |
|---|---|---|
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Codex | `.agents/skills` | `~/.codex/skills` |

- `CLAUDE_CONFIG_DIR`나 `CODEX_HOME`을 설정했다면 그 폴더 아래 `skills`가 글로벌 위치입니다.
- `--project`는 여러 번 쓸 수 있고, `--dest`로 설치 위치를 직접 정할 수도 있습니다.
- 위치 옵션이 없으면 터미널에서는 위치를 묻고, 비대화형 환경에서는 글로벌로 설치합니다.
- 프로젝트 설치 파일은 `.git/info/exclude`로 Git 변경 목록에서 뺍니다. 두 런타임을 쓰면 각각 설치·업데이트하세요.
- 결과가 `installed`나 `unchanged`면 성공입니다. 바꾸기 전에 확인하려면 `--dry-run`을 붙이세요.
- 직접 고친 파일이나 같은 이름의 다른 스킬과 충돌하면 아무것도 바꾸지 않고 멈춥니다.
- 글로벌 설치가 남아 있으면 다른 프로젝트에서도 스킬이 보입니다. 프로젝트에서만 쓰려면 `--remove-global`을 쓰세요.

세부 동작과 검증 명령은 [배포 안내](docs/distribution.md)에 있습니다.

## 문제 해결

- **스킬이 안 보이면:** 설치 결과의 `destination`을 확인하고, 그 프로젝트에서 새 세션을 여세요.
- **Python을 못 찾으면:** Python 3.9 이상을 설치하거나 `COCO_PYTHON`에 실행 파일 경로를 지정하세요.
- **수정한 파일과 충돌하면:** 개인 변경을 백업한 뒤 비교하세요. 설치 기록만 지워서 넘어가지 마세요.
- **목차 오류로 멈추면:** 고친 `SKILL.md`의 `**Contents:**` 줄이 `##` 섹션과 같은 이름·순서인지 확인하세요.
- **다른 프로젝트에서도 보이면:** 글로벌 설치가 남아 있는지 확인하세요.

Codex와 Claude Code의 로컬 스킬 설치만 지원합니다. claude.ai·Cowork 업로드용 패키지는 없습니다. npm 패키지를 받는 것만으로는 스킬 폴더가 바뀌지 않으며, `install` 명령을 실행해야 합니다.

## 출처와 라이선스

[Matt Pocock의 skills](https://github.com/mattpocock/skills), [Addy Osmani의 agent-skills](https://github.com/addyosmani/agent-skills), [Lauren Tan의 pstack](https://github.com/cursor/plugins/tree/main/pstack)을 목적별로 통합하고 팀 작업 절차를 더했습니다.

- [공통 계약](skills/_coco-shared/contracts.md): 검증 근거, 작업 단위 커밋, 권한 경계
- [결정 기록](skills/_coco-shared/decisions.md): 원본 규칙을 통합한 기준
- [원본 대응표](docs/source-index.md): 출처별 통합 위치
- [저작권 고지](THIRD_PARTY_NOTICES.md) · [MIT 라이선스](LICENSE)

원본 자료는 `sources/`에 증거로만 보관하며, 설치하거나 실행하지 않습니다.
