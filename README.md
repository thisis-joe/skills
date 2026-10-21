# COCO Skills

[![npm](https://img.shields.io/npm/v/@thisis-joe/coco-skills)](https://www.npmjs.com/package/@thisis-joe/coco-skills)
[![license](https://img.shields.io/npm/l/@thisis-joe/coco-skills)](https://github.com/thisis-joe/skills/blob/main/LICENSE)

Codex와 Claude Code에서 쓰는 **개발 작업 스킬 29개**(1.0.0 기준)입니다. 요구 정리부터 구현·리뷰·푸시·머지까지, 단계에 맞는 스킬을 부르면 에이전트가 정해진 절차와 검증 기준으로 작업합니다.

[Matt Pocock의 skills](https://github.com/mattpocock/skills), [Addy Osmani의 agent-skills](https://github.com/addyosmani/agent-skills), [Lauren Tan의 pstack](https://github.com/cursor/plugins/tree/main/pstack)을 목적별로 합쳤습니다.

## 빠른 시작

**필요한 것:** Node.js 22 이상, Python 3.9 이상. npm 계정은 필요 없습니다.

### 1. 설치

> **1.0.0은 아직 npm에 게시되지 않았습니다.** 지금 `@latest`로 설치하면 0.2.0이 설치되고, 이 문서의 스킬 중 `coco-docs`, `coco-learn`, `coco-merge`가 없습니다. 이 문서와 같은 버전을 쓰려면 [npm 없이 설치](#설치-관리)하세요.

Claude Code:

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime claude
```

Codex:

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime codex
```

설치가 끝나면 결과가 출력됩니다. `status`가 `installed`(새로 설치하거나 업데이트함) 또는 `unchanged`(설치된 내용과 같아 바꿀 것이 없음)이면 성공입니다.

```json
{
  "status": "installed",
  "skills": 29,
  "files": 116,
  "destination": "/Users/me/.claude/skills"
}
```

| 런타임 | 설치 폴더 | 스킬 호출 |
|---|---|---|
| Claude Code | `~/.claude/skills` (`CLAUDE_CONFIG_DIR`가 있으면 그 아래 `skills`) | `/coco-start` |
| Codex | `~/.codex/skills` (`CODEX_HOME`이 있으면 그 아래 `skills`) | `$coco-start` |

- `--runtime`을 생략하면 Codex에 설치합니다.
- 두 런타임을 모두 쓰면 두 명령을 각각 실행합니다. 한쪽을 업데이트해도 다른 쪽은 바뀌지 않습니다.
- 이 문서는 1.0.0 기준입니다. 버전마다 스킬 수가 다를 수 있으니, `@latest`로 설치되는 버전은 `npx --yes @thisis-joe/coco-skills@latest --version`으로 확인하세요.

### 2. 새 세션 열기

- **Claude Code:** 새 세션을 열고 `/`를 입력해 `coco-`로 시작하는 스킬이 보이는지 확인합니다.
- **Codex:** 새 대화를 시작하거나 스킬 목록을 새로고침합니다.

### 3. 첫 호출

스킬 이름 앞에 Claude Code는 `/`, Codex는 `$`를 붙입니다. 이 문서의 예시는 Claude Code 형식입니다.

먼저 아무것도 바꾸지 않는 설명 요청으로 스킬이 동작하는지 확인합니다.

```text
/coco-tellmeskill coco-build 간단 설명
```

그다음 하려는 일을 `coco-start`에 알려 주면 어떤 순서로 진행할지 정해 줍니다.

```text
/coco-start 결제 실패 알림 기능을 추가하려고 해. 어떤 순서로 진행할지 정해줘
```

## 어떤 스킬을 부를지 모를 때

| 상황 | 호출 | 결과 |
|---|---|---|
| 할 일은 있는데 진행 순서를 모름 | `/coco-start <하려는 일>` | 알맞은 스킬 순서와 필요한 검사 |
| 어떤 스킬이 있는지 보고 싶음 | `/coco-tellmeskill` | 최근 쓴 스킬 최대 3개 → 고르지 않으면 목적별 전체 목록 → 고른 스킬 설명 |
| 스킬은 정했는데 뭐라고 요청할지 모름 | `/coco-whattosay coco-review` | 지금 상황에 맞는 요청문 최대 3개와 추천. 번호를 고르면 그 요청을 실행 |

## 기능 하나를 끝까지 진행하는 흐름

보통 아래 순서로 진행합니다. 이미 끝난 단계는 건너뛰고, 범위가 분명한 작은 수정은 `coco-build`부터 시작해도 됩니다.

| 단계 | 호출 예시 | 결과 |
|---|---|---|
| 1. 요구 정리 | `/coco-clarify 주문 취소 기능에서 아직 안 정한 동작을 확인해줘` | 정한 내용과 남은 질문 |
| 2. 명세 | `/coco-spec 정리한 내용을 명세와 수용 조건으로 남겨줘` | 범위와 수용 조건이 있는 명세 |
| 3. 작업 분해 | `/coco-plan 명세를 의존 순서대로 작은 작업으로 나눠줘` | 순서와 검증 방법이 있는 작업 목록 |
| 4. 구현 | `/coco-build 승인한 계획의 다음 작업 하나를 구현해줘` | 테스트를 거친 구현과 작업 단위 커밋 |
| 5. 검토 | `/coco-review 미커밋 변경과 새 파일까지 포함해서 검토해줘` | 기준별 지적 사항과 판정 |
| 6. 푸시 | `/coco-push origin/develop 기준으로 최신화하고 검증 후 푸시해줘` | 충돌 해결과 검증을 마친 브랜치 푸시, 개발 브랜치 대상 draft PR/MR |
| 7. 머지 | `/coco-merge 푸시한 PR을 체크 통과 후 머지해줘` | 대상 브랜치에 머지된 PR과 결과 확인 |

`coco-push`는 푸시를 확인한 뒤 열린 PR/MR이 없으면 `dev`/`develop`을 대상으로 draft PR/MR을 엽니다. 본문은 저장소의 PR/MR 양식을 채우고, 양식이 없으면 기본 양식(요약·관련 이슈·변경 내용·검증·리뷰어 참고)을 따릅니다. PR 없이 푸시만 원하면 요청에 그렇게 적으세요. `coco-merge`는 이 draft를 ready로 바꾸고 체크 통과 후 개발 브랜치에 머지합니다. 열린 PR이 없을 때 `coco-merge`가 직접 여는 PR은 기본 브랜치(예: `main`)를 대상으로 합니다. 이때 개발 브랜치에만 있는 다른 커밋이 함께 들어가게 되면 머지하지 않고 멈춥니다.

중간에 이런 스킬을 함께 씁니다.

```text
/coco-clarify 이 마이그레이션 계획을 grill 해줘
/coco-debug 이 테스트가 CI에서만 가끔 실패하는 원인을 찾아줘
/coco-ship 이 PR을 출시해도 되는지 판단하고 롤아웃 계획을 세워줘
```

## 커밋·푸시·머지·배포를 하는 스킬

설명이나 검토만 요청하면 스킬은 코드, Git, Jira를 바꾸지 않습니다. 아래 스킬은 **실행을 요청하면** 커밋·푸시·머지·배포 같은 쓰기 작업까지 합니다.

| 스킬 | 실행 요청 시 하는 일 | 필요한 것 | 하지 않는 일 |
|---|---|---|---|
| `coco-build` | 기능 브랜치 만들기, 테스트 작성과 구현, 작업 단위 커밋 | 연결된 Jira 작업의 번호와 요약. 없으면 먼저 묻습니다. | 관련 없는 리팩터링을 같은 작업에 섞기 |
| `coco-push` | 원격 `dev`/`develop`을 반영(fetch + merge), 충돌 해결과 검증, 현재 브랜치 푸시. 브랜치 이름이 실제 작업과 맞지 않으면 이름과 연결된 Jira 요약·설명을 정리. 열린 PR/MR이 없으면 개발 브랜치 대상 draft PR/MR 생성 | 원격 `dev` 또는 `develop` 브랜치. Jira를 고쳐야 하는데 쓰기 권한이 없으면 푸시 전에 멈춥니다. PR/MR은 로그인된 `gh`·`glab`으로 만들고, 없거나 draft가 거절되면 준비한 제목·본문만 보고합니다. | 강제 푸시, 기존 PR/MR 수정·ready 전환·머지, 일반(non-draft) PR 생성, 리뷰어 지정, Jira 상태·담당자 변경, 배포 |
| `coco-merge` | PR/MR이 없으면 기본 브랜치로 열기, 초안 해제, 체크 통과를 기다린 뒤 대상 브랜치에 머지하고 결과 확인 | 로그인된 `gh`(GitHub) 또는 `glab`(GitLab) | 보호 규칙·필수 체크 우회, 자기 승인, 충돌 해결, 태그·배포, 요청 없는 브랜치 삭제 |
| `coco-ship` | 출시 가능 여부 판단과 PR 준비. 요청 범위에 따라 PR 생성·머지, 승인된 경우에만 배포 | 출시 대상 커밋과 검증 결과 | 롤백·모니터링 없는 배포, 공유 브랜치 강제 푸시 |
| `coco-updateskill` | 기준 브랜치에서 새 브랜치와 별도 git worktree를 만들고, 그 안에서만 스킬 원본 수정·검증·커밋, 로컬 설치 갱신 | 이 저장소의 clone 또는 fork (아래 참고). Git 저장소가 아니거나 워크트리를 만들 수 없으면 수정 전에 멈춥니다. | 원래 체크아웃 수정, 원격 푸시, PR, 다른 사람에게 배포 |

### 팀에 맞게 고친 스킬 유지하기

`coco-updateskill`은 npm으로 설치한 파일이 아니라 이 저장소를 clone(또는 fork)한 원본을 고치고, 그 원본에서 설치합니다. 이렇게 설치한 뒤 `npx --yes @thisis-joe/coco-skills@latest install`을 실행하면 팀 수정 내용이 npm 버전으로 바뀝니다. 팀 수정본을 쓰는 동안에는 새 버전을 원본 저장소에 merge하고, 그 원본에서 `python3 scripts/install.py --runtime claude`(또는 `codex`)로 다시 설치하세요.

### `coco-build`의 브랜치 이름

새 기능 브랜치는 `type(part)/작업번호-Jira요약` 형식으로 만듭니다.

```text
feat(be)/123-OAuth2.0_구글
```

- `type`과 `part`는 저장소 규칙, 작업 내용, 요청에서 정합니다.
- 작업번호는 Jira 키의 숫자 부분입니다. `TEAM-123`이면 `123`입니다.
- Jira 요약은 번역·축약 없이 그대로 씁니다. 공백처럼 Git 브랜치 이름에 쓸 수 없는 문자가 있으면 바꿀 방법을 먼저 묻습니다.

자세한 규칙: [coco-build 브랜치 준비](https://github.com/thisis-joe/skills/blob/main/skills/coco-build/SKILL.md#feature-branch-preparation)

### `coco-learn`의 노트 위치

학습 노트는 항상 현재 Git 저장소 루트 바로 아래 `TIL/` 폴더에 저장합니다. Git 저장소 밖이면 현재 작업 폴더 아래 `TIL/`을 씁니다. 위치를 따로 묻지 않습니다.

- `TIL/`이 없으면 만들고, `INDEX.md`, `TEMPLATE.md`, `notes/`를 준비합니다.
- Git 저장소 안이면 루트 `.gitignore`에 `TIL/` 줄이 항상 있도록 합니다. 파일이나 줄이 없으면 추가하고 알려 줍니다.
- 노트는 커밋하지 않습니다. 이미 Git이 추적 중인 노트가 있으면 ignore만으로는 추적이 풀리지 않는다고 알려 주고, `git rm --cached`는 사용자에게 맡깁니다.
- 설명만 요청하면 파일을 만들지 않습니다.

## 전체 스킬 목록

| 분류 | 스킬 | 이럴 때 부르세요 |
|---|---|---|
| 안내 | `coco-start` | 작업 절차를 고르거나 프로젝트의 실행 명령·품질 기준을 정할 때 |
| | `coco-tellmeskill` | 쓸 수 있는 스킬을 둘러보거나 특정 스킬이 언제, 어떻게 동작하는지 알고 싶을 때 |
| | `coco-whattosay` | 고른 스킬에 뭐라고 요청할지 지금 상황에 맞는 문장을 추천받을 때 |
| | `coco-updateskill` | 기존 스킬의 절차·규칙을 팀 방식에 맞게 고치고 설치할 때 |
| 요구·계획 | `coco-clarify` | 요구·용어·범위가 모호하거나 계획·아이디어를 압박 질문(grill)으로 검증할 때 |
| | `coco-research` | 기존 코드의 동작, 설계 이유, 설치된 버전 기준의 외부 API를 조사할 때 |
| | `coco-design` | 모듈·API 인터페이스, 구조 변경, 테스트 경계를 정하거나 대안을 비교할 때 |
| | `coco-spec` | 합의한 요구를 범위와 수용 조건이 있는 명세로 남길 때 |
| | `coco-plan` | 명세를 의존 순서가 있는 작고 검증 가능한 작업으로 나눌 때 |
| | `coco-triage` | 들어온 이슈를 분류·중복 확인하고 바로 할 수 있는 작업을 고를 때 |
| 구현·변경 | `coco-build` | 합의한 기능·버그 수정이나 계획된 작업을 구현하고 커밋할 때 |
| | `coco-debug` | 테스트·빌드 실패, 잘못된 동작, 간헐적 회귀의 원인을 찾을 때 |
| | `coco-simplify` | 동작은 그대로 두고 복잡도와 죽은 코드를 줄일 때 |
| | `coco-migrate` | API·스키마·데이터 형식을 바꾸거나 넓은 일괄 변경, 기능 폐기를 할 때 |
| | `coco-frontend` | 브라우저 UI의 동작, 화면 구성, 반응형, 접근성을 만들거나 바꿀 때 |
| 품질·검증 | `coco-verify` | 앱·API·CLI의 실제 동작이나 변경 영향을 증거로 확인할 때 |
| | `coco-review` | 변경을 요구사항, 저장소 규칙, 코드 품질 기준으로 검토할 때 |
| | `coco-security` | 인증·권한·결제·민감 정보·업로드·외부 입력을 다룰 때 |
| | `coco-performance` | 측정된 지연·메모리·처리량·번들 문제를 진단하거나 벤치마크를 판정할 때 |
| 출시·운영 | `coco-ship` | PR을 준비하고 출시 가능 여부와 단계적 롤아웃을 판단할 때 |
| | `coco-push` | 작업 브랜치를 `dev`/`develop`에 맞춰 최신화·검증해 푸시하고 draft PR/MR까지 열 때 |
| | `coco-merge` | 푸시한 PR/MR을 출시 판단 없이, 체크 통과 후 대상 브랜치에 머지할 때 |
| | `coco-automate` | CI/CD, 반복 작업, 이슈 봇, 재사용할 검증 도구를 만들 때 |
| | `coco-observe` | 로그·지표·추적·알림·런북을 추가하거나 고칠 때 |
| 지식·맥락 | `coco-docs` | README·ADR·API 문서·가이드·런북처럼 다른 사람이 읽을 문서를 쓰거나 점검할 때 |
| | `coco-learn` | 코드나 개념을 나를 위해 쉽게 설명받거나, 같은 양식의 60줄 이내 학습 노트를 저장소 루트의 `TIL/`에 남길 때 |
| | `coco-askme` | 작업한 코드나 기능을 한 번에 한 질문씩 복습하며 이해를 확인할 때 |
| | `coco-context` | 인수인계, 중단 후 재개, 긴 작업의 결정 기록이 필요할 때 |
| | `coco-retro` | 끝난 작업·장애·반복 실패를 돌아보고 재발을 막는 개선을 정할 때 |

## 설치 관리

| 하고 싶은 것 | 방법 |
|---|---|
| 업데이트 | 같은 `install` 명령을 다시 실행합니다. 이미 최신이면 `unchanged`를 출력합니다. |
| 설치하지 않고 확인만 하기 | 명령 끝에 `--dry-run`을 붙입니다. 파일은 바꾸지 않고, 설치할 수 있으면 `dry-run`, 이미 같으면 `unchanged`, 충돌이 있으면 오류 메시지를 출력합니다. |
| 한 프로젝트에만 설치 (Claude Code) | `--dest ./my-project/.claude/skills`를 붙입니다. `--dest`는 런타임 기본 폴더보다 우선합니다. |
| 특정 버전 설치·되돌리기 | `@latest` 대신 버전을 적습니다. 예: `@thisis-joe/coco-skills@0.2.0` |
| 게시된 버전 목록 보기 | `npm view @thisis-joe/coco-skills versions` |
| `@latest`가 가리키는 버전 보기 | `npx --yes @thisis-joe/coco-skills@latest --version` |
| 설치된 파일 검사 | `npx --yes @thisis-joe/coco-skills@latest validate --installed <설치 폴더>`. 설치 폴더는 설치 결과의 `destination`입니다. |
| Python 실행 파일 지정 | 환경 변수 `COCO_PYTHON`에 실행 파일 경로를 넣습니다. 기본은 `python3` → `python` → `py -3` 순서로 찾습니다. |
| npm 없이 설치 | 저장소를 clone하고 `python3 scripts/install.py --runtime claude`(또는 `codex`)를 실행합니다. |

업데이트할 때 새 버전에서 빠지거나 이름이 바뀐 스킬은 함께 정리됩니다. 예를 들어 0.2.0의 `coco-document`는 1.0.0으로 업데이트하면 `coco-docs`로 바뀝니다. 설치 폴더에 있는 다른 스킬은 건드리지 않습니다.

### 제거

설치 폴더(설치 결과의 `destination`)에서 COCO가 설치한 폴더와 설치 기록 파일을 지웁니다. 아래는 Claude Code 기본 폴더의 예입니다.

```sh
cd ~/.claude/skills    # Codex 기본: ~/.codex/skills
rm -rf coco-* _coco-shared .coco-install.json .coco-install.lock
```

직접 만든 스킬 중 이름이 `coco-`로 시작하는 것이 같은 폴더에 있으면 먼저 다른 곳으로 옮기세요.

## 문제 해결

설치기는 충돌을 발견하면 **아무것도 바꾸기 전에** 멈춥니다. 자주 만나는 메시지와 해결 방법입니다.

| 메시지·증상 | 원인 | 해결 |
|---|---|---|
| `Python 3.9 or newer is required` | Python이 없거나 3.9 미만 | Python 3.9 이상을 설치하거나 `COCO_PYTHON`에 경로를 지정합니다. |
| `Preserving user-modified or extra file: <경로>` | 설치된 스킬 파일을 직접 고쳤거나, 스킬 폴더에 파일을 추가함 | 바꾼 파일을 다른 곳에 보관한 뒤, 위 '제거' 방법으로 지우고 다시 설치합니다. 팀 규칙으로 고치려면 `coco-updateskill`을 씁니다. |
| `Managed file changed or missing: <경로>` | 설치된 파일이나 스킬 폴더를 지움 | 위 '제거' 방법으로 지우고 다시 설치합니다. |
| `Foreign skill directory already exists: <이름>` | COCO가 설치하지 않은 같은 이름의 폴더가 있음. 또는 설치 기록 파일 `.coco-install.json`만 지움 | 다른 스킬이면 그 폴더를 옮기거나 `--dest`로 다른 폴더에 설치합니다. 설치 기록만 지웠다면 위 '제거' 방법으로 나머지도 지우고 다시 설치합니다. |
| `Another installation owns .coco-install.lock` | 다른 설치가 실행 중이거나 중간에 끊김 | 실행 중인 설치가 없는지 확인하고 설치 폴더의 `.coco-install.lock`을 지운 뒤 다시 실행합니다. |
| `/` 메뉴에 `coco-` 스킬이 없음 | 세션이 스킬 목록을 다시 읽지 않았거나 다른 폴더에 설치함 | 새 세션을 엽니다. 설치 결과의 `destination`이 런타임의 설치 폴더인지 확인합니다. 조직 설정이 로컬 스킬을 막을 수도 있습니다. |

## 공통 원칙

모든 스킬이 따르는 규칙입니다. 자세한 내용은 [공통 계약](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/contracts.md)에 있습니다.

| 원칙 | 의미 |
|---|---|
| 근거 있는 완료 | 실행하지 못한 검사는 통과로 보고하지 않고, 확인한 범위를 구분해 알립니다. |
| 작업 단위 | 기능별 브랜치, 작업별 커밋. 사용자의 미커밋 변경은 그대로 둡니다. |
| 요청한 범위 | 배포·외부 쓰기·삭제는 요청하거나 승인한 범위 안에서만 합니다. |
| 멈춤 신호 | "나중에 테스트", "확실해" 같은 합리화가 보이면 멈추고 바로잡습니다. |
| 필요한 만큼만 읽기 | 각 스킬은 고급 절차가 필요한 조건일 때만 추가 문서를 읽습니다. |

## 지원 범위

- Codex와 Claude Code의 로컬 스킬 폴더에 설치합니다. claude.ai·Cowork 업로드용 패키지는 제공하지 않습니다.
- 스킬은 에이전트 자체를 설치하거나 로그인하지 않습니다.
- npm 패키지를 설치해도 스킬 폴더는 바뀌지 않습니다. `install` 명령을 실행해야 설치됩니다.

## 출처와 문서

| 원본 | 주로 반영한 절차 |
|---|---|
| Matt Pocock | 요구 구체화(grill), 명세·작업 분해, TDD, 구조 설계, 인수인계 |
| Addy Osmani | 명세 기반 개발, 구현·리뷰·출시 흐름, 보안·성능·운영, 멈춤 신호 |
| Lauren Tan (pstack) | 설계 대안 비교, 변경 영향 검토, 전제 재검증, 맥락 관리·회고 |

| 문서 | 내용 |
|---|---|
| [공통 계약](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/contracts.md) | 완료 조건, 검증 근거, 커밋, 권한 경계 |
| [결정 기록](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/decisions.md) | 원본 규칙이 충돌할 때 고른 기준과 이유 |
| [원본 대응표](https://github.com/thisis-joe/skills/blob/main/docs/source-index.md) | 원본 131개 항목의 통합 위치 |
| [배포 안내](https://github.com/thisis-joe/skills/blob/main/docs/distribution.md) | 설치 세부 동작, 게시 절차 |
| [THIRD_PARTY_NOTICES](https://github.com/thisis-joe/skills/blob/main/THIRD_PARTY_NOTICES.md) | 원본 저작권·라이선스 고지 |

`coco-tellmeskill`, `coco-whattosay`, `coco-askme`, `coco-updateskill`, `coco-push`, `coco-merge`는 원본에 없던 절차로, 팀 요청으로 추가했습니다.

원본 원문은 `sources/`에 체크섬과 함께 보관하며, 설치하거나 실행하지 않습니다.

라이선스: [MIT](https://github.com/thisis-joe/skills/blob/main/LICENSE)
