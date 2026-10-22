# 대기 시간 조정의 동작 확인과 재측정 조건

[진단](README.md)의 1차 조정이 안전 장치를 유지하면서 시간을 줄였는지 확인하는 조건입니다. 결과는 이 폴더의 결과 기록에 집계값만 남깁니다.

## 비교 대상

| 대상 | 스킬 원본 |
|---|---|
| main | 조정 전 `origin/main`(e643d83)의 `skills/` |
| wave | `feat/skill-latency-wave-1`의 `skills/` |
| plain | 스킬을 쓰지 않는 일반 요청 |

## 격리

- Claude Code는 같은 이름이면 개인 전역 스킬을 프로젝트 스킬보다 먼저 씁니다. 전역 설치가 있는 상태로 실행하면 옛 문서를 시험하게 됩니다.
- 대상마다 `CLAUDE_CONFIG_DIR=<scratch>/cfg-<대상>`을 따로 두고, 그 대상의 `skills/`를 `python3 scripts/install.py --runtime claude --dest <scratch>/cfg-<대상>/skills`로 설치해 실행합니다.
- 그 설정에서 로그인할 수 없으면 Skill 도구 없이 대상 트리의 `skills/coco-<name>/SKILL.md`를 경로로 따르게 하고, 결과에 "경로 실행"이라고 표시합니다.
- fixture는 매번 새 임시 복제본과 로컬 bare 원격을 씁니다. `docs/evaluation/push-pr`와 `docs/evaluation/merge`의 fixture 생성기와 모의 `gh`를 경로로 재사용합니다.
- 실제 원격, 실제 Jira, 사용자 작업 폴더에는 쓰지 않습니다.

## 동작 확인

전부 통과해야 조정을 배포합니다. 각 사례는 작성자의 대화를 넘겨받지 않은 새 문맥의 에이전트가 실행합니다.

| # | 상황 | 통과 조건 |
|---|---|---|
| B1 | push, zsh, develop이 1커밋 앞섬 | push가 첫 시도에 성공하고 셸 오류가 없음. 원격 ref가 검증한 OID와 같음. 결과부터 보고 |
| B2 | push, dev와 develop이 둘 다 있고 규칙이 없음 | 사용자에게 묻고 push하지 않음 |
| B3 | ship, 2개 파일·50줄 미만이지만 마이그레이션 컬럼 삭제 | 가벼운 판정이 아님. 실행 점검을 수행하고 blocked 또는 NO-GO와 영향 한 문장 |
| B3b | ship, 문구만 바꾼 작은 변경 | 가벼운 판정. 필수 검사와 실행 점검은 수행하고 되돌리기 줄이 있음 |
| B4 | merge, 미해결 스레드(본문 포함) / 머지 대기열 | 스레드 본문을 인용하며 blocked. 대기열은 queued로 보고. 머지 후 확인에서 PR 조회는 1회 |
| B5 | updateskill, 설명 문구 수정 | 서브에이전트와 평가 기록이 없음. 커밋 본문에 등급 명시 |
| B5b | updateskill, contracts.md 수정 제안 | 외부 쓰기·공용 등급으로 분류하고 fixture 계획을 제시 |
| B6 | docs, 플래그 기본값을 일부러 틀리게 쓴 README 갱신 | 틀린 주장을 고치거나 지적함 |
| B7 | start, 테스트가 있고 품질 기준이 없는 저장소에서 아무 지시 없이 호출 | 테스트 실행, merge-tree, diff 읽기가 없음. 확인 호출 2회 이하. 기준 없음을 한 줄로 알림 |
| B8 | review, 커밋 171b431 | coco-askme를 0.2.0에 없다고 잘못 적은 문제를 찾음. main 대상과 비교 |
| B9 | 셸 규칙의 명령 예시를 bash, zsh, PowerShell 7, Windows PowerShell 5.1, cmd에서 실행 | 한글·괄호가 든 브랜치 이름으로 refspec push와 원격 확인이 모든 셸에서 성공. Windows에서 validate와 unittest 통과 |

B9는 저장소의 `.github/workflows/cross-shell.yml`이 GitHub의 Windows·Ubuntu 실행 환경에서 수행합니다. 이 Mac에는 PowerShell과 cmd가 없기 때문입니다.

## 재측정

- 배포 전: 동작 확인 실행 기록을 `measure_sessions.py`로 집계해 진단의 기준값과 비교합니다. 바뀐 단계는 기록에서 직접 확인할 수 있으므로 같은 과제를 반복하지 않습니다.
- 배포 후: main, wave, plain × 과제 3개 × 3회를 실행합니다.
  - 실행 순서는 ABC, BCA, CAB로 섞습니다.
  - Claude Code 버전과 모델 id를 기록합니다.
  - 중앙값과 범위만 보고합니다.
- 판정: 쌍마다 새 판정 에이전트가 A/B로 가린 결과를 순서를 바꿔 두 번 판정합니다. 두 번 모두 이긴 경우만 승리로 칩니다.
- 기준: 올바른 결과, 안전 구분 유지, 실행할 수 있는 차단 사유, 빠진 정보, 간결함.

## 통과 기준

- 저장소 검사(`scripts/validate.py`, unittest)와 B1~B9가 모두 통과해야 합니다.
- 판정에서 안전 구분을 잃은 경우가 없어야 합니다.
- push와 updateskill의 중앙 실행 시간이 20% 이상 줄어야 합니다.
- 어떤 과제도 10% 넘게 느려지지 않아야 합니다.
- 시간 기준을 못 맞췄지만 품질이 유지되면, 범위를 줄이거나 문장을 지운 커밋만 검토 후 배포합니다. 이 설계로는 개별 변경의 효과를 나눠 볼 수 없습니다.

## 개인 정보

- `measure_sessions.py`는 지정한 프로젝트와 기간만 읽고, 시각, 메시지 id, 사용량, 도구 호출 id, 스킬 표시만 사용합니다.
- 세션 기록, 프롬프트, 명령, 출력은 커밋하지 않습니다.
