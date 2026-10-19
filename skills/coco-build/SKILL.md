---
name: coco-build
description: "Use when implementing an agreed feature or bug fix, completing one planned task, or executing an authorized sequence. 구현·TDD·작업별 커밋·연속 실행."
license: MIT
---

# coco-build

Own execution from the first ready task through evidence-backed work-unit completion.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/build.md) only when the task needs their additional procedure.

## 기능 브랜치 준비

구현 전에 작업 브랜치와 기준 커밋을 확인한다. 새 기능 브랜치의 이름은 다음 팀 규칙을 따른다. 연속 실행에서도 새 기능 브랜치를 만들 때 같은 규칙을 적용한다.

```text
종류(파트)/지라태스크번호-한글작업요약
feat(be)/123-OAuth2.0_구글
```

- **종류·파트:** 작업 성격과 담당 영역을 저장소 규칙·태스크·사용자 요청에서 확인한다. 예시의 `feat`·`be`를 모든 작업에 고정하지 않는다.
- **지라태스크번호:** 해당 Jira 태스크의 번호를 사용한다. 예를 들어 키가 `TEAM-123`이면 브랜치에는 `123`을 쓰고, 전체 키는 작업 기록에 남겨 태스크를 구분한다.
- **한글작업요약:** 해당 Jira 태스크의 작업요약(제목/Summary)을 그대로 사용한다. 상위 에픽 제목이나 설명에서 새로 만든 요약으로 대체하지 않는다. 한글·영문·대소문자·문장부호·밑줄을 보존하며 번역·축약·영문 슬러그화를 하지 않는다. 예시의 태스크 요약은 `OAuth2.0_구글`이다.

태스크 키·요약은 이미 제공된 티켓 내용이나 사용 가능한 Jira 조회 기능에서 확인하고, 정해진 정보는 다시 묻지 않는다. 번호·요약·종류·파트 중 확인할 수 없는 필수 정보만 질문하며 임의의 번호나 요약으로 브랜치를 만들지 않는다.

전체 후보를 `git check-ref-format --branch`로 검사한다. Jira 요약에 공백 등 Git에서 허용하지 않는 문자가 있으면 원래 요약과 필요한 최소 변환안을 제시하고 사용자에게 적용할 표기를 확인한다. 임의로 공백을 밑줄로 바꾸거나 문자를 삭제하지 않는다. 셸을 사용할 때는 괄호·한글을 포함한 전체 브랜치명을 하나의 인수로 안전하게 인용한다.

확인한 기준 커밋에서 유효한 이름으로 새 브랜치를 만든다. 같은 이름이 이미 있으면 동일 태스크의 적절한 브랜치인지 확인해 재사용하고, 무관한 브랜치를 덮어쓰지 않는다. 같은 태스크의 기존 작업 브랜치를 재개할 때 이름이 규칙과 다르면 차이를 알리고 처리 방향을 확인하며, 자동으로 개명·삭제·리셋하지 않는다. 기존 사용자 변경은 보존하고 최종 브랜치·기준 커밋·Jira 키·원래 요약을 작업 기록에 남긴다.

## Procedure and output

1. Read the agreed brief/spec and authoritative task state. Check dependencies and existing dirty paths, then complete the branch preparation above before implementation. Select one dependency-ready task; continuous mode repeats the same closure standard.
2. Discover actual test/build commands and reuse agreed observable test boundaries. For a behavior change, write one test for the desired behavior, run it and confirm the relevant failure, implement minimal green, and repeat in vertical slices. Static changes use appropriate direct checks.
3. After green, permit only small local cleanup inside the task and recheck it. Structural refactoring is separate scoped work. Avoid implementation-coupled mocks and expected values copied from the implementation.
4. Run required regression/build and actual UI/API/CLI acceptance checks. Obtain scoped review findings. Review includes current unstaged/staged/new files, not just HEAD. Resolve required findings and rerun affected checks; keep unchanged valid evidence.
5. Commit only this task's owned changes and state update on its feature branch. Record the commit and evidence in authoritative status; reconcile a commit that succeeded before an interrupted status update instead of implementing twice.
6. Stop advancement on unresolved required failure, missing material decisions or authorization boundaries; use debug for bounded in-scope diagnosis. Continuous mode resumes at the first incomplete ready task.

Return: task IDs, acceptance/check results, actual review scope, commit IDs, updated status, unresolved items and next ready task. Do not mark unavailable required checks as passed.
