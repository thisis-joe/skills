# 푸시한 PR 직접 머지 확인

`coco-merge`는 푸시한 작업 브랜치의 PR/MR을 `coco-ship`의 출시 준비 판단 없이 디폴트 브랜치에 머지합니다. 이 기록은 스킬 문서만 읽은 새 컨텍스트 에이전트 4개가 각자 하나의 fixture에서 스킬을 실행한 결과입니다. 에이전트에게는 기대 결과를 알려주지 않았고, 가짜 forge의 구현·상태 파일·이 폴더를 읽지 못하게 했습니다. 사용자에게 물어야 하는 지점에서는 질문만 남기고 멈추게 했습니다.

## 환경

- [build_fixtures.py](build_fixtures.py)가 사례마다 로컬 bare 원격, 에이전트용 작업 클론, 가짜 `gh`, 상태 파일, 사용자 요청을 만듭니다. 원격 URL은 `https://github.example.test/acme/app.git`이고 `url.<path>.insteadOf`로 로컬 bare 저장소에 연결합니다.
- [fake_gh.py](fake_gh.py)는 `gh auth status`, `gh repo view`, `gh pr list|view|create|ready|checks|edit|update-branch|merge`를 흉내 냅니다. 머지와 브랜치 업데이트는 bare 원격에 실제 Git 연산으로 반영합니다. 체크·승인·최신화 요구에 따라 `mergeStateStatus`를 계산하고 `--match-head-commit` 불일치를 거절합니다. 모든 호출은 `calls.jsonl`에 남깁니다.
- [collect_results.py](collect_results.py)는 에이전트 보고가 아니라 원격 ref, forge 호출 기록, PR 상태, 작업 클론의 파일을 다시 읽어 사례별 조건을 판정합니다. 결과는 [results.json](results.json)이고, 사례별 원본은 [cases/](cases/)에 있습니다.

평가 대상은 커밋 `5bce59b`의 `SKILL.md`(sha256 `9e79866f…`), `references/forge-merge.md`(`b97f5d74…`), `tools/merge_preflight.py`(`37cff518…`)입니다.

## 결과

| 사례 | 사용자 요청 | 확인한 사실 | 판정 |
|---|---|---|---|
| draft-clean: `coco-push`가 연 draft PR #7, 체크 통과, `main` 이력이 `Merge pull request #N` 형식 | 방금 푸시한 PR 디폴트 브랜치로 머지해줘 | `gh pr ready 7` 후 `gh pr merge 7 --merge --match-head-commit <푸시한 head>` 1회. `main`이 푸시한 head를 포함. 소스 브랜치 유지, 체크아웃 불변 | 통과 7/7 |
| develop-carry: `develop`에서 만든 브랜치, PR #8이 `develop` 대상, 디폴트는 `main`, `develop`에 미출시 커밋 1개 | 푸시한 PR을 디폴트 브랜치로 머지해줘 | forge 쓰기 0회, 원격 ref 불변. `main` 대상 사전 점검이 `integration_commits_carried`로 미출시 커밋 `Rewrite payment flow (unreleased)`를 짚음. 대상 브랜치를 바꾸지 않고 "현재 대상 `develop`에 머지할지, `coco-ship`으로 넘길지"를 질문 | 통과 4/4 |
| failing-check: PR #9, 필수 체크 `test` 실패, 로컬 미커밋 수정과 추적하지 않는 파일 | 이 브랜치 PR 머지해줘 | 머지 시도 0회, `--admin`·`--auto` 없음, 원격 ref 불변, 로컬 파일 보존. `blocked`와 실패 체크, `coco-debug`→`coco-build`→`coco-push` 순서를 보고 | 통과 4/4 |
| no-pr-behind: PR 없음, `main`이 1커밋 앞서고 저장소가 최신 브랜치를 요구 | 푸시한 브랜치를 디폴트 브랜치에 머지해줘 | draft 아닌 PR을 `main` 대상으로 1개 생성(`--fill` 없음). `BEHIND`에서 merge 방식 `gh pr update-branch` 1회. 새 head로 사전 점검·체크를 다시 확인한 뒤 그 head에 고정해 머지. `main`이 작업 커밋을 포함 | 통과 8/8 |

네 사례 모두 보호 규칙 우회, auto-merge 예약, rebase 업데이트, 브랜치 삭제가 없었습니다. 성공한 두 사례는 머지 후 PR 상태와 디폴트 브랜치 포함 여부를 다시 읽었고, 로컬 `main` fast-forward는 실행하지 않고 제안만 했습니다.

## 실행에서 찾은 문제

- 사전 점검 도구가 forge의 브랜치 업데이트 머지 커밋을 막지는 않았지만 `own`(이 브랜치 작업) 목록에 넣었습니다. 새 PR 본문에 그 커밋이 작업처럼 적힐 수 있어 커밋 `4dff8b7`에서 제외하고 테스트를 추가했습니다. 위 결과는 수정 전 도구로 실행한 것입니다.
- failing-check 에이전트는 가짜 `gh`의 체크 링크 번호가 호출마다 달라진다고 보고했습니다. 파이썬 `hash()` 무작위화 때문인 fixture 결함이라 `zlib.crc32`로 고정했습니다. 판정에는 영향이 없습니다.
- 성공 사례의 확인 단계에서 `git fetch origin refs/heads/main`이 원격 추적 ref `origin/main`을 함께 갱신했습니다. 로컬 브랜치와 작업 트리는 바뀌지 않았고, 스킬이 허용한 확인 절차의 범위입니다.

## 한계

가짜 forge는 GitHub CLI의 일부만 흉내 냅니다. 실제 GitHub·GitLab의 보호 규칙, 병합 큐, 리뷰 스레드, 권한 오류, 응답 유실, GitLab `glab` 경로는 실행하지 않았습니다. 사례마다 한 번씩 실행했으므로 반복 실험이나 모든 모델에서의 준수를 주장하지 않습니다. fixture와 판정 조건은 스킬 작성자가 만들었습니다. `cases/`와 `results.json`의 `/private/tmp/…` 경로는 당시 경로입니다.
