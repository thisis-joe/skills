# COCO Skills

[![npm](https://img.shields.io/npm/v/@thisis-joe/coco-skills)](https://www.npmjs.com/package/@thisis-joe/coco-skills)

Codex와 Claude Code에서 쓰는 개발 스킬 30개. 중요한 동작은 사용자가 결정하고, 에이전트는 명세·구현·실행 근거를 남겨 다음 작업자가 이어받을 수 있게 합니다.

## 시작하기

Node.js 22 이상과 Python 3.9 이상이 필요합니다. 사용할 에이전트는 별도로 설치하고 로그인하세요.

이번 버전은 **1.3.0**이며, `coco-learn`을 `coco-til`로 교체했습니다. 아래 npm 설치 명령은 **1.3.0용**입니다. [변경·이전 안내](docs/coco-1.3.0.md)를 확인하세요. [1.0.0 → 1.1.0 변경 지점](https://github.com/thisis-joe/skills/blob/v1.1.0/docs/coco-1.0.0-to-1.1.0.md)에 수정한 지침, 변경 전후 예시와 검증 방법을 정리했습니다.

사용할 프로젝트 폴더에서 런타임에 맞는 명령을 실행합니다.

```sh
# Claude Code
npx --yes @thisis-joe/coco-skills@1.3.0 install --runtime claude

# Codex
npx --yes @thisis-joe/coco-skills@1.3.0 install --runtime codex
```

터미널에서 설치 위치를 고를 수 있습니다. 기존 설치도 같은 명령으로 업데이트합니다. 설치 후 해당 프로젝트에서 **새 세션**을 여세요. Claude Code는 `/`, Codex는 `$`로 스킬을 호출합니다.

```text
/coco-start 주문 취소 기능을 만들려고 해. 진행 순서를 정해줘
$coco-start 주문 취소 기능을 만들려고 해. 진행 순서를 정해줘
```

스킬을 둘러보려면 `/coco-tellmeskill`, 특정 스킬을 알아보려면 `/coco-tellmeskill coco-build 간단 설명`을 입력하세요. Codex에서는 앞의 `/`를 `$`로 바꿉니다.

<details>
<summary>소스에서 설치 — npm 없이 사용</summary>

```sh
git clone https://github.com/thisis-joe/skills.git
cd skills
python3 scripts/install.py --runtime claude --project /path/to/your-project
# Codex는 --runtime codex
```

`/path/to/your-project`를 이미 존재하는 프로젝트 폴더로 바꾸세요. Python 직접 설치에는 Node.js와 npm이 필요 없습니다.

</details>

<details>
<summary>설치 위치 · 업데이트 · 제거</summary>

아래 명령은 **1.3.0 기준**입니다. `claude` 대신 `codex`를 지정하면 Codex에 적용됩니다.

```sh
# 현재 프로젝트에 설치하거나 업데이트
npx --yes @thisis-joe/coco-skills@1.3.0 install --runtime claude --project .

# 모든 프로젝트에서 사용
npx --yes @thisis-joe/coco-skills@1.3.0 install --runtime claude --global

# 프로젝트로 옮기면서 기존 글로벌 설치 제거
npx --yes @thisis-joe/coco-skills@1.3.0 install --runtime claude --project . --remove-global

# 현재 프로젝트에서 제거
npx --yes @thisis-joe/coco-skills@1.3.0 uninstall --runtime claude --project .
```

| 런타임 | 프로젝트 설치 | 글로벌 설치 |
|---|---|---|
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Codex | `.agents/skills` | `~/.codex/skills` |

- `CLAUDE_CONFIG_DIR` 또는 `CODEX_HOME`을 설정했다면 해당 폴더 아래 `skills`가 글로벌 위치입니다.
- `--project`는 여러 번 지정할 수 있습니다. `--dest`로 별도 설치 위치를 정할 수도 있습니다.
- 위치 옵션 없이 실행하면 터미널에서는 위치를 묻고, 비대화형 환경에서는 글로벌로 설치합니다.
- 프로젝트 설치 파일은 `.git/info/exclude`로 Git 변경 목록에서 제외합니다. 두 런타임을 쓰면 각각 설치·업데이트하세요.
- `installed` 또는 `unchanged`이면 설치 성공입니다. `--dry-run`으로 변경 전 확인할 수 있습니다.
- 설치·제거 시 직접 수정한 파일이나 다른 스킬과 충돌하면 중단합니다. 파일을 먼저 보관하고 충돌을 해결하세요.
- 글로벌 설치를 남기면 다른 프로젝트에서도 스킬이 보입니다. 프로젝트에서만 쓰려면 `--remove-global`을 사용하세요.

세부 동작과 검증 명령은 [배포 안내](docs/distribution.md)를 참고하세요.

</details>

## 1.3.0에서 바뀐 점

- `coco-learn`을 [coco-til](skills/coco-til/SKILL.md)로 교체합니다. 현재 세션에서 재사용할 개념을 주제별 **최대 3개** 골라 바로 작성하거나 기존 노트를 보완합니다. 개수를 채우기 위한 추가 내용이나 저장 확인 질문은 만들지 않습니다.
- Git 저장소의 TIL은 **기본 체크아웃의 `TIL/`**에 저장합니다. 현재 브랜치 이름과 관계없으며, 추가 worktree를 삭제해도 노트가 함께 사라지지 않습니다. 별도 Git 디렉터리에서는 기록된 `core.worktree`를 확인하고, 기본 경로를 검증할 수 없으면 대체 저장하지 않습니다.
- 노트 형식·분량 제한·검사기는 유지합니다. 같은 개념은 기존 노트를 갱신하며, 새 정보가 없으면 내용과 날짜를 바꾸지 않습니다. 남길 개념이 없으면 파일을 만들지 않습니다.
- 기존 설명·복습·장기 강의 모드는 제거합니다. 질문으로 이해도를 점검하려면 `coco-askme`, 근거를 조사하려면 `coco-research`를 사용합니다. 기존 노트는 보존하며, 추가 worktree의 노트를 옮길 때 충돌하는 내용은 덮어쓰지 않습니다.

위 npm 명령이나 소스 설치기로 업데이트한 뒤 새 세션에서 실행하세요. 지원 설치기는 기존 `coco-learn`을 제거하고 `coco-til`을 등록합니다. 두 런타임을 사용한다면 각각 업데이트해야 합니다.

```text
/coco-til
$coco-til
```

스킬 수는 30개이며, 이번 변경은 스킬 이름과 역할을 바꿉니다. Git에서 제외한 TIL은 별도 백업되지 않으므로 기본 작업 폴더 자체의 백업은 별도로 관리하세요. `1.3.0` 소스 준비·Git 병합과 npm 게시는 별개입니다.

## 1.2.0에서 바뀐 점

- [coco-blog](skills/coco-blog/SKILL.md)를 추가합니다. 로컬 TIL 선택, 근거 있는 개발 글 초안 작성, 저장소의 실제 게시 절차 준비를 지원합니다.
- 프로젝트의 실제 초안·공개 상태 필드를 따릅니다. Hugo의 `draft` 필드를 모든 프로젝트에 강제하지 않습니다.
- 원본 노트와 개발 브랜치를 보존하고, 게시 원고는 별도 worktree에 준비합니다. 글 작성·문구 수락·push 요청만으로 PR/MR 생성이나 공개 게시를 수행하지 않습니다.

스킬은 29개에서 30개로 늘며 기존 이름과 설치 인터페이스는 유지합니다. [1.2.0 배포 안내](docs/coco-1.2.0.md)에 변경 내용과 검증 범위를 정리합니다. 1.2.0 npm 게시와 공개 패키지의 Codex·Claude 프로젝트 설치·재설치 검증을 완료했습니다. 설치 후 해당 프로젝트에서 새 세션을 여세요.

## 1.1.0에서 바뀐 점

- 처음에는 네 단계와 입문 스킬 10개를 안내합니다. 전체 29개와 전문 스킬 직접 호출은 유지합니다.
- 아직 고르지 않은 다음 단계는 설명하고 선택받습니다. 이미 요청한 구현·리뷰·검증은 다시 승인받지 않습니다.
- 동작 변경 전에 기존 명세와 계획을 읽고, 결과를 바꿀 미정 선택만 구체적으로 묻습니다. 구현 중 새 제약을 발견해도 합의한 요구사항을 임의로 줄이지 않습니다.
- 프로젝트의 브랜치 규칙을 따릅니다. Jira가 없는 프로젝트에 티켓을 요구하지 않으며, 커밋 전 직접 리뷰도 가능합니다.
- 완료 보고에 처음 예상·실제 선택·달라진 이유를 남깁니다. 구현 완료, 리뷰 대기, 필수 실행 검증 대기를 구분합니다.
- 최근 사용 기록의 프로젝트 구분, 실제 PR 병합 대상 확인, 학습 노트의 Markdown 예제 판별을 고칩니다. 티켓 처리 실패 복구와 내부 테스트 정리 조건도 기존 운영 보완을 유지합니다.

설치 명령과 스킬 이름은 그대로입니다. 모델의 기능·속도 우위를 약속하는 변경이 아닙니다. 사용자가 정한 개발 절차와 확인 근거를 일관되게 남기는 데 목적이 있습니다.

## 기능 하나를 진행하는 네 단계


COCO는 합의한 동작을 작은 변경으로 구현하고 실제 실행 근거로 완료를
판단합니다. 처음에는 아래 10개로 흐름을 익히고, 필요할 때 조사·설계·보안·성능
등 전문 스킬을 고르세요. 모든 스킬은 설치되며 전체 목록도 계속 볼 수 있습니다.

| 단계 | 먼저 익힐 스킬 | 기대 결과 |
|---|---|---|
| 요구사항 정리 | `coco-clarify`, `coco-spec`, `coco-plan` | 합의한 동작, 저장된 명세와 작업 계획 |
| 구현 | `coco-build`, `coco-debug` | 테스트와 자체 점검을 거친 구현 커밋, 리뷰 대기 |
| 리뷰·검증 | `coco-review`, `coco-verify` | 별도 리뷰, 실제 실행 확인, 수정 후속 커밋 |
| 출시 | `coco-push`, `coco-merge`, `coco-ship` | 목적에 따라 PR 공유·병합·배포 |

모호한 새 기능을 자연어로 요청하면 요구사항 정리 단계라고 알리고 질문을
시작합니다. 명확한 문구 같은 정적 수정은 바로 처리합니다. 동작 추가·변경은
작아도 명세와 계획 파일을 먼저 갖추며, 기존에 충분한 파일은 재사용합니다.

기본은 **아직 선택하지 않은 다음 스킬을 설명하고 선택받기**입니다. 이미 같은 명세의 구현·리뷰·검증을 요청했다면 그 선택은 다시 묻지 않습니다. 다음 스킬 안내에서
“이번 스킬만 진행” 또는 “이번 명세의 기본 절차를 자동 진행”을 고릅니다.
자동 진행도 새로운 중요한 결정은 묻고, 리뷰·검증·수정 커밋까지 마친 뒤
**푸시 직전에 멈춰 보고**합니다. 전문 스킬은 별도로 소개하고 선택받으며,
특정 전문 스킬의 자동 적용은 해당 사용자·프로젝트·스킬에 한정합니다. 안전한 개인 저장이 가능할 때만 다음 작업에도 기억합니다.

질문은 구체적인 상황, 선택에 따른 동작과 비용, 추천안과 이유를 제시합니다.
추가로 논의할 질문과 추천값을 본 뒤 더 질문하거나 그 추천안에 맡길 수 있습니다.
완료 보고는 원래 예상 설계·실제 선택·변경 이유·영향·실행 근거를 구분합니다.

구현 커밋만 있으면 “구현 완료·리뷰 대기”입니다. 필수 실행 확인이 불가능하면
“실행 검증 대기”이며 개발 완료라고 하지 않습니다. 독립 리뷰의 한계와 실행
검증 누락도 구분합니다. [명세](https://github.com/thisis-joe/skills/blob/v1.1.0/docs/specs/staged-development.md)와
[공통 흐름](skills/_coco-shared/workflow.md)에 전체 기준이 있습니다.

`coco-push`는 요청한 동기화·푸시 후 열린 요청이 없으면 개발 브랜치 대상 draft
PR/MR을 엽니다. `coco-merge`는 선택한 PR/MR의 대상 브랜치로 체크 통과 후
병합합니다. `coco-ship`은 출시 판단과 요청 범위의 배포를 맡습니다.
자동 개발 진행만으로 이 작업들이 허용되지는 않습니다.


<details>
<summary>전체 스킬과 작업 흐름</summary>

필요한 단계부터 시작하세요. 모든 작업에 전체 절차가 필요한 것은 아닙니다. 할 일과 스킬이 정해졌다면 `coco-start`를 거치지 않고 바로 호출하세요.

A bare invocation reuses a settled request or offers request guidance. Exceptions: `coco-start` returns read-only routing; `coco-tellmeskill`, `coco-updateskill` and `coco-whattosay` use their own selection. `coco-askme` and its `coco-research` alias offer session concepts. `coco-til` captures the session directly; `coco-blog` selects local notes. `coco-push` and `coco-merge` execute on the current branch, so explicitly request an explanation when execution is not intended.

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

`coco-askme` offers up to three session concepts on a bare call, using bounded recovery when context was compressed. Explicit questions receive evidence-backed answers; quizzes run only when requested. `coco-research` is a compatibility alias with the same behavior.

각 스킬의 절차는 [스킬 원본](skills), 선택 기준은 [작업별 안내](skills/_coco-shared/routing.md)에 있습니다. 외부 서비스 연결과 권한이 필요한 작업은 해당 환경이 준비되어 있어야 합니다.

</details>

<details>
<summary>문제 해결과 지원 범위</summary>

- **스킬이 안 보이면:** 설치 결과의 `destination`을 확인하고 해당 프로젝트에서 새 세션을 여세요.
- **Python을 못 찾으면:** Python 3.9 이상을 설치하거나 `COCO_PYTHON`에 실행 파일 경로를 지정하세요.
- **수정 파일 충돌이 나면:** 개인 변경을 백업하고 비교하세요. 설치 기록만 지워서 해결하지 마세요.
- **다른 프로젝트에서도 보이면:** 기존 글로벌 설치가 남아 있는지 확인하세요.

Codex와 Claude Code의 로컬 스킬 설치를 지원합니다. claude.ai·Cowork 업로드용 패키지는 제공하지 않습니다. npm 패키지를 받는 것만으로 스킬 폴더가 바뀌지는 않으며, `install` 명령을 실행해야 합니다.

</details>

<details>
<summary>출처 · 운영 원칙 · 라이선스</summary>

[Matt Pocock의 skills](https://github.com/mattpocock/skills), [Addy Osmani의 agent-skills](https://github.com/addyosmani/agent-skills), [Lauren Tan의 pstack](https://github.com/cursor/plugins/tree/main/pstack)을 목적별로 통합하고 팀 작업 절차를 더했습니다.

- [공통 계약](skills/_coco-shared/contracts.md): 검증 근거, 작업 단위 커밋, 권한 경계
- [결정 기록](skills/_coco-shared/decisions.md): 원본 규칙의 통합 기준
- [원본 대응표](docs/source-index.md): 출처별 통합 위치
- [저작권 고지](THIRD_PARTY_NOTICES.md) · [MIT 라이선스](LICENSE)

원본 자료는 `sources/`에 증거로 보관하며 설치하거나 실행하지 않습니다.

</details>
