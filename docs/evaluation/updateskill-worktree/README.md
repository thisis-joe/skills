# coco-updateskill 전용 브랜치·워크트리 강제 확인

기존에는 유지보수 변경을 "기능 브랜치"에서 커밋하라고만 정해, 시작 체크아웃에서 바로 수정할 수 있었다. 사용자 요청에 따라 파일을 바꾸는 모든 업데이트는 확인한 기준 브랜치에서 새 브랜치와 새 linked worktree를 만들고, 그 안에서만 수정·검사·커밋·설치하도록 바꿨다. 시작 체크아웃은 읽기 전용이며, 제안 전용 요청은 둘 다 만들지 않고, 워크트리를 만들 수 없으면 수정 전에 멈춘다. 게이트는 `coco-updateskill/SKILL.md`의 3단계가, 세부 절차는 `references/team-update.md`의 "Dedicated branch and worktree" 절이 소유한다. 팀 추가 규칙임을 `decisions.md`에 기록했고 원본 대응표·고정 원문은 바꾸지 않았다.

## 새 컨텍스트 적용 3사례

[구조화 결과](results.json), [고정 전후 비교](inspection.txt), [fixture 구성](setup.sh)과 [검사 스크립트](inspect.sh)를 보존한다. 각 사례는 이 패키지 후보본을 복사한 임시 저장소에서 새 컨텍스트 서브에이전트 하나가 `coco-updateskill`을 읽고 요청을 처리했다. 에이전트에게는 워크트리 규칙을 따로 알려주지 않았다. Git fixture는 `main`보다 한 커밋 앞선 `feat/unrelated-work`에서 시작하며, 커밋하지 않은 `README.md` 수정과 미추적 `scratch-notes.txt`가 있다.

| 사례 | 실제 결과 |
|---|---|
| 파일 수정 요청 (`coco-askme` 5문항 제한) | `main`에서 새 브랜치 `feat/coco-askme-quiz-limit`와 형제 worktree를 만들고 그 안에서만 수정·검사·커밋 2개·설치. 시작 체크아웃의 파일·브랜치·HEAD·상태가 그대로이고, 사용자 미커밋 수정과 미추적 파일이 워크트리로 옮겨지지 않음. 설치본은 워크트리의 원본과 일치 |
| 제안만 요청 | 제안만 반환. 브랜치·워크트리·파일·설치 변화 없음. 적용 시 `main`에서 새 브랜치·워크트리를 만들 것이라고 명시 |
| Git 저장소가 아닌 원본 | `git rev-parse` 실패를 확인하고 격리 단계에서 멈춤. `git init`이나 제자리 수정 없이 사용자에게 할 질문만 반환. 원본·설치본 해시 동일 |

fixture를 만든 뒤 `team-update.md` 5단계의 마지막 문장 표현만 다듬었다. 규칙과 조건은 같으며, 두 버전의 해시를 결과에 기록했다. `SKILL.md`는 적용본과 최종본이 같다.

## 자동 검사

`tests/test_package.py`에 실제 임시 Git 저장소로 절차의 기계적 전제를 확인하는 검사를 추가했다. 미커밋 수정·미추적 파일이 있는 다른 기능 브랜치에서 `main` 기준 worktree를 만들고, 그 브랜치의 커밋을 `install.py --root <worktree>`로 설치하면 설치본이 브랜치 버전이 되고 시작 체크아웃은 그대로임을 확인한다. Git이 이미 다른 worktree에서 체크아웃된 브랜치와 비어 있지 않은 경로를 거절하는 것도 확인한다. 이 검사는 Git·설치기 동작에 대한 것이며 에이전트가 규칙을 따른다는 증명은 아니다.

`python3 scripts/validate.py`(27개 스킬)와 `python3 -m unittest discover -s tests`(63개), `git diff --check`가 통과했다. 로컬 `skill-creator/scripts/quick_validate.py`는 PyYAML이 없어 실행하지 못했다(unavailable).

## 범위

사례별 한 번의 적용이며 신뢰도 측정이 아니다. 호스트 관리형 worktree 기능(Claude Code·Codex 앱)과 중단된 같은 업데이트의 worktree 재사용 경로는 지침 검토만 했다. 파일 수정 사례의 askme 규칙 내용은 fixture 결과물이며 이 저장소의 `coco-askme`를 바꾸지 않았다.
