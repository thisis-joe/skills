# COCO Skills

**COCO는 [Matt Pocock의 skills](https://github.com/mattpocock/skills), [Addy Osmani의 agent-skills](https://github.com/addyosmani/agent-skills), [Lauren Tan의 pstack](https://github.com/cursor/plugins/tree/main/pstack)을 합쳐, Codex와 Claude Code에서 목적별로 사용할 수 있도록 정리한 개발 스킬 모음입니다.**

세 원본의 122개 스킬과 9개 명령을 22개 통합 스킬로 재구성하고, 사용 안내·요청문 추천·질의응답 학습·팀 맞춤 수정·원격 푸시를 위한 스킬 5개를 더했습니다. 총 **27개 스킬**로 요구사항 정리부터 구현·리뷰·검증·출시 준비까지 이어갈 수 있습니다.

두 런타임에 같은 27개 스킬과 `_coco-shared` 공통 자료를 함께 설치합니다. 표시 이름과 폴더명은 `coco-build`, 호출은 Codex에서 `$coco-build`, Claude Code에서 `/coco-build`입니다. 모든 통합 스킬이 같은 `coco-` 접두사를 사용합니다. pstack과 원본 팩은 설치·호출하지 않으며, 고정한 원문은 비활성 자료로 보관합니다.

## 빠른 설치 (npm)

**Node.js 22 이상과 Python 3.9 이상**이 필요합니다. npm 계정 없이 설치할 수 있습니다. 이 패키지는 스킬 묶음을 설치하므로, 사용할 Codex 또는 Claude Code 자체의 설치·인증은 별도로 완료해야 합니다.

Codex:

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime codex
npx --yes @thisis-joe/coco-skills@latest validate --installed "${CODEX_HOME:-$HOME/.codex}/skills"
```

Claude Code:

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime claude
npx --yes @thisis-joe/coco-skills@latest validate --installed "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
```

두 런타임을 함께 쓰면 위의 두 설치 명령을 모두 실행합니다. 업데이트도 같은 `install` 명령을 다시 실행합니다. `--runtime`을 생략한 기존 명령은 계속 Codex에 설치하며, 명시적 `--dest`가 기본 경로보다 우선합니다.

| 런타임 | 기본 설치 위치 | 환경 변수로 경로 변경 | 설치 후 호출 |
|---|---|---|---|
| Codex | `~/.codex/skills` | `$CODEX_HOME/skills` | `$coco-start` |
| Claude Code | `~/.claude/skills` | `$CLAUDE_CONFIG_DIR/skills` | `/coco-start` |

변경할 내용을 먼저 확인하려면 `--dry-run`을 사용합니다. 프로젝트 한 곳에서만 쓸 Claude Code 스킬은 그 프로젝트의 `.claude/skills`를 지정하고, 해당 프로젝트에서 Claude Code를 시작합니다.

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime codex --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --dest "$HOME/workspaces/my-project/.claude/skills" --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --dest "$HOME/workspaces/my-project/.claude/skills"
npx --yes @thisis-joe/coco-skills@latest validate --installed "$HOME/workspaces/my-project/.claude/skills"
```

`@0.2.0`처럼 버전을 고정하거나 `--dest ./my-skills`로 다른 설치 위치를 지정할 수도 있습니다. Python을 찾지 못하면 `COCO_PYTHON`에 인자 없이 Python 실행 파일 이름이나 경로를 지정합니다. 실제 게시와 로컬 패키지 검증 절차는 [배포 안내](https://github.com/thisis-joe/skills/blob/main/docs/distribution.md)에 있습니다.

## 저장소에서 설치 (Python)

Node.js/npm 없이 **Python 3.9 이상만으로도** 설치할 수 있습니다. 외부 Python 패키지는 없습니다. 저장소를 내려받아 검사한 뒤 사용할 런타임을 설치합니다.

```sh
git clone https://github.com/thisis-joe/skills.git
cd skills
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

### Codex

```sh
python3 scripts/install.py --runtime codex --dry-run
python3 scripts/install.py --runtime codex
python3 scripts/validate.py --installed "${CODEX_HOME:-$HOME/.codex}/skills"
```

기본 위치는 `~/.codex/skills`이며, `CODEX_HOME`이 설정되어 있으면 그 아래 `skills`를 사용합니다. 기존 `python3 scripts/install.py` 명령도 동일하게 Codex에 설치합니다. 설치 후 새 대화를 시작하거나 스킬 목록을 새로고침하고 `$coco-start`를 호출합니다.

### Claude Code

```sh
python3 scripts/install.py --runtime claude --dry-run
python3 scripts/install.py --runtime claude
python3 scripts/validate.py --installed "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
```

기본 위치는 `~/.claude/skills`이며, `CLAUDE_CONFIG_DIR`가 설정되어 있으면 그 아래 `skills`를 사용합니다. Claude Code를 같은 설정으로 다시 시작하거나 새 세션을 열고 `/` 메뉴에서 `coco-start`를 확인한 뒤 `/coco-start`를 호출합니다. 경로와 호출 방식은 [Claude Code 스킬 문서](https://code.claude.com/docs/en/skills), 사용자 설정 경로 변경은 [설정 문서](https://code.claude.com/docs/en/settings)를 참고하세요.

프로젝트 한 곳에만 설치하려면 `--dest`로 해당 프로젝트의 `.claude/skills`를 지정하고 그 프로젝트에서 Claude Code를 시작합니다.

```sh
python3 scripts/install.py --runtime claude --dest "$HOME/workspaces/my-project/.claude/skills" --dry-run
python3 scripts/install.py --runtime claude --dest "$HOME/workspaces/my-project/.claude/skills"
python3 scripts/validate.py --installed "$HOME/workspaces/my-project/.claude/skills"
```

설치 파일·체크섬·공통 참조는 위의 `scripts/validate.py --installed`로 검사합니다. 실제 클라이언트의 인식과 사용은 새 세션에서 `/coco-tellmeskill coco-build 간단 설명`처럼 읽기 전용 요청으로 확인하세요.

### 두 런타임에 함께 설치

```sh
python3 scripts/install.py --runtime codex
python3 scripts/install.py --runtime claude
```

각 설치는 독립된 디렉터리를 사용하며, `--dest /원하는/스킬/폴더`로 기본 위치를 바꿀 수 있습니다. 27개 스킬과 `_coco-shared`를 함께 복사하므로 공통 자료를 빼거나 스킬별로 따로 옮기지 마세요. `agents/openai.yaml`은 Codex용 표시 메타데이터이며 Claude Code는 이 파일에 의존하지 않습니다.

기존 다른 스킬은 유지합니다. 같은 이름의 외부 스킬, 수정한 설치 파일, 추가한 개인 파일이나 심볼릭 링크와 충돌하면 먼저 중단합니다. 동일한 재설치는 변경하지 않으며, 이전 설치의 파일이 그대로인 경우에만 업데이트합니다.

이 설치 경로는 로컬 Codex와 Claude Code용입니다. claude.ai와 Cowork는 계정 스킬 등 별도 배포 경로를 사용하며 로컬 `~/.claude/skills` 설치가 그대로 적용되지 않습니다. 이 저장소는 해당 서비스용 업로드 패키지를 제공하지 않습니다. [Claude Code의 Cowork·cloud 세션 안내](https://code.claude.com/docs/en/skills#use-skills-in-cowork-and-cloud-sessions)

## 어떻게 합쳤나요?

원본의 이름을 기준으로 묶기보다 **사용자가 하려는 작업**을 기준으로 절차를 모았습니다. 같은 목적의 단계는 합치고, 서로 다른 규칙은 선택 이유를 기록했습니다.

| 원본 | 통합에 반영한 절차의 예 |
|---|---|
| Matt Pocock · `mattpocock/skills` | 요구를 질문으로 구체화하기, 명세·작업 분해, TDD, 코드 구조 설계, 인수인계 |
| Addy Osmani · `addyosmani/agent-skills` | 제약·명세 기반 개발, 구현·리뷰·출시 흐름, 보안·성능·운영 검증 |
| Lauren Tan · `pstack` | 설계 대안 비교, 변경 영향 검토, 실제 동작 입증, 맥락 관리와 회고 |

1. **출처를 고정했습니다.** 원본 커밋과 파일 체크섬을 보관하고, 131개 스킬·명령 각각이 어디에 통합됐는지 [대응표](https://github.com/thisis-joe/skills/blob/main/docs/source-index.md)에 기록했습니다.
2. **중복 절차를 목적별로 묶었습니다.** 예를 들어 세 원본의 코드 리뷰 절차는 `coco-review`로 모으고, 명세 준수·팀 규칙·코드 품질을 나누어 판단하도록 정리했습니다.
3. **충돌하는 규칙은 공통 기준으로 맞췄습니다.** 이미 합의한 요구는 재사용하고 빠진 결정만 질문합니다. 동작을 바꾸는 작업에는 실패를 확인하는 테스트부터 적용하고, 정적 문서 수정에는 그에 맞는 직접 검사를 사용합니다. 선택 이유는 [결정 기록](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/decisions.md)에 남겼습니다.
4. **공통 규칙과 전문 절차를 분리했습니다.** 검증 근거·완료 조건·작업별 커밋은 [공통 계약](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/contracts.md)에 두고, 전문·실험 절차는 필요한 경우에 참조합니다. 특정 작성자의 도구·모델·개인 환경에 의존하는 부분은 사용 가능한 환경에 맞게 조정했습니다.
5. **원문과 실행할 스킬을 구분했습니다.** 원문은 `.source` 자료로 보존하며 설치하거나 호출하지 않습니다. 설치되는 것은 `coco-*` 스킬과 공통 자료뿐입니다. 별도로 추가한 5개 팀 스킬도 원본에서 유래한 기능과 구분했습니다.

## 통합해서 얻는 장점

- **목적에 맞는 스킬을 고르기 쉽습니다.** 세 원본에서 비슷한 스킬을 각각 찾는 대신, 구현은 `coco-build`, 리뷰는 `coco-review`, 실행 검증은 `coco-verify`처럼 같은 이름 체계를 사용합니다.
- **단계가 바뀌어도 기준이 이어집니다.** 요구사항·명세·계획을 재사용하고, 구현·리뷰·검증의 역할과 완료 조건을 함께 정의해 중복 질문과 기준 충돌을 줄이도록 구성했습니다.
- **필요한 지침을 골라 읽습니다.** 원본 전체를 매번 불러오지 않고, 작업별 진입점과 관련 공통·전문 절차를 참조합니다.
- **검증 근거와 한계를 남깁니다.** 코드 수정, 테스트 통과, 실제 동작 확인, 배포 성공을 구분합니다. 확인하지 못한 부분을 완료로 취급하지 않습니다.
- **출처를 확인하고 팀에 맞게 바꿀 수 있습니다.** 원문·통합 위치·변경 이유·MIT 고지를 보존하며, `coco-updateskill`로 팀의 개발 규칙에 맞춘 수정을 진행할 수 있습니다.
- **기존 설치를 보호합니다.** 다른 스킬은 유지하고, 개인적으로 수정한 설치 파일이나 같은 이름의 외부 스킬과 충돌하면 덮어쓰기 전에 중단합니다.

## 사용

어떤 절차가 필요한지 애매하면 Codex에서 `$coco-start`, Claude Code에서 `/coco-start`와 작업을 전달합니다. 목적이 분명하면 아래 표의 해당 런타임 호출을 사용합니다. 요청 내용과 개발 절차는 두 런타임에서 같습니다.

스킬을 알아보고 싶으면 `coco-tellmeskill`을 호출합니다. COCO·시스템·플러그인을 포함한 현재 사용 가능한 전체 목록을 보여주고, **스킬 선택 → 간단 설명/상세 설명 선택 → 원문 기반 설명** 순서로 진행합니다. 모든 스킬과 두 설명 모드에 [같은 양식](https://github.com/thisis-joe/skills/blob/main/skills/coco-tellmeskill/references/explanation-format.md)을 적용하고 설명 분량만 바꿉니다. 설명할 스킬의 작업은 실행하지 않습니다.

스킬은 골랐지만 무엇을 요청할지 고민되면 `coco-whattosay`를 호출합니다. 대화에서 확정한 스킬과 목적을 이어받거나 Codex의 `$coco-whattosay coco-review`, Claude Code의 `/coco-whattosay coco-review`처럼 직접 지정할 수 있습니다. **맥락에 맞는 전체 호출문을 기본 3개 추천 → 번호 선택 대기 → 선택한 요청 실행** 순서로 진행하며, “문장만”을 요청하면 선택 후에도 호출문만 제공합니다. `coco-whichskill`의 선택 결과가 있으면 재사용하지만, 현재 패키지에 그 스킬은 포함되지 않으며 직접 지정만으로도 사용할 수 있습니다.

작업한 코드를 제대로 이해했는지 확인하고 싶으면 `coco-askme`를 호출합니다. **범위 선택(이번 작업 전체·특정 기능/흐름·특정 코드·특정 변경, 복수 선택 가능) → 주제 선택(언어·프레임워크 원리, 코드 연결과 실행 흐름, 설계·아키텍처, 성능·최적화, 코드 스타일, 테스트·안정성, 골고루, 직접 입력) → 한 문제씩 질문 → 답변 피드백 → 심화 또는 전환** 순서로 진행합니다. 질문과 해설은 실제 코드 위치에 근거하며, 코드 동작·일반 원리·추정한 설계 의도와 측정하지 않은 최적화 효과를 구분합니다. `힌트`, `모르겠어`, `더 깊게`, `객관식으로`, `범위 변경`, `종료` 같은 요청으로 조절하고, 종료하면 다룬 내용·보완할 개념·다시 볼 코드를 정리합니다. 학습 중에는 코드를 수정하지 않습니다.

`coco-push`는 원격 `dev` 또는 `develop`의 최신 변경을 현재 작업 브랜치에 반영하고 충돌 해결·검증 후 해당 작업 브랜치를 일반 푸시합니다. 푸시 전에 실제 변경과 브랜치명의 작업요약을 비교하며, 요약이 부적절하면 브랜치명과 연결 Jira 태스크의 제목(Summary)·작업설명(Description)을 맞춥니다. 기존 요구사항·수용 조건은 보존하고 정리가 필요한데 티켓 갱신을 확인하지 못하면 푸시 전 멈춥니다. 적절한 이름·티켓은 유지하며 기존 원격 브랜치를 자동 삭제하지 않습니다. 두 개발 기준이 모두 있고 저장소 규칙으로 정할 수 없으면 선택을 받습니다. 기준 브랜치와 최종 푸시 목적지를 구분하며, 사용자 변경을 덮어쓰거나 강제 푸시하지 않습니다. 푸시가 확인되면 해당 브랜치에 열린 PR/MR이 있는지 조회하고, 없을 때만 개발 기준 브랜치를 대상으로 **draft** PR/MR을 만듭니다. 본문은 저장소·forge의 PR/MR 양식을 채우고, 양식이 없으면 조사한 기본 양식(요약·관련 이슈·변경 내용·검증·리뷰어 참고, 필요할 때만 위험·롤백과 스크린샷)을 따릅니다. 이미 열린 PR/MR은 수정하지 않고, 브랜치 이름을 바꿔 옛 브랜치에 열린 PR이 남아 있으면 중복 생성 전에 선택을 받습니다. draft를 만들 수 없으면 일반 PR로 대신 만들지 않고 준비한 제목·본문을 보고합니다. 리뷰어 지정·ready 전환·병합은 하지 않습니다.

`coco-updateskill`은 **전체 스킬 목록 → 수정할 스킬 선택 → 팀에 맞게 바꿀 내용 질문** 순서로 시작합니다. 목록에는 COCO·시스템·플러그인 스킬을 포함하고 각 선택·질문에서 답을 기다립니다. 대상과 수정 내용을 이미 알려줬다면 같은 질문을 반복하지 않습니다. 요구가 정해지면 공통 규칙·호출·출처의 영향을 정리한 뒤 수정·검증·커밋·설치 확인까지 진행합니다. 제안만 요청하면 파일을 변경하지 않으며, 외부 플러그인 캐시나 수정한 개인 설치 파일을 임의로 덮어쓰지 않습니다.

Codex 호출 예시:

```text
$coco-clarify 주문 취소 기능의 범위와 아직 정하지 않은 동작을 확인해줘.
$coco-build 승인한 계획의 다음 작업 하나를 구현해줘.
$coco-build 합의한 계획을 연속 실행하고 작업별로 검증·커밋해줘.
$coco-review 이 작업의 미커밋 변경과 새 파일까지 포함해서 검토해줘.
$coco-whattosay coco-review 현재 변경에 맞는 리뷰 요청문을 추천해줘.
$coco-whattosay coco-build 다음 작업 하나에 대한 요청 문장만 추천해줘.
$coco-askme 이번 작업 전체에서 코드 연결과 아키텍처를 질문해줘.
$coco-verify 캐시 무효화 변경이 다른 소비자를 깨뜨리지 않는지 실행으로 확인해줘.
$coco-push origin/develop 기준으로 현재 브랜치를 최신화하고 검증 후 푸시해줘.
$coco-updateskill coco-build 우리 팀의 검증 명령과 리뷰 절차에 맞게 수정해줘.
```

Claude Code 호출 예시:

```text
/coco-clarify 주문 취소 기능의 범위와 아직 정하지 않은 동작을 확인해줘.
/coco-build 합의한 계획을 연속 실행하고 작업별로 검증·커밋해줘.
/coco-review 이 작업의 미커밋 변경과 새 파일까지 포함해서 검토해줘.
/coco-ship 검증한 변경으로 PR을 준비해줘.
/coco-askme 이번 성능 개선에서 적용한 최적화와 트레이드오프를 질문해줘.
```

작은 정적 수정은 수정과 필요한 확인으로 끝냅니다. 명확한 기능은 기존 합의에서 구현으로 진행하며, 명세·설계·전문 검토는 필요한 경우에 추가합니다. 경량·표준·강화라는 검증 수준과, 작업 하나·연속 실행이라는 진행 모드는 별개입니다.

`coco-build`에서 새 기능 브랜치는 `type(part)/task-number-exact-summary` 형식으로 만듭니다. 예를 들어 Jira 태스크 `TEAM-123`의 요약이 `OAuth2.0_구글`이고 종류·파트가 `feat`·`be`이면 `feat(be)/123-OAuth2.0_구글`입니다. 요약은 해당 태스크의 제목/Summary와 같게 사용하며, 정보가 없거나 Git이 허용하지 않는 문자가 있으면 필요한 내용만 확인합니다. 상세 기준은 [브랜치 준비 규칙](https://github.com/thisis-joe/skills/blob/main/skills/coco-build/SKILL.md#feature-branch-preparation)에 있습니다.

| 상황과 목적 | Codex | Claude Code | 기대 결과 |
|---|---|---|---|
| 사용 가능한 스킬을 찾아보고 사용법을 이해함 | `$coco-tellmeskill` | `/coco-tellmeskill` | 전체 목록, 선택한 스킬의 공통 양식 간단/상세 설명 |
| 선택한 스킬에 어떤 요청을 할지 정함 | `$coco-whattosay` | `/coco-whattosay` | 맥락에 맞는 전체 호출문·추천 이유, 사용자 선택 후 실행 또는 문장만 제공 |
| 작업·코드를 질의응답으로 이해함 | `$coco-askme` | `/coco-askme` | 범위·주제 선택, 코드 근거 질문과 답변 피드백, 종료 시 학습 요약 |
| 기존 스킬을 팀의 개발 방식에 맞게 수정 | `$coco-updateskill` | `/coco-updateskill` | 변경 이유·공통 영향·검증 근거와 실제 설치 상태 |
| 개발 브랜치 최신 반영·작업요약 정리 후 작업 브랜치 게시 | `$coco-push` | `/coco-push` | 검증된 통합, 필요한 브랜치·Jira 정리, 일반 푸시와 원격 ref 확인, 열린 PR/MR이 없을 때 draft PR/MR |
| 절차 선택, 저장소 실행 방법·품질 기준 설정 | `$coco-start` | `/coco-start` | 작업 경로, 실제 검사 명령과 기준 |
| 요구·용어·아이디어가 모호함 | `$coco-clarify` | `/coco-clarify` | 합의한 동작·범위·결정, 필요한 용어집/ADR |
| 코드 동작·위치·설계 이유·외부 API 조사 | `$coco-research` | `/coco-research` | 근거 있는 설명, 사실·추론·미확인 구분 |
| 인터페이스·구조·테스트 경계·프로토타입 | `$coco-design` | `/coco-design` | 대안 비교, 선택한 계약과 검증 경계 |
| 합의한 내용을 명세로 남김 | `$coco-spec` | `/coco-spec` | 기준 명세, 범위와 관찰 가능한 수용 조건 |
| 의존관계가 있는 작은 작업으로 분해 | `$coco-plan` | `/coco-plan` | 작업 그래프, 작업별 수용 조건·검증 |
| 기능·버그 수정·계획 실행 | `$coco-build` | `/coco-build` | 구현, 검사·리뷰 근거, 작업별 커밋·상태 |
| 재현이 어렵거나 원인이 모호한 실패 | `$coco-debug` | `/coco-debug` | 재현 신호, 확인한 원인, 수정 검증 |
| 실제 동작·변경 영향·검증/형식 증명 도구 | `$coco-verify` | `/coco-verify` | 주장별 실행·증명 근거와 한계 |
| 명세·팀 규칙·코드 품질 검토 | `$coco-review` | `/coco-review` | 실제 변경 범위에 대한 관점별 판정·수정 항목 |
| 인증·권한·민감 정보·외부 입력 | `$coco-security` | `/coco-security` | 위협·방어·악용 시나리오 검증 |
| API·스키마 전환·폐기·넓은 변경 | `$coco-migrate` | `/coco-migrate` | 호환 전환·데이터 검증·복구·제거 조건 |
| 성능 문제·최적화·벤치마크 | `$coco-performance` | `/coco-performance` | 기준 측정, 병목, 잡음 대비 개선과 채택/되돌림 |
| UI·반응형·상태·접근성 | `$coco-frontend` | `/coco-frontend` | 제품 규칙에 맞는 화면과 실제 브라우저 근거 |
| 로그·지표·추적·알림·런북 | `$coco-observe` | `/coco-observe` | 운영 질문에 답하는 신호와 계측 검증 |
| CI·반복 작업·봇·검증 자동화 | `$coco-automate` | `/coco-automate` | 재시도·복구 가능한 자동화와 명시적 활성화 상태 |
| PR·출시 준비·롤아웃 | `$coco-ship` | `/coco-ship` | 출시 가능/차단 판단, 복구 계획, 실제 배포 상태 |
| ADR·API 문서·설명·교육·글쓰기 | `$coco-document` | `/coco-document` | 독자에게 필요한 문서·예제·교육 자료 |
| 인수인계·긴 작업 기록·맥락 관리 | `$coco-context` | `/coco-context` | 근거를 따라 재개할 수 있는 간결한 인계 자료 |
| 회고·실패 분석·스킬 평가 | `$coco-retro` | `/coco-retro` | 확인한 실패 패턴과 검증 가능한 개선 |
| 들어온 이슈·중복·작업 준비 상태 분류 | `$coco-triage` | `/coco-triage` | 근거 있는 분류와 다음 준비된 작업 |
| 복잡도·죽은 코드 제거·구조 정리 | `$coco-simplify` | `/coco-simplify` | 동작을 보존하면서 사라진 복잡도와 회귀 근거 |

## 통합 규칙과 원문

- [공통 계약](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/contracts.md): 입력·완료·검증 근거·커밋·재개·권한 경계.
- [충돌 해결 기록](https://github.com/thisis-joe/skills/blob/main/skills/_coco-shared/decisions.md): 원본의 다른 규칙을 어떻게 선택했는지와 이유.
- [원본별 대응표](https://github.com/thisis-joe/skills/blob/main/docs/source-index.md): 131개 원본 항목 각각의 통합 위치와 원문.
- [고정 원문과 체크섬](https://github.com/thisis-joe/skills/blob/main/sources/manifest.json), [규칙별 대응 정보](https://github.com/thisis-joe/skills/blob/main/sources/coverage.json).
- [동작 평가](https://github.com/thisis-joe/skills/blob/main/docs/evaluation/README.md): 기존 절차의 연결 문제, 통합 후 시나리오와 검증 한계.
- [설계](https://github.com/thisis-joe/skills/blob/main/docs/design.md), [작업 계획](https://github.com/thisis-joe/skills/blob/main/docs/implementation-plan.md).

`build`가 제품 작업 수정·커밋·완료 처리를, `push`가 요청한 동기화의 통합 커밋과 원격 푸시, 열린 요청이 없을 때의 draft PR/MR 생성을 맡습니다. `review`는 문제를, `verify`는 실행 근거를 반환합니다. 명세·상태의 기준 위치를 각각 정해 복제 체크리스트를 만들지 않습니다. 필수 검사가 실패했거나 실행되지 않았으면 완료로 표시하지 않습니다.

기능별 브랜치와 작업별 커밋을 사용합니다. 리뷰 범위에는 현재의 커밋·인덱스·작업 트리·새 파일을 포함합니다. 준비한 자동화와 실제 활성화, 출시 가능 판단과 실제 배포 성공은 각각 구분합니다. 스킬은 사용자의 권한 범위를 확대하지 않습니다.

라이선스는 MIT이며, 원본 저작권·허가 고지는 [THIRD_PARTY_NOTICES.md](https://github.com/thisis-joe/skills/blob/main/THIRD_PARTY_NOTICES.md)에 보존합니다.
