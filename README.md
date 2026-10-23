# COCO Skills

[![npm](https://img.shields.io/npm/v/@thisis-joe/coco-skills)](https://www.npmjs.com/package/@thisis-joe/coco-skills)

Codex와 Claude Code에서 쓰는 개발 스킬 29개. 요구 정리부터 구현, 검토, 머지까지 필요한 단계의 스킬을 호출합니다.

## 시작하기

Node.js 22 이상과 Python 3.9 이상이 필요합니다. 사용할 에이전트는 별도로 설치하고 로그인하세요.

> 이 저장소는 **1.0.0 기준**입니다. npm의 `latest`는 아직 **0.2.0**이며 프로젝트 설치와 일부 스킬을 지원하지 않습니다. 1.0.0 게시 전에는 아래 **소스에서 설치**를 이용하세요.

**1.0.0 게시 후**, 사용할 프로젝트 폴더에서 런타임에 맞는 명령을 실행합니다.

```sh
# Claude Code
npx --yes @thisis-joe/coco-skills@1.0.0 install --runtime claude

# Codex
npx --yes @thisis-joe/coco-skills@1.0.0 install --runtime codex
```

1.0.0에서는 터미널에서 설치 위치를 고를 수 있습니다. 설치 후 해당 프로젝트에서 **새 세션**을 여세요. Claude Code는 `/`, Codex는 `$`로 스킬을 호출합니다.

```text
/coco-start 주문 취소 기능을 만들려고 해. 진행 순서를 정해줘
$coco-start 주문 취소 기능을 만들려고 해. 진행 순서를 정해줘
```

스킬을 둘러보려면 `/coco-tellmeskill`, 특정 스킬을 알아보려면 `/coco-tellmeskill coco-build 간단 설명`을 입력하세요. Codex에서는 앞의 `/`를 `$`로 바꿉니다.

<details>
<summary>소스에서 설치 — npm 게시 전에도 1.0.0 사용</summary>

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

아래 npm 명령은 **1.0.0 게시 후** 사용할 수 있습니다. `claude` 대신 `codex`를 지정하면 Codex에 적용됩니다.

```sh
# 현재 프로젝트에 설치하거나 업데이트
npx --yes @thisis-joe/coco-skills@1.0.0 install --runtime claude --project .

# 모든 프로젝트에서 사용
npx --yes @thisis-joe/coco-skills@1.0.0 install --runtime claude --global

# 프로젝트로 옮기면서 기존 글로벌 설치 제거
npx --yes @thisis-joe/coco-skills@1.0.0 install --runtime claude --project . --remove-global

# 현재 프로젝트에서 제거
npx --yes @thisis-joe/coco-skills@1.0.0 uninstall --runtime claude --project .
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

<details>
<summary>전체 스킬과 작업 흐름</summary>

필요한 단계부터 시작하세요. 모든 작업에 전체 절차가 필요한 것은 아닙니다. 할 일과 스킬이 정해졌다면 `coco-start`를 거치지 않고 바로 호출하세요.

이름만 호출했을 때 대화에서 할 일이 하나로 정해져 있으면 그 요청으로 진행하고, 그렇지 않으면 요청문 선택을 안내합니다. `coco-tellmeskill`, `coco-askme`, `coco-updateskill`, `coco-whattosay`는 각자의 선택 단계로 시작합니다. **`coco-push`와 `coco-merge`는 이름만 호출해도 현재 브랜치 기준으로 실행**하므로, 설명만 원하면 요청에 명시하세요.

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
| 문서·학습·협업 | `coco-docs`, `coco-learn`, `coco-askme`, `coco-context`, `coco-retro`, `coco-triage`, `coco-updateskill` |

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
